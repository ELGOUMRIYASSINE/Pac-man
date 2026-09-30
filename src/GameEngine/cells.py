from dataclasses import dataclass
from typing import Tuple 

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
    has_player: bool = False
    palyer_init_pos: bool = False
