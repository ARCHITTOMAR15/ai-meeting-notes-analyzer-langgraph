

from src.evaluation.metrics import EvaluationMetrics

REFERENCE = ("The team discussed improving website performance and database indexing.")
PREDICTION = PREDICTION = ("The meeting focused on website performance improvements and database optimization.")


def test_rouge():
    scores = EvaluationMetrics.calculate_rouge(
        REFERENCE,
        PREDICTION,
    )

    assert "rouge1" in scores
    assert "rouge2" in scores
    assert "rougeL" in scores

def test_bertscore():
    score = EvaluationMetrics.calculate_bertscore(
        REFERENCE,
        PREDICTION,
    )

    assert 0 <= score <= 1


def test_precision_recall():
    y_true = [1, 1, 0, 1]
    y_pred = [1, 0, 0, 1]

    metrics = EvaluationMetrics.calculate_precision_recall(
        y_true,
        y_pred,
    )

    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 2 / 3
