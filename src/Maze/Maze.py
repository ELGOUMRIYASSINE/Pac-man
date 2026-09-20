from enum import IntEnum
from dataclasses import dataclass
from typing import Tuple
from mazegenerator import MazeGenerator

class Directions(IntEnum):
    N=1
    E=2
    S=4
    W=8

@dataclass
class Cell:
    position:Tuple[int, int]
    North:bool = False
    Est: bool = False
    South: bool = False
    West: bool = False
    supgum:bool = False
    gum:bool = False
    player:bool = False
    ghost:bool = False

@dataclass
class Maze:

    @classmethod
    def creat_cells(cls, maze:MazeGenerator):
        height = maze._height
        width = maze._width
        maze_obj = []
        for n in range(height):
            cells = []
            for m in range(width):
                cell = Cell((n, m))
                if maze.maze[n][m] & Directions.N:
                    cell.North = True
                if maze.maze[n][m] & Directions.E:
                    cell.Est = True
                if maze.maze[n][m] & Directions.S:
                    cell.South = True
                if maze.maze[n][m] & Directions.W:
                    cell.West = True
                cells.append(cell)
            maze_obj.append(cells)
        return maze_obj
