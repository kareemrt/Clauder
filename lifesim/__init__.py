"""LifeSim — Interactive Cellular Automata Simulator."""

__version__ = "1.0.0"
__author__ = "Clauder"

from .automata import GameOfLife, BriansBrain, LangtonsAnt
from .patterns import place_pattern, list_patterns, PATTERNS

__all__ = [
    "GameOfLife",
    "BriansBrain",
    "LangtonsAnt",
    "place_pattern",
    "list_patterns",
    "PATTERNS",
]
