
from src.llm.output_parser import OutputParser


def test_topic_parser():
    assert OutputParser.topic_parser() is not None


def test_summary_parser():
    assert OutputParser.summary_parser() is not None


def test_action_parser():
    assert OutputParser.action_parser() is not None


def test_priority_parser():
    assert OutputParser.priority_parser() is not None
