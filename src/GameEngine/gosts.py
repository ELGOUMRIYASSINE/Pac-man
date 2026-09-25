from dataclasses import dataclass
from typing import Tuple, List
from .player import Player, Maze, Cell


@dataclass
class Ghost:
    position: Tuple[int, int] = (0, 0)
    weak: bool = False
    eaten: bool = False
    id:int = 0

    # def move_ghost(self, player:Player, maze:List[List[Cell]]):
    #     y = player.positiony
    #     x = player.positionx
    #     if maze[y][x].Est :

    #     elif maze[y][x].West:

    #     elif maze[y][x].North:

    #     elif maze[y][x].South:

    #     dist = abs(self.position[0] - y) + abs(self.position[1] - x)

