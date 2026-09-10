
from langchain_core.prompts import PromptTemplate

SUMMARY_PROMPT = PromptTemplate.from_template("""
You are an AI Meeting Notes Assistant.

Generate a concise meeting summary from the meeting transcript.

Meeting Transcript:
{transcript}

{format_instructions}

IMPORTANT:
- Your response MUST start with `{{`.
- Your response MUST end with `}}`.
- Return ONLY a valid JSON object.
- Do NOT add markdown headings.
- Do NOT add an extra "Summary" section.
- Do NOT repeat the transcript.
- Keep the summary concise and factual.
""")
