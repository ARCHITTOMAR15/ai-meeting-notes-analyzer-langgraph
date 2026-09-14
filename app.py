
import os
import tempfile
from pathlib import Path

import streamlit as st

# -----------------------------
# Hugging Face cache (Streamlit Cloud)
# -----------------------------
os.environ["HF_HOME"] = "/tmp/huggingface"
os.environ["TRANSFORMERS_CACHE"] = "/tmp/huggingface"

# -----------------------------
# Project Imports
# -----------------------------
from src.data_ingestion.loader import TranscriptLoader
#from src.preprocessing.cleaner import TranscriptCleaner
from src.preprocessing.chunker import TranscriptChunker
from src.vector_store.embedding_model import EmbeddingModel
from src.vector_store.faiss_index import FAISSIndexManager
from src.vector_store.retriever import TranscriptRetriever
from src.graph.workflow import MeetingWorkflow
from src.graph.meeting_state import MeetingState

# -----------------------------
# Streamlit Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Meeting Notes Analyzer",
    page_icon="📝",
    layout="wide",
)

st.title("📝 AI Meeting Notes Analyzer")
st.caption(
    "Upload a meeting transcript and generate AI-powered meeting notes using LangGraph + LlamaCpp + FAISS."
)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("Project Information")
    st.success("Portfolio Project")
    st.write("**LLM:** Qwen2.5-3B-Instruct (GGUF)")
    st.write("**Framework:** LangGraph + LangChain + LlamaIndex")
    st.write("**Vector Store:** FAISS")
    st.write("**Embeddings:** BAAI/bge-small-en-v1.5")

# -----------------------------
# Resource Caching
# -----------------------------
@st.cache_resource(show_spinner=False)
def load_embedding_model():
    return EmbeddingModel.load_model()


@st.cache_resource(show_spinner=False)
def load_workflow():
    return MeetingWorkflow.build()


embedding_model = load_embedding_model()
workflow = load_workflow()

# -----------------------------
# Meeting Notes Generator (TXT)
# -----------------------------
def generate_meeting_notes(result):
    content = []

    content.append("AI MEETING NOTES ANALYZER")
    content.append("=" * 60)
    content.append("")

    content.append("DISCUSSION TOPICS")
    content.append("-" * 30)
    for topic in result["topics"].topics:
        content.append(f"• {topic}")

    content.append("")
    content.append("MEETING SUMMARY")
    content.append("-" * 30)

    content.append("Meeting Objective:")
    content.append(result["summary"].meeting_objective)
    content.append("")

    content.append("Key Discussion Points:")
    for point in result["summary"].key_discussion_points:
        content.append(f"• {point}")

    content.append("")
    content.append("Decisions Taken:")
    for decision in result["summary"].decisions_taken:
        content.append(f"• {decision}")

    content.append("")
    content.append("ACTION ITEMS")
    content.append("-" * 30)

    for item in result["action_items"].action_items:
        content.append(f"Task     : {item.task}")
        content.append(f"Owner    : {item.owner}")
        content.append(f"Deadline : {item.deadline}")
        content.append("")

    content.append("PRIORITY CLASSIFICATION")
    content.append("-" * 30)

    for item in result["priorities"].priorities:
        content.append(f"{item.task}  --->  {item.priority}")

    return "\n".join(content)


# -----------------------------
# File Upload
# -----------------------------
uploaded_file = st.file_uploader(
    "📂 Upload Meeting Transcript",
    type=["txt", "docx", "pdf"],
)

analyze_button = st.button(
    "🚀 Analyze Meeting",
    use_container_width=True,
)

# -----------------------------
# Analysis Pipeline
# -----------------------------
if uploaded_file and analyze_button:

    with st.spinner("Analyzing meeting transcript..."):

        suffix = Path(uploaded_file.name).suffix

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getbuffer())
            transcript_path = tmp.name

        # Load transcript
        document = TranscriptLoader.load_document(transcript_path)

        # Clean transcript
        #clean_document = TranscriptCleaner.clean(document)
        clean_document=document

        # Chunk transcript
        nodes = TranscriptChunker.create_nodes(clean_document)

        # Create FAISS index
        vector_index = FAISSIndexManager.create_index(
            nodes=nodes,
            embedding_model=embedding_model,
        )

        # Retriever
        retriever = TranscriptRetriever.create_retriever(vector_index)

        # LangGraph State
        state: MeetingState = {
            "retriever": retriever,
            "topics": None,
            "summary": None,
            "action_items": None,
            "priorities": None,
        }

        # Execute workflow
        result = workflow.invoke(state)

    st.success("✅ Meeting analyzed successfully!")

    # -----------------------------
    # Discussion Topics
    # -----------------------------
    st.header("📌 Discussion Topics")

    for topic in result["topics"].topics:
        st.markdown(f"- {topic}")

    # -----------------------------
    # Meeting Summary
    # -----------------------------
    st.header("📝 Meeting Summary")

    st.subheader("Meeting Objective")
    st.write(result["summary"].meeting_objective)

    st.subheader("Key Discussion Points")
    for point in result["summary"].key_discussion_points:
        st.markdown(f"- {point}")

    st.subheader("Decisions Taken")
    for decision in result["summary"].decisions_taken:
        st.markdown(f"- {decision}")

    # -----------------------------
    # Action Items
    # -----------------------------
    st.header("✅ Action Items")

    for item in result["action_items"].action_items:
        st.markdown(
            f"""
**Task:** {item.task}

**Owner:** {item.owner}

**Deadline:** {item.deadline}
"""
        )
        st.divider()

    # -----------------------------
    # Priority Classification
    # -----------------------------
    st.header("🚨 Priority Classification")

    for item in result["priorities"].priorities:
        priority = item.priority.upper()

        if priority == "HIGH":
            st.error(f"🔴 {item.task}")
        elif priority == "MEDIUM":
            st.warning(f"🟡 {item.task}")
        else:
            st.success(f"🟢 {item.task}")

    # -----------------------------
    # Download Meeting Notes
    # -----------------------------
    st.header("📄 Download Meeting Notes")

    meeting_notes = generate_meeting_notes(result)

    st.download_button(
        label="⬇️ Download Meeting Notes (.txt)",
        data=meeting_notes,
        file_name="meeting_notes_summary.txt",
        mime="text/plain",
        use_container_width=True,
    )

elif analyze_button:
    st.warning("Please upload a meeting transcript before clicking **Analyze Meeting**.")
