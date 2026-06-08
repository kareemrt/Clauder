"""L-System Garden: a tiny toolkit for growing fractal art from rewriting grammars."""

from .core import LSystem, expand
from .turtle import Segment, walk
from .render import render_svg
from . import presets

__all__ = [
    "LSystem",
    "expand",
    "Segment",
    "walk",
    "render_svg",
    "presets",
]

__version__ = "0.1.0"
