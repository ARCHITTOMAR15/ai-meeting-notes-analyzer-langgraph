

import os
os.environ["HF_HOME"] = "C:/Users/Lenovo/.cache/huggingface"

import tempfile
from pathlib import Path

import streamlit as st

from src.config.config import load_config
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

st.set_page_config(
    page_title="AI Meeting Notes Analyzer",
    page_icon="📝",
    layout="wide",
)

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

        # Embeddings
        embedding_model = EmbeddingModel.load_model()

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

# ----------------------------------------------------
# No File Uploaded
# ----------------------------------------------------

elif analyze_button:
    st.warning("Please upload a meeting transcript before clicking Analyze Meeting.")
