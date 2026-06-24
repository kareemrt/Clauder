"""lsystemgarden: grow botanical fractals from Lindenmayer-system grammars."""

from .lsystem import LSystem
from .turtle import Segment, interpret

__all__ = ["LSystem", "Segment", "interpret"]
__version__ = "0.1.0"
