"""Chaos-game fractals: iterated function systems (IFS) sampled randomly.

A chaos game repeatedly picks one of several affine transforms (weighted
by probability) and applies it to a point, plotting where the point lands
after a short warm-up. Many classic fractals (Sierpinski triangle,
Barnsley fern) are nothing more than a handful of these transforms.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from fracta.palette import apply_palette


@dataclass(frozen=True)
class AffineMap:
    a: float
    b: float
    c: float
    d: float
    e: float
    f: float
    weight: float


# (a, b, c, d, e, f, weight) per Barnsley's classic fern parameterization.
PRESETS: dict[str, list[AffineMap]] = {
    "barnsley_fern": [
        AffineMap(0.0, 0.0, 0.0, 0.16, 0.0, 0.0, 0.01),
        AffineMap(0.85, 0.04, -0.04, 0.85, 0.0, 1.6, 0.85),
        AffineMap(0.2, -0.26, 0.23, 0.22, 0.0, 1.6, 0.07),
        AffineMap(-0.15, 0.28, 0.26, 0.24, 0.0, 0.44, 0.07),
    ],
    "sierpinski_triangle": [
        AffineMap(0.5, 0.0, 0.0, 0.5, 0.0, 0.0, 1 / 3),
        AffineMap(0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 1 / 3),
        AffineMap(0.5, 0.0, 0.0, 0.5, 0.25, 0.5, 1 / 3),
    ],
    "dragon_curve": [
        AffineMap(0.5, -0.5, 0.5, 0.5, 0.0, 0.0, 0.5),
        AffineMap(-0.5, -0.5, 0.5, -0.5, 1.0, 0.0, 0.5),
    ],
}


def run_chaos_game(
    maps: list[AffineMap], n_points: int = 200_000, warmup: int = 20, seed: int = 0
) -> np.ndarray:
    """Run the chaos game and return an (n_points, 2) array of xy points."""
    rng = np.random.default_rng(seed)
    weights = np.array([m.weight for m in maps], dtype=np.float64)
    weights /= weights.sum()
    choices = rng.choice(len(maps), size=n_points + warmup, p=weights)

    points = np.empty((n_points + warmup, 2), dtype=np.float64)
    x, y = 0.0, 0.0
    for i, idx in enumerate(choices):
        m = maps[idx]
        x, y = m.a * x + m.b * y + m.e, m.c * x + m.d * y + m.f
        points[i] = (x, y)

    return points[warmup:]


def render_chaos_game(
    preset: str = "barnsley_fern",
    width: int = 800,
    height: int = 900,
    n_points: int = 300_000,
    palette: str = "forest",
    seed: int = 0,
) -> np.ndarray:
    """Render a named IFS preset as a density-colored image, uint8 (H, W, 3)."""
    if preset not in PRESETS:
        raise ValueError(f"Unknown preset {preset!r}. Options: {sorted(PRESETS)}")
    points = run_chaos_game(PRESETS[preset], n_points=n_points, seed=seed)

    xs, ys = points[:, 0], points[:, 1]
    min_x, max_x = xs.min(), xs.max()
    min_y, max_y = ys.min(), ys.max()
    span_x = max(max_x - min_x, 1e-9)
    span_y = max(max_y - min_y, 1e-9)
    margin = 0.04

    px = ((xs - min_x) / span_x) * width * (1 - 2 * margin) + width * margin
    py = height - (((ys - min_y) / span_y) * height * (1 - 2 * margin) + height * margin)

    grid = np.zeros((height, width), dtype=np.float64)
    px_i = np.clip(px.astype(np.int64), 0, width - 1)
    py_i = np.clip(py.astype(np.int64), 0, height - 1)
    np.add.at(grid, (py_i, px_i), 1.0)

    # Log-scale density so sparse and dense regions are both visible.
    grid = np.log1p(grid)
    if grid.max() > 0:
        grid /= grid.max()
    return apply_palette(grid, palette)
