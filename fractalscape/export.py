"""
High-resolution PNG export engine.
Generates publication-quality fractal images with anti-aliasing and custom resolution.
"""
import os
from typing import List, Optional, Tuple

from .colors import iteration_to_color, THEMES

try:
    from PIL import Image, ImageFilter, ImageEnhance
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False


RESOLUTIONS = {
    "720p":   (1280, 720),
    "1080p":  (1920, 1080),
    "1440p":  (2560, 1440),
    "4k":     (3840, 2160),
    "square": (2048, 2048),
    "thumb":  (512, 512),
}


def export_png(
    data: List[List[float]],
    max_iter: int,
    theme: str,
    output_path: str,
    cycle_period: float = 64.0,
    upscale: int = 1,
    sharpen: bool = False,
    enhance_contrast: float = 1.0,
) -> bool:
    """
    Export fractal data as a PNG image.

    Args:
        data:           Fractal iteration data (height × width).
        max_iter:       Max iteration count (in-set points).
        theme:          Color theme name.
        output_path:    Where to save the PNG.
        cycle_period:   Color cycle length in iterations.
        upscale:        Integer upscale factor (e.g. 2 = 2× resolution).
        sharpen:        Apply unsharp-mask for crisp edges.
        enhance_contrast: PIL contrast factor (1.0 = unchanged).

    Returns:
        True on success, False if Pillow is unavailable.
    """
    if not PILLOW_AVAILABLE:
        print("Pillow not installed. Run: pip install Pillow")
        return False

    height = len(data)
    width = len(data[0]) if data else 0
    out_w, out_h = width * upscale, height * upscale

    pixels = []
    for row in data:
        pixel_row = []
        for val in row:
            color = iteration_to_color(val, max_iter, theme, cycle_period)
            pixel_row.append(color)
        pixels.append(pixel_row)

    img = Image.new("RGB", (width, height))
    img.putdata([px for row in pixels for px in row])

    if upscale > 1:
        img = img.resize((out_w, out_h), Image.NEAREST)

    if sharpen:
        img = img.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=2))

    if enhance_contrast != 1.0:
        img = ImageEnhance.Contrast(img).enhance(enhance_contrast)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, "PNG", optimize=True)
    return True


def export_hires(
    width: int,
    height: int,
    x_min: float, x_max: float,
    y_min: float, y_max: float,
    fractal_type: str,
    max_iter: int,
    theme: str,
    output_path: str,
    julia_c: Tuple[float, float] = (-0.7, 0.27015),
    cycle_period: float = 64.0,
    progress_callback=None,
) -> bool:
    """
    Render a fractal at native high resolution and export as PNG.
    Uses the core compute engine with full resolution (no upscaling needed).
    """
    from .core import compute_fractal

    data = compute_fractal(
        width, height, x_min, x_max, y_min, y_max,
        fractal_type=fractal_type,
        max_iter=max_iter,
        julia_c=julia_c,
        progress_callback=progress_callback,
    )

    return export_png(data, max_iter, theme, output_path,
                       cycle_period=cycle_period, sharpen=True)
