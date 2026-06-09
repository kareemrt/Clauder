"""Fractal Terminal Explorer — pure Python, zero dependencies."""
from .mandelbrot import mandelbrot_escape
from .julia import julia_escape
from .barnsley import barnsley_fern
from .colormap import PALETTES
from .renderer import render_fractal, render_fern, clear_screen, hide_cursor, show_cursor
