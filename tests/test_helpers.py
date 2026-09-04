
from pathlib import Path

from src.utils.helpers import (
    create_directories,
    save_json,
    load_json,
    save_yaml,
    load_yaml,
    file_exists,
    get_file_size,
)


# Test 1: Create Directory
def test_create_directories():
    create_directories(["tests/temp_folder"])

    assert Path("tests/temp_folder").exists()


# Test 2: Save and Load JSON
def test_json_functions():
    data = {
        "name": "Archit",
        "project": "Meeting Notes"
    }

    save_json(data, "tests/sample.json")

    loaded_data = load_json("tests/sample.json")

    assert loaded_data == data


# Test 3: Save and Load YAML
def test_yaml_functions():
    data = {
        "model": "Mistral",
        "temperature": 0.2
    }

    save_yaml(data, "tests/sample.yaml")

    loaded_data = load_yaml("tests/sample.yaml")

    assert loaded_data == data


# Test 4: Check File Exists
def test_file_exists():
    Path("tests/test.txt").write_text("Hello")

    assert file_exists("tests/test.txt")


# Test 5: Check File Size
def test_get_file_size():
    Path("tests/size.txt").write_text("A" * 20000)  # 20 KB file

    assert get_file_size("tests/size.txt") > 0
