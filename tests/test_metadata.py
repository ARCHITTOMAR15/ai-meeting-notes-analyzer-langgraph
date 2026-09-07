from pathlib import Path
from src.utils.helpers import save_json, load_json
from src.data_ingestion.loader import TranscriptLoader
from src.data_ingestion.metadata import TranscriptMetadata


RAW_DATA_PATH = Path("data/raw/Meeting_Transcript.txt")


def test_extract_metadata_returns_dictionary():
    document = TranscriptLoader.load_document(str(RAW_DATA_PATH))

    metadata = TranscriptMetadata.extract(
        document=document,
        file_path=str(RAW_DATA_PATH),
    )

    assert isinstance(metadata, dict)


def test_metadata_contains_expected_keys():
    document = TranscriptLoader.load_document(str(RAW_DATA_PATH))

    metadata = TranscriptMetadata.extract(
        document=document,
        file_path=str(RAW_DATA_PATH),
    )

    expected_keys = {
        "file_name",
        "file_type",
        "file_size_mb",
        "character_count",
        "word_count",
        "line_count",
    }

    assert expected_keys.issubset(metadata.keys())


def test_metadata_values_are_valid():
    document = TranscriptLoader.load_document(str(RAW_DATA_PATH))

    metadata = TranscriptMetadata.extract(
        document=document,
        file_path=str(RAW_DATA_PATH),
    )

    assert metadata["file_name"] == "Meeting_Transcript.txt"
    assert metadata["file_type"] == "txt"
    assert metadata["character_count"] > 0
    assert metadata["word_count"] > 0
    assert metadata["line_count"] > 0
    assert metadata["file_size_mb"] > 0

def test_save_metadata_json(tmp_path):
    document = TranscriptLoader.load_document(str(RAW_DATA_PATH))

    metadata = TranscriptMetadata.extract(
        document=document,
        file_path=str(RAW_DATA_PATH),
    )

    json_path = tmp_path / "metadata.json"

    save_json(metadata, str(json_path))

    loaded_metadata = load_json(str(json_path))

    assert metadata == loaded_metadata

