from pydantic import BaseModel
from typing import Literal

class PriorityItem(BaseModel):
    task: str
    priority: Literal["High", "Medium", "Low"]


class PriorityOutput(BaseModel):
    priorities: list[PriorityItem]
