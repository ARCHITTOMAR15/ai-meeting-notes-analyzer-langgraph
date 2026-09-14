
import sys

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config.config import load_config
from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TranscriptChunker:

    @classmethod
    def split(cls, document):
        try:
            config = load_config()["rag"]

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=config["chunk_size"],
                chunk_overlap=config["chunk_overlap"]
            )

            chunks = splitter.split_documents([document])

            logger.info(f"Created {len(chunks)} transcript chunks.")

            return chunks

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)
