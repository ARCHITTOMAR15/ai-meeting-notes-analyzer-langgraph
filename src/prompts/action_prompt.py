from langchain_core.prompts import PromptTemplate

ACTION_PROMPT = PromptTemplate(
    template="""
You are an expert AI meeting analyst.

Extract every action item from the meeting.

For each task provide exactly this format:

Task: <task>
Owner: <owner or Not Assigned>
Deadline: <deadline or Not Mentioned>

Meeting Transcript:
{transcript}

Return only action items.
Do not add explanations.
""",
    input_variables=["transcript"],
)
