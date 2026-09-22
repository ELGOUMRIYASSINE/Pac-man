from ..Maze.Maze import Maze, dataclass, Cell

@dataclass
class Gums:

    @classmethod
    def pacgums_position(cls, cell:Cell):
            if not all(cell.directions) and not cell.supgum and not cell.player_init_position:
                cell.gum = True
                  
                  
