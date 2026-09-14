from langchain_core.prompts import PromptTemplate

PRIORITY_PROMPT = PromptTemplate(
    template="""
You are an expert AI meeting analyst.

Identify every task discussed in this meeting transcript.

Classify each task as:
- High
- Medium
- Low

Meeting Transcript:
{transcript}

Return ONLY valid JSON.

{{
    "priorities": [
        {{
            "task": "Finish deployment",
            "priority": "High"
        }}
    ]
}}

Do not add explanations.
Do not use markdown.
Do not wrap JSON inside ```json.
""",
    input_variables=["transcript"],
)
