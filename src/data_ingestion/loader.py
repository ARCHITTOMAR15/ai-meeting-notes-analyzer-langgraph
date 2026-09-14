
import os
import sys

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)

from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TranscriptLoader:

    @classmethod
    def load_document(cls, file_path: str) -> Document:
        """
        Load TXT, PDF or DOCX transcript and return a single LangChain Document.
        """

        try:
            extension = os.path.splitext(file_path)[1].lower()

            if extension == ".pdf":
                loader = PyPDFLoader(file_path)

            elif extension == ".txt":
                loader = TextLoader(file_path, encoding="utf-8")

            elif extension == ".docx":
                loader = Docx2txtLoader(file_path)

            else:
                raise ValueError(f"Unsupported file format: {extension}")

            documents = loader.load()

            # Merge all pages into one transcript
            transcript = "\n\n".join(doc.page_content for doc in documents)

            logger.info(f"Transcript loaded successfully: {extension}")

            return Document(page_content=transcript)

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)

