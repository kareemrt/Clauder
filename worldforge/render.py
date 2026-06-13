"""Render generated worlds as PNG images or ASCII maps."""

from __future__ import annotations

import numpy as np
from PIL import Image

from .worldgen import BIOME_INDEX, World

BIOME_COLORS: dict[str, tuple[int, int, int]] = {
    "ocean": (54, 94, 168),
    "beach": (237, 213, 158),
    "desert": (231, 198, 142),
    "grassland": (149, 191, 98),
    "forest": (79, 134, 75),
    "rainforest": (38, 99, 64),
    "taiga": (140, 173, 150),
    "rock": (140, 130, 120),
    "mountain": (152, 142, 132),
    "snow": (245, 245, 250),
    "river": (94, 154, 214),
}

BIOME_CHARS: dict[str, str] = {
    "ocean": "~",
    "beach": ".",
    "desert": ":",
    "grassland": '"',
    "forest": "f",
    "rainforest": "F",
    "taiga": "t",
    "rock": ",",
    "mountain": "^",
    "snow": "*",
    "river": "=",
}


def _hillshade(elevation: np.ndarray) -> np.ndarray:
    """Return a per-pixel brightness multiplier based on local elevation slope."""
    gy, gx = np.gradient(elevation)
    # A simple directional light from the upper-left.
    shade = 1.0 - (gx * 2.5 + gy * 2.5)
    return np.clip(shade, 0.6, 1.4)


def render_png(world: World, path: str, scale_factor: int = 1) -> None:
    """Render the world to a PNG file, with elevation-based shading and rivers."""
    h, w = world.elevation.shape
    rgb = np.zeros((h, w, 3), dtype=np.float64)

    for name, color in BIOME_COLORS.items():
        if name == "river":
            continue
        mask = world.biome_ids == BIOME_INDEX[name]
        rgb[mask] = color

    shade = _hillshade(world.elevation)
    land_mask = world.biome_ids != BIOME_INDEX["ocean"]
    for c in range(3):
        rgb[..., c] = np.where(land_mask, rgb[..., c] * shade, rgb[..., c])

    rgb[world.river_mask] = BIOME_COLORS["river"]

    rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    image = Image.fromarray(rgb, mode="RGB")

    if scale_factor != 1:
        image = image.resize((w * scale_factor, h * scale_factor), Image.NEAREST)

    image.save(path)


def render_ascii(world: World, step: int = 1) -> str:
    """Render the world as an ASCII map, sampling every `step` cells."""
    lines = []
    for y in range(0, world.height, step):
        row_chars = []
        for x in range(0, world.width, step):
            if world.river_mask[y, x]:
                row_chars.append(BIOME_CHARS["river"])
            else:
                biome_name = world.biome_at(x, y)
                row_chars.append(BIOME_CHARS[biome_name])
        lines.append("".join(row_chars))
    return "\n".join(lines)
