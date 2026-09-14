PRIORITY_PROMPT = PromptTemplate(
    template="""
Identify every task discussed in this meeting.

Classify each task as High, Medium, or Low priority.

Transcript:
{transcript}

Return ONLY valid JSON.

{format_instructions}
""",
    input_variables=["transcript", "format_instructions"],
)
