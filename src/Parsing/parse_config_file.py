from ..imports import dataclass
import json
from pathlib import Path
from pydantic import BaseModel

"""
This class implement the parsing of the config file
given to the program and return the valid data, with
ignoring the comments
"""

class ValidJson(BaseModel):
    pass

@dataclass
class ParseConfig:

    @property
    def get_file_content(self):
        pass

    @property
    def parse_content(self):
        pass

    @property
    def load_json(self):
        pass

@dataclass
class ParseHiscore:
    pass