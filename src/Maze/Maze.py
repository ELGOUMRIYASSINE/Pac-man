from enum import IntEnum
from dataclasses import dataclass
from typing import Tuple, List
from mazegenerator import MazeGenerator
from .get_maze_bylevel import LevelMaze
from ..GameEngine.player import Player


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
    player_init_position:bool = False
    ghost:bool = False
    has_player:bool = False

@dataclass
class Maze:

    @classmethod
    def creat_cells(cls, level:int, data):
        maze: MazeGenerator = LevelMaze.get_maze_bylevel(level, data)
        height:int = maze._height
        width:int = maze._width
        player_position: Tuple[int,int] = Player.creat_player(level, data)
        maze_obj = []
        for n in range(height):
            cells = []
            closed = 0
            for m in range(width):
                cell = Cell((n, m))
                if (n, m) == player_position:
                    cell.player_init_position = True
                else:
                    if m == 0 and n == 0:
                        cell.supgum = True
                        cell.ghost = True
                    elif m == width - 1 and n == 0:
                        cell.supgum = True
                        cell.ghost = True
                    elif m == 0 and n == height -1:
                        cell.supgum = True
                        cell.ghost = True
                    elif m == width -1 and n == height - 1:
                        cell.supgum = True
                        cell.ghost = True
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
                if closed !=4  and not cell.supgum and not cell.player_init_position:
                                cell.gum = True
                cells.append(cell)
            maze_obj.append(cells)
        
        return maze_obj
