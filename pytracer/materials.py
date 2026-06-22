from dataclasses import dataclass

from .vector import Vec3


@dataclass(frozen=True, slots=True)
class Material:
    color: Vec3
    ambient: float = 0.05
    diffuse: float = 0.8
    specular: float = 0.5
    shininess: float = 50.0
    reflectivity: float = 0.0
