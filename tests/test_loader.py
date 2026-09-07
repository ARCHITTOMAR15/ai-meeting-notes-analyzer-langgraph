
from pathlib import Path
import pytest

from llama_index.core.schema import Document

from src.data_ingestion.loader import TranscriptLoader
from src.utils.exception import ProjectException

RAW_DATA= Path("data/raw")

def test_load_text_document():
    document=TranscriptLoader.load_document(str(RAW_DATA/ "Meeting_Transcript.txt"))

    assert isinstance(document,Document)

def test_document_contains_text():
     document = TranscriptLoader.load_document(str(RAW_DATA / "Meeting_Transcript.txt"))

     assert len(document.text)>0



def test_file_not_found():
    with pytest.raises(ProjectException):
        TranscriptLoader.load_document("data/raw/not_found.txt")


def test_invalid_extension(tmp_path):
    file_path = tmp_path / "sample.csv"
    file_path.write_text("dummy data")

    with pytest.raises(ProjectException):
        TranscriptLoader.load_document(str(file_path))






