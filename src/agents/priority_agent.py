

import sys

from langchain_core.output_parsers import StrOutputParser

from src.llm.llm import MeetingLLM
from src.llm.output_parser import OutputParser
from src.prompts.priority_prompt import PRIORITY_PROMPT
from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PriorityAgent:

    QUERY = (
        "Identify all tasks discussed in this meeting and classify "
        "their priority as High, Medium, or Low."
    )

    @classmethod
    def invoke(cls, retriever):

        try:
            # Load cached LLM
            llm = MeetingLLM.load_model()

            # Output parser
            parser = OutputParser.priority_parser()

            # Retrieve relevant transcript chunks
            results = retriever.invoke(cls.QUERY)

            transcript = "\n\n".join(
                doc.page_content for doc in results
            )

            # Prompt → LLM → String
            chain = (
                PRIORITY_PROMPT
                | llm
                | StrOutputParser()
            )

            # Pass transcript + format instructions
            response = chain.invoke({
                "transcript": transcript,
                "format_instructions": parser.get_format_instructions(),
            })

            logger.info("Priority Agent executed successfully.")

            # Parse JSON response
            parsed = parser.parse(response)

            return parsed.priorities

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)
