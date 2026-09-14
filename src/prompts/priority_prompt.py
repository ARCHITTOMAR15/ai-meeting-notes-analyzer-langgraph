
from langchain_core.prompts import PromptTemplate

PRIORITY_PROMPT = PromptTemplate(
    template="""
You are an expert AI meeting analyst.

Identify every task discussed in the meeting.

For each task classify its priority.

Format exactly like this:

Task: Finish deployment
Priority: High

Task: Send meeting minutes
Priority: Medium

Task: Archive documents
Priority: Low

Meeting Transcript:
{transcript}

Return only task/priority pairs.
""",
    input_variables=["transcript"],
)
