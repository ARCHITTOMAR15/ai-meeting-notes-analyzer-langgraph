
import sys

from langchain_core.runnables import RunnableLambda

from src.llm.llm import MeetingLLM
from src.llm.output_parser import OutputParser
from src.prompts.summary_prompt import SUMMARY_PROMPT
from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SummaryAgent:
    QUERY = ("Summarize this meeting including objective, key discussions, and decisions.")

    @classmethod
    def invoke(cls,retriever):

        try:
            llm=MeetingLLM.load_model()
            parser=OutputParser.summary_parser()

            def retrieve_context(_):
                results=retriever.retrieve(cls.QUERY)
                return "\n\n".join(node.text for node in results)

            chain=(RunnableLambda(lambda _:{"transcript": retrieve_context(None),
                        "format_instructions": parser.get_format_instructions(),})
                       |SUMMARY_PROMPT|llm|parser)

            logger.info("Summary Agent executed successfully.")

            return chain.invoke({})

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)



