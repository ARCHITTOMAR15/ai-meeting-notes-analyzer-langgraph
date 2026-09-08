
"""
Retriever Module

Phase 3 — Vector Store & Retrieval

Retrieves relevant transcript chunks from FAISS.
"""

import sys

from llama_index.core.indices.vector_store.retrievers import VectorIndexRetriever

from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TranscriptRetriever:


    TOP_K = 3

    @classmethod
    def create_retriever(cls, vector_index):


        try:
            retriever = VectorIndexRetriever(
                index=vector_index,
                similarity_top_k=cls.TOP_K,
            )

            logger.info(f"Retriever created with Top-K = {cls.TOP_K}")

            return retriever

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)

    @staticmethod
    def retrieve(retriever, query: str):


        try:
            return retriever.retrieve(query)

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)







