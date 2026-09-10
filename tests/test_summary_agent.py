
from pathlib import Path

from src.agents.summary_agent import SummaryAgent
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


def test_summary_agent_runs():
    retriever = build_retriever()

    output = SummaryAgent.invoke(retriever)

    assert output is not None


def test_summary_output_fields():
    retriever = build_retriever()

    output = SummaryAgent.invoke(retriever)

    assert output.meeting_objective != ""
    assert len(output.key_discussion_points) > 0
    assert isinstance(output.decisions_taken, list)
