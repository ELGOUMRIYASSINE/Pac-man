from enum import IntEnum
from dataclasses import dataclass
from typing import Tuple
from mazegenerator import MazeGenerator
from .get_maze_bylevel import LevelMaze
from ..metadata import MetaData


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
    ghost:bool = False
    has_player:bool = False
    palyer_init_pos:bool=False

@dataclass
class Maze:

    @classmethod
    def creat_cells(cls, level: int, data:MetaData, player_position: Tuple[int, int]):

        maze: MazeGenerator = LevelMaze.get_maze_bylevel(level, data)
        height:int = maze._height
        width:int = maze._width
        maze_obj = []
        score:int = 0

        for n in range(height):
            cells = []
            for m in range(width):
                closed = 0
                cell = Cell((n, m))
                if (n, m) == player_position:
                    cell.has_player = True
                    cell.palyer_init_pos = True
                    
                else:
                    if m == 0 and n == 0:
                        cell.supgum = True
                        cell.ghost = True
                        score += data.get_supgum_points()

                    elif m == width - 1 and n == 0:
                        cell.supgum = True
                        cell.ghost = True
                        score += data.get_supgum_points()

                    elif m == 0 and n == height -1:
                        cell.supgum = True
                        cell.ghost = True
                        score += data.get_supgum_points()

                    elif m == width -1 and n == height - 1:
                        cell.supgum = True
                        cell.ghost = True
                        score += data.get_supgum_points()

                if maze.maze[n][m] & Directions.N:
                    cell.North = True
                    closed += 1
                if maze.maze[n][m] & Directions.E:
                    cell.Est = True
                    closed += 1
                if maze.maze[n][m] & Directions.S:
                    cell.South = True
                    closed += 1
                if maze.maze[n][m] & Directions.W:
                    cell.West = True
                    closed += 1
                if closed !=4  and not cell.supgum and not cell.palyer_init_pos:
                    cell.gum = True
                    score += data.get_pacgum_points()
                cells.append(cell)

            maze_obj.append(cells)
        return maze_obj, score
