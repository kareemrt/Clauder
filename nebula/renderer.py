"""Image and ASCII rendering for fractals."""

import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .palettes import apply_palette, apply_newton_palette, list_palettes
from .fractals import mandelbrot, julia, burning_ship, newton
from .fractals.julia import JULIA_PRESETS
from .fractals.newton import ROOT_COLORS


ASCII_CHARS = " .:-=+*#%@█"


def _to_ascii(field: np.ndarray, width: int = 80) -> str:
    """Render a normalized field as ASCII art."""
    h, w = field.shape
    aspect = 0.45  # Terminal chars are taller than wide
    new_h = int(width * h / w * aspect)
    img = Image.fromarray((field * 255).astype(np.uint8), mode="L")
    img = img.resize((width, new_h), Image.LANCZOS)
    arr = np.array(img) / 255.0
    chars = np.array(list(ASCII_CHARS))
    idx = (arr * (len(chars) - 1)).astype(int)
    lines = ["".join(chars[row]) for row in idx]
    return "\n".join(lines)


def _add_watermark(img: Image.Image, text: str) -> Image.Image:
    """Burn a small label into the bottom-right corner."""
    draw = ImageDraw.Draw(img)
    margin = 8
    x = img.width - margin - len(text) * 6
    y = img.height - margin - 12
    draw.text((x + 1, y + 1), text, fill=(0, 0, 0, 160))
    draw.text((x, y), text, fill=(200, 200, 200, 200))
    return img


def render(
    fractal: str,
    palette: str = "deep_space",
    width: int = 1200,
    height: int = 800,
    max_iter: int = 256,
    output: str | None = None,
    ascii_mode: bool = False,
    julia_preset: str = "spiral",
    zoom: float = 1.0,
    cx: float = 0.0,
    cy: float = 0.0,
    show_info: bool = True,
) -> Image.Image | str:
    """
    Render a fractal and either return the image or save it.

    Args:
        fractal: One of 'mandelbrot', 'julia', 'burning_ship', 'newton'
        palette: Color palette name (see nebula.palettes.list_palettes())
        width, height: Output image dimensions in pixels
        max_iter: Maximum iteration depth (higher = more detail, slower)
        output: If set, save to this path
        ascii_mode: If True, return ASCII string instead of Image
        julia_preset: Named Julia set constant (see nebula.fractals.julia.JULIA_PRESETS)
        zoom: Zoom level (1.0 = full view, 10.0 = 10x zoom)
        cx, cy: Center coordinates for the viewport
        show_info: Overlay fractal info text on image
    """
    t0 = time.perf_counter()

    # Build viewport
    def viewport(base_x, base_y, base_w, base_h):
        hw = base_w / (2 * zoom)
        hh = base_h / (2 * zoom)
        return cx - hw + base_x, cx + hw + base_x, cy - hh + base_y, cy + hh + base_y

    fractal = fractal.lower()

    if fractal == "mandelbrot":
        bx, by, bw, bh = -0.75, 0.0, 1.75, 1.25
        x_min, x_max, y_min, y_max = (
            bx - bw / zoom, bx + bw / zoom,
            by - bh / zoom, by + bh / zoom,
        )
        field = mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter)
        img = apply_palette(field, palette)
        label = f"Mandelbrot Set | {palette} | iter={max_iter}"

    elif fractal == "julia":
        c = JULIA_PRESETS.get(julia_preset, JULIA_PRESETS["spiral"])
        span = 1.5 / zoom
        field = julia(
            width, height, c,
            cx - span, cx + span, cy - span, cy + span,
            max_iter,
        )
        img = apply_palette(field, palette)
        label = f"Julia Set ({julia_preset}, c={c:.4f}) | {palette}"

    elif fractal == "burning_ship":
        bx, by = -0.5, -0.75
        span_x, span_y = 2.0 / zoom, 1.25 / zoom
        field = burning_ship(
            width, height,
            bx + cx - span_x, bx + cx + span_x,
            by + cy - span_y, by + cy + span_y,
            max_iter,
        )
        img = apply_palette(field, palette)
        label = f"Burning Ship | {palette} | iter={max_iter}"

    elif fractal == "newton":
        span = 1.5 / zoom
        root_map, speed_map = newton(
            width, height,
            cx - span, cx + span, cy - span, cy + span,
            min(max_iter, 64),
        )
        img = apply_newton_palette(root_map, speed_map, palette)
        label = f"Newton Fractal (z³−1) | 3 basins of attraction"

    else:
        raise ValueError(f"Unknown fractal '{fractal}'. Choose: mandelbrot, julia, burning_ship, newton")

    elapsed = time.perf_counter() - t0

    if ascii_mode:
        h, w = np.array(img).shape[:2]
        field_gray = np.array(img.convert("L")) / 255.0
        return _to_ascii(field_gray)

    if show_info:
        img = _add_watermark(img, f"nebula | {label} | {elapsed:.2f}s")

    if output:
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        img.save(output, quality=95)

    return img, elapsed
