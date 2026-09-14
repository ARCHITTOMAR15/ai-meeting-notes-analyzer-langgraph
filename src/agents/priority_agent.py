import json
import re
import sys

from langchain_core.output_parsers import StrOutputParser

from src.llm.llm import MeetingLLM
from src.prompts.priority_prompt import PRIORITY_PROMPT
from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PriorityAgent:

    QUERY = "Identify all tasks discussed in this meeting and classify their priority."

    @classmethod
    def invoke(cls, retriever):

        try:
            llm = MeetingLLM.load_model()

            results = retriever.invoke(cls.QUERY)

            transcript = "\n\n".join(doc.page_content for doc in results)

            chain = (
                PRIORITY_PROMPT
                | llm
                | StrOutputParser()
            )

            response = chain.invoke({"transcript": transcript})

            logger.info(f"RAW PRIORITY RESPONSE:\n{response}")

            match = re.search(r"\{.*\}", response, re.DOTALL)

            if not match:
                raise ValueError("No valid JSON returned by LLM.")

            parsed = json.loads(match.group())

            logger.info("Priority Agent executed successfully.")

            return parsed["priorities"]

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)
