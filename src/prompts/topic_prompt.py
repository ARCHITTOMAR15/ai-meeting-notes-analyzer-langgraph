
from langchain_core.prompts import PromptTemplate

TOPIC_PROMPT = PromptTemplate.from_template("""
You are an AI Meeting Notes Assistant.

Extract the MAIN DISCUSSION TOPICS from the meeting transcript.

Meeting Transcript:
{transcript}

{format_instructions}

IMPORTANT:
- Return ONLY a valid JSON object.
- Topics must be discussion subjects, NOT speaker names or job titles.
- Ignore names such as Product Manager, Customer Support Lead, QA Tester, Mobile Developer, Backend Developer, etc.
- Each topic should be a short phrase (3–8 words).
- Return between 3 and 8 unique topics.
- Do not repeat the transcript.
- Do not include explanations.
""")
