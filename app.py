
import os
import tempfile
from pathlib import Path

import streamlit as st

# -------------------------------------------------------------------
# Streamlit Cloud / HuggingFace Cache
# -------------------------------------------------------------------
os.environ["HF_HOME"] = "/tmp/huggingface"
os.environ["TRANSFORMERS_CACHE"] = "/tmp/huggingface"

# -------------------------------------------------------------------
# Page Config
# -------------------------------------------------------------------
st.set_page_config(
    page_title="AI Meeting Notes Analyzer",
    page_icon="📝",
    layout="wide",
)

# -------------------------------------------------------------------
# Cache Heavy Resources
# -------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def get_embedding_model():
    from src.vector_store.embedding_model import EmbeddingModel
    return EmbeddingModel.load_model()


@st.cache_resource(show_spinner=False)
def get_workflow():
    from src.graph.workflow import MeetingWorkflow
    return MeetingWorkflow.build()


# -------------------------------------------------------------------
# UI
# -------------------------------------------------------------------
st.title("📝 AI Meeting Notes Analyzer")

st.markdown("""
Upload a meeting transcript (**TXT / PDF / DOCX**) and generate AI-powered insights.

### Features
- 📋 Meeting Summary
- 🗂 Topics Discussed
- ✅ Action Items
- 🎯 Priority Classification
- 📄 Download Meeting Notes
""")

uploaded_file = st.file_uploader(
    "Upload Meeting Transcript",
    type=["txt", "pdf", "docx"],
)

analyze_button = st.button(
    "🚀 Analyze Meeting",
    type="primary",
    use_container_width=True,
)

# -------------------------------------------------------------------
# Analysis Pipeline
# -------------------------------------------------------------------
if analyze_button:

    if uploaded_file is None:
        st.warning("⚠️ Please upload a transcript first.")
        st.stop()

    transcript_path = None
    result = None

    try:
        # ----------------------------------------------------------
        # Save Uploaded File
        # ----------------------------------------------------------
        suffix = Path(uploaded_file.name).suffix

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(uploaded_file.read())
            transcript_path = temp_file.name

        # ----------------------------------------------------------
        # Load Cached Resources
        # ----------------------------------------------------------
        with st.spinner("🔄 Loading AI models (first run takes 1-2 minutes)..."):
            embedding_model = get_embedding_model()
            workflow = get_workflow()

        # Lazy imports
        from src.data_ingestion.loader import TranscriptLoader
        from src.preprocessing.cleaner import TranscriptCleaner
        from src.preprocessing.chunker import TranscriptChunker
        from src.vector_store.faiss_index import FAISSIndexManager
        from src.vector_store.retriever import TranscriptRetriever
        from src.graph.meeting_state import MeetingState

        # ----------------------------------------------------------
        # Transcript Processing
        # ----------------------------------------------------------
        with st.spinner("🤖 Analyzing meeting transcript..."):

            # 1. Load transcript
            document = TranscriptLoader.load_document(transcript_path)

            # 2. Clean transcript
            cleaned_document = TranscriptCleaner.clean(document)

            # 3. Chunk transcript
            chunks = TranscriptChunker.split(cleaned_document)

            # 4. Build FAISS Vector Store
            vector_store = FAISSIndexManager.create_index(
                documents=chunks,
                embedding_model=embedding_model,
            )

            # 5. Create Retriever
            retriever = TranscriptRetriever.create_retriever(vector_store)

            # 6. Initial LangGraph State
            state = MeetingState(
                transcript=cleaned_document.page_content,
                retriever=retriever,
                summary=None,
                topics=None,
                action_items=None,
                priorities=None,
            )

            # 7. Execute LangGraph Workflow
            result = workflow.invoke(state)

        st.success("✅ Meeting analyzed successfully!")

    except Exception as error:
        st.error("❌ Analysis failed.")
        st.exception(error)

    finally:
        if transcript_path and os.path.exists(transcript_path):
            os.remove(transcript_path)

    # -------------------------------------------------------------------
    # Results Section
    # -------------------------------------------------------------------
    if result:

        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 Summary",
            "🗂 Topics",
            "✅ Action Items",
            "🎯 Priorities",
        ])

        # --------------------------------------------------------------
        # Summary
        # --------------------------------------------------------------
        with tab1:
            st.subheader("Meeting Summary")
            st.write(result.get("summary", "No summary generated."))

        # --------------------------------------------------------------
        # Topics
        # --------------------------------------------------------------
        with tab2:
            st.subheader("Topics Discussed")

            topics = result.get("topics", [])

            if topics:
                for topic in topics:
                    st.markdown(f"- {topic}")
            else:
                st.info("No topics identified.")

        # --------------------------------------------------------------
        # Action Items
        # --------------------------------------------------------------
        with tab3:
            st.subheader("Action Items")

            action_items = result.get("action_items", [])

            if action_items:
                st.table(action_items)
            else:
                st.info("No action items found.")

        # --------------------------------------------------------------
        # Priorities
        # --------------------------------------------------------------
        with tab4:
            st.subheader("Priority Classification")

            priorities = result.get("priorities", [])

            if priorities:
                st.table(priorities)
            else:
                st.info("No priorities identified.")

        # -------------------------------------------------------------------
        # Download Notes
        # -------------------------------------------------------------------
        summary = result.get("summary", "")

        topics_text = "\n".join(
            f"- {topic}" for topic in result.get("topics", [])
        )

        actions_text = "\n".join(
            f"- {item['task']} | Owner: {item['owner']} | Deadline: {item['deadline']}"
            for item in result.get("action_items", [])
        )

        priorities_text = "\n".join(
            f"- {item['task']} ({item['priority']})"
            for item in result.get("priorities", [])
        )

        output_text = f"""
==============================
AI MEETING NOTES ANALYZER
==============================

MEETING SUMMARY
---------------
{summary}

TOPICS DISCUSSED
----------------
{topics_text}

ACTION ITEMS
------------
{actions_text}

PRIORITIES
----------
{priorities_text}
"""

        st.download_button(
            label="📄 Download Meeting Notes (.txt)",
            data=output_text,
            file_name="meeting_notes.txt",
            mime="text/plain",
            use_container_width=True,
        )

# -------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------
st.markdown("---")
st.caption("Built with LangGraph • FAISS • Hugging Face • Streamlit")
