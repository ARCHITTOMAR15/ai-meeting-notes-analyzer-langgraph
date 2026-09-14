from langchain_core.prompts import PromptTemplate

ACTION_PROMPT = PromptTemplate(
    template="""
You are an expert AI meeting analyst.

Extract all action items from this meeting transcript.

For every action item include:
- task
- owner
- deadline

If owner or deadline is missing, use:
"Not Assigned"
"Not Mentioned"

Meeting Transcript:
{transcript}

Return ONLY valid JSON.

{{
    "action_items": [
        {{
            "task": "Complete project report",
            "owner": "John",
            "deadline": "Friday"
        }}
    ]
}}

Do not add explanations.
Do not use markdown.
Do not wrap JSON inside ```json.
""",
    input_variables=["transcript"],
)
