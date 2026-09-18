from mazegenerator import MazeGenerator
from dataclasses import dataclass

"""
This class creat instance from MazeGenerator for each level
"""


@dataclass
class MazeIntegration:

    def get_maze(self, level: int, height: int, width: int) -> MazeGenerator:
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
