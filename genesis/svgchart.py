"""Minimal pure-stdlib SVG rendering: no matplotlib, no pillow, no deps.

Two outputs are produced for the README:
  * a multi-series line chart (population & trait evolution over time)
  * a snapshot of the world grid (food + organisms, colored by genome)
"""

from __future__ import annotations

from xml.sax.saxutils import escape

from genesis.organism import Organism
from genesis.world import World

PALETTE = ["#e63946", "#2a9d8f", "#457b9d", "#f4a261", "#8338ec"]


def line_chart(
    series: dict[str, list[float]],
    *,
    width: int = 760,
    height: int = 340,
    title: str = "",
    x_label: str = "tick",
) -> str:
    pad_left, pad_right, pad_top, pad_bottom = 60, 20, 40, 40
    plot_w = width - pad_left - pad_right
    plot_h = height - pad_top - pad_bottom

    all_values = [v for values in series.values() for v in values]
    n = max((len(v) for v in series.values()), default=0)
    y_min, y_max = (min(all_values), max(all_values)) if all_values else (0, 1)
    if y_max == y_min:
        y_max += 1
    y_pad = (y_max - y_min) * 0.08
    y_min, y_max = y_min - y_pad, y_max + y_pad

    def sx(i: int) -> float:
        return pad_left + (i / max(n - 1, 1)) * plot_w

    def sy(v: float) -> float:
        return pad_top + plot_h - ((v - y_min) / (y_max - y_min)) * plot_h

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="monospace" font-size="12">',
        f'<rect width="{width}" height="{height}" fill="#0d1117"/>',
        f'<text x="{width / 2}" y="22" fill="#e6edf3" font-size="15" text-anchor="middle">{escape(title)}</text>',
    ]

    # gridlines + y-axis labels
    for i in range(5):
        gy = pad_top + plot_h * i / 4
        value = y_max - (y_max - y_min) * i / 4
        parts.append(f'<line x1="{pad_left}" y1="{gy:.1f}" x2="{width - pad_right}" y2="{gy:.1f}" '
                      f'stroke="#30363d" stroke-width="1"/>')
        parts.append(f'<text x="{pad_left - 8}" y="{gy + 4:.1f}" fill="#8b949e" text-anchor="end">{value:.1f}</text>')

    parts.append(f'<text x="{width / 2}" y="{height - 8}" fill="#8b949e" text-anchor="middle">{escape(x_label)}</text>')

    for idx, (name, values) in enumerate(series.items()):
        color = PALETTE[idx % len(PALETTE)]
        points = " ".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in enumerate(values))
        parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2"/>')
        legend_y = pad_top + idx * 16
        parts.append(f'<rect x="{width - pad_right - 110}" y="{legend_y:.1f}" width="10" height="10" fill="{color}"/>')
        parts.append(f'<text x="{width - pad_right - 95}" y="{legend_y + 9:.1f}" fill="#e6edf3">{escape(name)}</text>')

    parts.append("</svg>")
    return "\n".join(parts)


def world_snapshot(world: World, *, cell: int = 8) -> str:
    width_px = world.width * cell
    height_px = world.height * cell

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width_px}" height="{height_px}" '
        f'viewBox="0 0 {width_px} {height_px}">',
        f'<rect width="{width_px}" height="{height_px}" fill="#0d1117"/>',
    ]

    for fx, fy in world.food:
        cx, cy = fx * cell + cell / 2, fy * cell + cell / 2
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{cell * 0.18:.1f}" fill="#2a9d8f"/>')

    for org in world.organisms():
        parts.append(_organism_marker(org, cell))

    parts.append("</svg>")
    return "\n".join(parts)


def _hsl_to_hex(h: float, s: float, l: float) -> str:
    """Convert HSL (degrees, 0-100, 0-100) to a #rrggbb string.

    Some SVG consumers (e.g. headless renderers used for thumbnails) don't
    support the CSS hsl() function, so colors are pre-converted to hex.
    """
    h, s, l = h / 360, s / 100, l / 100
    if s == 0:
        r = g = b = l
    else:
        def hue_to_rgb(p: float, q: float, t: float) -> float:
            if t < 0:
                t += 1
            if t > 1:
                t -= 1
            if t < 1 / 6:
                return p + (q - p) * 6 * t
            if t < 1 / 2:
                return q
            if t < 2 / 3:
                return p + (q - p) * (2 / 3 - t) * 6
            return p

        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1 / 3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1 / 3)
    return "#{:02x}{:02x}{:02x}".format(round(r * 255), round(g * 255), round(b * 255))


def _organism_marker(org: Organism, cell: int) -> str:
    g = org.genome
    hue = (g.vision / 8) * 270  # blue (low vision) -> red (high vision)
    sat = 55 + 15 * (g.speed - 1)
    color = _hsl_to_hex(hue, sat, 55)
    cx, cy = org.x * cell + cell / 2, org.y * cell + cell / 2
    r = cell * 0.32 * (0.7 + 0.15 * g.speed)
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{color}" stroke="#0d1117" stroke-width="0.5"/>'
