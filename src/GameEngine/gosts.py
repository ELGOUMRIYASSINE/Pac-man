from dataclasses import dataclass
from typing import Tuple


@dataclass
class Ghost:
    position: Tuple[int, int] = (0, 0)
    weak: bool = False
    eaten: bool = False
