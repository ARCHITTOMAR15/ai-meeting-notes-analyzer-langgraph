from langchain_core.prompts import PromptTemplate

SUMMARY_PROMPT = PromptTemplate(
    template="""
You are an expert AI meeting analyst.

Summarize the meeting professionally.

Include:
- Meeting objective.
- Important discussion points.
- Final decisions.

Meeting Transcript:
{transcript}

Write one concise professional summary (150-250 words).

Do not use markdown.
Do not use JSON.
""",
    input_variables=["transcript"],
)
