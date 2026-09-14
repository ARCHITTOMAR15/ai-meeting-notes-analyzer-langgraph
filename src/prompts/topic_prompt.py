from langchain_core.prompts import PromptTemplate

TOPIC_PROMPT = PromptTemplate(
    template="""
You are an expert AI meeting analyst.

Analyze the meeting transcript below and extract the main discussion topics.

Transcript:
{transcript}

Return your answer ONLY in the JSON format described below.

{format_instructions}
""",
    input_variables=["transcript", "format_instructions"],
)
