from dataclasses import dataclass
from typing import Tuple, List
from .player import Player, Maze, Cell, MetaData


@dataclass
class Ghost:
    position: Tuple[int, int] = (0, 0)
    weak: bool = False
    eaten: bool = False
    id: int = 0

    def move_ghost(self, player: Player, maze: List[List[Cell]], data):
        y = self.position[0]
        x = self.position[1]
        dist = 0
        if maze[y][x].Est and x + 1 < data.get_width(
            player.level
        ):
            d = abs(y - player.positiony) + abs(x - player.positionx)
            if d < dist:
                dist = d
        if maze[y][x].West and x - 1 >= 0:
            d = abs(y - player.positiony) + abs(x - player.positionx)
            if d < dist:
                dist = d
        if maze[y][x].North and y - 1 >= 0:
            d = abs(y - player.positiony) + abs(x - player.positionx)
            if d < dist:
                dist = d
        if maze[y][x].South and y + 1 < data.get_height(player.level):
            d = abs(y - player.positiony) + abs(x - player.positionx)
            if d < dist:
                dist = d
        
