import sys

from langchain_core.output_parsers import StrOutputParser

from src.llm.llm import MeetingLLM
from src.prompts.summary_prompt import SUMMARY_PROMPT
from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SummaryAgent:

    QUERY = "Summarize this meeting."

    @classmethod
    def invoke(cls, retriever):
        try:
            llm = MeetingLLM.load_model()

            docs = retriever.invoke(cls.QUERY)
            transcript = "\n\n".join(doc.page_content for doc in docs)

            chain = SUMMARY_PROMPT | llm | StrOutputParser()

            response = chain.invoke({"transcript": transcript})

            logger.info("Summary Agent executed successfully.")

            return response.strip()

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)

