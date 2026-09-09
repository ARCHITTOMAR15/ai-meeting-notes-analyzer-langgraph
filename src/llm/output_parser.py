
"""
Output Parser Module

Phase 4 — LLM Integration
"""

from langchain_core.output_parsers import PydanticOutputParser

from src.schema.topic_schema import TopicOutput
from src.schema.summary_schema import SummaryOutput
from src.schema.action_schema import ActionOutput
from src.schema.priority_schema import PriorityOutput


class OutputParser:

    @staticmethod
    def topic_parser():
        return PydanticOutputParser(pydantic_object=TopicOutput)

    @staticmethod
    def summary_parser():
        return PydanticOutputParser(pydantic_object=SummaryOutput)

    @staticmethod
    def action_parser():
        return PydanticOutputParser(pydantic_object=ActionOutput)

    @staticmethod
    def priority_parser():
        return PydanticOutputParser(pydantic_object=PriorityOutput)
