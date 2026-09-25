from dataclasses import dataclass
from typing import Tuple, List
from .player import Player, Maze, Cell


@dataclass
class Ghost:
    position: Tuple[int, int] = (0, 0)
    weak: bool = False
    eaten: bool = False
    id:int = 0

    def move_ghost(self, player:Player, maze:List[Cell]):
        y = player.positiony
        x = player.positionx
        # if maze[y][x].Est 
        dist = abs(self.position[0] - y) + abs(self.position[1] - x)

