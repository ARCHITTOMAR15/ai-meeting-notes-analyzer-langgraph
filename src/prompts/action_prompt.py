from langchain_core.prompts import PromptTemplate
ACTION_PROMPT = PromptTemplate(
    template="""
Extract all action items from this meeting.

Include task owner and deadline if mentioned.

Transcript:
{transcript}

Return ONLY valid JSON.

{format_instructions}
""",
    input_variables=["transcript", "format_instructions"],
)
