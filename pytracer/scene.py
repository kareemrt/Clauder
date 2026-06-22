from dataclasses import dataclass, field

from .lights import PointLight
from .shapes import Shape
from .vector import Vec3


@dataclass
class Scene:
    objects: list[Shape] = field(default_factory=list)
    lights: list[PointLight] = field(default_factory=list)
    background_top: Vec3 = Vec3(0.6, 0.8, 1.0)
    background_bottom: Vec3 = Vec3(1.0, 1.0, 1.0)
    ambient_light: float = 0.1

    def background(self, direction: Vec3) -> Vec3:
        t = 0.5 * (direction.y + 1.0)
        return self.background_bottom * (1 - t) + self.background_top * t
