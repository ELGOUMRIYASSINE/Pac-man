import pygame
from pygame.math import Vector2


class Mover:
    def __init__(self, pos, duration):
        self.start = Vector2(pos)
        self.target = Vector2(pos)
        self.pos = Vector2(pos)
        self.t0 = pygame.time.get_ticks()
        self.duration = duration

    def set_target(self, new_target, now):
        new_target = Vector2(new_target)
        if new_target == self.target:
            return
        self.start = Vector2(self.pos)
        self.target = new_target
        self.t0 = now

    def update(self, now):
        t = (now - self.t0) / self.duration
        t = max(0.0, min(1.0, t))      # force t into [0, 1]
        self.pos = self.start.lerp(self.target, t)
        return self.pos