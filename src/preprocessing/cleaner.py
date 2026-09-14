
import re
import sys

from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TranscriptCleaner:
    @staticmethod
    def clean(document):
        try:
            from llama_index.core.schema import Document

            text = document.text.strip()

            text = re.sub(r"\n{3,}", "\n\n", text)
            text = re.sub(r"[ \t]+", " ", text)

            cleaned_document = Document(
                text=text,
                metadata=document.metadata if hasattr(document, "metadata") else {}
            )

            logger.info("Transcript cleaned successfully.")
            return cleaned_document

        except Exception as e:
            logger.exception("Cleaning failed.")
            raise ProjectException(e, sys)
