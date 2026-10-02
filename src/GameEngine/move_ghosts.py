from ..Maze.Maze import Cell, Tuple, List, dataclass, Ghost
from .player import Player, MetaData
from collections import deque

@dataclass
class MoveGhost:

    def _get_neighboars(
            self,
            position: Tuple[int, int],
            maze: List[List[Cell]],
            h_w: Tuple[int, int],
        )-> List[Tuple[int, int]]:
        x = position[1]
        y = position[0]
        height = h_w[0]
        width = h_w[1]
        neighboars = []
        if not maze[y][x].Est and x + 1 < width:
            neighboars.append(maze[y][x + 1].position)
        if not maze[y][x].North and y - 1 >= 0:
            neighboars.append(maze[y - 1][x].position)
        if not maze[y][x].West and x - 1 >= 0:
            neighboars.append(maze[y][x - 1].position)
        if not maze[y][x].South and y + 1 < height:
            neighboars.append(maze[y + 1][x].position)
        return neighboars

    def move_ghost_bfs(
        self, player: Player, maze: List[List[Cell]], data: MetaData, ghost:Ghost
    ):
        q = deque()
        while q:
            pass

    def move_ghost_dfs(
            self,
            start: Tuple[int, int],
            maze: List[List[Cell]],
            h_w: Tuple[int, int],
            ghost:Ghost,
            end,visited=None
        ):
        if visited is None:
            visited = []
        visited.append(start)
        if start == end:
            ghost.neighboars = visited
            return True
        for pos in self._get_neighboars(start, maze, h_w):
            if pos not in visited:
                if self.move_ghost_dfs(
                    pos,
                    maze,
                    h_w,
                    ghost,end,
                    visited
                ):
                    ghost.neighboars = visited
                    return True
        return False
