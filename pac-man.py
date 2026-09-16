from src.Parsing.parse_config_file import ParseConfig
from src.Maze.each_level_maze import LevelMaze

if __name__ == "__main__":
    # try:
    data = ParseConfig().load_json
    maze = LevelMaze().get_mazes_list(data)
# except Exception as e:
#     err = ""
#     for er in e.errors():
#         err += str(er["loc"]) + ":" + er["msg"] + "\n"
#     print(err)
