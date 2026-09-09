
from pydantic import BaseModel

class TopicOutput(BaseModel):
    topics:list[str]



