"""Terminal and image rendering for fractals."""

import sys
import os
import numpy as np
from typing import Optional

from .colormap import apply_colormap, rgb_to_ansi_block, rgb_to_ansi_char, iteration_to_ascii, ASCII_GRADIENT


def render_terminal(
    iteration_counts: np.ndarray,
    max_iter: int,
    palette: str = "inferno",
    mode: str = "block",
    width: Optional[int] = None,
) -> str:
    """Render fractal as a colored ANSI string for the terminal.

    mode: 'block' (full color blocks), 'ascii' (ASCII art gradient), 'color_ascii'
    """
    rgb = apply_colormap(iteration_counts, max_iter, palette)
    h, w, _ = rgb.shape

    lines = []
    for row in range(h):
        chars = []
        for col in range(w):
            r, g, b = int(rgb[row, col, 0]), int(rgb[row, col, 1]), int(rgb[row, col, 2])
            if mode == "block":
                chars.append(rgb_to_ansi_block(r, g, b))
            elif mode == "ascii":
                chars.append(iteration_to_ascii(iteration_counts[row, col], max_iter))
            elif mode == "color_ascii":
                ch = iteration_to_ascii(iteration_counts[row, col], max_iter)
                chars.append(rgb_to_ansi_char(r, g, b, ch if ch != " " else "."))
        lines.append("".join(chars))

    return "\n".join(lines)


def save_png(
    iteration_counts: np.ndarray,
    max_iter: int,
    output_path: str,
    palette: str = "inferno",
    scale: int = 1,
) -> str:
    """Save fractal as a PNG image using Pillow."""
    try:
        from PIL import Image
    except ImportError:
        raise ImportError("Pillow is required for PNG export. Install with: pip install Pillow")

    rgb = apply_colormap(iteration_counts, max_iter, palette)
    img = Image.fromarray(rgb.astype(np.uint8), mode="RGB")

    if scale > 1:
        new_size = (img.width * scale, img.height * scale)
        img = img.resize(new_size, Image.NEAREST)

    img.save(output_path)
    return output_path


def generate_zoom_frames(
    fractal_fn,
    center_x: float,
    center_y: float,
    start_zoom: float,
    end_zoom: float,
    frames: int,
    width: int,
    height: int,
    max_iter: int,
    palette: str,
    output_dir: str,
) -> list:
    """Generate a sequence of zoom frames into a fractal point."""
    from .core import zoom_region
    import os

    os.makedirs(output_dir, exist_ok=True)
    zoom_levels = np.geomspace(start_zoom, end_zoom, frames)
    paths = []

    for i, zoom in enumerate(zoom_levels):
        x_min, x_max, y_min, y_max = zoom_region(
            center_x, center_y, zoom, aspect_ratio=width / height
        )
        counts = fractal_fn(
            width, height, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max, max_iter=max_iter
        )
        path = os.path.join(output_dir, f"frame_{i:04d}.png")
        save_png(counts, max_iter, path, palette)
        paths.append(path)
        print(f"  Frame {i+1}/{frames} — zoom {zoom:.1f}x", flush=True)

    return paths
