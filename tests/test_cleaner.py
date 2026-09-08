
from pathlib import Path

from llama_index.core.schema import Document
from src.data_ingestion.loader import TranscriptLoader
from src.preprocessing.cleaner import TranscriptCleaner

RAW_PATH=Path("data/raw/Meeting_Transcript.txt")


def test_clean_returns_document():
    document=TranscriptLoader.load_document(str(RAW_PATH))

    cleaned_document=TranscriptCleaner.clean(document)

    assert isinstance (cleaned_document,Document)

def test_clean_document_not_empty():
    document = TranscriptLoader.load_document(str(RAW_PATH))

    cleaned_document = TranscriptCleaner.clean(document)

    assert len(cleaned_document.text) > 0

def test_extra_blank_lines_removed():
    sample_document = Document(
        text="John: Hello\n\n\n\nSarah: Hi John."
    )

    cleaned_document = TranscriptCleaner.clean(sample_document)

    assert "\n\n\n" not in cleaned_document.text

def test_metadata_preserved():
    sample_document = Document(
        text="John: Hello",
        metadata={"file_name": "sample.txt"},
    )

    cleaned_document = TranscriptCleaner.clean(sample_document)

    assert cleaned_document.metadata["file_name"] == "sample.txt"



