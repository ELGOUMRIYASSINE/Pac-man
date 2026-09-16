from .parse_args import dataclass, Args
import json
from pydantic import BaseModel, Field, ValidationError
from typing import List, Union, Dict, Any

"""
This class validate the json file data using pydantic
"""


class Level(BaseModel):
    width: int = Field(gt=0, default=10)
    height: int = Field(gt=0, default=30)


class ValidJson(BaseModel):
    # this forbid to add extra params to the config file
    # model_config = ConfigDict(extra="forbid")

    highscore_file: str = Field(
        min_length=1, max_length=20, default="score_file"
    )
    levels: List[Level] = Field(
        default_factory=lambda: [Level(width=10, height=30) for _ in range(10)]
    )
    player_lives: int = Field(gt=0, default=3)
    pacgum_points: int = Field(gt=0, default=13)
    supergum_points: int = Field(gt=0, default=37)
    gost_points: int = Field(gt=0, default=42)


"""
This class get the content of the config file,
filter and fetch the data from it, and return the valid json data
with ignoring the comments
"""


@dataclass
class ParseConfig:

    @property
    def _clean_content(self) -> str:
        content1 = Args().get_args
        content = content1.split("\n")
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
    def load_json(self) -> Dict[str, Any]:
        defaults = ValidJson().model_dump()
        default_level = Level().model_dump()
        data = json.loads(self._clean_content)

        for key in ValidJson.model_fields:

            if key not in data:
                print(f"Warning: '{key}' is missing, using default...")
                data[key] = defaults[key]

            elif key not in ["highscore_file", "levels"] and data[key] < 1:
                print(
                    f"Warning: {key} -> {data[key]} invalid, using default..."
                )
                data[key] = defaults[key]

            elif key == "highscore_file" and (not isinstance(data[key], str) or not data[key]):
                print(
                    "Warning: highscore filename should be none emptystring, using default..."
                )
                data[key] = defaults[key]

        if not isinstance(data.get("levels"), list):
            print(
                "Warning: 'levels' value itself is missing or invalid, using default..."
            )
            data["levels"] = defaults["levels"]

        else:
            for i, level in enumerate(data["levels"]):

                if not isinstance(level, dict):
                    print(f"Warning: levels[{i}] is invalid, using default...")
                    data["levels"][i] = default_level
                    continue

                width = level.get("width", None)
                if not width:
                    width = 10
                    print(
                        f"Warning: levels[{i}].width is missing, using default..."
                    )

                if width < 1 or width > 90:
                    print(
                        f"Warning: levels[{i}].width value invalid, using default..."
                    )
                    width = 10

                height = level.get("height", None)
                if not height:
                    height = 30
                    print(
                        f"Warning: levels[{i}].height is missing, using default..."
                    )

                if height < 1 or height > 90:
                    print(
                        f"Warning: levels[{i}].height value invalid, using default..."
                    )
                    height = 30

                data["levels"][i] = {"width": width, "height": height}
        validated = ValidJson.model_validate(data)
        return validated.model_dump()

