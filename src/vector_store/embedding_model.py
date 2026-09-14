import sys
from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

from src.config.config import load_config
from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class EmbeddingModel:

    @classmethod
    @lru_cache(maxsize=1)
    def load_model(cls):
        """
        Load Hugging Face embedding model once.
        Compatible with Streamlit Cloud.
        """

        try:
            config = load_config()
            model_name = config["embedding"]["model_name"]

            embedding_model = HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
                cache_folder="/tmp/huggingface"
            )

            logger.info(f"Embedding model loaded: {model_name}")

            return embedding_model

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)
