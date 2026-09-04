
from pathlib import Path
import logging

from logging.handlers import  RotatingFileHandler
from src.config.config import load_config

def get_logger(name:str)->logging.Logger:

    config= load_config()
    log_dir=Path(config["paths"]["logs"])
    log_dir.mkdir(parents=True,exist_ok=True)

    log_file=log_dir/"project.log"

    logger=logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(config["logging"]["level"])
    logger.propagate = False

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=1_048_576,   # 1 MB
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


