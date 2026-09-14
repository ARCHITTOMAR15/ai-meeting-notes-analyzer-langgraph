import re
import sys

from langchain_core.output_parsers import StrOutputParser

from src.llm.llm import MeetingLLM
from src.prompts.action_prompt import ACTION_PROMPT
from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ActionAgent:

    QUERY = "Extract action items from this meeting."

    @classmethod
    def invoke(cls, retriever):
        try:
            llm = MeetingLLM.load_model()

            docs = retriever.invoke(cls.QUERY)
            transcript = "\n\n".join(doc.page_content for doc in docs)

            chain = ACTION_PROMPT | llm | StrOutputParser()

            response = chain.invoke({"transcript": transcript})

            logger.info(f"RAW ACTION RESPONSE:\n{response}")

            actions = []

            task = owner = deadline = None

            for line in response.splitlines():
                line = line.strip()

                if line.lower().startswith("task:"):
                    if task:
                        actions.append({
                            "task": task,
                            "owner": owner or "Not Assigned",
                            "deadline": deadline or "Not Mentioned",
                        })

                    task = line.split(":", 1)[1].strip()
                    owner = deadline = None

                elif line.lower().startswith("owner:"):
                    owner = line.split(":", 1)[1].strip()

                elif line.lower().startswith("deadline:"):
                    deadline = line.split(":", 1)[1].strip()

            if task:
                actions.append({
                    "task": task,
                    "owner": owner or "Not Assigned",
                    "deadline": deadline or "Not Mentioned",
                })

            return actions

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)

