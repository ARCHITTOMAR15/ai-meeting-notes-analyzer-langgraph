
from src.evaluation.validator import HallucinationValidator


TRANSCRIPT = """
John will optimize frontend assets this week.

Sarah will prepare the deployment report by Friday.

David will improve database indexing.
"""


def test_supported_statement():
    statement = "David will improve database indexing"

    assert HallucinationValidator.validate_statement(
        TRANSCRIPT,
        statement,
    )


def test_unsupported_statement():
    statement = "Alice will create a mobile application"

    assert not HallucinationValidator.validate_statement(
        TRANSCRIPT,
        statement,
    )


def test_multiple_statements():
    statements = [
        "David will improve database indexing",
        "Alice will create a mobile application",
    ]

    results = HallucinationValidator.validate_statements(
        TRANSCRIPT,
        statements,
    )

    assert results["David will improve database indexing"] is True
    assert results["Alice will create a mobile application"] is False
