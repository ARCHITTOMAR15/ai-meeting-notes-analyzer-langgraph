
from typing import TypedDict

from src.schema.action_schema import ActionOutput
from src.schema.priority_schema import PriorityOutput
from src.schema.summary_schema import SummaryOutput
from src.schema.topic_schema import TopicOutput


class MeetingState(TypedDict):
    retriever:object

    topics:TopicOutput|None
    summary:SummaryOutput|None
    action_items:ActionOutput|None
    priorities:PriorityOutput|None

