
import sys 
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger=get_logger(__name__)


class EmbeddingModel:
    MODEL_NAME= "BAAI/bge-small-en-v1.5"

    @classmethod
    def load_model(cls)->HuggingFaceEmbedding:

        try:
            embedding_model=HuggingFaceEmbedding(model_name=cls.MODEL_NAME)
            logger.info(f"Embedding model loaded: {cls.MODEL_NAME}")

            return embedding_model

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)

