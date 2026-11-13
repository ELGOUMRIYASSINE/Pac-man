"""Start Pac-Man by loading its configuration and launching the game loop."""

from src.Parsing.parse_config_file import ParseConfig
from src.GameEngine.Game_loop import GameLoop
from src.metadata import MetaData

if __name__ == "__main__":
    # try:

    # get data from the config file
    datas = ParseConfig().load_json
    data = MetaData(datas)

    # get the list of levels mazes as objects

    # maze of one level

    ren = GameLoop()
    ren.entry(data)


# except Exception as e:
#     err = ""
#     for er in e.errors():
#         err += str(er["loc"]) + ":" + er["msg"] + "\n"
#     print(err)
