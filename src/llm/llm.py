
import os
import sys

from langchain_community.llms import LlamaCpp

from functools import lru_cache
from huggingface_hub import hf_hub_download
from src.config.config import load_config
from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MeetingLLM:
    @classmethod
    @lru_cache(maxsize=1)
    def load_model(cls) -> LlamaCpp:

        try:
            config = load_config()
            llm_config = config["llm"]
            #model_path = llm_config["model_path"]

            #if not os.path.exists(model_path):
                #raise FileNotFoundError(
                    #f"GGUF model not found at: {model_path}"
                #)
            model_path = hf_hub_download(
                  repo_id="Qwen/Qwen2.5-3B-Instruct-GGUF",
                  filename="qwen2.5-3b-instruct-q4_k_m.gguf",
                  cache_dir=os.getenv("HF_HOME", "/tmp/huggingface"),)



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

