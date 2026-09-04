
import pytest
import sys
from src.utils.exception import ProjectException

def test_project_exception():
    with pytest.raises(ProjectException):
        try:
            10 / 0                  # Create a real exception
        except Exception as e:
            raise ProjectException(str(e), sys)
