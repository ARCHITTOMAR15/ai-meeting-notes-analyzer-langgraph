
from typing import TypedDict


class ActionItem(TypedDict):
    task: str
    owner: str
    deadline: str


class PriorityItem(TypedDict):
    task: str
    priority: str


class MeetingState(TypedDict):
    # Input
    retriever: object

    # LangGraph outputs
    topics: list[str] | None
    summary: str | None
    action_items: list[ActionItem] | None
    priorities: list[PriorityItem] | None
