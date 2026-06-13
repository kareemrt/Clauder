"""WorldForge: procedural fantasy world map generator."""

from .worldgen import World, generate_world
from .names import generate_world_name

__version__ = "0.1.0"

__all__ = ["World", "generate_world", "generate_world_name", "__version__"]
