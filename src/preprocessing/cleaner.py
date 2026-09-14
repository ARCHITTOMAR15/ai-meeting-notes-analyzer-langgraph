
import re
import sys

from langchain_core.documents import Document

from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TranscriptCleaner:
    @staticmethod
    def clean(document: Document) -> Document:
        """
        Clean transcript text while preserving metadata.
        Compatible with LangChain Documents.
        """

        try:
            # LangChain stores text in page_content
            text = document.page_content.strip()

            # Remove extra blank lines
            text = re.sub(r"\n{3,}", "\n\n", text)

            # Remove repeated spaces/tabs
            text = re.sub(r"[ \t]+", " ", text)

            cleaned_document = Document(
                page_content=text,
                metadata=document.metadata,
            )

            logger.info("Transcript cleaned successfully.")

            return cleaned_document

        except Exception as error:
            logger.exception("Cleaning failed.")
            raise ProjectException(str(error), sys)
