"""Update and persist the game's high-score table."""

from dataclasses import dataclass
from typing import Dict
from ..Parsing.parse_highscore import Parsehighscore, json


@dataclass
class HighScore:
    """Add player scores and keep only the highest results."""

    def one_player_score(self, name: str, score: int) -> Dict[str, int]:
        """Return a score mapping containing one player's result."""
        return {name: score}

    def multiplayers_scores(
        self, name: str, score: int, scores: Dict[str, int]
    ) -> Dict[str, int]:
        """Add a player's score to the existing score mapping."""
        scores.update(self.one_player_score(name, score))
        return scores

    def top_10_scores(self, score: int) -> None:
        """Prompt for a player name and save the ten highest scores."""
        scores = Parsehighscore().parse_score_file
        name = Parsehighscore().get_name(scores)
        new_scores = self.multiplayers_scores(name, score, scores)
        top = sorted(new_scores.values(), reverse=True)
        if len(top) > 10:
            top = top[:10]
        with open("scores.json", "w") as f:
            res = {key: val for key, val in new_scores.items() if val in top}
            if len(list(res.items())) > 10:
                res = dict(list(res.items())[:10])
                if not res.get(name):
                    res.popitem()
                    res.update({name: score})
            json.dump(res, f, indent=4)
