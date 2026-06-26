"""Minimal 2D vector math used by the simulation. No external deps."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class Vector2:
    x: float = 0.0
    y: float = 0.0

    def __add__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector2":
        return Vector2(self.x * scalar, self.y * scalar)

    __rmul__ = __mul__

    def __truediv__(self, scalar: float) -> "Vector2":
        return Vector2(self.x / scalar, self.y / scalar)

    def length(self) -> float:
        return math.hypot(self.x, self.y)

    def normalized(self) -> "Vector2":
        length = self.length()
        if length == 0:
            return Vector2(0.0, 0.0)
        return self / length

    def limited(self, max_length: float) -> "Vector2":
        length = self.length()
        if length <= max_length or length == 0:
            return Vector2(self.x, self.y)
        return self.normalized() * max_length

    def angle(self) -> float:
        return math.atan2(self.y, self.x)

    def as_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)


def distance(a: Vector2, b: Vector2) -> float:
    return math.hypot(a.x - b.x, a.y - b.y)


def toroidal_delta(a: Vector2, b: Vector2, width: float, height: float) -> Vector2:
    """Shortest displacement from b to a on a wrap-around (toroidal) plane."""
    dx = a.x - b.x
    dy = a.y - b.y
    if dx > width / 2:
        dx -= width
    elif dx < -width / 2:
        dx += width
    if dy > height / 2:
        dy -= height
    elif dy < -height / 2:
        dy += height
    return Vector2(dx, dy)
