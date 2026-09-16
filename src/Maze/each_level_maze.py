from .maze_integration import MazeIntegration, dataclass, MazeGenerator
from typing import List, Dict, Any

"""
This class returns a list of MazeGenerator objects,
those objects represent a maze object for each level
"""


@dataclass
class LevelMaze:

    def get_mazes_list(self, data: Dict[str, Any]) -> List[MazeGenerator]:
        mazes = []
        for level in range(10):
            height = data["levels"][level]["height"]
            width = data["levels"][level]["width"]
            mazes.append(MazeIntegration().get_maze(level, height, width))
        return mazes
