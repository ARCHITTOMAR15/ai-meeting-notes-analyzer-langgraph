
from pathlib import Path

from src.data_ingestion.loader import TranscriptLoader
from src.preprocessing.cleaner import TranscriptCleaner
from src.preprocessing.speaker_parser import SpeakerParser

RAW_PATH = Path("data/raw/Meeting_Transcript.txt")


def test_parse_returns_list():

    document = TranscriptLoader.load_document(str(RAW_PATH))
    clean_document = TranscriptCleaner.clean(document)

    speaker_messages = SpeakerParser.parse(clean_document)

    assert isinstance(speaker_messages, list)

def test_speaker_message_structure():

    document = TranscriptLoader.load_document(str(RAW_PATH))
    clean_document = TranscriptCleaner.clean(document)

    speaker_messages = SpeakerParser.parse(clean_document)

    assert "speaker" in speaker_messages[0]
    assert "message" in speaker_messages[0]

def test_speaker_and_message_not_empty():

    document = TranscriptLoader.load_document(str(RAW_PATH))
    clean_document = TranscriptCleaner.clean(document)

    speaker_messages = SpeakerParser.parse(clean_document)

    assert speaker_messages[0]["speaker"] != ""
    assert speaker_messages[0]["message"] != ""
