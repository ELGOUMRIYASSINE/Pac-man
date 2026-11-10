from enum import IntEnum
from dataclasses import dataclass
from typing import Tuple, List
from mazegenerator import MazeGenerator
from .get_maze_bylevel import LevelMaze
from ..metadata import MetaData
from ..GameEngine.gosts import Ghost


@dataclass
class Cell:
    position: Tuple[int, int]
    North: bool = False
    Est: bool = False
    South: bool = False
    West: bool = False
    supgum: bool = False
    gum: bool = False
    has_ghost: bool = False
    ghost_id: int | None = None
    has_player: bool = False
    edible_ghost: bool = False
    palyer_init_pos: bool = False


class Directions(IntEnum):
    N = 1
    E = 2
    S = 4
    W = 8


SEALED = Directions.N | Directions.E | Directions.S | Directions.W


@dataclass
class Maze:

    @staticmethod
    def _open_cell_near(
        grid: List[List[int]], wanted: Tuple[int, int]
    ) -> Tuple[int, int]:
        """Closest cell to `wanted` that is not sealed inside the '42'."""
        open_cells = [
            (row, col)
            for row, line in enumerate(grid)
            for col, walls in enumerate(line)
            if walls != SEALED
        ]
        return min(
            open_cells,
            key=lambda c: abs(c[0] - wanted[0]) + abs(c[1] - wanted[1]),
            default=wanted,
        )

    @classmethod
    def creat_cells(
        cls,
        level: int,
        data: MetaData,
        player_position: Tuple[int, int],
        ghosts: List[Ghost],
    ) -> Tuple[List[List[Cell]], List[Ghost], Tuple[int, int]]:
        maze: MazeGenerator = LevelMaze.get_maze_bylevel(level, data)
        height: int = maze._height
        width: int = maze._width
        player_position = cls._open_cell_near(maze.maze, player_position)

        # ghosts start on the corners (dict.fromkeys: tiny mazes share corners)
        corners = list(dict.fromkeys([
            (0, 0), (0, width - 1), (height - 1, 0), (height - 1, width - 1)
        ]))
        spawns = [c for c in corners if c != player_position]
        spawns = spawns or [player_position]

        maze_obj = []
        for n in range(height):
            cells = []
            for m in range(width):
                cell = Cell((n, m))
                walls = maze.maze[n][m]
                cell.North = bool(walls & Directions.N)
                cell.Est = bool(walls & Directions.E)
                cell.South = bool(walls & Directions.S)
                cell.West = bool(walls & Directions.W)
                if (n, m) == player_position:
                    cell.has_player = True
                    cell.palyer_init_pos = True
                elif (n, m) in corners:
                    cell.supgum = True
                elif walls != SEALED:
                    cell.gum = True
                cells.append(cell)
            maze_obj.append(cells)

        for index, ghost in enumerate(ghosts):
            ghost.id = index
            ghost.home = spawns[index % len(spawns)]
            ghost.reset()
            cell = maze_obj[ghost.home[0]][ghost.home[1]]
            cell.has_ghost = True
            cell.ghost_id = index
        return maze_obj, ghosts, player_position
