import sys
import faiss

from langchain_community.vectorstores import FAISS

from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class FAISSIndexManager:
    """
    Creates and stores a FAISS vector database using
    LangChain + HuggingFace embeddings.
    """

    @classmethod
    def create_index(cls, documents, embedding_model):
        try:
            # Build FAISS index directly from LangChain documents
            vector_store = FAISS.from_documents(
                documents=documents,
                embedding=embedding_model
            )

            logger.info("FAISS vector index created successfully.")

            return vector_store

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)
