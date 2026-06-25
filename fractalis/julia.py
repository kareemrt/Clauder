"""Julia set rendering: z_{n+1} = z_n^2 + c for a fixed c, seeded at z_0 = pixel."""

from . import colormaps
from .escape_time import render

DEFAULT_BOUNDS = (-1.5, 1.5, -1.5, 1.5)

# A handful of c values known to produce visually rich Julia sets.
PRESETS = {
    "classic": -0.7269 + 0.1889j,
    "dendrite": 0 + 1j,
    "spiral": -0.8 + 0.156j,
    "san_marco": -0.75 + 0j,
    "siegel_disk": -0.391 - 0.587j,
}


def _make_step(c):
    def step(z, _c):
        return z * z + c
    return step


def _seed(c):
    return c


def render_julia(width=800, height=800, c=PRESETS["classic"],
                  bounds=DEFAULT_BOUNDS, max_iter=200, cmap="ocean"):
    if isinstance(c, str):
        c = PRESETS[c]
    x_min, x_max, y_min, y_max = bounds
    cmap_fn = colormaps.get(cmap) if isinstance(cmap, str) else cmap
    return render(width, height, x_min, x_max, y_min, y_max, max_iter,
                  _make_step(c), _seed, cmap_fn)
