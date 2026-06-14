"""Render turtle :class:`~fractal_garden.turtle.Segment` lists to SVG."""

from __future__ import annotations

import math
from typing import Iterable, Literal

from . import palette as palette_mod
from .turtle import Segment

ColorBy = Literal["auto", "depth", "position", "solid"]


def _default_base_width(min_x: float, min_y: float, max_x: float, max_y: float) -> float:
    """Pick a stroke width proportional to the drawing's size.

    Dense, high-iteration curves end up with thousands of short segments
    packed into a small area; a fixed stroke width would turn them into a
    solid blob. Scaling the stroke to the bounding-box diagonal keeps
    individual strokes visible regardless of how detailed the L-system is.
    """
    diag = math.hypot(max_x - min_x, max_y - min_y)
    return max(0.4, min(4.0, diag / 220))


def _bbox(segments: Iterable[Segment]) -> tuple[float, float, float, float]:
    xs: list[float] = []
    ys: list[float] = []
    for seg in segments:
        xs.extend((seg.x1, seg.x2))
        ys.extend((seg.y1, seg.y2))
    if not xs:
        raise ValueError("no segments to measure")
    return min(xs), min(ys), max(xs), max(ys)


def _segment_lines(
    segments: list[Segment],
    *,
    palette: tuple[str, str],
    base_width: float,
    width_falloff: float,
    color_by: ColorBy,
    offset_x: float,
    offset_y: float,
) -> str:
    base, accent = palette
    max_depth = max((seg.depth for seg in segments), default=0)
    resolved = "depth" if (color_by == "auto" and max_depth) else "position" if color_by == "auto" else color_by

    count = len(segments)
    lines = []
    for i, seg in enumerate(segments):
        if resolved == "depth" and max_depth:
            t = seg.depth / max_depth
        elif resolved == "position":
            t = i / max(count - 1, 1)
        else:
            t = 0.0
        color = palette_mod.interpolate(base, accent, t)
        width = max(0.4, base_width * (width_falloff**seg.depth))
        lines.append(
            f'<line x1="{seg.x1 - offset_x:.2f}" y1="{seg.y1 - offset_y:.2f}" '
            f'x2="{seg.x2 - offset_x:.2f}" y2="{seg.y2 - offset_y:.2f}" '
            f'stroke="{color}" stroke-width="{width:.2f}" stroke-linecap="round" />'
        )
    return "\n    ".join(lines)


def render_svg(
    segments: list[Segment],
    *,
    palette: tuple[str, str],
    background: str = "#0f1115",
    width_px: int = 900,
    padding: float = 24.0,
    base_width: float | None = None,
    width_falloff: float = 0.85,
    color_by: ColorBy = "auto",
) -> str:
    """Render a single plant/curve to a standalone SVG document."""
    min_x, min_y, max_x, max_y = _bbox(segments)
    w = max(max_x - min_x, 1e-6)
    h = max(max_y - min_y, 1e-6)
    if base_width is None:
        base_width = _default_base_width(min_x, min_y, max_x, max_y)

    body = _segment_lines(
        segments,
        palette=palette,
        base_width=base_width,
        width_falloff=width_falloff,
        color_by=color_by,
        offset_x=min_x,
        offset_y=min_y,
    )

    vb_w = w + 2 * padding
    vb_h = h + 2 * padding
    height_px = max(1, round(width_px * vb_h / vb_w))

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="{-padding:.2f} {-padding:.2f} {vb_w:.2f} {vb_h:.2f}" '
        f'width="{width_px}" height="{height_px}">\n'
        f'  <rect x="{-padding:.2f}" y="{-padding:.2f}" width="{vb_w:.2f}" height="{vb_h:.2f}" fill="{background}" />\n'
        f'  <g transform="translate(0 {h:.2f}) scale(1 -1)">\n'
        f"    {body}\n"
        f"  </g>\n"
        f"</svg>\n"
    )


class GardenPlant:
    """A grown plant ready to be placed inside a :func:`render_garden` scene."""

    __slots__ = ("segments", "palette", "color_by")

    def __init__(self, segments: list[Segment], palette: tuple[str, str], color_by: ColorBy = "auto"):
        self.segments = segments
        self.palette = palette
        self.color_by = color_by


def render_garden(
    plants: list[GardenPlant],
    *,
    background: str = "#0f1115",
    ground_color: str = "#23262e",
    width_px: int = 1600,
    padding: float = 30.0,
    gap: float = 24.0,
    plant_height: float = 320.0,
    ground_height: float = 18.0,
    base_width: float | None = None,
    width_falloff: float = 0.85,
) -> str:
    """Render multiple plants side-by-side on a shared ground line."""
    if not plants:
        raise ValueError("no plants to render")

    groups: list[str] = []
    cursor_x = 0.0
    max_scaled_w = 0.0

    for plant in plants:
        min_x, min_y, max_x, max_y = _bbox(plant.segments)
        w = max(max_x - min_x, 1e-6)
        h = max(max_y - min_y, 1e-6)
        scale = plant_height / h
        scaled_w = w * scale
        plant_base_width = base_width if base_width is not None else _default_base_width(min_x, min_y, max_x, max_y)

        body = _segment_lines(
            plant.segments,
            palette=plant.palette,
            base_width=plant_base_width,
            width_falloff=width_falloff,
            color_by=plant.color_by,
            offset_x=min_x,
            offset_y=min_y,
        )
        # Place the plant's bottom-center on the ground line at cursor_x + scaled_w / 2.
        tx = cursor_x + scaled_w / 2
        groups.append(
            f'  <g transform="translate({tx:.2f} 0) scale({scale:.4f} -{scale:.4f}) '
            f'translate({-w / 2:.2f} 0)">\n    {body}\n  </g>'
        )
        cursor_x += scaled_w + gap
        max_scaled_w = max(max_scaled_w, scaled_w)

    total_w = max(cursor_x - gap, 0.0)
    vb_w = total_w + 2 * padding
    vb_h = plant_height + ground_height + 2 * padding
    height_px = max(1, round(width_px * vb_h / vb_w))

    body_groups = "\n".join(groups)
    min_y = -(plant_height + padding)

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="{-padding:.2f} {min_y:.2f} {vb_w:.2f} {vb_h:.2f}" '
        f'width="{width_px}" height="{height_px}">\n'
        f'  <rect x="{-padding:.2f}" y="{min_y:.2f}" width="{vb_w:.2f}" height="{vb_h:.2f}" fill="{background}" />\n'
        f'  <rect x="{-padding:.2f}" y="0" width="{vb_w:.2f}" height="{ground_height:.2f}" fill="{ground_color}" />\n'
        f"{body_groups}\n"
        f"</svg>\n"
    )
