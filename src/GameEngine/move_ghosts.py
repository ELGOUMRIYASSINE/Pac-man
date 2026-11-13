"""Pathfinding and movement decisions for maze ghosts."""

from ..Maze.Maze import Cell, Tuple, List, dataclass, Ghost
from collections import deque
from typing import Optional


@dataclass
class MoveGhost:
    """Choose reachable cells and paths for ghosts."""

    def _get_neighboars(
        self,
        position: Tuple[int, int],
        maze: List[List[Cell]],
        h_w: Tuple[int, int],
    ) -> List[Tuple[int, int]]:
        """Return adjacent cells reachable from the given position."""
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
        """Find and store the shortest path from a ghost to a target cell."""
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
        ghost.neighboars = list(reversed(path))
        return True

    def next_cell(
        self,
        ghost: Ghost,
        maze: List[List[Cell]],
        h_w: Tuple[int, int],
        player_position: Tuple[int, int],
    ) -> Optional[Tuple[int, int]]:
        """Choose the ghost's next cell, or ``None`` if it should stay.

        Weak ghosts move away from the player. Active even-numbered ghosts use
        breadth-first search, while odd-numbered ghosts choose the closest
        available neighbor. Weak and odd-numbered ghosts avoid reversing
        direction unless they reach a dead end.
        """
        if ghost.position == player_position:
            return None
        if not ghost.weak and ghost.id % 2 == 0:
            self.move_ghost_bfs(
                ghost.position, maze, h_w, ghost, player_position
            )
            return ghost.neighboars[1] if len(ghost.neighboars) > 1 else None

        moves = self._get_neighboars(ghost.position, maze, h_w)
        moves = [cell for cell in moves if cell != ghost.previous] or moves
        if not moves:
            return None

        def distance(cell: Tuple[int, int]) -> int:
            """Measure the grid distance from a candidate cell to the player."""
            return (
                abs(cell[0] - player_position[0])
                + abs(cell[1] - player_position[1])
            )

        return max(moves, key=distance) if ghost.weak else min(
            moves, key=distance
        )
