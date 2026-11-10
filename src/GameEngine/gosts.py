from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class Ghost:
    position: Tuple[int, int] = (0, 0)
    home: Tuple[int, int] = (0, 0)
    weak: bool = False
    eaten: bool = False
    respawn_at: int = 0
    id: int = 0
    previous: Optional[Tuple[int, int]] = None   # cell it just came from
    neighboars: List[Tuple[int, int]] = field(default_factory=list)

    def reset(self) -> None:
        """Back to the spawn cell, dangerous and visible."""
        self.position = self.home
        self.weak = False
        self.eaten = False
        self.respawn_at = 0
        self.previous = None
        self.neighboars = []
