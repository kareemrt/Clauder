"""Fractal Garden: grow and render Lindenmayer-system fractals."""

from .lsystem import LSystem, Segment, interpret
from .presets import PRESETS, get_preset

__version__ = "0.1.0"

__all__ = [
    "LSystem",
    "Segment",
    "interpret",
    "PRESETS",
    "get_preset",
    "__version__",
]
