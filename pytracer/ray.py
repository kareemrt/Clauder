from dataclasses import dataclass

from .vector import Vec3


@dataclass(frozen=True, slots=True)
class Ray:
    origin: Vec3
    direction: Vec3

    def point_at(self, t: float) -> Vec3:
        return self.origin + self.direction * t
