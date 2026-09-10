
from pathlib import Path

from src.agents.action_agent import ActionAgent
from src.data_ingestion.loader import TranscriptLoader
from src.preprocessing.cleaner import TranscriptCleaner
from src.preprocessing.chunker import TranscriptChunker
from src.vector_store.embedding_model import EmbeddingModel
from src.vector_store.faiss_index import FAISSIndexManager
from src.vector_store.retriever import TranscriptRetriever


RAW_PATH = Path("data/raw/Meeting_Transcript.txt")


def build_retriever():
    document = TranscriptLoader.load_document(str(RAW_PATH))
    clean_document = TranscriptCleaner.clean(document)
    nodes = TranscriptChunker.create_nodes(clean_document)

    embedding_model = EmbeddingModel.load_model()

    vector_index = FAISSIndexManager.create_index(
        nodes=nodes,
        embedding_model=embedding_model,
    )

    return TranscriptRetriever.create_retriever(vector_index)


def test_action_agent_runs():
    retriever = build_retriever()

    output = ActionAgent.invoke(retriever)

    assert output is not None


def test_action_output_contains_items():
    retriever = build_retriever()

    output = ActionAgent.invoke(retriever)

    assert len(output.action_items) > 0


def test_action_item_fields():
    retriever = build_retriever()

    output = ActionAgent.invoke(retriever)

    item = output.action_items[0]

    assert item.task != ""
    assert item.owner != ""
    assert isinstance(item.deadline, str)
