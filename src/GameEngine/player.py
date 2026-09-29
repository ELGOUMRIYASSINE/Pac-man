from dataclasses import dataclass
import curses
from ..Maze.Maze import Maze, Cell, MetaData
from typing import List, Tuple


@dataclass
class Player:
    can_move:bool = False
    lives:int = 3
    positionx:int = 0
    positiony: int= 0
    position:Tuple[int,int]=(0, 0)
    level:int = 0
    dead:bool=False
    score:int = 0
    required_score:int = 0
    super_power:bool=True

class MovePlayer:
    def move_player(self, move, player:Player, data:MetaData, maze:List[List[Cell]])->None:
        if move == "UP":
            if (
                player.positiony - 1 >= 0
                and not maze[player.positiony][player.positionx].North
            ):
                maze[player.positiony][player.positionx].has_player = False
                player.positiony -= 1
                player.position = (player.positiony, player.positionx)
                maze[player.positiony][player.positionx].has_player = True
                if maze[player.positiony][player.positionx].gum:
                    player.score += data.get_pacgum_points()
                    maze[player.positiony][player.positionx].gum = False
                elif maze[player.positiony][player.positionx].supgum:
                    player.score += data.get_supgum_points()
                    player.super_power = True
                    maze[player.positiony][player.positionx].supgum = False
            else:
                player.can_move = False
        # -----------------------------------------------------------------------------
        elif move == "DOWN":
            # i have to init level outside
            if player.positiony + 1 < data.get_height(player.level) and not maze[player.positiony][player.positionx].South:
                maze[player.positiony][player.positionx].has_player = False
                player.positiony += 1
                maze[player.positiony][player.positionx].has_player = True
                player.position = (player.positiony, player.positionx)
                if maze[player.positiony][player.positionx].gum:
                    player.score += data.get_pacgum_points()
                    maze[player.positiony][player.positionx].gum = False
                elif maze[player.positiony][player.positionx].supgum:
                    player.score += data.get_supgum_points()
                    player.super_power = True
                    maze[player.positiony][player.positionx].supgum = False
            else:
                player.can_move = False
        # ------------------------------------------------------------------------------------
        elif move == "LEFT":
            if (
                player.positionx - 1 >= 0
                and not maze[player.positiony][player.positionx].West
            ):
                maze[player.positiony][player.positionx].has_player = False
                player.positionx -= 1
                maze[player.positiony][player.positionx].has_player = True
                player.position = (player.positiony, player.positionx)
                if maze[player.positiony][player.positionx].gum:
                    player.score += data.get_pacgum_points()
                    maze[player.positiony][player.positionx].gum = False
                elif maze[player.positiony][player.positionx].supgum:
                    player.score += data.get_supgum_points()
                    player.super_power = True
                    maze[player.positiony][player.positionx].supgum = False
            else:
                player.can_move = False
        # --------------------------------------------------------------------------------
        elif move == "RIGHT":
            if player.positionx + 1 < data.get_width(player.level) and not maze[player.positiony][player.positionx].Est:
                maze[player.positiony][player.positionx].has_player = False
                player.positionx += 1
                maze[player.positiony][player.positionx].has_player = True
                player.position = (player.positiony, player.positionx)
                if maze[player.positiony][player.positionx].gum:
                    player.score += data.get_pacgum_points()
                    maze[player.positiony][player.positionx].gum = False
                elif maze[player.positiony][player.positionx].supgum:
                    player.score += data.get_supgum_points()
                    player.super_power = True
                    maze[player.positiony][player.positionx].supgum = False
            else:
                player.can_move = False

    def check_level(self, player:Player)-> str:
        if player.score == player.required_score and player.lives > 0:
            if player.level < 10:
                player.level += 1
                return "NEXT"
            else:
                return "END"
        else:
            if player.lives > 0:
                return "RESPOWN"
            else:
                return "LOSE"
            
