"""Render turtle segments to a self-contained SVG document.

No imaging libraries are required — SVG is just XML, and GitHub (along
with virtually every browser) renders it natively, which makes it an
ideal zero-dependency output format for a tool that wants its README to
show real, regenerable artwork.
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

from .turtle import Segment, bounds

Color = Tuple[int, int, int]


def _hex_to_rgb(value: str) -> Color:
    value = value.lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _lerp(a: Color, b: Color, t: float) -> Color:
    t = max(0.0, min(1.0, t))
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))  # type: ignore[return-value]


def _to_hex(color: Color) -> str:
    return "#{:02x}{:02x}{:02x}".format(*color)


def gradient(
    depth: int, max_depth: int, start: str = "#5d4037", end: str = "#a5d6a7"
) -> str:
    """Map a branch ``depth`` to a color between trunk ``start`` and tip ``end``.

    Shallow segments (the trunk) are colored ``start`` and the deepest
    twigs fade toward ``end`` — by default a bark-brown to leaf-green
    gradient, evoking how real plants darken near their base.
    """

    if max_depth <= 0:
        return start
    t = depth / max_depth
    return _to_hex(_lerp(_hex_to_rgb(start), _hex_to_rgb(end), t))


def render_svg(
    segments: Sequence[Segment],
    *,
    background: str = "#0b1020",
    trunk_color: str = "#5d4037",
    tip_color: str = "#a5d6a7",
    stroke_width: float = 1.4,
    taper: bool = True,
    padding: float = 12.0,
    title: str = "L-System Garden",
) -> str:
    """Build an SVG document string from a sequence of :class:`Segment`.

    Args:
        segments: Output of :func:`lsystem_garden.turtle.walk`.
        background: Canvas background color (any CSS color string).
        trunk_color: Color used for the shallowest (depth 0) segments.
        tip_color: Color used for the deepest segments.
        stroke_width: Base line width for depth-0 segments.
        taper: If true, deeper (more nested) segments are drawn thinner,
            mimicking how branches narrow toward their tips.
        padding: Margin, in user units, added around the drawing's bounds.
        title: Embedded ``<title>`` element, shown as alt text/tooltip.
    """

    if not segments:
        raise ValueError("cannot render an empty drawing — check the L-system rules")

    min_x, min_y, max_x, max_y = bounds(segments)
    width = (max_x - min_x) + 2 * padding
    height = (max_y - min_y) + 2 * padding
    max_depth = max(seg.depth for seg in segments)

    lines: List[str] = []
    lines.append(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.2f} {height:.2f}" '
        f'width="{width:.0f}" height="{height:.0f}" role="img" aria-label="{title}">'
    )
    lines.append(f"  <title>{title}</title>")
    lines.append(f'  <rect x="0" y="0" width="{width:.2f}" height="{height:.2f}" fill="{background}"/>')
    lines.append(f'  <g stroke-linecap="round" fill="none">')

    for seg in segments:
        x1 = seg.x1 - min_x + padding
        y1 = seg.y1 - min_y + padding
        x2 = seg.x2 - min_x + padding
        y2 = seg.y2 - min_y + padding
        color = gradient(seg.depth, max_depth, trunk_color, tip_color)
        width_here = stroke_width
        if taper and max_depth > 0:
            width_here = max(0.35, stroke_width * (1.0 - 0.6 * seg.depth / max_depth))
        lines.append(
            f'    <line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            f'stroke="{color}" stroke-width="{width_here:.2f}"/>'
        )

    lines.append("  </g>")
    lines.append("</svg>\n")
    return "\n".join(lines)
