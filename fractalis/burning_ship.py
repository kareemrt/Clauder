"""Burning Ship fractal: z_{n+1} = (|Re(z_n)| + i|Im(z_n)|)^2 + c."""

from . import colormaps
from .escape_time import render

# The ship sits in the lower half-plane; this framing shows the full hull.
DEFAULT_BOUNDS = (-2.2, 1.2, -1.9, 0.6)


def _step(z, c):
    z = complex(abs(z.real), abs(z.imag))
    return z * z + c


def _seed(c):
    return 0j


def render_burning_ship(width=800, height=800, bounds=DEFAULT_BOUNDS,
                         max_iter=200, cmap="fire"):
    x_min, x_max, y_min, y_max = bounds
    cmap_fn = colormaps.get(cmap) if isinstance(cmap, str) else cmap
    return render(width, height, x_min, x_max, y_min, y_max, max_iter,
                  _step, _seed, cmap_fn)
