
from langchain_core.prompts import PromptTemplate

PRIORITY_PROMPT = PromptTemplate.from_template("""
You are an AI Meeting Notes Assistant.

Assign a priority to each action item from the meeting transcript.

Priority levels:
- High
- Medium
- Low

Meeting Transcript:
{transcript}

{format_instructions}

IMPORTANT:
- Your response MUST start with `{{`.
- Your response MUST end with `}}`.
- Return ONLY a valid JSON object.
- Every task must have exactly one priority: High, Medium, or Low.
- Do NOT explain the priority.
- Do NOT repeat the transcript.
""")
