
from langchain_core.prompts import PromptTemplate

SUMMARY_PROMPT = PromptTemplate(
    template="""
You are an expert AI meeting analyst.

Read the transcript and generate a concise meeting summary.

Include:
- Meeting objective
- Key discussion points
- Decisions made

Meeting Transcript:
{transcript}

Return ONLY valid JSON in this exact format.

{{
    "summary": "A concise meeting summary covering the objective, discussion points and decisions."
}}

Do not add explanations.
Do not use markdown.
Do not wrap JSON inside ```json.
""",
    input_variables=["transcript"],
)
