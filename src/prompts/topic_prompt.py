
from langchain_core.prompts import PromptTemplate

TOPIC_PROMPT = PromptTemplate.from_template("""
You are an AI Meeting Notes Assistant.

Your task is to extract the main discussion topics from the meeting transcript.

### Rules
- Extract only the main discussion topics.
- Return each topic only once.
- Do not explain the topics.
- Do not include speaker names.
- Do not repeat the transcript.
- Return between 3 and 8 topics, depending on the meeting content.
- End your response after the numbered list.

### Transcript
{transcript}

Generate only the numbered list of discussion topics.
Do not add any heading, explanation, or summary.
Do not repeat any topic or transcript.
""")
