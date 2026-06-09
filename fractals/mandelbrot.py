"""Mandelbrot set computation with smooth escape-time coloring."""
from __future__ import annotations
import math


def mandelbrot_escape(cx: float, cy: float, max_iter: int) -> tuple[int, float]:
    """
    Return (iteration_count, smooth_t) for point (cx, cy).
    smooth_t is in [0, 1]: 0 = in set, 1 = escaped immediately.
    Uses smooth/continuous coloring via logarithmic escape radius.
    """
    zx, zy = 0.0, 0.0
    for i in range(max_iter):
        zx2, zy2 = zx * zx, zy * zy
        if zx2 + zy2 > 256.0:
            # Smooth iteration count
            log_zn = math.log(zx2 + zy2) / 2.0
            nu = math.log(log_zn / math.log(2.0)) / math.log(2.0)
            smooth = (i + 1 - nu) / max_iter
            return i, max(0.0, min(1.0, smooth))
        zy = 2.0 * zx * zy + cy
        zx = zx2 - zy2 + cx
    return max_iter, 0.0


def compute_mandelbrot(
    width: int,
    height: int,
    cx: float,
    cy: float,
    zoom: float,
    max_iter: int,
) -> list[list[float]]:
    """
    Compute the full Mandelbrot grid.
    Returns a 2-D list [row][col] of smooth_t values in [0,1].
    0 = inside the set (black), >0 = escaped (colored).
    """
    # Terminal chars are roughly 2x taller than wide, compensate with aspect
    aspect = 2.0
    half_w = (width / 2) / zoom
    half_h = (height / 2) / zoom / aspect

    grid: list[list[float]] = []
    for row in range(height):
        line: list[float] = []
        y = cy + (row / (height - 1) - 0.5) * 2.0 * half_h
        for col in range(width):
            x = cx + (col / (width - 1) - 0.5) * 2.0 * half_w
            _, t = mandelbrot_escape(x, y, max_iter)
            line.append(t)
        grid.append(line)
    return grid
