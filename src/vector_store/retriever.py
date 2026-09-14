import sys

from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TranscriptRetriever:

    TOP_K = 3

    @classmethod
    def create_retriever(cls, vector_store):
        """
        Create LangChain FAISS retriever.
        """

        try:
            retriever = vector_store.as_retriever(
                search_kwargs={"k": cls.TOP_K}
            )

            logger.info(f"Retriever created with Top-K = {cls.TOP_K}")

            return retriever

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)

    @staticmethod
    def retrieve(retriever, query: str):
        """
        Retrieve relevant transcript chunks.
        """

        try:
            return retriever.invoke(query)

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)
