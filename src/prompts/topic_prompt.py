from langchain_core.prompts import PromptTemplate

TOPIC_PROMPT = PromptTemplate(
    template="""
You are an expert AI meeting analyst.

Analyze the meeting transcript below and identify the main discussion topics.

Meeting Transcript:
{transcript}

IMPORTANT:
Return ONLY valid JSON in this exact format.

{{
    "topics": [
        "Topic 1",
        "Topic 2",
        "Topic 3"
    ]
}}

Do not add explanations.
Do not use markdown.
Do not wrap JSON inside ```json.
""",
    input_variables=["transcript"],
)
