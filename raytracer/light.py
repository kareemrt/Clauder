"""Light sources."""

from dataclasses import dataclass
from .vector import Vec3


@dataclass
class AmbientLight:
    color: Vec3 = None

    def __post_init__(self):
        if self.color is None:
            self.color = Vec3(0.1, 0.1, 0.15)


@dataclass
class PointLight:
    position: Vec3
    color: Vec3 = None
    intensity: float = 1.0

    def __post_init__(self):
        if self.color is None:
            self.color = Vec3(1, 1, 1)
