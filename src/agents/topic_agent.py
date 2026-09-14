
import sys

from langchain_core.output_parsers import StrOutputParser

from src.llm.llm import MeetingLLM
from src.llm.output_parser import OutputParser
from src.prompts.topic_prompt import TOPIC_PROMPT
from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TopicAgent:

    QUERY = "What are the main discussion topics in this meeting?"

    @classmethod
    def invoke(cls, retriever):

        try:
            # Load cached Hugging Face LLM
            llm = MeetingLLM.load_model()

            # Pydantic parser
            parser = OutputParser.topic_parser()

            # Retrieve relevant transcript chunks
            results = retriever.invoke(cls.QUERY)

            transcript = "\n\n".join(
                doc.page_content for doc in results
            )

            # Prompt → LLM → String
            chain = (
                TOPIC_PROMPT
                | llm
                | StrOutputParser()
            )

            # Pass transcript and JSON format instructions
            response = chain.invoke({
                "transcript": transcript,
                "format_instructions": parser.get_format_instructions(),
            })

            logger.info("Topic Agent executed successfully.")

            # Parse JSON response into TopicOutput
            parsed = parser.parse(response)

            return parsed.topics

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)
