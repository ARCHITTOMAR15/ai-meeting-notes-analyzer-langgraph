
from pathlib import Path
import json
from typing import Any


import yaml



def  create_directories(paths:list[str])->None:
    for path in paths:
        Path(path).mkdir(parents=True,exist_ok=True)

def save_json(data:dict,file_path:str)->None:

    path=Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path,"w",encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_json(file_path:str)->dict:
    with open(file_path,"r",encoding="utf-8") as file:
        return json.load(file)


def save_yaml(data:dict,file_path:str)->None:

    path=Path(file_path)
    path.parent.mkdir(parents=True,exist_ok=True)

    with open (path,"w",encoding="utf-8") as file:
         yaml.safe_dump(data, file, sort_keys=False)

def load_yaml(file_path:str)->dict:

    with open (file_path,"r",encoding="utf-8") as file:
        return yaml.safe_load(file)



def file_exists(file_path:str)->bool:
    return Path(file_path).exists()


def get_file_size(file_path:str)->float:
    size_bytes = Path(file_path).stat().st_size
    return round(size_bytes / (1024 * 1024), 4)

