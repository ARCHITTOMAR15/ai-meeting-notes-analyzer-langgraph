
import re
import sys

from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TranscriptCleaner:

    @staticmethod
    def clean(document):
        try:
            # Lazy import (important for Streamlit Cloud)
            from llama_index.core.schema import Document

            text = document.text.strip()

            text = re.sub(r"\n{3,}", "\n\n", text)
            text = re.sub(r"[ \t]+", " ", text)

            cleaned_document = Document(
                text=text,
                metadata=document.metadata.copy() if document.metadata else {},
            )

            logger.info("Transcript cleaned successfully.")
            return cleaned_document

        except Exception as e:
            logger.error(str(e))
            raise ProjectException(e, sys)
