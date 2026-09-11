
from pathlib import Path

from src.graph.meeting_state import MeetingState
from src.graph.workflow import MeetingWorkflow

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


def test_workflow_builds():
    app = MeetingWorkflow.build()

    assert app is not None


def test_workflow_runs():
    app = MeetingWorkflow.build()

    state = build_state()

    result = app.invoke(state)

    assert result["topics"] is not None
    assert result["summary"] is not None
    assert result["action_items"] is not None
    assert result["priorities"] is not None
