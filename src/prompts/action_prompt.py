
from langchain_core.prompts import PromptTemplate

ACTION_PROMPT = PromptTemplate.from_template("""
You are an AI Meeting Notes Assistant.

Extract all action items from the meeting transcript.

Meeting Transcript:
{transcript}

{format_instructions}

IMPORTANT RULES:
- Return ONLY a valid JSON object.
- Your response MUST start with {{ and end with }}.
- Do NOT write headings.
- Do NOT write explanations.
- Do NOT repeat the transcript.
- Do NOT use Markdown code fences (```json).
- If a deadline is not mentioned, use "Not Mentioned".
- If an owner is not mentioned, use "Not Mentioned".

Each action item should contain:
- task
- owner
- deadline
""")
