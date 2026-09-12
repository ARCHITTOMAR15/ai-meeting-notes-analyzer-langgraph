


import os
import tempfile
from pathlib import Path
from io import BytesIO
import streamlit as st

# MUST be before importing other project modules
st.set_page_config(
    page_title="AI Meeting Notes Analyzer",
    page_icon="📝",
    layout="wide",
)

os.environ["HF_HOME"] = os.getenv("HF_HOME", "/tmp/huggingface")

try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
except Exception as e:
    st.error(f"ReportLab import failed: {type(e).__name__}: {e}")
    st.stop()

from src.data_ingestion.loader import TranscriptLoader
from src.preprocessing.cleaner import TranscriptCleaner
from src.preprocessing.chunker import TranscriptChunker
from src.vector_store.embedding_model import EmbeddingModel
from src.vector_store.faiss_index import FAISSIndexManager
from src.vector_store.retriever import TranscriptRetriever
from src.graph.workflow import MeetingWorkflow
from src.graph.meeting_state import MeetingState
# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------



st.title("📝 AI Meeting Notes Analyzer")
st.caption("Upload a meeting transcript and generate AI-powered meeting notes using LangGraph.")

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

with st.sidebar:
    st.header("Project Information")
    st.write("Model: Qwen2.5-3B-Instruct (GGUF)")
    st.write("Framework: LangGraph + LangChain + LlamaIndex")
    st.write("Vector Store: FAISS")

# ----------------------------------------------------
# PDF Generator
# ----------------------------------------------------

def generate_pdf(result):
    """Generate a PDF containing the meeting analysis results."""

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("AI Meeting Notes Analyzer", styles["Title"]))

    # Discussion Topics
    elements.append(Paragraph("Discussion Topics", styles["Heading2"]))
    for topic in result["topics"].topics:
        elements.append(Paragraph(f"• {topic}", styles["BodyText"]))

    # Meeting Summary
    elements.append(Paragraph("Meeting Summary", styles["Heading2"]))

    elements.append(Paragraph("Meeting Objective", styles["Heading3"]))
    elements.append(
        Paragraph(result["summary"].meeting_objective, styles["BodyText"])
    )

    elements.append(Paragraph("Key Discussion Points", styles["Heading3"]))
    for point in result["summary"].key_discussion_points:
        elements.append(Paragraph(f"• {point}", styles["BodyText"]))

    elements.append(Paragraph("Decisions Taken", styles["Heading3"]))
    for decision in result["summary"].decisions_taken:
        elements.append(Paragraph(f"• {decision}", styles["BodyText"]))

    # Action Items
    elements.append(Paragraph("Action Items", styles["Heading2"]))

    for item in result["action_items"].action_items:
        elements.append(
            Paragraph(
                f"<b>Task:</b> {item.task}<br/>"
                f"<b>Owner:</b> {item.owner}<br/>"
                f"<b>Deadline:</b> {item.deadline}",
                styles["BodyText"],
            )
        )
        elements.append(Paragraph("<br/>", styles["BodyText"]))

    # Priority Classification
    elements.append(Paragraph("Priority Classification", styles["Heading2"]))

    for item in result["priorities"].priorities:
        elements.append(
            Paragraph(
                f"• <b>{item.task}</b> — {item.priority}",
                styles["BodyText"],
            )
        )




    doc.build(elements)
    buffer.seek(0)

    return buffer

# ====================================================
# ✅ ADD THESE LINES HERE
# ====================================================

@st.cache_resource
def load_embedding_model():
    """Load embedding model only once."""
    return EmbeddingModel.load_model()



# ----------------------------------------------------
# File Upload
# ----------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Meeting Transcript",
    type=["txt", "docx", "pdf"],
)

analyze_button = st.button("🚀 Analyze Meeting", use_container_width=True)

# ----------------------------------------------------
# Backend Pipeline
# ----------------------------------------------------

if uploaded_file and analyze_button:

    with st.spinner("Analyzing meeting transcript..."):

        # Save uploaded file temporarily
        suffix = Path(uploaded_file.name).suffix

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getbuffer())
            transcript_path = tmp.name

        # Load document
        document = TranscriptLoader.load_document(transcript_path)

        # Clean transcript
        clean_document = TranscriptCleaner.clean(document)

        # Chunk transcript
        nodes = TranscriptChunker.create_nodes(clean_document)

        # Embeddings (cached)
        embedding_model = load_embedding_model()

        # FAISS Index
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

        # Run Workflow
        workflow = MeetingWorkflow.build()
        result = workflow.invoke(state)

    st.success("Meeting analyzed successfully!")

    # ------------------------------------------------
    # Topics
    # ------------------------------------------------

    st.header("📌 Discussion Topics")

    for topic in result["topics"].topics:
        st.markdown(f"- {topic}")

    # ------------------------------------------------
    # Summary
    # ------------------------------------------------

    st.header("📝 Meeting Summary")

    st.subheader("Meeting Objective")
    st.write(result["summary"].meeting_objective)

    st.subheader("Key Discussion Points")

    for point in result["summary"].key_discussion_points:
        st.markdown(f"- {point}")

    st.subheader("Decisions Taken")

    for decision in result["summary"].decisions_taken:
        st.markdown(f"- {decision}")

    # ------------------------------------------------
    # Action Items
    # ------------------------------------------------

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

    # ------------------------------------------------
    # Priority Classification
    # ------------------------------------------------

    st.header("🚨 Priority Classification")

    for item in result["priorities"].priorities:
        st.markdown(f"**{item.task}** — `{item.priority}`")

    # ------------------------------------------------
    # Download PDF
    # ------------------------------------------------

    st.header("📄 Download Meeting Notes")

    pdf_file = generate_pdf(result)

    st.download_button(
        label="⬇️ Download Meeting Notes as PDF",
        data=pdf_file,
        file_name="meeting_notes_summary.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

# ----------------------------------------------------
# No File Uploaded
# ----------------------------------------------------

elif analyze_button:
    st.warning("Please upload a meeting transcript before clicking Analyze Meeting.")
