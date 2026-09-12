


import os
import tempfile
from pathlib import Path
from io import BytesIO
import streamlit as st

# MUST be before importing other project modules
st.set_page_config(
    page_title="AI Meeting Notes Analyzer",
    layout="wide",
)

os.environ["HF_HOME"] = os.getenv("HF_HOME", "/tmp/huggingface")
os.environ["TRANSFORMERS_CACHE"] = "/tmp/huggingface"

from fpdf import FPDF


from src.data_ingestion.loader import TranscriptLoader
from src.preprocessing.cleaner import TranscriptCleaner
from src.preprocessing.chunker import TranscriptChunker
from src.vector_store.embedding_model import EmbeddingModel
from src.vector_store.faiss_index import FAISSIndexManager
from src.vector_store.retriever import TranscriptRetriever
from src.graph.workflow import MeetingWorkflow
from src.graph.meeting_state import MeetingState



st.title(" AI Meeting Notes Analyzer")
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
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "AI Meeting Notes Analyzer", ln=True)

    # Topics
    pdf.set_font("Helvetica", "B", 14)
    pdf.ln(5)
    pdf.cell(0, 10, "Discussion Topics", ln=True)

    pdf.set_font("Helvetica", size=12)
    for topic in result["topics"].topics:
        pdf.multi_cell(0, 8, f"- {topic}")

    # Summary
    pdf.set_font("Helvetica", "B", 14)
    pdf.ln(4)
    pdf.cell(0, 10, "Meeting Summary", ln=True)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Meeting Objective", ln=True)

    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 8, result["summary"].meeting_objective)

    pdf.set_font("Helvetica", "B", 12)
    pdf.ln(2)
    pdf.cell(0, 8, "Key Discussion Points", ln=True)

    pdf.set_font("Helvetica", size=12)
    for point in result["summary"].key_discussion_points:
        pdf.multi_cell(0, 8, f"- {point}")

    pdf.set_font("Helvetica", "B", 12)
    pdf.ln(2)
    pdf.cell(0, 8, "Decisions Taken", ln=True)

    pdf.set_font("Helvetica", size=12)
    for decision in result["summary"].decisions_taken:
        pdf.multi_cell(0, 8, f"- {decision}")

    # Action Items
    pdf.set_font("Helvetica", "B", 14)
    pdf.ln(4)
    pdf.cell(0, 10, "Action Items", ln=True)

    pdf.set_font("Helvetica", size=12)
    for item in result["action_items"].action_items:
        pdf.multi_cell(0, 8, f"Task: {item.task}")
        pdf.multi_cell(0, 8, f"Owner: {item.owner}")
        pdf.multi_cell(0, 8, f"Deadline: {item.deadline}")
        pdf.ln(2)

    # Priority
    pdf.set_font("Helvetica", "B", 14)
    pdf.ln(4)
    pdf.cell(0, 10, "Priority Classification", ln=True)

    pdf.set_font("Helvetica", size=12)
    for item in result["priorities"].priorities:
        pdf.multi_cell(0, 8, f"{item.task} - {item.priority}")

    # Return bytes for Streamlit
    pdf_bytes = pdf.output(dest="S")

    if isinstance(pdf_bytes, str):
       pdf_bytes = pdf_bytes.encode("latin-1")

    return BytesIO(pdf_bytes)
# ====================================================
# ✅ ADD THESE LINES HERE
# ====================================================

@st.cache_resource
def load_embedding_model():
    """Load embedding model only once."""
    return EmbeddingModel.load_model()

@st.cache_resource
def load_workflow():
    """Build LangGraph workflow only once."""
    return MeetingWorkflow.build()

# ----------------------------------------------------
# File Upload
# ----------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Meeting Transcript",
    type=["txt", "docx", "pdf"],
)

analyze_button = st.button("Analyze Meeting", use_container_width=True)

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
        workflow = load_workflow()
        result = workflow.invoke(state)

    st.success("Meeting analyzed successfully!")

    # ------------------------------------------------
    # Topics
    # ------------------------------------------------

    st.header(" Discussion Topics")

    for topic in result["topics"].topics:
        st.markdown(f"- {topic}")

    # ------------------------------------------------
    # Summary
    # ------------------------------------------------

    st.header(" Meeting Summary")

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

    st.header(" Action Items")

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

    st.header(" Priority Classification")

    for item in result["priorities"].priorities:
        st.markdown(f"**{item.task}** — `{item.priority}`")

    # ------------------------------------------------
    # Download PDF
    # ------------------------------------------------

    st.header(" Download Meeting Notes")

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
