
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
# Cached Heavy Resources
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

**Features**
- 📋 Meeting Summary
- ✅ Action Items
- 🎯 Priorities
- 😊 Sentiment Analysis
- 🗂 Topics Discussed
- ❓ Question & Answer
""")

uploaded_file = st.file_uploader(
    "Upload Transcript",
    type=["txt", "pdf", "docx"]
)

analyze_button = st.button(
    "🚀 Analyze Meeting",
    use_container_width=True,
    type="primary"
)

# -------------------------------------------------------------------
# Analysis Pipeline
# -------------------------------------------------------------------
if analyze_button:

    if uploaded_file is None:
        st.warning("⚠️ Please upload a meeting transcript first.")
        st.stop()

    result = None
    transcript_path = None

    try:
        # -----------------------------
        # Save uploaded file
        # -----------------------------
        suffix = Path(uploaded_file.name).suffix

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(uploaded_file.read())
            transcript_path = temp_file.name

        # -----------------------------
        # Load AI Models (Cached Once)
        # -----------------------------
        with st.spinner("🔄 Loading AI models (first run may take 1-2 minutes)..."):
            embedding_model = get_embedding_model()
            workflow = get_workflow()

        # Lazy imports (faster startup)
        from src.data_ingestion.loader import TranscriptLoader
        from src.preprocessing.cleaner import TranscriptCleaner
        from src.preprocessing.chunker import TranscriptChunker
        from src.vector_store.faiss_index import FAISSIndexManager
        from src.vector_store.retriever import TranscriptRetriever
        from src.graph.meeting_state import MeetingState

        # -----------------------------
        # Meeting Analysis
        # -----------------------------
        with st.spinner("🤖 Analyzing meeting transcript..."):

            # 1. Load transcript
            document = TranscriptLoader.load_document(transcript_path)

            # 2. Clean transcript
            cleaned_document = TranscriptCleaner.clean(document)

            # 3. Split transcript into chunks
            chunks = TranscriptChunker.split(cleaned_document)

            # 4. Create FAISS vector index
            index_manager = FAISSIndexManager(
                embedding_model=embedding_model
            )
            index_manager.create_index(chunks)

            # 5. Retriever
            retriever = TranscriptRetriever(index_manager)

            # 6. Initial LangGraph state
            state = MeetingState(
                transcript=cleaned_document.text,
                retriever=retriever,
            )

            # 7. Execute LangGraph workflow
            result = workflow.invoke(state)

        st.success("✅ Meeting analyzed successfully!")

    except Exception as e:
        st.error("❌ Analysis failed.")
        st.exception(e)

    finally:
        if transcript_path and os.path.exists(transcript_path):
            os.remove(transcript_path)

    # ----------------------------------------------------------------
    # Results
    # ----------------------------------------------------------------
    if result is not None:

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📋 Summary",
            "✅ Action Items",
            "🎯 Priorities",
            "😊 Sentiment",
            "🗂 Topics",
            "❓ Q&A",
        ])

        with tab1:
            st.markdown(result.get("summary", "No summary generated."))

        with tab2:
            st.markdown(result.get("action_items", "No action items generated."))

        with tab3:
            st.markdown(result.get("priorities", "No priorities generated."))

        with tab4:
            st.markdown(result.get("sentiment", "No sentiment generated."))

        with tab5:
            st.markdown(result.get("topics", "No topics generated."))

        with tab6:
            st.markdown(result.get("qa", "No Q&A generated."))

        # -----------------------------
        # Download Notes
        # -----------------------------
        output_text = f"""
===========================
AI MEETING NOTES ANALYZER
===========================

MEETING SUMMARY
---------------
{result.get("summary", "")}

ACTION ITEMS
------------
{result.get("action_items", "")}

PRIORITIES
----------
{result.get("priorities", "")}

SENTIMENT
---------
{result.get("sentiment", "")}

TOPICS DISCUSSED
----------------
{result.get("topics", "")}

QUESTION & ANSWER
-----------------
{result.get("qa", "")}
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
