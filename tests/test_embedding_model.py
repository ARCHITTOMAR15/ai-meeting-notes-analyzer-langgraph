
from src.vector_store.embedding_model import EmbeddingModel

def test_embedding_model_load():
    embedding_model=EmbeddingModel.load_model()

    assert embedding_model is not None

def test_embedding_dimension():
    embedding_model = EmbeddingModel.load_model()

    embedding = embedding_model.get_text_embedding("Hello world")

    assert isinstance(embedding, list)
    assert len(embedding) == 384
