from langchain_core.prompts import PromptTemplate

TOPIC_PROMPT = PromptTemplate(
    template="""
You are an expert AI meeting analyst.

Extract ONLY the main discussion topics from the meeting transcript.

Meeting Transcript:
{transcript}

Return between 3 and 8 short topic names.

Example output:

Budget Planning
Project Timeline
Client Feedback
Team Responsibilities

Do NOT explain anything.
Do NOT use markdown.
""",
    input_variables=["transcript"],
)
