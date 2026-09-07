
from pathlib import Path
import sys

from llama_index.core import SimpleDirectoryReader
from llama_index.core.schema import Document

from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TranscriptLoader:


    SUPPORTED_FORMATS = {".txt", ".docx", ".pdf"}

    @classmethod
    def load_document(cls, file_path: str) -> Document:


        try:
            path = Path(file_path)

            # File existence check
            if not path.exists():
                raise FileNotFoundError(
                    f"Transcript not found: {file_path}"
                )

            # File format validation
            if path.suffix.lower() not in cls.SUPPORTED_FORMATS:
                raise ValueError(
                    f"Unsupported file format: {path.suffix}. "
                    f"Supported formats: {sorted(cls.SUPPORTED_FORMATS)}"
                )

            # Load document
            reader = SimpleDirectoryReader(
                input_files=[str(path)],
                filename_as_id=True,
            )

            documents = reader.load_data()

            if len(documents) != 1:
                raise ValueError(
                    "Expected exactly one transcript document."
                )

            document = documents[0]

            # Add custom metadata


            logger.info(f"Transcript loaded successfully: {path.name}")

            return document

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)

    @classmethod
    def load_documents(cls, folder_path: str) -> list[Document]:


        try:
            path = Path(folder_path)

            # Folder existence check
            if not path.exists():
                raise FileNotFoundError(
                    f"Transcript folder not found: {folder_path}"
                )

            # Ensure it is a directory
            if not path.is_dir():
                raise NotADirectoryError(
                    f"Expected a folder path, got: {folder_path}"
                )

            # Load all supported documents
            reader = SimpleDirectoryReader(
                input_dir=str(path),
                filename_as_id=True,
            )

            documents = reader.load_data()

            # Check if any documents were loaded
            if len(documents) == 0:
                raise ValueError(
                    "No supported transcript files found in the folder."
                )

            # Add custom metadata to every document


            logger.info(
                f"Loaded {len(documents)} transcripts successfully from: {path.name}"
            )

            return documents

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)


