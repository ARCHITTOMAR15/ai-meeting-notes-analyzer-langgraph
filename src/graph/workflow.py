
import sys 

from langgraph.graph import END,START,StateGraph
from src.graph.graph_nodes import GraphNodes
from src.graph.meeting_state import MeetingState
from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)

class MeetingWorkflow:

    @staticmethod
    def build():

        try:
            workflow=StateGraph(MeetingState)
            workflow.add_node("topic",GraphNodes.topic_node)
            workflow.add_node("summary",GraphNodes.summary_node)
            workflow.add_node("action",GraphNodes.action_node)
            workflow.add_node("priority", GraphNodes.priority_node)

            workflow.add_edge(START,"topic")
            workflow.add_edge("topic","summary")
            workflow.add_edge("summary","action")
            workflow.add_edge("action","priority")
            workflow.add_edge("priority",END)

            app=workflow.compile()

            logger.info("meeting workflow compiled successfully")

            return app

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)
