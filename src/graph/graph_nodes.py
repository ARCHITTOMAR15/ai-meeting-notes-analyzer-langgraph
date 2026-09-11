
import sys 
from src.agents.action_agent import ActionAgent
from src.agents.priority_agent import PriorityAgent
from src.agents.summary_agent import SummaryAgent
from src.agents.topic_agent import TopicAgent
from src.graph.meeting_state import MeetingState
from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class GraphNodes:

    @staticmethod
    def topic_node(state:MeetingState)->MeetingState:

        try:
            state["topics"]=TopicAgent.invoke(state["retriever"])

            logger.info("Topic node Completed")

            return state

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)


    @staticmethod
    def summary_node(state:MeetingState)->MeetingState:

        try:
            state["summary"]=SummaryAgent.invoke(state["retriever"])

            logger.info("Summary node completed.")

            return state

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)


    @staticmethod
    def action_node(state: MeetingState) -> MeetingState:

        try:
            state["action_items"] = ActionAgent.invoke(state["retriever"])

            logger.info("Action node completed.")

            return state

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)

    @staticmethod
    def priority_node(state: MeetingState) -> MeetingState:

        try:
            state["priorities"] = PriorityAgent.invoke(state["retriever"])

            logger.info("Priority node completed.")

            return state

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)




