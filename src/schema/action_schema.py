
from typing import Optional
from pydantic import BaseModel


class ActionItem(BaseModel):
    task: str
    owner: Optional[str] = "Not Assigned"
    deadline: Optional[str] = "Not Mentioned"


class ActionOutput(BaseModel):
    action_items: list[ActionItem]
