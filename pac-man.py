from src.Parsing.parse_config_file import ParseConfig
from src.Maze.each_level_maze import LevelMaze
from src.Highscore_system.get_highscore import HighScore
from src.GameEngine.player import Player


if __name__ == "__main__":
    # try:

    # get data from the config file
    data = ParseConfig().load_json

    # get the list of levels mazes as objects
    mazes = LevelMaze().get_mazes_list(data)


    # should get the score from the end of the game and replace 10 by it
    Player().initial_position(mazes, 0)
    # data = HighScore().top_10_scores(10)
    
# except Exception as e:
#     err = ""
#     for er in e.errors():
#         err += str(er["loc"]) + ":" + er["msg"] + "\n"
#     print(err)
