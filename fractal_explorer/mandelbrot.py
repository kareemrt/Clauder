"""Mandelbrot set computation."""

from typing import Generator


def compute_mandelbrot(
    width: int,
    height: int,
    x_min: float = -2.5,
    x_max: float = 1.0,
    y_min: float = -1.25,
    y_max: float = 1.25,
    max_iter: int = 80,
) -> list[list[int]]:
    """
    Compute the Mandelbrot set for a grid of complex numbers.
    Returns a 2D grid of iteration counts (0 = inside the set).
    """
    grid = []
    for row in range(height):
        line = []
        for col in range(width):
            cx = x_min + (x_max - x_min) * col / (width - 1)
            cy = y_min + (y_max - y_min) * row / (height - 1)
            line.append(_escape_count(cx, cy, max_iter))
        grid.append(line)
    return grid


def _escape_count(cx: float, cy: float, max_iter: int) -> int:
    """Return iteration count before escape, or 0 if inside the set."""
    zx, zy = 0.0, 0.0
    for i in range(1, max_iter + 1):
        zx, zy = zx * zx - zy * zy + cx, 2 * zx * zy + cy
        if zx * zx + zy * zy > 4.0:
            return i
    return 0


# Famous zoom targets: (x_min, x_max, y_min, y_max, name)
ZOOM_PRESETS = [
    (-2.5, 1.0, -1.25, 1.25, "Full View"),
    (-0.75, -0.73, 0.10, 0.12, "Seahorse Valley"),
    (-0.16, -0.12, 1.025, 1.045, "Elephant Valley"),
    (-1.77, -1.75, -0.02, 0.02, "Mini Mandelbrot"),
    (-0.7269, -0.7266, 0.1889, 0.1892, "Deep Spiral"),
    (-0.5, 0.5, -0.5, 0.5, "Center Zoom"),
]
