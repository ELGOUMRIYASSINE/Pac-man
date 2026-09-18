from src.Parsing.parse_config_file import ParseConfig
from src.Maze.each_level_maze import LevelMaze
from src.Parsing.parse_highscore import Parsehighscore
from src.Highscore_system.get_highscore import HighScore
from pathlib import Path

if __name__ == "__main__":
    # try:
    data = ParseConfig().load_json
    maze = LevelMaze().get_mazes_list(data)
    data = HighScore().top_10_scores(10)
    # scores = Path("./score.json").read_text(encoding="utf-8")
    # HighScore().top_10_scores(name, 10, {})
# except Exception as e:
#     err = ""
#     for er in e.errors():
#         err += str(er["loc"]) + ":" + er["msg"] + "\n"
#     print(err)
