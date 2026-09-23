from dataclasses import dataclass
import curses
from ..Maze.Maze import Maze, Cell, MetaData


@dataclass
class Player:
    can_move:bool = False
    positionx:int = 0
    positiony: int= 0
    level:int = 0

class MovePlayer:
     
    def move_player(self, move:int, player:Player, data:MetaData)->bool:
        # i have to init player object once 
        if move == curses.KEY_UP:
            while player.can_move:
                if player.positiony - 1 >= 0:
                    player.positiony -= 1
                else:
                    player.can_move = False

        elif move == curses.KEY_DOWN:
            while player.can_move:
                # i have to init level outside
                if player.positiony + 1 < data.get_height(player.level):
                    player.positiony += 1
                else:
                    player.can_move = False

        elif move == curses.KEY_LEFT:
            while player.can_move:
                if player.positionx - 1 >= 0:
                    player.positionx -= 1
                else:
                    player.can_move = False

        elif move == curses.KEY_RIGHT:
            while player.can_move:
                if player.positionx + 1 < data.get_width(player.level):
                    player.positionx += 1
                else:
                    player.can_move = False
        return False
