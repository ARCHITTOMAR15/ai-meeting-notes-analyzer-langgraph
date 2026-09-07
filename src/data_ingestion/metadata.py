
from pathlib import Path
import sys 

from llama_index.core.schema import Document
from src.utils.exception import ProjectException

from src.utils.logger import get_logger
logger = get_logger(__name__)

class TranscriptMetadata:

    @staticmethod
    def extract(document:Document,file_path:str)->dict:

        try:
            path=Path(file_path)

            metadata={"file_name":path.name,
                      "file_type":path.suffix.lower().replace(".",""),
                      "file_size_mb":round(path.stat().st_size/(1024*1024),4),
                      "character_count":len(document.text),
                      "word_count":len(document.text.split()),
                      "line_count":len(document.text.splitlines()),}

            logger.info(f"Metadata extracted for {path.name}")

            return metadata

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)


