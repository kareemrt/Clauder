"""
Terminal and image rendering for fractal data.

Terminal rendering uses Unicode half-block characters (▀) so each terminal
cell represents TWO pixel rows, effectively doubling vertical resolution.
"""

import math
import os
from typing import Optional, Callable, Tuple

import numpy as np
from rich.console import Console
from rich.text import Text

from .palettes import PALETTES, RGB

# Half-block trick: ▀ with fg=top-row color, bg=bottom-row color
HALF_BLOCK = "▀"


def _normalize(data: np.ndarray, max_iter: int) -> np.ndarray:
    """Map iteration counts to [0, 1]. Interior (== max_iter) maps to 1.0."""
    interior = data >= max_iter
    exterior = ~interior
    norm = np.zeros_like(data, dtype=float)
    if exterior.any():
        vals = data[exterior]
        # Cyclic coloring — wrap every 64 iterations so detail stays visible
        norm[exterior] = (vals % 64.0) / 64.0
    norm[interior] = 1.0
    return norm


def render_terminal(
    data: np.ndarray,
    max_iter: int,
    palette: str = "classic",
    console: Optional[Console] = None,
) -> None:
    """Render a fractal array to the terminal using Rich colored half-blocks."""
    if console is None:
        console = Console()

    color_fn: Callable[[float], RGB] = PALETTES.get(palette, PALETTES["classic"])
    norm = _normalize(data, max_iter)
    height, width = norm.shape

    # Process pairs of rows at a time
    for row in range(0, height - 1, 2):
        line = Text()
        for col in range(width):
            top_t = norm[row, col]
            bot_t = norm[row + 1, col]
            tr, tg, tb = color_fn(top_t)
            br, bg, bb = color_fn(bot_t)
            fg = f"rgb({tr},{tg},{tb})"
            bg_color = f"rgb({br},{bg},{bb})"
            line.append(HALF_BLOCK, style=f"{fg} on {bg_color}")
        console.print(line, end="\n", highlight=False)


def render_to_image(
    data: np.ndarray,
    max_iter: int,
    palette: str = "classic",
    output_path: str = "fractal.png",
    scale: int = 1,
) -> str:
    """Save a fractal array as a PNG image. Returns the output path."""
    try:
        from PIL import Image
    except ImportError:
        raise RuntimeError("Pillow is required for image export: pip install Pillow")

    color_fn: Callable[[float], RGB] = PALETTES.get(palette, PALETTES["classic"])
    norm = _normalize(data, max_iter)
    height, width = norm.shape

    pixels = np.zeros((height, width, 3), dtype=np.uint8)
    for r in range(height):
        for c in range(width):
            pixels[r, c] = color_fn(norm[r, c])

    img = Image.fromarray(pixels, "RGB")
    if scale > 1:
        img = img.resize((width * scale, height * scale), Image.NEAREST)
    img.save(output_path)
    return output_path


def render_ascii(
    data: np.ndarray,
    max_iter: int,
    invert: bool = False,
) -> str:
    """Return a plain ASCII string for environments without color support."""
    chars = " .,:;i1tfLCG08@#"
    if invert:
        chars = chars[::-1]
    norm = _normalize(data, max_iter)
    lines = []
    for row in norm:
        line = "".join(chars[int(v * (len(chars) - 1))] for v in row)
        lines.append(line)
    return "\n".join(lines)


def render_info_panel(
    console: Console,
    fractal: str,
    palette: str,
    bounds: Tuple[float, float, float, float],
    max_iter: int,
    width: int,
    height: int,
    extra: Optional[dict] = None,
) -> None:
    """Print a styled info panel below the fractal."""
    from rich.panel import Panel
    from rich.table import Table

    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold cyan")
    table.add_column(style="white")

    table.add_row("Fractal", fractal.upper())
    table.add_row("Palette", palette)
    table.add_row("Bounds", f"x=[{bounds[0]:.6f}, {bounds[1]:.6f}]  y=[{bounds[2]:.6f}, {bounds[3]:.6f}]")
    table.add_row("Max Iterations", str(max_iter))
    table.add_row("Resolution", f"{width} × {height} cells  ({width} × {height * 2} pixels)")
    if extra:
        for k, v in extra.items():
            table.add_row(k, str(v))

    console.print(Panel(table, title="[bold magenta]✦ Fractal Universe[/bold magenta]", border_style="magenta"))
