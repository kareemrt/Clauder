"""Rendering engine: terminal ASCII preview and high-resolution PNG export."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import numpy as np
from PIL import Image

from .colormaps import apply_colormap, COLORMAPS
from .fractals import mandelbrot, julia, burning_ship


# ── ASCII density gradient (darkest → brightest) ──────────────────────────────
_CHARS = " .'`^\",:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


def _escape_to_ascii(data: np.ndarray) -> str:
    """Convert a 2-D escape-time array to a coloured ANSI terminal string."""
    lines = []
    vmax = data.max()
    if vmax == 0:
        vmax = 1
    for row in data:
        parts = []
        for v in row:
            t = v / vmax
            ci = int(t * (len(_CHARS) - 1))
            ch = _CHARS[ci]
            if v == 0:
                parts.append(ch)
            else:
                # Map to 256-colour ANSI
                r = int(t ** 0.5 * 5)
                g = int(t ** 0.4 * 5)
                b = int((1 - t) ** 0.3 * 5)
                r, g, b = min(r, 5), min(g, 5), min(b, 5)
                colour_idx = 16 + 36 * r + 6 * g + b
                parts.append(f"\x1b[38;5;{colour_idx}m{ch}\x1b[0m")
        lines.append("".join(parts))
    return "\n".join(lines)


def compute(fractal: str, width: int, height: int,
            x_min: float, x_max: float,
            y_min: float, y_max: float,
            max_iter: int,
            julia_c: Optional[complex] = None) -> np.ndarray:
    """Dispatch to the appropriate fractal kernel."""
    if fractal == "julia":
        if julia_c is None:
            raise ValueError("julia_c must be provided for Julia sets")
        return julia(width, height, x_min, x_max, y_min, y_max, julia_c, max_iter)
    elif fractal == "burning_ship":
        return burning_ship(width, height, x_min, x_max, y_min, y_max, max_iter)
    else:
        return mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter)


def render_terminal(data: np.ndarray,
                    term_width: Optional[int] = None,
                    term_height: Optional[int] = None) -> str:
    """Downsample data to terminal dimensions and return ANSI string."""
    tw = term_width  or (os.get_terminal_size().columns if hasattr(os, "get_terminal_size") else 120)
    th = term_height or (os.get_terminal_size().lines   if hasattr(os, "get_terminal_size") else 40)
    th = max(1, th - 4)   # leave room for borders

    from PIL import Image as _PILImg
    h, w = data.shape
    # Quick downsample via PIL
    arr = (data / max(data.max(), 1) * 255).astype(np.uint8)
    img = _PILImg.fromarray(arr, mode="L")
    img = img.resize((tw, th), _PILImg.LANCZOS)
    small = np.array(img, dtype=np.float64)
    return _escape_to_ascii(small)


def render_png(data: np.ndarray, colormap: str = "nebula",
               gamma: float = 0.5, upscale: int = 1) -> Image.Image:
    """Convert escape-time data to a PIL Image using the chosen colormap."""
    rgb = apply_colormap(data, name=colormap, gamma=gamma)
    img = Image.fromarray(rgb, mode="RGB")
    if upscale > 1:
        new_w = img.width  * upscale
        new_h = img.height * upscale
        img = img.resize((new_w, new_h), Image.LANCZOS)
    return img


def save_png(img: Image.Image, path: str) -> str:
    """Save image, creating parent directories as needed. Returns resolved path."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(p))
    return str(p.resolve())
