
from langchain_core.prompts import PromptTemplate

SUMMARY_PROMPT = PromptTemplate.from_template("""
You are an AI Meeting Notes Assistant.

Your task is to generate **one concise meeting summary** from the transcript.

### Rules
- Generate only one summary.
- Do not repeat or rewrite the summary.
- Do not repeat or copy the transcript.
- Keep the response under **120 words**.
- Follow the output format exactly.
- End your response after the **Decisions Taken** section.

### Output Format

## Meeting Objective
Write 1-2 sentences describing the purpose of the meeting.

## Key Discussion Points
- Point 1
- Point 2
- Point 3

## Decisions Taken
- Decision 1
- Decision 2

### Transcript
{transcript}

Generate only the formatted meeting summary above.
Do not add another "Summary" section.
Do not repeat any section or the transcript.
End your response after "Decisions Taken".
""")
