

import re
import sys
from llama_index.core.schema import Document
from src.utils.exception import ProjectException
from src.utils.logger import get_logger
logger=get_logger(__name__)


class TranscriptCleaner:
    @staticmethod
    def clean(document:Document)->Document:

        try:
            text=document.text.strip()

            text=re.sub(r"\n{3,}", "\n\n", text)

            cleaned_document=Document(text=text,metadata=document.metadata.copy())

            logger.info("Transcript Normalized Sucessfully")

            return cleaned_document

        except Exception as e:
            logger.e(str(error))
            raise ProjectException(str(error), sys)

