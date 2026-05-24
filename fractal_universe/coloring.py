import numpy as np
from typing import Callable


# ── Palette definitions ───────────────────────────────────────────────────────

def _make_gradient(stops: list[tuple[float, tuple[int, int, int]]]) -> Callable[[float], tuple[int, int, int]]:
    """Build a smooth RGB gradient from (position, color) stops."""
    def gradient(t: float) -> tuple[int, int, int]:
        t = max(0.0, min(1.0, t))
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                alpha = (t - t0) / (t1 - t0)
                r = int(c0[0] + alpha * (c1[0] - c0[0]))
                g = int(c0[1] + alpha * (c1[1] - c0[1]))
                b = int(c0[2] + alpha * (c1[2] - c0[2]))
                return (r, g, b)
        return stops[-1][1]
    return gradient


PALETTES: dict[str, list[tuple[float, tuple[int, int, int]]]] = {
    "cosmic": [
        (0.00, (0,   0,   20)),
        (0.15, (10,  5,   60)),
        (0.30, (80,  0,  140)),
        (0.45, (220, 40,  80)),
        (0.60, (255, 140,  0)),
        (0.75, (255, 240, 60)),
        (0.90, (255, 255, 220)),
        (1.00, (255, 255, 255)),
    ],
    "ocean": [
        (0.00, (0,   0,   30)),
        (0.20, (0,   20,  80)),
        (0.40, (0,   80, 160)),
        (0.60, (0,  180, 200)),
        (0.80, (60, 230, 200)),
        (1.00, (220, 255, 255)),
    ],
    "lava": [
        (0.00, (0,   0,   0)),
        (0.20, (60,  0,   0)),
        (0.40, (160, 20,  0)),
        (0.55, (255, 80,  0)),
        (0.70, (255, 200, 0)),
        (0.85, (255, 255, 120)),
        (1.00, (255, 255, 255)),
    ],
    "electric": [
        (0.00, (0,   0,   0)),
        (0.15, (0,   0,   60)),
        (0.35, (0,   40, 180)),
        (0.55, (0,  160, 255)),
        (0.75, (100, 240, 255)),
        (1.00, (255, 255, 255)),
    ],
    "aurora": [
        (0.00, (5,   0,   20)),
        (0.20, (0,   60,  80)),
        (0.40, (0,  160,  80)),
        (0.60, (80, 220, 120)),
        (0.80, (160, 255, 200)),
        (1.00, (220, 255, 255)),
    ],
}


# ── Coloring algorithms ───────────────────────────────────────────────────────

def histogram_coloring(data: np.ndarray, palette_name: str = "cosmic",
                       max_iter: int = 256) -> np.ndarray:
    """
    Map iteration counts to RGB using histogram equalization for even color distribution.
    Interior points (==max_iter) are painted black.
    """
    interior = data >= max_iter
    exterior = ~interior

    # Build histogram of exterior escape counts
    normed = np.zeros(data.shape, dtype=np.float64)
    if exterior.any():
        # Histogram equalization on smooth values
        vals = data[exterior]
        # Quantize to bins for histogram
        bins = 4096
        counts, edges = np.histogram(vals, bins=bins)
        cdf = np.cumsum(counts).astype(np.float64)
        cdf /= cdf[-1]

        # Map each pixel's value through the CDF
        bin_idx = np.searchsorted(edges[:-1], vals) - 1
        bin_idx = np.clip(bin_idx, 0, bins - 1)
        normed[exterior] = cdf[bin_idx]

    grad = _make_gradient(PALETTES[palette_name])

    # Vectorised palette lookup
    flat = normed.ravel()
    rgb = np.array([grad(t) for t in flat], dtype=np.uint8).reshape(*data.shape, 3)
    rgb[interior] = (0, 0, 0)
    return rgb


def newton_coloring(root_id: np.ndarray, iteration: np.ndarray,
                    max_iter: int = 64) -> np.ndarray:
    """
    Color Newton fractal by root + convergence speed.
    """
    root_hues = [
        np.array([220, 80,  40],  dtype=np.float64),   # root 0 — orange-red
        np.array([60,  180, 255], dtype=np.float64),   # root 1 — cyan-blue
        np.array([100, 220, 80],  dtype=np.float64),   # root 2 — green
    ]
    h, w = root_id.shape
    rgb = np.zeros((h, w, 3), dtype=np.uint8)

    speed = np.clip(iteration / max_iter, 0, 1)
    brightness = 0.2 + 0.8 * (1 - speed)  # faster convergence → brighter

    for r in range(3):
        mask = root_id == r
        if mask.any():
            color = root_hues[r]
            rgb[mask] = (color * brightness[mask, np.newaxis]).astype(np.uint8)

    # Unconverged pixels stay black
    return rgb
