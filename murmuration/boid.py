"""A single agent in the flock."""

from __future__ import annotations

from .vector import Vector2


class Boid:
    """An autonomous agent with a position and velocity.

    ``is_predator`` boids are rendered differently and are exempt from
    the standard flocking rules: they simply hunt the nearest prey.
    """

    __slots__ = ("position", "velocity", "is_predator")

    def __init__(self, position: Vector2, velocity: Vector2, is_predator: bool = False):
        self.position = position
        self.velocity = velocity
        self.is_predator = is_predator

    def speed(self) -> float:
        return self.velocity.length()

    def heading(self) -> float:
        return self.velocity.angle()
