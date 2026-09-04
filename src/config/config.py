"""
Configuration Loader

Project: AI Meeting Notes Analyzer using LangGraph
"""

from pathlib import Path
import yaml


CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.yaml"


def load_config() -> dict:
    """
    Load project configuration from config.yaml.

    Returns:
        Dictionary containing project configuration.
    """

    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config