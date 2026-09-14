from .parse_args import dataclass, Args
import json
from pydantic import BaseModel, Field, ValidationError
from typing import List

"""
This class validate the json file data using pydantic
"""


class Level(BaseModel):
    width: int = Field(gt=0, default=10)
    height: int = Field(gt=0, default=30)


class ValidJson(BaseModel):
    # this forbid to add extra params to the config file
    # model_config = ConfigDict(extra="forbid")

    hiscore_file: str = Field(min_length=2, max_length=20, default="score_file")
    levels: List[Level] = Field(
        default_factory=lambda: [Level(width=10, height=30) for _ in range(10)]
    )
    player_lives: int = Field(
        gt=0,
        default=3
    )
    pacgum_points: int = Field(gt=0, default=13)
    supergum_points: int = Field(gt=0, default=37)
    gost_points: int = Field(gt=0,default=42)


"""
This class get the content of the config file,
filter and fetch the data from it, and return the valid json data
with ignoring the comments
"""


@dataclass
class ParseConfig:

    @property
    def _clean_content(self):
        content = Args().get_args
        content = content.split("\n")
        json_content = []
        for line in content:
            if (
                line.strip().startswith("#")
                or line.strip().startswith("//")
                or line.strip() == ""
            ):
                continue
            else:
                json_content.append(line)
        return "".join(json_content)

    @property
    def load_json(self):
        try:
            ValidJson.model_validate_json(self._clean_content)
        except ValidationError as e:
            err = ""
            for er in e.errors():
                err += str(er["loc"]) + ":" + er["msg"]
            print(err)
            defaults = ValidJson().model_dump()
            # should replace the invalids with the defaults
        with open("Valid_config.json","w") as f:
            json.dump(json.loads(self._clean_content), f)


@dataclass
class ParseHiscore:
    pass
