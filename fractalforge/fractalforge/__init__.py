"""FractalForge — Terminal fractal art engine."""

__version__ = "1.0.0"
__author__ = "FractalForge"

from . import mandelbrot, julia, sierpinski, renderer, palettes

__all__ = ["mandelbrot", "julia", "sierpinski", "renderer", "palettes"]
