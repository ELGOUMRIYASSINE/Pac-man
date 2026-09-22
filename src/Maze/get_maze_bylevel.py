from mazegenerator import MazeGenerator
from dataclasses import dataclass
from ..metadata import MetaData

"""
This class returns a list of MazeGenerator objects,
those objects represent a maze object for each level
"""


@dataclass
class LevelMaze:

    @classmethod
    def get_maze_bylevel(cls, level) -> MazeGenerator:
            height = MetaData().get_height(level)
            width = MetaData().get_width(level)
            try:
                if level == 0:
                    maze_gen = MazeGenerator(
                        size=(height, width),
                        entry_cell=(0, 0),
                        exit_cell=(height - 1, width - 1),
                        perfect=False,
                        seed=42,
                    )
                else:
                    maze_gen = MazeGenerator(
                        size=(height, width),
                        entry_cell=(0, 0),
                        exit_cell=(height - 1, width - 1),
                        perfect=False,
                    )
            except Exception:
                raise ValueError(f"Error: maze generation failed at level {level}")
            return maze_gen
