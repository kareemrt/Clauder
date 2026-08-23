"""Color palettes for fractal rendering."""

import numpy as np


def _lerp_colors(colors: list[tuple], t: np.ndarray) -> np.ndarray:
    """Linearly interpolate between a list of (r, g, b) color stops."""
    n = len(colors) - 1
    t_scaled = t * n
    idx = np.clip(t_scaled.astype(int), 0, n - 1)
    frac = t_scaled - idx

    result = np.zeros((*t.shape, 3), dtype=np.uint8)
    for i in range(n):
        mask = idx == i
        if not np.any(mask):
            continue
        c0 = np.array(colors[i], dtype=float)
        c1 = np.array(colors[i + 1], dtype=float)
        f = frac[mask][..., np.newaxis]
        result[mask] = np.clip(c0 * (1 - f) + c1 * f, 0, 255).astype(np.uint8)

    return result


PALETTES = {
    "inferno": [
        (0, 0, 4),
        (40, 11, 84),
        (101, 21, 110),
        (159, 42, 99),
        (212, 72, 66),
        (245, 125, 21),
        (252, 193, 42),
        (252, 255, 164),
    ],
    "ocean": [
        (3, 4, 94),
        (2, 62, 138),
        (0, 119, 182),
        (0, 180, 216),
        (72, 202, 228),
        (144, 224, 239),
        (202, 240, 248),
        (255, 255, 255),
    ],
    "fire": [
        (0, 0, 0),
        (64, 0, 0),
        (160, 0, 0),
        (255, 64, 0),
        (255, 160, 0),
        (255, 255, 0),
        (255, 255, 200),
        (255, 255, 255),
    ],
    "electric": [
        (0, 0, 0),
        (10, 0, 40),
        (40, 0, 120),
        (80, 20, 220),
        (120, 100, 255),
        (180, 200, 255),
        (220, 240, 255),
        (255, 255, 255),
    ],
    "forest": [
        (0, 10, 0),
        (0, 40, 10),
        (0, 80, 20),
        (10, 120, 40),
        (40, 160, 80),
        (100, 200, 120),
        (180, 230, 160),
        (230, 255, 210),
    ],
    "psychedelic": [
        (255, 0, 128),
        (128, 0, 255),
        (0, 128, 255),
        (0, 255, 128),
        (255, 255, 0),
        (255, 128, 0),
        (255, 0, 64),
        (255, 0, 128),
    ],
    "grayscale": [
        (0, 0, 0),
        (64, 64, 64),
        (128, 128, 128),
        (192, 192, 192),
        (255, 255, 255),
    ],
    "gold": [
        (0, 0, 0),
        (50, 30, 0),
        (120, 80, 0),
        (200, 150, 0),
        (255, 220, 50),
        (255, 255, 180),
        (255, 255, 255),
    ],
}


def apply_palette(iteration_map: np.ndarray, palette_name: str = "inferno",
                  max_iter: int = 256) -> np.ndarray:
    """Map iteration counts to RGB colors using the named palette."""
    colors = PALETTES.get(palette_name, PALETTES["inferno"])

    # Normalize to [0, 1], interior stays black
    escaped = iteration_map > 0
    t = np.zeros_like(iteration_map)
    t[escaped] = np.clip(iteration_map[escaped] / max_iter, 0, 1)
    # Apply gamma for better distribution
    t = np.power(t, 0.5)

    rgb = _lerp_colors(colors, t)
    # Interior (not escaped) → black
    rgb[~escaped] = [0, 0, 0]
    return rgb


def apply_newton_palette(root_map: np.ndarray, speed_map: np.ndarray) -> np.ndarray:
    """Color Newton fractal by root convergence and speed."""
    base_colors = [
        [220, 60, 60],    # red  — root 0
        [60, 180, 60],    # green — root 1
        [60, 100, 220],   # blue  — root 2
        [30, 30, 30],     # dark  — no convergence
    ]
    h, w = root_map.shape
    rgb = np.zeros((h, w, 3), dtype=np.uint8)

    for ri, base in enumerate(base_colors):
        mask = root_map == (ri if ri < 3 else -1)
        if not np.any(mask):
            continue
        speed = speed_map[mask][..., np.newaxis]
        rgb[mask] = (np.array(base) * (0.4 + 0.6 * speed)).astype(np.uint8)

    unconverged = root_map == -1
    rgb[unconverged] = [15, 15, 15]
    return rgb


def list_palettes() -> list[str]:
    return list(PALETTES.keys())
