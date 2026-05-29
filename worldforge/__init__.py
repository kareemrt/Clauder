"""WorldForge: Procedural ASCII World Generator."""

from .world import World
from .renderer import render_terminal, render_plain, render_legend

__all__ = ["World", "render_terminal", "render_plain", "render_legend"]
__version__ = "1.0.0"
