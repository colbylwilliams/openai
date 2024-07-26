import json
import os
import re

from typing import Any

from rich.spinner import Spinner
from rich.text import Text


def data_dir() -> str:
    file_dir = os.path.dirname(__file__)
    return os.path.join(file_dir, '../data')

def data_file_path(filename: str) -> str:
    return os.path.join(data_dir(), filename)

def get_json_from_file(filename: str) -> Any:
    '''Load items from a JSON file. The file must be in the 'data' directory.'''
    if not filename:
        raise ValueError('filename is required')
    # ensure the file ends with .json
    filename = re.sub(r'\.json$', '', filename) + '.json'
    with open(data_file_path(filename)) as f:
        _json = json.load(f)

    return _json

def get_text(filename: str) -> str:
    '''Get the text content of a file'''
    with open(filename) as f:
        text = f.read()

    return text

def status(text: str) -> Spinner:
    return Spinner(name='dots', text=Text(f' {text}', style='dim'), style='dim')
