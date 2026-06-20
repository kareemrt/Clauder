"""Renders turtle line segments to a standalone SVG document."""

from .turtle import Segment


def segments_to_svg(
    segments: list[Segment],
    *,
    width: int = 600,
    padding: float = 10.0,
    stroke: str = "#0b6e4f",
    stroke_width: float = 1.4,
    background: str = "#ffffff",
) -> str:
    """Fit `segments` into a `width`-px-wide SVG, preserving aspect ratio.

    The turtle's coordinate system has +y "up"; SVG has +y "down", so the
    y-axis is flipped here to render right-side up.
    """
    if not segments:
        raise ValueError("cannot render an empty set of segments")

    xs = [c for seg in segments for c in (seg.x1, seg.x2)]
    ys = [c for seg in segments for c in (seg.y1, seg.y2)]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    span_x = max(max_x - min_x, 1e-9)
    span_y = max(max_y - min_y, 1e-9)

    drawable_w = width - 2 * padding
    scale = drawable_w / span_x
    height = span_y * scale + 2 * padding

    def transform(x: float, y: float) -> tuple[float, float]:
        sx = (x - min_x) * scale + padding
        sy = (max_y - y) * scale + padding  # flip y
        return sx, sy

    lines = []
    for seg in segments:
        x1, y1 = transform(seg.x1, seg.y1)
        x2, y2 = transform(seg.x2, seg.y2)
        lines.append(
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" />'
        )

    body = "\n  ".join(lines)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" '
        f'height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}">\n'
        f'  <rect width="100%" height="100%" fill="{background}" />\n'
        f'  <g fill="none" stroke="{stroke}" stroke-width="{stroke_width}" '
        f'stroke-linecap="round">\n  {body}\n  </g>\n'
        f"</svg>\n"
    )
