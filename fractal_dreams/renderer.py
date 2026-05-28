"""Terminal rendering engine — converts fractal frames to colored ASCII art."""

from __future__ import annotations

from fractal_dreams.palette import Color, RESET, PALETTES

# Ordered from sparse (low iterations = near set) to dense (high iterations = far)
_CHARS_DENSE = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
_CHARS_SIMPLE = " .:-=+*#%@$"
_CHARS_BLOCKS = " ░▒▓█"


def _map_char(smooth: float, max_iter: int, charset: str) -> str:
    if smooth == 0.0:
        return charset[0]  # in-set: use space/lightest char
    t = min(1.0, (smooth % max_iter) / max_iter)
    idx = int(t * (len(charset) - 1))
    return charset[idx]


def render_frame(
    frame: list[list[tuple[float, int]]],
    max_iter: int,
    palette_name: str = "fire",
    charset: str = "dense",
    color: bool = True,
) -> str:
    """
    Render a computed fractal frame to a colored ANSI string.

    Args:
        frame: 2D list of (smooth_value, raw_iter) tuples from compute_frame().
        max_iter: Maximum iteration count used during computation.
        palette_name: Name from PALETTES dict.
        charset: "dense" | "simple" | "blocks"
        color: Whether to emit ANSI color codes.

    Returns:
        Multi-line string ready to print to a terminal.
    """
    palette_fn = PALETTES.get(palette_name, PALETTES["fire"])
    chars = {"dense": _CHARS_DENSE, "simple": _CHARS_SIMPLE, "blocks": _CHARS_BLOCKS}.get(
        charset, _CHARS_DENSE
    )

    lines = []
    for row in frame:
        parts = []
        prev_color: Color | None = None
        for smooth, raw in row:
            ch = _map_char(smooth, max_iter, chars)
            if color:
                c = palette_fn(smooth, max_iter)
                if prev_color is None or (c.r, c.g, c.b) != (prev_color.r, prev_color.g, prev_color.b):
                    parts.append(c.to_ansi_fg())
                    prev_color = c
            parts.append(ch)
        if color:
            parts.append(RESET)
        lines.append("".join(parts))
    return "\n".join(lines)


def render_frame_plain(
    frame: list[list[tuple[float, int]]],
    max_iter: int,
    charset: str = "dense",
) -> str:
    """Render without any ANSI color codes (for saving to file)."""
    chars = {"dense": _CHARS_DENSE, "simple": _CHARS_SIMPLE, "blocks": _CHARS_BLOCKS}.get(
        charset, _CHARS_DENSE
    )
    lines = []
    for row in frame:
        line = "".join(_map_char(smooth, max_iter, chars) for smooth, _ in row)
        lines.append(line)
    return "\n".join(lines)


def render_info_panel(
    name: str,
    fractal_type: str,
    viewport: tuple[float, float, float, float],
    max_iter: int,
    palette_name: str,
    width: int,
    height: int,
) -> str:
    """Render a metadata panel for display alongside the fractal."""
    xmin, xmax, ymin, ymax = viewport
    lines = [
        f"┌{'─' * (width - 2)}┐",
        f"│  {name:<{width - 5}}│",
        f"│  Fractal : {fractal_type:<{width - 15}}│",
        f"│  Palette : {palette_name:<{width - 15}}│",
        f"│  Iter    : {max_iter:<{width - 15}}│",
        f"│  x ∈ [{xmin:+.6f}, {xmax:+.6f}]  y ∈ [{ymin:+.6f}, {ymax:+.6f}]",
        f"│  Size    : {width} × {height} chars{' ' * (width - 28)}│",
        f"└{'─' * (width - 2)}┘",
    ]
    return "\n".join(lines)
