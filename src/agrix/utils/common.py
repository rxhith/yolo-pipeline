import os 
from box.exceptions import BoxValueError
import yaml
import json
import joblib
from box import ConfigBox
from pathlib import Path
from ensure import ensure_annotations
from typing import Any

@ensure_annotations
def read_yaml(path_to_yaml:Path):
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_directories:list , verbose=True):
    for Path in path_to_directories:
        os.makedirs(Path , exist_ok=True)

    

