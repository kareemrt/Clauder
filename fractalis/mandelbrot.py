"""Mandelbrot set rendering: z_{n+1} = z_n^2 + c, seeded at z_0 = 0."""

from . import colormaps
from .escape_time import render

# A classic full view of the Mandelbrot set.
DEFAULT_BOUNDS = (-2.5, 1.0, -1.25, 1.25)

# "Seahorse valley", a popular zoom target near the main cusp.
SEAHORSE_VALLEY = (-0.775, -0.715, 0.085, 0.145)


def _step(z, c):
    return z * z + c


def _seed(c):
    return 0j


def render_mandelbrot(width=800, height=800, bounds=DEFAULT_BOUNDS,
                       max_iter=200, cmap="inferno"):
    x_min, x_max, y_min, y_max = bounds
    cmap_fn = colormaps.get(cmap) if isinstance(cmap, str) else cmap
    return render(width, height, x_min, x_max, y_min, y_max, max_iter,
                  _step, _seed, cmap_fn)
