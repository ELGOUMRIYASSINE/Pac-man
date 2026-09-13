from .parse_args import dataclass, Args
import json
from pydantic import BaseModel

"""
This class validate the json file data using pydantic
"""
class ValidJson(BaseModel):
    pass


"""
This class get the content of the config file,
filter and fetch the data from it, and return the valid json data
with ignoring the comments
"""
@dataclass
class ParseConfig:

    @property
    def parse_content(self):
        content = Args().get_args
        print(content.split("\n"))

    @property
    def load_json(self):
        pass

@dataclass
class ParseHiscore:
    pass
