from dataclasses import dataclass
from typing import Dict
from ..Parsing.parse_highscore import Parsehighscore, json


@dataclass
class HighScore:

    def one_player_score(self, name:str, score:int)->Dict[str, int]:
        return {name:score}

    def multiplayers_scores(
        self, name: str, score: int, scores: Dict[str, int]
    ) -> Dict[str, int]:
        scores.update(self.one_player_score(name, score))
        return scores

    def top_10_scores(self, score:int) -> None:
        scores = Parsehighscore().parse_score_file
        name = Parsehighscore().get_name
        # check of names are duplicated messing
        new_scores = self.multiplayers_scores(name, score, scores)
        top = sorted(new_scores.values(), reverse=True)
        if len(top) > 10:
            top = top[:10]
        with open("scores.json", "w") as f:
            res = {key: val for key, val in new_scores.items() if val in top}
            json.dump(res, f, indent=4)
