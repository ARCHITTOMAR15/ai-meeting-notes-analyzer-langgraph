import sys

from langchain_core.output_parsers import StrOutputParser

from src.llm.llm import MeetingLLM
from src.llm.output_parser import OutputParser
from src.prompts.summary_prompt import SUMMARY_PROMPT
from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SummaryAgent:

    QUERY = (
        "Summarize this meeting including objective, key discussions, and decisions."
    )

    @classmethod
    def invoke(cls, retriever):

        try:
            llm = MeetingLLM.load_model()
            parser = OutputParser.summary_parser()

            # Retrieve relevant transcript chunks
            results = retriever.invoke(cls.QUERY)

            transcript = "\n\n".join(
                doc.page_content for doc in results
            )

            # Chain: Prompt → LLM → Text Output
            chain = (
                SUMMARY_PROMPT
                | llm
                | StrOutputParser()
            )

            # Pass BOTH transcript and format instructions
            response = chain.invoke({
                "transcript": transcript,
                "format_instructions": parser.get_format_instructions(),
            })

            logger.info("Summary Agent executed successfully.")

            # Convert JSON string to Pydantic object
            parsed = parser.parse(response)

            return parsed.summary

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)
