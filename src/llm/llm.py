import os
import re
import sys

import streamlit as st
import torch

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.runnables import RunnableLambda

from src.config.config import load_config
from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"


# ------------------------------------------------------------------
# Clean Qwen output before Pydantic parsing
# ------------------------------------------------------------------
def strip_markdown_json(text: str) -> str:
    """
    Removes markdown code fences like ```json ... ``` from model output.
    """

    if not isinstance(text, str):
        text = str(text)

    text = text.strip()

    # Remove opening fence
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)

    # Remove closing fence
    text = re.sub(r"\s*```$", "", text)

    return text.strip()


# ------------------------------------------------------------------
# Cache Hugging Face model (loads only once)
# ------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def _cached_model():
    try:
        config = load_config()
        llm_config = config["llm"]

        logger.info(f"Loading Hugging Face model: {MODEL_NAME}")

        tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME,
            cache_dir=os.getenv("HF_HOME", "/tmp/huggingface"),
        )

        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            cache_dir=os.getenv("HF_HOME", "/tmp/huggingface"),
            torch_dtype=torch.float32,
            device_map="cpu",
            low_cpu_mem_usage=True,
        )

        text_pipeline = pipeline(
            task="text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=llm_config["max_tokens"],
            temperature=llm_config["temperature"],
            do_sample=False,
            repetition_penalty=1.1,
            pad_token_id=tokenizer.eos_token_id,
            truncation=True,
        )

        llm = HuggingFacePipeline(pipeline=text_pipeline)

        logger.info("Qwen model loaded successfully.")

        # Automatically remove ```json ... ``` wrappers
        return llm | RunnableLambda(strip_markdown_json)

    except Exception as error:
        logger.error(str(error))
        raise ProjectException(str(error), sys)


# ------------------------------------------------------------------
# Used by all agents
# ------------------------------------------------------------------
class MeetingLLM:

    @staticmethod
    def load_model():
        try:
            return _cached_model()

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)
