
"""
Speaker Parser Module

Phase 2 — Preprocessing

Extracts speaker-message pairs from a meeting transcript.
"""

import re
import sys

from llama_index.core.schema import Document

from src.utils.exception import ProjectException
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SpeakerParser:
    """Parse transcript into speaker-message pairs."""

    SPEAKER_PATTERN = re.compile(r"^([^:\n]+):\s*(.+)$")

    @classmethod
    def parse(cls, document: Document) -> list[dict]:
        """
        Parse a cleaned transcript.

        Args:
            document: Cleaned LlamaIndex Document.

        Returns:
            List of speaker-message dictionaries.
        """

        try:
            speaker_messages = []

            for line in document.text.splitlines():

                line = line.strip()

                if not line:
                    continue

                match = cls.SPEAKER_PATTERN.match(line)

                if match:
                    speaker_messages.append(
                        {
                            "speaker": match.group(1).strip(),
                            "message": match.group(2).strip(),
                        }
                    )

            logger.info(f"Parsed {len(speaker_messages)} speaker messages.")

            return speaker_messages

        except Exception as error:
            logger.error(str(error))
            raise ProjectException(str(error), sys)

