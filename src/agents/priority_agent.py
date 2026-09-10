

import sys

from langchain_core.runnables import RunnableLambda

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
            llm = MeetingLLM.load_model()
            parser = OutputParser.priority_parser()

            def retrieve_context(_):
                results = retriever.retrieve(cls.QUERY)

                return "\n\n".join(node.text for node in results)

            chain = (RunnableLambda(lambda _: {
                        "transcript": retrieve_context(None),
                        "format_instructions": parser.get_format_instructions(),})| PRIORITY_PROMPT| llm| parser)

            logger.info("Priority Agent executed successfully.")

            return chain.invoke({})

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)
