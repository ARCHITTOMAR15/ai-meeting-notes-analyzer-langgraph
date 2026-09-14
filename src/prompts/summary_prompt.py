SUMMARY_PROMPT = PromptTemplate(
    template="""
You are an expert AI meeting analyst.

Summarize the meeting including:
- Meeting objective
- Key discussions
- Decisions made

Transcript:
{transcript}

Return ONLY valid JSON.

{format_instructions}
""",
    input_variables=["transcript", "format_instructions"],
)
