from dataclasses import dataclass
from typing import Tuple, List
from ..Maze.Maze import  MetaData
from collections import deque


@dataclass
class Ghost:
    position: Tuple[int, int] = (0, 0)
    weak: bool = False
    eaten: bool = False
    id: int = 0
    neighboars = []
    
