"""State model for an individual maze ghost."""

from dataclasses import dataclass, field
from typing import Optional, Tuple


@dataclass
class Ghost:
    """Store a ghost's position, behavior, and respawn state."""

    position: Tuple[int, int] = (0, 0)
    home: Tuple[int, int] = (0, 0)
    weak: bool = False
    eaten: bool = False
    respawn_at: int = 0
    id: int = 0
    previous: Optional[tuple[int, int]] = None
    neighboars: list[tuple[int, int]] = field(default_factory=list)

    def reset(self) -> None:
        """Return the ghost to its spawn cell in its normal state."""
        self.position = self.home
        self.weak = False
        self.eaten = False
        self.respawn_at = 0
        self.previous = None
        self.neighboars = []
