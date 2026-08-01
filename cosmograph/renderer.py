"""
Rendering engine for Cosmograph.
Handles PNG output (via Pillow) and terminal preview (via rich).
"""

import math
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def save_png(img_array: np.ndarray, output_path: str | Path,
             title: str = "", subtitle: str = "",
             add_glow: bool = True) -> Path:
    """
    Save a numpy RGB array as a PNG with optional title overlay and glow effect.
    """
    output_path = Path(output_path)
    h, w = img_array.shape[:2]

    img = Image.fromarray(img_array.astype(np.uint8), mode="RGB")

    if add_glow:
        # Soft glow: blend a blurred version back in
        blurred = img.filter(ImageFilter.GaussianBlur(radius=3))
        img = Image.blend(img, blurred, alpha=0.15)

    if title:
        # Add a subtle title in the bottom-left corner
        draw = ImageDraw.Draw(img)
        font_size = max(12, h // 40)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                                            max(10, font_size - 4))
        except OSError:
            font = ImageFont.load_default()
            small_font = font

        margin = font_size
        # Shadow
        draw.text((margin + 1, h - margin * 2 - font_size + 1), title, fill=(0, 0, 0, 180), font=font)
        draw.text((margin, h - margin * 2 - font_size), title, fill=(220, 220, 220), font=font)
        if subtitle:
            draw.text((margin + 1, h - margin + 1), subtitle, fill=(0, 0, 0, 180), font=small_font)
            draw.text((margin, h - margin), subtitle, fill=(160, 160, 160), font=small_font)

    img.save(output_path, format="PNG", optimize=True)
    return output_path


def render_fractal(iteration_map: np.ndarray, max_iter: float,
                   output_path: str | Path, theme_name: str = "cosmic",
                   title: str = "", subtitle: str = "",
                   width: int = 1200, height: int = 900) -> Path:
    """Full pipeline: iteration map → themed colors → PNG."""
    from themes import apply_theme
    img_array = apply_theme(iteration_map, max_iter, theme_name)
    return save_png(img_array, output_path, title=title, subtitle=subtitle)


def render_ulam(grid: np.ndarray, output_path: str | Path,
                theme_name: str = "cosmic", dot_scale: float = 1.0) -> Path:
    """Render an Ulam spiral grid to PNG."""
    from themes import THEMES, apply_binary_theme
    h, w = grid.shape
    cell = max(1, int(4 * dot_scale))
    img_h, img_w = h * cell, w * cell

    img = Image.new("RGB", (img_w, img_h), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    fn = THEMES.get(theme_name, THEMES["cosmic"])
    ys, xs = np.where(grid == 1)
    for y, x in zip(ys, xs):
        t = math.sqrt((x - w // 2) ** 2 + (y - h // 2) ** 2) / (min(w, h) / 2)
        t = math.pow(min(t, 1.0), 0.5)
        color = fn(t)
        px0, py0 = x * cell, y * cell
        draw.ellipse([px0, py0, px0 + cell - 1, py0 + cell - 1], fill=color)

    arr = np.array(img)
    return save_png(arr, output_path,
                    title="Ulam Spiral",
                    subtitle="Primes plotted in a clockwise spiral")


def render_sunflower(seeds: list, canvas_size: int, output_path: str | Path,
                     theme_name: str = "gold") -> Path:
    """Render the Fibonacci sunflower pattern to PNG."""
    from themes import THEMES
    fn = THEMES.get(theme_name, THEMES["gold"])
    img = Image.new("RGB", (canvas_size, canvas_size), (3, 6, 0))
    draw = ImageDraw.Draw(img)

    n = len(seeds)
    for x, y, r, i in seeds:
        t = math.pow(i / n, 0.7)
        color = fn(t)
        r_draw = max(0.5, r)
        draw.ellipse([x - r_draw, y - r_draw, x + r_draw, y + r_draw], fill=color)

    arr = np.array(img)
    return save_png(arr, output_path,
                    title="Fibonacci Sunflower",
                    subtitle=f"Golden angle φ ≈ 137.508° · {n} seeds")


def render_lissajous(x_arr: np.ndarray, y_arr: np.ndarray,
                     output_path: str | Path, a: int = 3, b: int = 4,
                     delta: float = math.pi / 4, theme_name: str = "neon",
                     canvas: int = 900) -> Path:
    """Render a Lissajous figure as a luminous trail."""
    from themes import THEMES
    fn = THEMES.get(theme_name, THEMES["neon"])
    img = Image.new("RGB", (canvas, canvas), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    n = len(x_arr)

    # Draw as colored polyline segments
    for i in range(n - 1):
        t = i / n
        color = fn(t)
        x0 = int(x_arr[i] * (canvas - 20) + 10)
        y0 = int(y_arr[i] * (canvas - 20) + 10)
        x1 = int(x_arr[i + 1] * (canvas - 20) + 10)
        y1 = int(y_arr[i + 1] * (canvas - 20) + 10)
        draw.line([x0, y0, x1, y1], fill=color, width=2)

    # Second pass — slightly blurred bright core for glow effect
    core = img.copy()
    bright = core.filter(ImageFilter.GaussianBlur(radius=2))
    img = Image.blend(img, bright, alpha=0.4)

    arr = np.array(img)
    return save_png(arr, output_path,
                    title=f"Lissajous Figure  a={a}, b={b}",
                    subtitle=f"x=sin({a}t+δ)  y=sin({b}t)  δ=π/{round(math.pi/delta) if delta else 0}",
                    add_glow=False)


def render_dragon(vertices: list, output_path: str | Path,
                  theme_name: str = "inferno", canvas: int = 1000) -> Path:
    """Render the Dragon Curve fractal."""
    from themes import THEMES
    fn = THEMES.get(theme_name, THEMES["inferno"])

    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    padding = canvas * 0.05
    x_range = x_max - x_min or 1
    y_range = y_max - y_min or 1
    scale = (canvas - 2 * padding) / max(x_range, y_range)

    def to_px(x, y):
        px = int((x - x_min) * scale + padding + (canvas - 2 * padding - x_range * scale) / 2)
        py = int((y - y_min) * scale + padding + (canvas - 2 * padding - y_range * scale) / 2)
        return px, py

    img = Image.new("RGB", (canvas, canvas), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    n = len(vertices)

    for i in range(n - 1):
        t = i / n
        color = fn(t)
        p0 = to_px(*vertices[i])
        p1 = to_px(*vertices[i + 1])
        draw.line([p0, p1], fill=color, width=1)

    blurred = img.filter(ImageFilter.GaussianBlur(radius=1))
    img = Image.blend(img, blurred, alpha=0.3)

    arr = np.array(img)
    return save_png(arr, output_path,
                    title="Dragon Curve",
                    subtitle="Paper-fold fractal, 14 iterations")


def terminal_preview(img_array: np.ndarray, width: int = 60, height: int = 30) -> None:
    """Render a tiny terminal preview of an image using Unicode half-blocks."""
    h, w = img_array.shape[:2]
    step_x = max(1, w // width)
    step_y = max(1, h // (height * 2))  # 2 rows per terminal row with half-blocks

    text = Text()
    for row in range(0, min(h - step_y, height * step_y * 2), step_y * 2):
        for col in range(0, min(w - step_x, width * step_x), step_x):
            r_top, g_top, b_top = img_array[row, col]
            r_bot = g_bot = b_bot = 0
            if row + step_y < h:
                r_bot, g_bot, b_bot = img_array[row + step_y, col]
            # Upper half block ▀: fg = top pixel, bg = bottom pixel
            text.append("▀",
                style=f"rgb({r_top},{g_top},{b_top}) on rgb({r_bot},{g_bot},{b_bot})")
        text.append("\n")

    console.print(text)
