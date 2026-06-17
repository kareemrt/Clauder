"""Escape-time fractals: Mandelbrot and Julia sets.

Both are rendered with smooth (continuous) iteration coloring so that
gradients look smooth instead of banded.
"""

from __future__ import annotations

import numpy as np

from fracta.palette import apply_palette


def _smooth_escape(c: np.ndarray, z0: np.ndarray, max_iter: int) -> np.ndarray:
    """Vectorized escape-time computation with smooth coloring.

    Returns a float array in [0, 1] where 0 means "never escaped"
    (inside the set) and values approaching 1 mean "escaped quickly".
    """
    z = z0.copy()
    escaped_at = np.full(c.shape, max_iter, dtype=np.float64)
    not_escaped = np.ones(c.shape, dtype=bool)

    for i in range(max_iter):
        z[not_escaped] = z[not_escaped] ** 2 + c[not_escaped]
        mag = np.abs(z)
        newly_escaped = not_escaped & (mag > 2.0)
        if np.any(newly_escaped):
            # Smooth iteration count: i + 1 - log2(log(|z|))
            log_zn = np.log(mag[newly_escaped])
            nu = np.log(log_zn / np.log(2)) / np.log(2)
            escaped_at[newly_escaped] = i + 1 - nu
        not_escaped &= ~newly_escaped
        if not np.any(not_escaped):
            break

    inside = escaped_at >= max_iter
    smooth = escaped_at / max_iter
    smooth[inside] = 0.0
    # Boost contrast so detail near the boundary is visible.
    smooth = np.sqrt(np.clip(smooth, 0, 1))
    return smooth


def _make_grid(
    width: int, height: int, center: tuple[float, float], scale: float
) -> np.ndarray:
    aspect = width / height
    x = np.linspace(-scale * aspect, scale * aspect, width) + center[0]
    y = np.linspace(-scale, scale, height) + center[1]
    xx, yy = np.meshgrid(x, y)
    return xx + 1j * yy


def render_mandelbrot(
    width: int = 800,
    height: int = 800,
    center: tuple[float, float] = (-0.5, 0.0),
    scale: float = 1.4,
    max_iter: int = 300,
    palette: str = "ocean",
) -> np.ndarray:
    """Render a Mandelbrot set image. Returns an (H, W, 3) uint8 array."""
    c = _make_grid(width, height, center, scale)
    z0 = np.zeros_like(c)
    field = _smooth_escape(c, z0, max_iter)
    return apply_palette(field, palette)


def render_julia(
    width: int = 800,
    height: int = 800,
    c: complex = -0.74543 + 0.11301j,
    center: tuple[float, float] = (0.0, 0.0),
    scale: float = 1.4,
    max_iter: int = 300,
    palette: str = "fire",
) -> np.ndarray:
    """Render a Julia set image for the given complex parameter c."""
    z0 = _make_grid(width, height, center, scale)
    c_grid = np.full_like(z0, c)
    field = _smooth_escape(c_grid, z0, max_iter)
    return apply_palette(field, palette)
