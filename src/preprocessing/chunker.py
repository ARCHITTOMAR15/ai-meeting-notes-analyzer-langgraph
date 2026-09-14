
import sys

from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TranscriptChunker:

    @staticmethod
    def split(document, chunk_size=512, chunk_overlap=50):
        try:
            text = document.text if hasattr(document, "text") else str(document)

            chunks = []

            start = 0
            while start < len(text):
                end = start + chunk_size
                chunks.append(text[start:end])
                start += chunk_size - chunk_overlap

            logger.info(f"Created {len(chunks)} transcript chunks.")
            return chunks

        except Exception as e:
            logger.exception("Chunking failed.")
            raise ProjectException(e, sys)
