from pydantic import BaseModel


class PriorityItem(BaseModel):
    task: str
    priority: str


class PriorityOutput(BaseModel):
    priorities: list[PriorityItem]
