"""Barnsley Fern IFS (Iterated Function System) fractal."""
from __future__ import annotations
import random
import math


# IFS transformations: (a, b, c, d, e, f, probability)
BARNSLEY_IFS = [
    (0.0,   0.0,   0.0,  0.16, 0.0, 0.0,  0.01),   # stem
    (0.85,  0.04, -0.04, 0.85, 0.0, 1.60, 0.85),   # leaflet
    (0.20, -0.26,  0.23, 0.22, 0.0, 1.60, 0.07),   # left leaflet
    (-0.15, 0.28,  0.26, 0.24, 0.0, 0.44, 0.07),   # right leaflet
]

# Other IFS fractals
TREE_IFS = [
    (0.0,   0.0,  0.0,  0.5,  0.0, 0.0,  0.05),
    (0.42,  -0.42, 0.42, 0.42, 0.0, 0.2,  0.40),
    (0.42,  0.42, -0.42, 0.42, 0.0, 0.2,  0.40),
    (0.1,   0.0,  0.0,  0.1,  0.0, 0.2,  0.15),
]

SNOWFLAKE_IFS = [
    (0.333, 0.0,   0.0,  0.333, 0.0,   0.0,   0.2),
    (0.333, 0.0,   0.0,  0.333, 0.333, 0.0,   0.2),
    (0.333, 0.0,   0.0,  0.333, 0.667, 0.0,   0.2),
    (0.333, 0.0,   0.0,  0.333, 0.167, 0.289, 0.2),
    (0.333, 0.0,   0.0,  0.333, 0.5,   0.289, 0.2),
]

IFS_SYSTEMS: dict[str, list] = {
    "fern":      BARNSLEY_IFS,
    "tree":      TREE_IFS,
    "snowflake": SNOWFLAKE_IFS,
}


def barnsley_fern(
    width: int,
    height: int,
    iterations: int = 200_000,
    ifs_name: str = "fern",
) -> list[list[bool]]:
    """
    Generate an IFS fractal on a width×height boolean grid.
    Returns True where a point was plotted.
    """
    ifs = IFS_SYSTEMS.get(ifs_name, BARNSLEY_IFS)
    grid = [[False] * width for _ in range(height)]

    x, y = 0.0, 0.0
    pts: list[tuple[float, float]] = []

    # Build cumulative probability table
    probs = [t[-1] for t in ifs]
    cum = []
    acc = 0.0
    for p in probs:
        acc += p
        cum.append(acc)

    rng = random.Random(42)
    for _ in range(iterations):
        r = rng.random()
        for idx, cp in enumerate(cum):
            if r <= cp:
                a, b, c, d, e, f, _ = ifs[idx]
                x, y = a * x + b * y + e, c * x + d * y + f
                pts.append((x, y))
                break

    if not pts:
        return grid

    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    xrange = xmax - xmin or 1
    yrange = ymax - ymin or 1

    for px, py in pts:
        col = int((px - xmin) / xrange * (width - 1))
        row = height - 1 - int((py - ymin) / yrange * (height - 1))
        if 0 <= col < width and 0 <= row < height:
            grid[row][col] = True

    return grid
