

import sys

from langchain_core.runnables import RunnableLambda

from src.llm.llm import MeetingLLM
from src.llm.output_parser import OutputParser
from src.prompts.action_prompt import ACTION_PROMPT
from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ActionAgent:

    QUERY=("Extract all action items, task owners, and deadlines from this meeting.")

    @classmethod
    def invoke(cls,retriever):
        try:
            llm = MeetingLLM.load_model()
            parser = OutputParser.action_parser()

            def retrieve_context(_):
                results = retriever.retrieve(cls.QUERY)

                return "\n\n".join(node.text for node in results)

            chain = (
                RunnableLambda(
                    lambda _: {
                        "transcript": retrieve_context(None),
                        "format_instructions": parser.get_format_instructions(),})| ACTION_PROMPT| llm| parser)

            logger.info("Action Agent executed successfully.")

            return chain.invoke({})

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)

