
import sys 

from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.faiss import FaissVectorStore

import faiss

from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)

class FAISSIndexManager:
    EMBEDDING_DIMENSION=384

    @classmethod
    def create_index(cls,nodes,embedding_model):

        try:
            faiss_index=faiss.IndexFlatL2(cls.EMBEDDING_DIMENSION)

            vector_store= FaissVectorStore(faiss_index=faiss_index)

            index=VectorStoreIndex(nodes=nodes,embed_model=embedding_model,vector_store=vector_store,)
            logger.info("FAISS vector index created successfully.")

            return index

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)
