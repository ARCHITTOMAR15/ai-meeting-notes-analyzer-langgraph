from pathlib import Path

from llama_index.core.schema import TextNode

from src.data_ingestion.loader import TranscriptLoader
from src.preprocessing.cleaner import TranscriptCleaner
from src.preprocessing.chunker import TranscriptChunker


RAW_PATH = Path("data/raw/Meeting_Transcript.txt")

def test_create_node_return_list():
    document=TranscriptLoader.load_document(str(RAW_PATH))
    clean_document=TranscriptCleaner.clean(document)
    nodes=TranscriptChunker.create_nodes(clean_document)

    assert isinstance(nodes, list)

def test_nodes_are_textnodes():
    document = TranscriptLoader.load_document(str(RAW_PATH))
    clean_document = TranscriptCleaner.clean(document)

    nodes = TranscriptChunker.create_nodes(clean_document)

    assert isinstance(nodes[0], TextNode)


def test_node_text_not_empty():
    document = TranscriptLoader.load_document(str(RAW_PATH))
    clean_document = TranscriptCleaner.clean(document)

    nodes = TranscriptChunker.create_nodes(clean_document)

    assert len(nodes[0].text) > 0

def test_multiple_nodes_created():
    document = TranscriptLoader.load_document(str(RAW_PATH))
    clean_document = TranscriptCleaner.clean(document)

    nodes = TranscriptChunker.create_nodes(clean_document)

    assert len(nodes) >= 1
