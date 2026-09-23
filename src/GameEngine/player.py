from dataclasses import dataclass
import curses
from ..Maze.Maze import Maze, Cell, MetaData


@dataclass
class Player:
    can_move:bool = False
    lives:int = 3
    positionx:int = 0
    positiony: int= 0
    level:int = 0
    dead:bool=False
    score:int = 0

class MovePlayer:
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def move_player(self,player:Player, data:MetaData)->None:
        # i have to init player object once
        move = self.stdscr.getch()
        if move == curses.KEY_UP or move == ord("w") or move == ord("W"):
            if player.positiony - 1 >= 0:
                player.positiony -= 1
            else:
                player.can_move = False
        elif move == curses.KEY_DOWN or move == ord("S") or move == ord("s"):
            # i have to init level outside
            if player.positiony + 1 < data.get_height(player.level):
                player.positiony += 1
            else:
                player.can_move = False
        elif move == curses.KEY_LEFT or move == ord("A") or move == ord("a"):
            if player.positionx - 1 >= 0:
                player.positionx -= 1
            else:
                player.can_move = False
        elif move == curses.KEY_RIGHT or move == ord("D") or move == ord("d"):
            if player.positionx + 1 < data.get_width(player.level):
                player.positionx += 1
            else:
                player.can_move = False
