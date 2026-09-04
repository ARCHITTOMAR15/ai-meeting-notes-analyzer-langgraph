
from pathlib import Path
from src.utils.logger import get_logger

def test_logger_creation():
    logger=get_logger("test_logger")

    assert logger.name=="test_logger"
    assert logger.handlers

def test_log_file_created():
    logger=get_logger("test_file")
    logger.info("Testing logger file creation")

    log_path=Path("logs/project.log")

    assert log_path.exists()

def test_multiple_logger_calls():
    logger_one = get_logger("duplicate_logger")
    logger_two = get_logger("duplicate_logger")

    assert logger_one is logger_two
    assert len(logger_one.handlers) == 2

