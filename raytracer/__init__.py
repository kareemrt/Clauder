"""ASCII Ray Tracer — pure-Python 3D renderer for the terminal."""

from .vector import Vec3
from .ray import Ray
from .objects import Sphere, Plane, Material
from .light import PointLight, AmbientLight
from .scene import Scene, Camera
from .renderer import Renderer
from .display import AsciiDisplay

__all__ = [
    "Vec3", "Ray",
    "Sphere", "Plane", "Material",
    "PointLight", "AmbientLight",
    "Scene", "Camera",
    "Renderer",
    "AsciiDisplay",
]
