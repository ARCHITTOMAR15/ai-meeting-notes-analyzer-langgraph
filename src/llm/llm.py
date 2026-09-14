import os
import sys
import streamlit as st
import torch

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline

from src.config.config import load_config
from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"


# ------------------------------------------------------------------
# Cache ONLY this standalone function
# ------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def _cached_model():
    config = load_config()
    llm_config = config["llm"]

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

    logger.info("Qwen model loaded successfully.")

    return HuggingFacePipeline(pipeline=text_pipeline)


# ------------------------------------------------------------------
# This class is used by all agents
# ------------------------------------------------------------------
class MeetingLLM:

    @staticmethod
    def load_model():
        try:
            return _cached_model()
        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)
