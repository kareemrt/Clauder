"""lsystems: generate fractal curves from Lindenmayer (L-) systems and render them as SVG."""

from .core import LSystem
from .turtle import TurtleInterpreter, Segment
from .svg import segments_to_svg

__all__ = ["LSystem", "TurtleInterpreter", "Segment", "segments_to_svg"]

__version__ = "0.1.0"
