"""Turn a `Viewport` + fractal family into a coloured pixel grid / PNG file."""

from __future__ import annotations

from . import palettes
from .fractals import FAMILIES, Viewport, escape_value
from .png import write_png

# Smooth counts are unbounded; this caps how many "bands" map across one
# full palette traversal so colour cycles stay visually consistent across
# zoom levels and iteration limits.
_BAND_PERIOD = 48.0


def render_grid(
    fractal: str,
    viewport: Viewport,
    max_iter: int,
    palette: str,
    julia_c: complex | None = None,
) -> list[list[tuple[int, int, int]]]:
    """Compute the full RGB grid for `viewport` (rows of pixel tuples)."""
    if fractal not in FAMILIES:
        raise ValueError(f"Unknown fractal family: {fractal!r} (expected one of {FAMILIES})")
    if palette not in palettes.PALETTES:
        raise ValueError(f"Unknown palette: {palette!r} (expected one of {palettes.names()})")

    grid: list[list[tuple[int, int, int]]] = []
    for py in range(viewport.height):
        row: list[tuple[int, int, int]] = []
        for px in range(viewport.width):
            point = viewport.to_complex(px, py)
            value = escape_value(fractal, point, max_iter, julia_c)
            if value is None:
                row.append(palettes.INSIDE_COLOUR)
            else:
                t = (value % _BAND_PERIOD) / _BAND_PERIOD
                row.append(palettes.colour_at(palette, t))
        grid.append(row)
    return grid


def render_to_file(
    path: str,
    fractal: str,
    viewport: Viewport,
    max_iter: int,
    palette: str,
    julia_c: complex | None = None,
) -> None:
    """Render `fractal` over `viewport` and write the result to `path` as PNG."""
    grid = render_grid(fractal, viewport, max_iter, palette, julia_c)
    write_png(path, grid)
