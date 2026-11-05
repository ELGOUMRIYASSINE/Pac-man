import pygame
from pygame.math import Vector2


class Mover:
    """Slides a sprite between grid cells over a fixed duration (ms)."""

    def __init__(self, pos, duration: int) -> None:
        self.start = Vector2(pos)
        self.target = Vector2(pos)
        self.pos = Vector2(pos)
        self.previous = Vector2(pos)   # position on the previous frame
        self.duration = duration
        self.t0 = pygame.time.get_ticks() - duration

    def set_target(self, new_target, now: int) -> None:
        new_target = Vector2(new_target)
        if new_target == self.target:
            return
        self.start = Vector2(self.pos)
        self.target = new_target
        self.t0 = now

    def snap(self, pos, now: int) -> None:
        """Teleport with no sliding (respawn): never crosses the walls."""
        self.start = Vector2(pos)
        self.target = Vector2(pos)
        self.pos = Vector2(pos)
        self.previous = Vector2(pos)
        self.t0 = now - self.duration

    def progress(self, now: int) -> float:
        """How far along the current step: 0.0 = just left, 1.0 = arrived."""
        return max(0.0, min(1.0, (now - self.t0) / self.duration))

    def update(self, now: int) -> Vector2:
        self.previous = self.pos
        self.pos = self.start.lerp(self.target, self.progress(now))
        return self.pos


def closest_distance(a_from: Vector2, a_to: Vector2,
                     b_from: Vector2, b_to: Vector2) -> float:
    """Smallest distance between two sprites moving during the same frame.

    Checking the whole movement instead of only the end positions means a
    slow frame cannot make two sprites jump over each other.
    """
    gap = a_from - b_from
    closing = (a_to - a_from) - (b_to - b_from)
    speed = closing.length_squared()
    t = 0.0 if speed == 0 else max(0.0, min(1.0, -gap.dot(closing) / speed))
    return (gap + closing * t).length()
