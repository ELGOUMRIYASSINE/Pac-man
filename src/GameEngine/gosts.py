from dataclasses import dataclass
from typing import Tuple, List
from .player import Player, Cell, MetaData
from collections import deque


@dataclass
class Ghost:
    position: Tuple[int, int] = (0,0)
    weak: bool = False
    eaten: bool = False
    id: int = 0

    def _get_neighboars(self, position:Tuple[int,int], maze:List[List[Cell]], h_w:Tuple[int, int]):
        x = position[0]
        y = position[1]
        height= h_w[0]
        width=h_w[1]
        neighboars = []
        # if x == 0 and y == 0:
        #     if maze[y][x].Est:
        #         neighboars.append(maze[y][x + 1].position)
        #     if maze[y][x].South:
        #         neighboars.append(maze[y + 1][x].position)
        # elif x == width and y == height:
        #     if maze[y][x].West:
        #         neighboars.append(maze[y][x - 1].position)
        #     if maze[y][x].North:
        #         neighboars.append(maze[y - 1][x].position)
        # elif y == height and x == 0:
        #     if maze[y][x].Est:
        #         neighboars.append(maze[y][x + 1].position)
        #     if maze[y][x].North:
        #         neighboars.append(maze[y - 1][x].position)
        # elif x == width and y == 0:
        #     if maze[y][x].West:
        #         neighboars.append(maze[y][x - 1].position)
        #     if maze[y][x].South:
        #         neighboars.append(maze[y - 1][x].position)
        # else:
        if maze[y][x].Est and x + 1 < width:
            neighboars.append(maze[y][x + 1].position)
        if maze[y][x].North and y - 1 >= 0:
            neighboars.append(maze[y - 1][x].position)
        if maze[y][x].West and x - 1 >= 0:
            neighboars.append(maze[y][x - 1].position)
        if maze[y][x].South and  y + 1 < height:
            neighboars.append(maze[y + 1][x].position)
        return neighboars
        


    def move_ghost(self, player: Player, maze: List[List[Cell]], data:MetaData):
        player_pos = player.position
        ghost_pos = self.position
        visited = []
        q = deque(ghost_pos)
        while q:
            pos = q.popleft()
            neighboars = self._get_neighboars(pos, maze, (data.get_height(player.level), data.get_width(player.level)))
            if pos not in visited:
                visited.append(pos)
            
