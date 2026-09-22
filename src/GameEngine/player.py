from typing import Tuple
from dataclasses import dataclass

@dataclass
class Player:
    @classmethod
    def creat_player(cls, level, metadata) -> Tuple[int,int]:
        return (
            metadata.get_height(level) // 2,
            metadata.get_width(level) // 2,
        )

    
