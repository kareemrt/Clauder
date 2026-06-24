"""Render turtle segments to a depth-gradient SVG, using only the stdlib."""

from __future__ import annotations

from .turtle import Segment, bounding_box

RGB = tuple[int, int, int]


def _hex_to_rgb(value: str) -> RGB:
    value = value.lstrip("#")
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def _rgb_to_hex(rgb: RGB) -> str:
    r, g, b = rgb
    return f"#{r:02x}{g:02x}{b:02x}"


def _lerp_color(start: RGB, end: RGB, t: float) -> RGB:
    return tuple(round(s + (e - s) * t) for s, e in zip(start, end))  # type: ignore[return-value]


def render(
    segments: list[Segment],
    *,
    width: int = 800,
    height: int = 800,
    padding: int = 24,
    background: str = "#0d1117",
    start_color: str = "#7ee787",
    end_color: str = "#58a6ff",
    stroke_width: float = 1.6,
) -> str:
    """Project segments into an SVG canvas, coloring each by its branch depth."""
    if not segments:
        raise ValueError("cannot render zero segments")

    min_x, min_y, max_x, max_y = bounding_box(segments)
    span_x = max(max_x - min_x, 1e-9)
    span_y = max(max_y - min_y, 1e-9)
    scale = min((width - 2 * padding) / span_x, (height - 2 * padding) / span_y)

    def project(x: float, y: float) -> tuple[float, float]:
        px = (x - min_x) * scale + padding
        py = height - ((y - min_y) * scale + padding)  # flip: SVG y grows downward
        return px, py

    max_depth = max((s.depth for s in segments), default=0) or 1
    rgb_start, rgb_end = _hex_to_rgb(start_color), _hex_to_rgb(end_color)

    lines = []
    for s in segments:
        x1, y1 = project(s.x1, s.y1)
        x2, y2 = project(s.x2, s.y2)
        color = _rgb_to_hex(_lerp_color(rgb_start, rgb_end, s.depth / max_depth))
        lines.append(
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" />'
        )

    body = "\n  ".join(lines)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">\n'
        f'  <rect width="100%" height="100%" fill="{background}" />\n'
        f"  {body}\n"
        f"</svg>\n"
    )
