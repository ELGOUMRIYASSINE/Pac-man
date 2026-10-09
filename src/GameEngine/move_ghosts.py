from ..Maze.Maze import Cell, Tuple, List, dataclass, Ghost
from collections import deque


@dataclass
class MoveGhost:

    def _get_neighboars(
        self,
        position: Tuple[int, int],
        maze: List[List[Cell]],
        h_w: Tuple[int, int],
    ) -> List[Tuple[int, int]]:
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
        self,
        start: Tuple[int, int],
        maze: List[List[Cell]],
        h_w: Tuple[int, int],
        ghost: Ghost,
        end: Tuple[int, int],
    ) -> bool:
        ghost.neighboars = []
        parents = {start: start}
        queue = deque([start])

        while queue:
            position = queue.popleft()
            if position == end:
                break
            for neighbor in self._get_neighboars(position, maze, h_w):
                if neighbor not in parents:
                    parents[neighbor] = position
                    queue.append(neighbor)

        if end not in parents:
            return False

        path = []
        position = end
        while position != start:
            path.append(position)
            position = parents[position]
        path.append(start)
        ghost.back = list(path)
        ghost.neighboars = list(reversed(path))
        return True
