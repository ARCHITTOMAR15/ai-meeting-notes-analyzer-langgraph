
from pathlib import Path

from llama_index.core import VectorStoreIndex

from src.data_ingestion.loader import TranscriptLoader
from src.preprocessing.cleaner import TranscriptCleaner
from src.preprocessing.chunker import TranscriptChunker
from src.vector_store.embedding_model import EmbeddingModel
from src.vector_store.faiss_index import FAISSIndexManager


RAW_PATH = Path("data/raw/Meeting_Transcript.txt")

def test_create_faiss_index():
    document = TranscriptLoader.load_document(str(RAW_PATH))
    clean_document = TranscriptCleaner.clean(document)
    nodes = TranscriptChunker.create_nodes(clean_document)

    embedding_model = EmbeddingModel.load_model()

    index = FAISSIndexManager.create_index(
        nodes=nodes,
        embedding_model=embedding_model,
    )

    assert isinstance(index, VectorStoreIndex)

def test_faiss_index_contains_nodes():

    document = TranscriptLoader.load_document(str(RAW_PATH))
    clean_document = TranscriptCleaner.clean(document)
    nodes = TranscriptChunker.create_nodes(clean_document)

    embedding_model = EmbeddingModel.load_model()

    index = FAISSIndexManager.create_index(
        nodes=nodes,
        embedding_model=embedding_model,
    )

    assert index is not None


