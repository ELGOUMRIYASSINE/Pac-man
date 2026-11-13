"""Player state and movement rules for the maze game."""

from dataclasses import dataclass
from typing import Literal, Optional, Tuple

from ..Maze.Maze import Cell, MetaData

Move = Literal["UP", "DOWN", "LEFT", "RIGHT"]
LevelStatus = Literal["RESPOWN", "LOSE", "CON", "END", "NEXT"]

# move -> (row change, column change, wall that blocks it)
MOVES: dict[Move, tuple[int, int, str]] = {
    "UP": (-1, 0, "North"),
    "DOWN": (1, 0, "South"),
    "LEFT": (0, -1, "West"),
    "RIGHT": (0, 1, "Est"),
}


@dataclass
class Player:
    """Track a player's position, score, lives, and active power state."""

    lives: int = 6
    positionx: int = 0
    positiony: int = 0
    position: Tuple[int, int] = (0, 0)
    level: int = 0
    dead: bool = False
    score: int = 0
    super_power: bool = False
    super_until: int = 0
    facing: Optional[Move] = None


class MovePlayer:
    """Apply player movement and update maze-level game state."""

    SUPER_POWER_MS = 7000

    def can_move(
        self,
        move: Move,
        player: Player,
        data: MetaData,
        maze: list[list[Cell]],
    ) -> bool:
        """Return whether the player can step in the requested direction."""
        move_row, move_col, direct = MOVES[move]
        row = player.positiony + move_row
        col = player.positionx + move_col
        return (
            0 <= row < data.get_height(player.level)
            and 0 <= col < data.get_width(player.level)
            and not getattr(maze[player.positiony][player.positionx], direct)
        )

    def move_player(
        self,
        move: Move,
        player: Player,
        data: MetaData,
        maze: list[list[Cell]],
    ) -> bool:
        """Move the player one logical step unless a wall blocks the way.

        Nothing is eaten and nobody dies here: the sprite has not arrived
        yet. Gum collection and collisions are handled after the sprite moves.
        """
        if not self.can_move(move, player, data, maze):
            return False
        move_row, move_col, _ = MOVES[move]
        maze[player.positiony][player.positionx].has_player = False
        player.positiony += move_row
        player.positionx += move_col
        player.position = (player.positiony, player.positionx)
        maze[player.positiony][player.positionx].has_player = True
        player.facing = move
        return True

    def eat_gum(
        self, player: Player, data: MetaData, maze: list[list[Cell]], now: int
    ) -> bool:
        """Collect gum and return whether the player found super gum."""
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

    def check_level(
        self, player: Player, data: MetaData, maze: list[list[Cell]]
    ) -> LevelStatus:
        """Return the transition required by the player's current state."""
        if player.dead:
            return "RESPOWN" if player.lives > 1 else "LOSE"
        if any(cell.gum or cell.supgum for row in maze for cell in row):
            return "CON"
        if player.level + 1 >= data.get_level_count():
            return "END"
        player.level += 1
        player.lives = data.get_lives()
        return "NEXT"
