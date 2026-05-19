"""Image rendering, ASCII preview, and GIF animation."""

import io
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .fractals import mandelbrot, julia, burning_ship, newton
from .colorizer import colorize, colorize_newton, PALETTES


# ── Presets ────────────────────────────────────────────────────────────────

MANDELBROT_PRESETS = {
    "classic":       (-2.5, 1.0, -1.25, 1.25),
    "seahorse":      (-0.76, -0.72, 0.09, 0.13),
    "elephant":      (0.26, 0.285, 0.01, 0.025),
    "triple-spiral": (-0.088, -0.078, 0.6545, 0.6645),
    "lightning":     (-1.77, -1.73, -0.025, 0.025),
}

JULIA_PRESETS = {
    "douady-rabbit":  -0.123 + 0.745j,
    "san-marco":      -0.75 + 0.1j,
    "siegel-disk":    -0.391 - 0.587j,
    "dentrite":       0.0 + 1.0j,
    "airplane":       -1.755 + 0.0j,
    "basilica":       -1.0 + 0.0j,
}


# ── Watermark ──────────────────────────────────────────────────────────────

def _watermark(img: Image.Image, text: str) -> Image.Image:
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except OSError:
        font = ImageFont.load_default()
    draw.text((8, img.height - 22), text, fill=(200, 200, 200, 180), font=font)
    return img


# ── Single-frame renders ───────────────────────────────────────────────────

def render_mandelbrot(width=800, height=600, preset="classic",
                      palette="inferno", max_iter=256,
                      x_min=None, x_max=None, y_min=None, y_max=None) -> Image.Image:
    if x_min is None:
        x_min, x_max, y_min, y_max = MANDELBROT_PRESETS.get(preset, MANDELBROT_PRESETS["classic"])
    data = mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter)
    img = colorize(data, palette, max_iter)
    return _watermark(img, f"Mandelbrot · {preset} · {palette}")


def render_julia(width=800, height=800, preset="douady-rabbit",
                 palette="midnight", max_iter=256, c=None) -> Image.Image:
    if c is None:
        c = JULIA_PRESETS.get(preset, JULIA_PRESETS["douady-rabbit"])
    data = julia(width, height, -1.8, 1.8, -1.8, 1.8, max_iter, c)
    img = colorize(data, palette, max_iter)
    return _watermark(img, f"Julia  c={c:.4f}  ·  {palette}")


def render_burning_ship(width=800, height=600, palette="fire",
                        max_iter=200) -> Image.Image:
    data = burning_ship(width, height, -2.5, 1.5, -2.0, 0.5, max_iter)
    img = colorize(data, palette, max_iter)
    return _watermark(img, f"Burning Ship · {palette}")


def render_newton(width=700, height=700, poly="z3-1",
                  max_iter=80) -> Image.Image:
    degrees = {"z3-1": 3, "z4-1": 4, "z6-1": 6}
    n = degrees.get(poly, 3)
    roots_map, speed_map = newton(width, height, -1.5, 1.5, -1.5, 1.5, max_iter, poly)
    img = colorize_newton(roots_map, speed_map, n)
    return _watermark(img, f"Newton  f(z)={poly}  ·  {n} roots")


# ── ASCII preview ──────────────────────────────────────────────────────────

_ASCII_CHARS = " .,:;+*?%S#@"


def ascii_preview(iteration_map: np.ndarray, cols=80, rows=30) -> str:
    """Downsample iteration_map to a monochrome ASCII art preview."""
    # Normalise
    flat = iteration_map.copy()
    inside = flat == 0
    if flat.max() > 0:
        flat = flat / flat.max()
    flat[inside] = 0.0

    # Resize via PIL
    img_arr = (flat * 255).astype(np.uint8)
    img = Image.fromarray(img_arr, "L").resize((cols, rows), Image.LANCZOS)
    pixels = np.array(img)

    lines = []
    for row in pixels:
        chars = [_ASCII_CHARS[int(p / 255 * (len(_ASCII_CHARS) - 1))] for p in row]
        lines.append("".join(chars))
    return "\n".join(lines)


# ── GIF animation ──────────────────────────────────────────────────────────

def animate_julia_orbit(width=480, height=480, frames=48,
                        palette="aurora", max_iter=128,
                        output_path: str = "julia_orbit.gif") -> str:
    """Animate Julia set as c moves around a circle in the complex plane."""
    images = []
    angles = np.linspace(0, 2 * math.pi, frames, endpoint=False)
    # Orbit that produces interesting Julia sets
    radius, cx, cy = 0.7885, 0.0, 0.0

    for angle in angles:
        c = complex(cx + radius * math.cos(angle), cy + radius * math.sin(angle))
        data = julia(width, height, -1.8, 1.8, -1.8, 1.8, max_iter, c)
        img = colorize(data, palette, max_iter)
        images.append(img)

    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        loop=0,
        duration=60,
        optimize=False,
    )
    return output_path


def animate_mandelbrot_zoom(width=480, height=480, frames=40,
                            palette="ocean", max_iter=512,
                            target_x=-0.7452, target_y=0.1130,
                            output_path: str = "mandelbrot_zoom.gif") -> str:
    """Animate a smooth zoom into a Mandelbrot detail region."""
    images = []
    zoom_levels = np.geomspace(1.5, 0.0004, frames)

    for zoom in zoom_levels:
        x_min = target_x - zoom
        x_max = target_x + zoom
        aspect = height / width
        y_min = target_y - zoom * aspect
        y_max = target_y + zoom * aspect
        data = mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter)
        img = colorize(data, palette, max_iter)
        images.append(img)

    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        loop=0,
        duration=80,
        optimize=False,
    )
    return output_path


def animate_palette_cycle(fractal_type="mandelbrot", width=480, height=480,
                          max_iter=256, output_path="palette_cycle.gif") -> str:
    """Cycle through all palettes on a single fractal render."""
    palette_names = list(PALETTES.keys())
    images = []

    for pal in palette_names:
        if fractal_type == "julia":
            data = julia(width, height, -1.8, 1.8, -1.8, 1.8, max_iter,
                         JULIA_PRESETS["douady-rabbit"])
        else:
            x_min, x_max, y_min, y_max = MANDELBROT_PRESETS["classic"]
            data = mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter)
        img = colorize(data, pal, max_iter)
        # Show palette name
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        except OSError:
            font = ImageFont.load_default()
        draw.text((12, 12), pal.upper(), fill=(255, 255, 255), font=font)
        images.append(img)
        # Hold each frame for 0.8 s
        for _ in range(7):
            images.append(img)

    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        loop=0,
        duration=100,
        optimize=False,
    )
    return output_path
