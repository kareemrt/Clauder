"""Color palette system — maps smooth escape-time values to RGB colors."""

import numpy as np
from typing import Tuple


def _lerp_palette(stops: list[Tuple[float, Tuple[int, int, int]]],
                  t: np.ndarray) -> np.ndarray:
    """Interpolate between color stops. stops = [(t0, rgb0), (t1, rgb1), ...]."""
    t = np.clip(t, 0.0, 1.0)
    result = np.zeros((*t.shape, 3), dtype=np.uint8)
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        mask = (t >= t0) & (t <= t1)
        if not np.any(mask):
            continue
        local = (t[mask] - t0) / (t1 - t0)
        for ch in range(3):
            result[mask, ch] = np.clip(c0[ch] + local * (c1[ch] - c0[ch]), 0, 255).astype(np.uint8)
    return result


def _cyclic_hue(t: np.ndarray, stops: list[Tuple[float, Tuple[int, int, int]]]) -> np.ndarray:
    """Wrap t into [0,1) and apply palette cyclically."""
    t_cyc = t % 1.0
    return _lerp_palette(stops, t_cyc)


PALETTES = {
    "fire": [
        (0.00, (0,   0,   0)),
        (0.15, (64,  0,   0)),
        (0.35, (192, 32,  0)),
        (0.55, (255, 160, 0)),
        (0.75, (255, 255, 80)),
        (1.00, (255, 255, 255)),
    ],
    "ice": [
        (0.00, (0,   0,   0)),
        (0.20, (0,   20,  80)),
        (0.45, (0,   120, 200)),
        (0.65, (80,  200, 255)),
        (0.85, (200, 240, 255)),
        (1.00, (255, 255, 255)),
    ],
    "psychedelic": [
        (0.00, (0,   0,   0)),
        (0.17, (148, 0,   211)),
        (0.33, (0,   0,   255)),
        (0.50, (0,   255, 0)),
        (0.67, (255, 255, 0)),
        (0.83, (255, 128, 0)),
        (1.00, (255, 0,   0)),
    ],
    "ocean": [
        (0.00, (0,   0,   0)),
        (0.20, (0,   10,  60)),
        (0.45, (0,   80,  120)),
        (0.65, (0,   160, 160)),
        (0.82, (80,  220, 180)),
        (1.00, (255, 255, 255)),
    ],
    "gold": [
        (0.00, (0,   0,   0)),
        (0.25, (40,  20,  0)),
        (0.50, (140, 80,  0)),
        (0.70, (220, 180, 20)),
        (0.85, (255, 230, 100)),
        (1.00, (255, 255, 220)),
    ],
    "aurora": [
        (0.00, (0,   0,   0)),
        (0.20, (0,   40,  20)),
        (0.40, (0,   160, 80)),
        (0.60, (80,  255, 180)),
        (0.80, (180, 100, 255)),
        (1.00, (255, 200, 255)),
    ],
    "monochrome": [
        (0.00, (0,   0,   0)),
        (1.00, (255, 255, 255)),
    ],
}


def colorize(smooth: np.ndarray, palette_name: str = "fire",
             cycle_speed: float = 0.05) -> np.ndarray:
    """
    Map smooth escape-time array to an RGBA image array (H x W x 4).
    Interior points (smooth == 0) are always black.
    """
    stops = PALETTES.get(palette_name, PALETTES["fire"])
    max_val = smooth.max()
    if max_val == 0:
        max_val = 1.0

    t = (smooth * cycle_speed) % 1.0
    rgb = _lerp_palette(stops, t)

    # Force interior (escaped == False i.e. smooth == 0) to black
    interior = smooth == 0.0
    rgb[interior] = (0, 0, 0)

    alpha = np.full((*smooth.shape,), 255, dtype=np.uint8)
    rgba = np.concatenate([rgb, alpha[..., np.newaxis]], axis=2)
    return rgba


# ASCII brightness chars from darkest to brightest
ASCII_CHARS = " .`-_':,;^~=+<>i!lI?/\\|()1{}[]rcvunxzjftLCJUYXZO0Qoahkbdpqwm*WMB8&%$#@"


def to_ascii(smooth: np.ndarray, width: int = 120, height: int = 40) -> str:
    """Downsample the iteration array and map to ASCII characters."""
    from PIL import Image

    # Normalize to 0-255 for downsample via PIL
    norm = smooth.copy()
    norm[norm == 0] = 0
    max_v = norm.max()
    if max_v > 0:
        norm = (norm / max_v * 255).astype(np.uint8)
    else:
        norm = norm.astype(np.uint8)

    img = Image.fromarray(norm, mode="L")
    img = img.resize((width, height), Image.LANCZOS)
    arr = np.array(img)

    lines = []
    n = len(ASCII_CHARS) - 1
    for row in arr:
        line = "".join(ASCII_CHARS[int(v / 255 * n)] for v in row)
        lines.append(line)
    return "\n".join(lines)
