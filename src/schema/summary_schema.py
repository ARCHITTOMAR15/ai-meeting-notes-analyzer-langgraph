from pydantic import BaseModel


class SummaryOutput(BaseModel):
    meeting_objective: str
    key_discussion_points: list[str]
    decisions_taken: list[str]
