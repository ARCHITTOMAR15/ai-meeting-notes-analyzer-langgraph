
import os
import sys

from langchain_community.llms import LlamaCpp

from src.config.config import load_config
from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MeetingLLM:
    @classmethod
    def load_model(cls) -> LlamaCpp:

        try:
            config = load_config()
            llm_config = config["llm"]
            model_path = llm_config["model_path"]

            if not os.path.exists(model_path):
                raise FileNotFoundError(
                    f"GGUF model not found at: {model_path}"
                )

            llm = LlamaCpp(
                model_path=model_path,
                temperature=llm_config["temperature"],
                max_tokens=llm_config["max_tokens"],
                n_ctx=llm_config["context_window"],
                n_gpu_layers=llm_config["gpu_layers"],
                stop=["\n\nThe", "\n\nExplanation", "\n\nSummary"],
                verbose=False,
            )

            logger.info(f"Loaded LLM: {llm_config['model_name']}")

            return llm

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)

