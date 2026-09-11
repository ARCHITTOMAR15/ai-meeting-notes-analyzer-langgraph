
from pathlib import Path

from src.graph.graph_nodes import GraphNodes
from src.graph.meeting_state import MeetingState

from src.data_ingestion.loader import TranscriptLoader
from src.preprocessing.cleaner import TranscriptCleaner
from src.preprocessing.chunker import TranscriptChunker
from src.vector_store.embedding_model import EmbeddingModel
from src.vector_store.faiss_index import FAISSIndexManager
from src.vector_store.retriever import TranscriptRetriever


RAW_PATH = Path("data/raw/Meeting_Transcript.txt")


def build_state() -> MeetingState:

    document = TranscriptLoader.load_document(str(RAW_PATH))
    clean_document = TranscriptCleaner.clean(document)
    nodes = TranscriptChunker.create_nodes(clean_document)

    embedding_model = EmbeddingModel.load_model()

    vector_index = FAISSIndexManager.create_index(
        nodes=nodes,
        embedding_model=embedding_model,
    )

    retriever = TranscriptRetriever.create_retriever(vector_index)

    return {
        "retriever": retriever,
        "topics": None,
        "summary": None,
        "action_items": None,
        "priorities": None,
    }


def test_topic_node():
    state = build_state()

    state = GraphNodes.topic_node(state)

    assert state["topics"] is not None


def test_summary_node():
    state = build_state()

    state = GraphNodes.summary_node(state)

    assert state["summary"] is not None


def test_action_node():
    state = build_state()

    state = GraphNodes.action_node(state)

    assert state["action_items"] is not None


def test_priority_node():
    state = build_state()

    state = GraphNodes.priority_node(state)

    assert state["priorities"] is not None


