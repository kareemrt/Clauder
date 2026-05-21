"""Color palettes for fractal rendering."""

import numpy as np
from PIL import Image


def _make_gradient(colors: list[tuple], n: int = 256) -> np.ndarray:
    """Build a smooth n-step RGB gradient from a list of (r, g, b) waypoints."""
    colors = np.array(colors, dtype=float)
    steps = np.linspace(0, 1, n)
    waypoints = np.linspace(0, 1, len(colors))
    result = np.zeros((n, 3), dtype=np.uint8)
    for ch in range(3):
        result[:, ch] = np.clip(
            np.interp(steps, waypoints, colors[:, ch]), 0, 255
        ).astype(np.uint8)
    return result


PALETTES: dict[str, np.ndarray] = {
    "fire": _make_gradient([
        (0, 0, 0), (30, 0, 60), (100, 0, 120),
        (200, 30, 0), (255, 140, 0), (255, 240, 100), (255, 255, 255),
    ]),
    "deep_space": _make_gradient([
        (0, 0, 20), (5, 10, 60), (20, 40, 120),
        (60, 120, 200), (140, 200, 255), (200, 240, 255), (255, 255, 255),
    ]),
    "psychedelic": _make_gradient([
        (0, 0, 0), (128, 0, 128), (0, 0, 255),
        (0, 255, 255), (0, 255, 0), (255, 255, 0),
        (255, 0, 0), (255, 0, 255), (255, 255, 255),
    ]),
    "ice": _make_gradient([
        (0, 0, 30), (0, 30, 80), (0, 80, 160),
        (40, 160, 220), (160, 220, 255), (220, 240, 255), (255, 255, 255),
    ]),
    "neon": _make_gradient([
        (0, 0, 0), (0, 20, 40), (0, 80, 0),
        (0, 200, 60), (200, 255, 0), (255, 60, 0),
        (255, 0, 200), (180, 0, 255), (255, 255, 255),
    ]),
    "gold": _make_gradient([
        (0, 0, 0), (20, 10, 0), (80, 40, 0),
        (180, 100, 0), (240, 200, 40), (255, 240, 160), (255, 255, 255),
    ]),
    "monochrome": _make_gradient([
        (0, 0, 0), (40, 40, 40), (120, 120, 120),
        (200, 200, 200), (255, 255, 255),
    ]),
    "aurora": _make_gradient([
        (5, 0, 20), (0, 20, 60), (0, 100, 80),
        (20, 200, 100), (100, 255, 150), (200, 255, 200),
        (255, 200, 255), (180, 100, 255), (80, 0, 200),
    ]),
}


def apply_palette(field: np.ndarray, palette_name: str = "deep_space") -> Image.Image:
    """Map a normalized [0, 1] float field to an RGB image via a palette."""
    palette = PALETTES.get(palette_name, PALETTES["deep_space"])
    clean = np.nan_to_num(field, nan=0.0, posinf=1.0, neginf=0.0)
    idx = np.clip((clean * (len(palette) - 1)).astype(int), 0, len(palette) - 1)
    rgb = palette[idx]
    return Image.fromarray(rgb.astype(np.uint8), mode="RGB")


def apply_newton_palette(
    root_map: np.ndarray,
    speed_map: np.ndarray,
    palette_name: str = "deep_space",
) -> Image.Image:
    """Special coloring for Newton fractals: root determines hue, speed determines brightness."""
    from .fractals.newton import ROOT_COLORS

    h, w = root_map.shape
    rgb = np.zeros((h, w, 3), dtype=float)

    for r_idx, color in enumerate(ROOT_COLORS):
        mask = root_map == r_idx
        brightness = speed_map[mask, np.newaxis] ** 0.5
        rgb[mask] = color * brightness

    # Unconverged points are black
    rgb = (np.clip(rgb, 0, 1) * 255).astype(np.uint8)
    return Image.fromarray(rgb, mode="RGB")


def list_palettes() -> list[str]:
    return list(PALETTES.keys())
