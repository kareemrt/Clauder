"""
Color themes for Cosmograph visualizations.
Each theme is a function mapping a float [0, 1] → (R, G, B) tuple of ints 0–255.
"""

import numpy as np
import colorsys


def _lerp_color(t: float, stops: list) -> tuple:
    """Interpolate between a list of (position, color) stops."""
    if t <= stops[0][0]:
        return stops[0][1]
    if t >= stops[-1][0]:
        return stops[-1][1]
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        if p0 <= t <= p1:
            f = (t - p0) / (p1 - p0)
            return tuple(int(c0[k] + f * (c1[k] - c0[k])) for k in range(3))
    return stops[-1][1]


def _vectorized(fn):
    """Wrap a scalar color function so it accepts numpy arrays."""
    def wrapper(arr):
        arr = np.asarray(arr)
        flat = arr.ravel()
        result = np.zeros((len(flat), 3), dtype=np.uint8)
        for i, v in enumerate(flat):
            result[i] = fn(float(v))
        return result.reshape(arr.shape + (3,))
    return wrapper


def _cosmic(t):
    stops = [
        (0.00, (0,   0,   0)),
        (0.10, (15,  0,   40)),
        (0.25, (60,  0,  100)),
        (0.45, (140, 20, 200)),
        (0.60, (220, 80, 255)),
        (0.75, (255, 160, 200)),
        (0.88, (255, 220, 130)),
        (1.00, (255, 255, 255)),
    ]
    return _lerp_color(t, stops)


def _inferno(t):
    stops = [
        (0.00, (0,   0,   4)),
        (0.13, (20,  11,  52)),
        (0.25, (58,  9,  100)),
        (0.38, (96,  19,  110)),
        (0.50, (140, 41,  99)),
        (0.63, (188, 80,  72)),
        (0.75, (228, 130,  42)),
        (0.88, (251, 185,  26)),
        (1.00, (252, 255, 165)),
    ]
    return _lerp_color(t, stops)


def _ocean(t):
    stops = [
        (0.00, (0,   0,  20)),
        (0.20, (0,  20,  80)),
        (0.40, (0,  80, 160)),
        (0.60, (0, 160, 200)),
        (0.80, (60, 210, 220)),
        (1.00, (200, 240, 255)),
    ]
    return _lerp_color(t, stops)


def _forest(t):
    stops = [
        (0.00, (0,   5,   0)),
        (0.20, (0,  40,  10)),
        (0.40, (10,  90,  20)),
        (0.60, (40, 150,  40)),
        (0.80, (100, 200, 80)),
        (1.00, (200, 255, 150)),
    ]
    return _lerp_color(t, stops)


def _gold(t):
    stops = [
        (0.00, (0,   0,   0)),
        (0.20, (40,  10,   0)),
        (0.40, (120,  50,   0)),
        (0.60, (200, 120,  20)),
        (0.80, (240, 190,  60)),
        (1.00, (255, 240, 180)),
    ]
    return _lerp_color(t, stops)


def _ice(t):
    stops = [
        (0.00, (0,   0,  20)),
        (0.30, (10,  40, 100)),
        (0.55, (60, 120, 200)),
        (0.75, (140, 200, 240)),
        (0.90, (210, 235, 255)),
        (1.00, (255, 255, 255)),
    ]
    return _lerp_color(t, stops)


def _neon(t):
    # Cycle through hues with saturation boost
    hue = (t * 0.8 + 0.55) % 1.0  # magenta → green cycle
    sat = 1.0
    val = t ** 0.4
    r, g, b = colorsys.hsv_to_rgb(hue, sat, val)
    return (int(r * 255), int(g * 255), int(b * 255))


THEMES = {
    "cosmic":  _cosmic,
    "inferno": _inferno,
    "ocean":   _ocean,
    "forest":  _forest,
    "gold":    _gold,
    "ice":     _ice,
    "neon":    _neon,
}

DEFAULT_THEME = "cosmic"


def apply_theme(iteration_map: np.ndarray, max_iter: float, theme_name: str) -> np.ndarray:
    """
    Convert a 2D iteration count array to an RGB image array.
    Interior points (== max_iter) are mapped to black.
    """
    fn = THEMES.get(theme_name, _cosmic)
    h, w = iteration_map.shape
    img = np.zeros((h, w, 3), dtype=np.uint8)

    interior = iteration_map >= max_iter
    exterior = ~interior

    if np.any(exterior):
        vals = iteration_map[exterior]
        # Histogram equalization for perceptual uniformity
        t = vals / max_iter
        # Gamma correction for visual pop
        t = np.power(np.clip(t, 0, 1), 0.5)
        for idx, (i, j) in enumerate(zip(*np.where(exterior))):
            img[i, j] = fn(t[idx])

    # Interior stays (0, 0, 0) — black

    return img


def apply_binary_theme(grid: np.ndarray, theme_name: str,
                        fg: tuple = None, bg: tuple = (0, 0, 0)) -> np.ndarray:
    """Map a binary grid to an RGB image with foreground/background colors."""
    fn = THEMES.get(theme_name, _cosmic)
    h, w = grid.shape
    img = np.zeros((h, w, 3), dtype=np.uint8)
    img[:] = bg  # background
    ys, xs = np.where(grid == 1)
    if fg is None:
        # Color by position for visual interest
        for y, x in zip(ys, xs):
            t = ((x + y) / (h + w)) ** 0.6
            img[y, x] = fn(t)
    else:
        img[ys, xs] = fg
    return img
