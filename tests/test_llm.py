import pytest
from src.llm.llm import MeetingLLM


@pytest.fixture(scope="module")
def llm():
    return MeetingLLM.load_model()


def test_llm_loads(llm):
    assert llm is not None


def test_llm_generates_response(llm):
    response = llm.invoke("What is the capital of India?")

    assert isinstance(response, str)
    assert len(response) > 0
