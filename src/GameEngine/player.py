from mazegenerator import MazeGenerator
from typing import List, Dict, Any

class Player:

    def initial_position(self, mazes:List[MazeGenerator], level: int):
        maze: MazeGenerator = mazes[level]
        maze.generate
        print(maze.maze)
        