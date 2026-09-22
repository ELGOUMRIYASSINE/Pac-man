from enum import IntEnum
from dataclasses import dataclass
from typing import Tuple, List
from mazegenerator import MazeGenerator
from .get_maze_bylevel import LevelMaze
from ..GameEngine.player import Player
from ..GameEngine.pacgums_position import Gums

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
    directions:List[bool] = [North, South, Est, West]
    has_player:bool = False

@dataclass
class Maze:

    @classmethod
    def creat_cells(cls, level:int):
        maze: MazeGenerator = LevelMaze.get_maze_bylevel(level)
        height:int = maze._height
        width:int = maze._width
        player_position: Tuple[int,int] = Player.creat_player(level)
        maze_obj = []
        for n in range(height):
            cells = []
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
                if maze.maze[n][m] & Directions.E:
                    cell.Est = True
                if maze.maze[n][m] & Directions.S:
                    cell.South = True
                if maze.maze[n][m] & Directions.W:
                    cell.West = True
                Gums.pacgums_position(cell)
                cells.append(cell)
            maze_obj.append(cells)
        
        return maze_obj
