
from bert_score import score
from rouge_score import rouge_scorer
from sklearn.metrics import precision_score, recall_score


class EvaluationMetrics:

    @staticmethod
    def calculate_rouge(reference:str,prediction:str)->dict:
        scorer= rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"],use_stemmer=True,)
        scores=scorer.score(reference,prediction)

        return {
            "rouge1": scores["rouge1"].fmeasure,
            "rouge2": scores["rouge2"].fmeasure,
            "rougeL": scores["rougeL"].fmeasure,}

    @staticmethod 
    def calculate_bertscore(reference: str, prediction: str) -> float:
        _, _, f1 = score([prediction],[reference],lang="en",verbose=False,)

        return float(f1.mean())

    @staticmethod
    def calculate_precision_recall(
        y_true: list[int],
        y_pred: list[int],
    ) -> dict:

        precision = precision_score(
            y_true,
            y_pred,
            zero_division=0,
        )

        recall = recall_score(
            y_true,
            y_pred,
            zero_division=0,
        )

        return {
            "precision": precision,
            "recall": recall,
        }
