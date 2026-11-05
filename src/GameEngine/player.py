from dataclasses import dataclass
from typing import List, Optional, Tuple

from ..Maze.Maze import Cell, MetaData

# move -> (row change, column change, wall that blocks it)
MOVES = {
    "UP": (-1, 0, "North"),
    "DOWN": (1, 0, "South"),
    "LEFT": (0, -1, "West"),
    "RIGHT": (0, 1, "Est"),
}


@dataclass
class Player:
    lives: int = 6
    positionx: int = 0
    positiony: int = 0
    position: Tuple[int, int] = (0, 0)
    level: int = 0
    dead: bool = False
    score: int = 0
    super_power: bool = False
    super_until: int = 0
    facing: Optional[str] = None   # last real move, the sprite rotates with it


class MovePlayer:
    SUPER_POWER_MS = 7000

    def can_move(self, move: str, player: Player, data: MetaData,
                 maze: List[List[Cell]]) -> bool:
        d_row, d_col, wall = MOVES[move]
        row = player.positiony + d_row
        col = player.positionx + d_col
        return (
            0 <= row < data.get_height(player.level)
            and 0 <= col < data.get_width(player.level)
            and not getattr(maze[player.positiony][player.positionx], wall)
        )

    def move_player(self, move: str, player: Player, data: MetaData,
                    maze: List[List[Cell]]) -> bool:
        """One logical step. Returns False when a wall blocks it.

        Nothing is eaten and nobody dies here: the sprite has not arrived
        yet. See eat_cell() and GameLoop.check_collision().
        """
        if not self.can_move(move, player, data, maze):
            return False
        d_row, d_col, _ = MOVES[move]
        maze[player.positiony][player.positionx].has_player = False
        player.positiony += d_row
        player.positionx += d_col
        player.position = (player.positiony, player.positionx)
        maze[player.positiony][player.positionx].has_player = True
        player.facing = move
        return True

    def eat_cell(self, player: Player, data: MetaData,
                 maze: List[List[Cell]], now: int) -> bool:
        """Eat what is on the player's cell. True if it was a super gum."""
        cell = maze[player.positiony][player.positionx]
        if cell.gum:
            player.score += data.get_pacgum_points()
            cell.gum = False
        elif cell.supgum:
            player.score += data.get_supgum_points()
            player.super_power = True
            player.super_until = now + self.SUPER_POWER_MS
            cell.supgum = False
            return True
        return False

    def check_level(self, player: Player, data: MetaData,
                    maze: List[List[Cell]]) -> str:
        if player.dead:
            return "RESPOWN" if player.lives > 1 else "LOSE"
        if any(cell.gum or cell.supgum for row in maze for cell in row):
            return "CON"
        if player.level + 1 >= data.get_level_count():
            return "END"
        player.level += 1
        player.lives = data.get_lives()
        return "NEXT"
