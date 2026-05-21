"""Fractal computation engines."""

from .mandelbrot import mandelbrot
from .julia import julia
from .burning_ship import burning_ship
from .newton import newton

__all__ = ["mandelbrot", "julia", "burning_ship", "newton"]
