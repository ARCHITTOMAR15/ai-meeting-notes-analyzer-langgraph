
import json
import re
import sys

from langchain_core.output_parsers import StrOutputParser

from src.llm.llm import MeetingLLM
from src.prompts.topic_prompt import TOPIC_PROMPT
from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TopicAgent:

    QUERY = "What are the main discussion topics in this meeting?"

    @classmethod
    def invoke(cls, retriever):

        try:
            llm = MeetingLLM.load_model()

            results = retriever.invoke(cls.QUERY)

            transcript = "\n\n".join(doc.page_content for doc in results)

            chain = (
                TOPIC_PROMPT
                | llm
                | StrOutputParser()
            )

            response = chain.invoke({"transcript": transcript})

            logger.info(f"RAW TOPIC RESPONSE:\n{response}")

            # ---------------- Try JSON first ----------------
            try:
                match = re.search(r"\{.*\}", response, flags=re.DOTALL)
                if match:
                    parsed = json.loads(match.group())
                    if "topics" in parsed:
                        return parsed["topics"]
            except Exception:
                pass

            # ---------------- Fallback for plain text ----------------
            topics = []

            for line in response.splitlines():
                line = line.strip()

                # Remove bullets/numbers
                line = re.sub(r"^[-•*]\s*", "", line)
                line = re.sub(r"^\d+[.)]\s*", "", line)

                if len(line) > 3:
                    topics.append(line)

            if topics:
                return topics[:8]

            raise ValueError("Could not extract topics from LLM response.")

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)

