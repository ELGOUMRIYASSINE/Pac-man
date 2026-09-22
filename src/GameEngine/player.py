from ..Maze.Maze import Maze, MazeGenerator
from typing import List, Dict, Any, Tuple
from ..metadata import MetaData, dataclass

@dataclass
class Player:

    @classmethod
    def creat_player(cls, level) -> Tuple[int,int]:
        return (
            MetaData().get_height(level) // 2,
            MetaData().get_width(level) // 2,
        )

    
