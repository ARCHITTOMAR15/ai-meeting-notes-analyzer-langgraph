
"""
Transcript Chunker Module

Phase 2 — Preprocessing

Creates LlamaIndex Nodes from meeting transcripts.
"""

import sys

from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import Document, TextNode

from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TranscriptChunker:


    CHUNK_SIZE = 512
    CHUNK_OVERLAP = 50

    @classmethod
    def create_nodes(cls, document: Document) -> list[TextNode]:

        try:
            splitter = SentenceSplitter(
                chunk_size=cls.CHUNK_SIZE,
                chunk_overlap=cls.CHUNK_OVERLAP,
            )

            nodes = splitter.get_nodes_from_documents([document])

            logger.info(f"Created {len(nodes)} transcript chunks.")

            return nodes

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)

