from src.Parsing.parse_config_file import ParseConfig
from src.Highscore_system.get_highscore import HighScore
from src.GameEngine.player import Player
from src.Maze.Maze import Maze
from src.metadata import MetaData

if __name__ == "__main__":
    # try:

    # get data from the config file
    datas = ParseConfig().load_json
    data = MetaData(datas)

    # get the list of levels mazes as objects


    #maze of one level
    maze = Maze.creat_cells(0, data)


# except Exception as e:
#     err = ""
#     for er in e.errors():
#         err += str(er["loc"]) + ":" + er["msg"] + "\n"
#     print(err)
