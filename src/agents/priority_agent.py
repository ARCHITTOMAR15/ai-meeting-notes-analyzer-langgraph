import sys

from langchain_core.output_parsers import StrOutputParser

from src.llm.llm import MeetingLLM
from src.prompts.priority_prompt import PRIORITY_PROMPT
from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PriorityAgent:

    QUERY = "Identify tasks and classify their priority."

    @classmethod
    def invoke(cls, retriever):
        try:
            llm = MeetingLLM.load_model()

            docs = retriever.invoke(cls.QUERY)
            transcript = "\n\n".join(doc.page_content for doc in docs)

            chain = PRIORITY_PROMPT | llm | StrOutputParser()

            response = chain.invoke({"transcript": transcript})

            if hasattr(response, "content"):
                response = response.content

            logger.info(f"RAW PRIORITY RESPONSE:\n{response}")

            priorities = []

            task = priority = None

            for line in response.splitlines():
                line = line.strip()

                if line.lower().startswith("task:"):
                    if task:
                        priorities.append({
                            "task": task,
                            "priority": priority or "Medium",
                        })

                    task = line.split(":", 1)[1].strip()
                    priority = None

                elif line.lower().startswith("priority:"):
                    priority = line.split(":", 1)[1].strip().title()

            if task:
                priorities.append({
                    "task": task,
                    "priority": priority or "Medium",
                })

            return priorities

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)

