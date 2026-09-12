

import re

class HallucinationValidator:
    @staticmethod
    def normalize_text(text:str)->str:
        text=text.lower()
        text=re.sub(r"[^\w\s]", "", text)
        text=re.sub(r"\s+", " ", text).strip()

        return text 

    @classmethod
    def validate_statement(cls,transcript:str,statement:str)->bool:
        transcript=cls.normalize_text(transcript)
        statement=cls.normalize_text(statement)

        return statement in transcript

    @classmethod
    def validate_statements(cls,transcript: str,statements: list[str],) -> dict:

        results = {}

        for statement in statements:
            results[statement] = cls.validate_statement(
                transcript,
                statement,
            )

        return results
