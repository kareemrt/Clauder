"""Julia set computation with smooth escape-time coloring."""
from __future__ import annotations
import math


# Famous Julia set seed constants
JULIA_SEEDS: dict[str, tuple[float, float]] = {
    "dendrite":      (-0.0,       1.0),
    "rabbit":        (-0.123,     0.745),
    "dragon":        (-0.7269,    0.1889),
    "lightning":     (-0.8,       0.156),
    "douady_rabbit": (-0.12256,   0.74486),
    "snowflake":     (-0.4,       0.6),
    "spiral":        (0.285,      0.01),
    "galaxy":        (-0.70176,  -0.3842),
}


def julia_escape(zx: float, zy: float, cx: float, cy: float, max_iter: int) -> tuple[int, float]:
    """
    Return (iteration_count, smooth_t) for Julia set with seed (cx, cy).
    smooth_t is in [0, 1]: 0 = in set, 1 = escaped immediately.
    """
    for i in range(max_iter):
        zx2, zy2 = zx * zx, zy * zy
        if zx2 + zy2 > 256.0:
            log_zn = math.log(zx2 + zy2) / 2.0
            nu = math.log(log_zn / math.log(2.0)) / math.log(2.0)
            smooth = (i + 1 - nu) / max_iter
            return i, max(0.0, min(1.0, smooth))
        zy = 2.0 * zx * zy + cy
        zx = zx2 - zy2 + cx
    return max_iter, 0.0


def compute_julia(
    width: int,
    height: int,
    cx: float,
    cy: float,
    zoom: float,
    max_iter: int,
    seed_name: str = "dragon",
) -> list[list[float]]:
    """
    Compute the full Julia set grid for the given seed.
    Returns a 2-D list [row][col] of smooth_t values in [0,1].
    """
    seed_cx, seed_cy = JULIA_SEEDS.get(seed_name, (-0.7, 0.27015))
    aspect = 2.0
    half_w = (width / 2) / zoom
    half_h = (height / 2) / zoom / aspect

    grid: list[list[float]] = []
    for row in range(height):
        line: list[float] = []
        y = cy + (row / (height - 1) - 0.5) * 2.0 * half_h
        for col in range(width):
            x = cx + (col / (width - 1) - 0.5) * 2.0 * half_w
            _, t = julia_escape(x, y, seed_cx, seed_cy, max_iter)
            line.append(t)
        grid.append(line)
    return grid
