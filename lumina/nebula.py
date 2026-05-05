"""Nebula rendering using layered fBm noise and emission color palettes."""
import numpy as np
from .noise import fbm

# Named nebula palettes: list of (RGB float, weight) for color stops
PALETTES = {
    "pillars": [
        ((0.05, 0.02, 0.15), 0.0),
        ((0.25, 0.05, 0.35), 0.3),
        ((0.70, 0.20, 0.10), 0.6),
        ((0.95, 0.60, 0.20), 0.85),
        ((1.00, 0.95, 0.80), 1.0),
    ],
    "crab": [
        ((0.02, 0.02, 0.10), 0.0),
        ((0.10, 0.05, 0.40), 0.25),
        ((0.05, 0.35, 0.70), 0.55),
        ((0.40, 0.80, 0.90), 0.80),
        ((0.95, 1.00, 1.00), 1.0),
    ],
    "rosette": [
        ((0.05, 0.00, 0.08), 0.0),
        ((0.40, 0.02, 0.20), 0.3),
        ((0.85, 0.10, 0.35), 0.6),
        ((1.00, 0.55, 0.45), 0.85),
        ((1.00, 0.90, 0.85), 1.0),
    ],
    "orion": [
        ((0.02, 0.03, 0.12), 0.0),
        ((0.05, 0.15, 0.50), 0.3),
        ((0.15, 0.55, 0.80), 0.6),
        ((0.70, 0.90, 1.00), 0.85),
        ((0.95, 0.98, 1.00), 1.0),
    ],
    "butterfly": [
        ((0.03, 0.01, 0.08), 0.0),
        ((0.20, 0.03, 0.45), 0.25),
        ((0.55, 0.10, 0.65), 0.5),
        ((0.90, 0.50, 0.20), 0.75),
        ((1.00, 0.92, 0.60), 1.0),
    ],
}


def _interpolate_palette(t: float, palette: list) -> np.ndarray:
    """Map scalar t ∈ [0,1] to an RGB color via palette color stops."""
    for i in range(len(palette) - 1):
        c0, t0 = palette[i]
        c1, t1 = palette[i + 1]
        if t0 <= t <= t1:
            alpha = (t - t0) / (t1 - t0 + 1e-9)
            return np.array(c0) * (1 - alpha) + np.array(c1) * alpha
    return np.array(palette[-1][0])


def _vectorized_palette(field: np.ndarray, palette: list) -> np.ndarray:
    """Apply palette to a 2D field, returning H x W x 3 RGB array."""
    h, w = field.shape
    rgb = np.zeros((h, w, 3))
    stops = [(np.array(c), t) for c, t in palette]
    for i in range(len(stops) - 1):
        c0, t0 = stops[i]
        c1, t1 = stops[i + 1]
        mask = (field >= t0) & (field < t1)
        alpha = np.where(mask, (field - t0) / (t1 - t0 + 1e-9), 0.0)
        for ch in range(3):
            rgb[:, :, ch] += mask * (c0[ch] * (1 - alpha) + c1[ch] * alpha)
    # Last stop
    mask = field >= stops[-1][1]
    for ch in range(3):
        rgb[:, :, ch] += mask * stops[-1][0][ch]
    return np.clip(rgb, 0, 1)


def render_nebula(width: int, height: int, palette_name: str,
                  rng: np.random.Generator, density: float = 0.6) -> np.ndarray:
    """
    Returns H x W x 4 RGBA float array for a procedural nebula.
    density controls how much of the frame is filled with nebula.
    """
    palette = PALETTES[palette_name]

    # Primary nebula shape via fBm
    shape = fbm(width, height, octaves=7, lacunarity=2.1, gain=0.52,
                base_scale=width / 3.5, rng=rng)
    # Secondary wispy detail
    detail = fbm(width, height, octaves=5, lacunarity=2.3, gain=0.48,
                 base_scale=width / 6.0, rng=rng)
    # Domain-warp the shape field for more organic forms
    warp_x = fbm(width, height, octaves=4, lacunarity=2.0, gain=0.5,
                 base_scale=width / 4.0, rng=rng) * 0.4
    warp_y = fbm(width, height, octaves=4, lacunarity=2.0, gain=0.5,
                 base_scale=width / 4.0, rng=rng) * 0.4

    # Apply domain warp (shift lookup coordinates by noise offset)
    h_idx, w_idx = np.mgrid[0:height, 0:width]
    wx = np.clip((w_idx + warp_x * width * 0.12).astype(int), 0, width - 1)
    wy = np.clip((h_idx + warp_y * height * 0.12).astype(int), 0, height - 1)
    warped = shape[wy, wx]

    combined = np.clip(warped * 0.7 + detail * 0.3, 0, 1)

    # Threshold + soft alpha mask
    threshold = 1.0 - density
    alpha = np.clip((combined - threshold) / (1.0 - threshold + 1e-6), 0, 1)
    # Power curve for sharper edges
    alpha = np.power(alpha, 1.4)

    # Apply color palette
    rgb = _vectorized_palette(combined, palette)

    # Add subtle emission brighten at peaks
    peaks = np.power(np.clip(combined - 0.75, 0, 1) * 4, 2)
    rgb = np.clip(rgb + peaks[:, :, np.newaxis] * 0.25, 0, 1)

    rgba = np.concatenate([rgb, alpha[:, :, np.newaxis]], axis=2)
    return rgba.astype(np.float32)
