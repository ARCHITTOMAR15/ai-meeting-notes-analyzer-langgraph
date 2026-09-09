
from pydantic import BaseModel


class ActionItem(BaseModel):
    task: str
    owner: str
    deadline: str


class ActionOutput(BaseModel):
    action_items: list[ActionItem]
