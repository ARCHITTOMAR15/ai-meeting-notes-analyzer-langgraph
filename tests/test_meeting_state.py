
from src.graph.meeting_state import MeetingState

def test_meeting_state_creation():
    state:MeetingState={
        "retriever": object(),
        "topics": None,
        "summary": None,
        "action_items": None,
        "priorities": None,
    }

    assert state["topics"] is None
    assert state["summary"] is None



