"""Ray: a point plus a direction."""

from .vector import Vec3


class Ray:
    __slots__ = ("origin", "direction")

    def __init__(self, origin: Vec3, direction: Vec3):
        self.origin = origin
        self.direction = direction.normalize()

    def at(self, t: float) -> Vec3:
        return self.origin + self.direction * t
