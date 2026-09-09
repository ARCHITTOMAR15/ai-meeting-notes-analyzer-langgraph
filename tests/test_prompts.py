
from langchain_core.prompts import PromptTemplate

from src.prompts.summary_prompt import SUMMARY_PROMPT
from src.prompts.topic_prompt import TOPIC_PROMPT
from src.prompts.action_prompt import ACTION_PROMPT
from src.prompts.priority_prompt import PRIORITY_PROMPT


def test_summary_prompt():
    assert isinstance(SUMMARY_PROMPT, PromptTemplate)


def test_topic_prompt():
    assert isinstance(TOPIC_PROMPT, PromptTemplate)


def test_action_prompt():
    assert isinstance(ACTION_PROMPT, PromptTemplate)


def test_priority_prompt():
    assert isinstance(PRIORITY_PROMPT, PromptTemplate)


def test_prompt_formatting():
    prompt = SUMMARY_PROMPT.format(
        transcript="John discussed website performance."
    )

    assert "website performance" in prompt
