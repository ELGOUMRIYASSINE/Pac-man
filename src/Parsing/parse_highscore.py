from .parse_args import dataclass
from pathlib import Path
import json
from pydantic import BaseModel, Field, ValidationError
from typing import Any, Dict


class ValidScores(BaseModel):
    name: str = Field(max_length=10, min_length=1, pattern=r"^[A-Za-z0-9 ]+$")
    score: int = Field(gt=0)


@dataclass
class Parsehighscore:

    def get_name(self, scores: Dict[str, int]) -> str:
        user: str = input("Enter your name!\n")
        if user in scores.keys():
            print("Error: player-name already exists, enter diffrent name")
            self.get_name(scores)
        if len(user) > 10 or len(user) < 1:
            print("Error: the name should be in range of 1 and 10 characters")
            self.get_name(scores)
        elif not user.replace(" ", "").isalnum():
            print(
                "Error: your name should be composed of  alphanumeric and spaces only"
            )
            self.get_name(scores)
        return user

    @property
    def get_file(self) -> str:
        scores: Path = Path.cwd() / "scores.json"
        if not scores.exists():
            print("Warning: missing scores file, using default...")
            score = {}
            with open("scores.json", "w") as f:
                json.dump(score, f, indent=4)
                data = json.dumps(score, indent=4)
        else:
            data = scores.read_text(encoding="utf-8")
            if data == "":
                score = {
                }
                data = json.dumps(score, indent=4)
        return data

    @property
    def parse_score_file(self) -> Any:
        try:
            data = json.loads(self.get_file)
        except json.JSONDecodeError:
            print("Warning: invalid scores.json format, using default...")
            score = {}
            data = json.loads(json.dumps(score))

        for key, val in data.items():
            try:
                ValidScores(name=key, score=val)
            except ValidationError as e:
                print(
                    "Warning (scores file):",
                    "(",
                    e.errors()[0]["input"],
                    ")",
                    e.errors()[0]["msg"],
                    ",using default...",
                )
                score = {}
                data = json.loads(json.dumps(score))
        return data
