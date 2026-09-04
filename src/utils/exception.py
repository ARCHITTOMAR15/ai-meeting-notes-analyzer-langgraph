
from pathlib import Path
import sys


class ProjectException(Exception):
    """Base exception for the project."""

    def __init__(self, error_message: str, error_detail: sys):
        _, _, exc_tb = error_detail.exc_info()

        self.file_name = Path(exc_tb.tb_frame.f_code.co_filename).name
        self.line_number = exc_tb.tb_lineno

        message = (
            f"Error occurred in [{self.file_name}] "
            f"at line [{self.line_number}] : {error_message}"
        )

        super().__init__(message)