"""Colour palette management for fractal renders."""

import numpy as np
from PIL import Image


PALETTES = {
    "inferno": [
        (0, 0, 4), (40, 11, 84), (101, 21, 110), (159, 42, 99),
        (212, 72, 66), (245, 125, 21), (250, 193, 39), (252, 255, 164),
    ],
    "ocean": [
        (3, 5, 18), (10, 30, 80), (15, 80, 140), (20, 140, 180),
        (40, 200, 200), (120, 230, 210), (210, 250, 240), (255, 255, 255),
    ],
    "fire": [
        (0, 0, 0), (30, 0, 0), (80, 10, 0), (150, 30, 0),
        (220, 80, 0), (255, 150, 20), (255, 220, 100), (255, 255, 200),
    ],
    "midnight": [
        (5, 0, 30), (20, 0, 80), (60, 10, 130), (120, 40, 180),
        (180, 100, 220), (220, 160, 240), (240, 210, 250), (255, 240, 255),
    ],
    "forest": [
        (0, 5, 0), (5, 30, 5), (15, 80, 20), (40, 130, 40),
        (80, 180, 60), (150, 220, 100), (210, 240, 160), (240, 255, 220),
    ],
    "copper": [
        (0, 0, 0), (40, 20, 5), (100, 55, 15), (160, 90, 30),
        (200, 130, 60), (230, 170, 100), (245, 210, 150), (255, 245, 210),
    ],
    "aurora": [
        (5, 0, 20), (10, 20, 60), (10, 80, 100), (20, 160, 120),
        (80, 200, 150), (160, 230, 180), (220, 245, 210), (250, 255, 240),
    ],
}


def _interpolate_palette(palette: list[tuple], n: int = 2048) -> np.ndarray:
    """Linearly interpolate a sparse palette to n colours."""
    lut = np.zeros((n, 3), dtype=np.uint8)
    stops = len(palette)
    for i in range(n):
        t = i / (n - 1) * (stops - 1)
        lo = int(t)
        hi = min(lo + 1, stops - 1)
        frac = t - lo
        for ch in range(3):
            lut[i, ch] = int(palette[lo][ch] * (1 - frac) + palette[hi][ch] * frac)
    return lut


def colorize(iteration_map: np.ndarray, palette_name: str = "inferno",
             max_iter: int = 256) -> Image.Image:
    """Map float iteration values to an RGB image using the chosen palette."""
    palette = PALETTES.get(palette_name, PALETTES["inferno"])
    lut = _interpolate_palette(palette)

    # Normalise to [0, 1], treating 0 (inside set) as black
    inside = iteration_map == 0
    flat = iteration_map.copy()
    flat[inside] = 0
    valid = flat[~inside]
    if valid.size:
        flat[~inside] = (valid - valid.min()) / (valid.max() - valid.min() + 1e-9)

    indices = (flat * (len(lut) - 1)).astype(int).clip(0, len(lut) - 1)
    rgb = lut[indices]
    rgb[inside] = [0, 0, 0]

    return Image.fromarray(rgb.astype(np.uint8), "RGB")


def colorize_newton(roots_map: np.ndarray, speed_map: np.ndarray,
                    n_roots: int) -> Image.Image:
    """Colour Newton fractal — hue by root, brightness by convergence speed."""
    root_hues = [
        (220, 60, 180),   # violet-blue
        (60, 200, 80),    # green
        (255, 120, 30),   # orange
        (180, 60, 220),   # purple
        (30, 180, 200),   # teal
        (255, 60, 60),    # red
    ]
    h, w = roots_map.shape
    rgb = np.zeros((h, w, 3), dtype=np.uint8)

    for k in range(n_roots):
        mask = roots_map == k
        base = np.array(root_hues[k % len(root_hues)], dtype=float)
        brightness = 0.3 + 0.7 * (1 - speed_map[mask])
        rgb[mask] = (base * brightness[:, np.newaxis]).clip(0, 255).astype(np.uint8)

    # Unconverged pixels stay black
    return Image.fromarray(rgb, "RGB")
