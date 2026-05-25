"""
Fractal Canvas — Terminal Fractal Art Generator
Generate stunning ASCII fractal art directly in your terminal.
"""

__version__ = "1.0.0"
__author__ = "Claude"

from .fractals import mandelbrot, julia, burning_ship, newton, tricorn, JULIA_PRESETS
from .palettes import CHAR_SETS, COLOR_PALETTES
from .renderer import render_frame, print_frame, save_frame, animate_zoom, FRACTAL_PRESETS

__all__ = [
    "mandelbrot", "julia", "burning_ship", "newton", "tricorn",
    "JULIA_PRESETS", "CHAR_SETS", "COLOR_PALETTES",
    "render_frame", "print_frame", "save_frame", "animate_zoom", "FRACTAL_PRESETS",
]
