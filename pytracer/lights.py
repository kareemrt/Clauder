from dataclasses import dataclass

from .vector import Vec3


@dataclass(frozen=True, slots=True)
class PointLight:
    position: Vec3
    color: Vec3 = Vec3(1, 1, 1)
    intensity: float = 1.0
