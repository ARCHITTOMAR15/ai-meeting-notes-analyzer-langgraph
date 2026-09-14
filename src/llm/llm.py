import os
import sys
import streamlit as st

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

from src.config.config import load_config
from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"


@st.cache_resource(show_spinner=False)
def _cached_model():
    try:
        config = load_config()
        llm_config = config["llm"]

        hf_token = os.getenv("HF_TOKEN")

        if not hf_token:
            raise ValueError("HF_TOKEN not found in Streamlit Secrets.")

        logger.info(f"Connecting to Hugging Face Inference API: {MODEL_NAME}")

        endpoint = HuggingFaceEndpoint(
            repo_id=MODEL_NAME,
            huggingfacehub_api_token=hf_token,
            max_new_tokens=llm_config["max_tokens"],
            temperature=llm_config["temperature"],
            do_sample=False,
            timeout=120,
        )

        # Wrap endpoint as a chat model
        llm = ChatHuggingFace(llm=endpoint)

        logger.info("Hugging Face chat endpoint initialized successfully.")

        return llm

    except Exception as error:
        logger.error(str(error))
        raise ProjectException(str(error), sys)


class MeetingLLM:

    @staticmethod
    def load_model():
        return _cached_model()
