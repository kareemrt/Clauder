"""
FractalScape - A stunning terminal fractal explorer.
Explore the infinite complexity of mathematical fractals rendered in living color.
"""
__version__ = "1.0.0"
__author__ = "FractalScape"

from .core import compute_fractal
from .colors import THEMES, iteration_to_color
from .presets import PRESETS

__all__ = ["compute_fractal", "THEMES", "PRESETS", "iteration_to_color"]
