import sys

from langchain_core.output_parsers import StrOutputParser

from src.llm.llm import MeetingLLM
from src.llm.output_parser import OutputParser
from src.prompts.action_prompt import ACTION_PROMPT
from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ActionAgent:

    QUERY = "Extract all action items, task owners, and deadlines from this meeting."

    @classmethod
    def invoke(cls, retriever):

        try:
            # Load cached LLM
            llm = MeetingLLM.load_model()

            # Output parser
            parser = OutputParser.action_parser()

            # Retrieve relevant transcript chunks
            results = retriever.invoke(cls.QUERY)

            transcript = "\n\n".join(
                doc.page_content for doc in results
            )

            # Prompt → LLM → Text
            chain = (
                ACTION_PROMPT
                | llm
                | StrOutputParser()
            )

            # Pass transcript + format instructions
            response = chain.invoke({
                "transcript": transcript,
                "format_instructions": parser.get_format_instructions(),
            })

            logger.info("Action Agent executed successfully.")

            # Parse JSON response
            parsed = parser.parse(response)

            return parsed.action_items

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)
