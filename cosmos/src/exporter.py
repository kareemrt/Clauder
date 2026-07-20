"""
SVG exporter for Cosmos.
Generates a beautiful SVG snapshot of the solar system.
"""

import math
from datetime import datetime, timezone

from .orbital import PLANETS, SUN, get_all_positions, days_since_j2000

SVG_W = 900
SVG_H = 900
VIEW_AU = 32.5

SVG_PLANET_COLORS = {
    "Sun":     "#FFD700",
    "Mercury": "#B5B5B5",
    "Venus":   "#E8C97A",
    "Earth":   "#4B9CD3",
    "Mars":    "#C1440E",
    "Jupiter": "#C88B3A",
    "Saturn":  "#EAD5A4",
    "Uranus":  "#7DE8E8",
    "Neptune": "#3F54BA",
}

SVG_PLANET_RADII = {
    "Sun":     22,
    "Mercury":  5,
    "Venus":    8,
    "Earth":    8,
    "Mars":     7,
    "Jupiter": 14,
    "Saturn":  12,
    "Uranus":  10,
    "Neptune": 10,
}

GLOW_COLORS = {
    "Sun":     "#FFE87C",
    "Earth":   "#7EB8F7",
    "Jupiter": "#D4A96A",
    "Saturn":  "#EDD78A",
    "Uranus":  "#A8F0F0",
    "Neptune": "#6B8FE0",
}


def au_to_svg(x_au: float, y_au: float) -> tuple[float, float]:
    cx, cy = SVG_W / 2, SVG_H / 2
    scale = (SVG_W * 0.44) / VIEW_AU
    sx = cx + x_au * scale
    sy = cy - y_au * scale
    return sx, sy


def svg_orbit(planet) -> str:
    a = planet.semi_major_au
    e = planet.eccentricity
    b = a * math.sqrt(1 - e * e)
    cx, cy = SVG_W / 2, SVG_H / 2
    scale = (SVG_W * 0.44) / VIEW_AU
    rx = a * scale
    ry = b * scale
    # Ellipse center offset from Sun (focus)
    offset = a * e * scale
    color = SVG_PLANET_COLORS.get(planet.name, "#888888")
    return (
        f'<ellipse cx="{cx - offset:.2f}" cy="{cy:.2f}" '
        f'rx="{rx:.2f}" ry="{ry:.2f}" '
        f'fill="none" stroke="{color}" stroke-opacity="0.25" stroke-width="0.8"/>'
    )


def star_field_svg(count: int = 300, seed: int = 42) -> list[str]:
    import random
    rng = random.Random(seed)
    elems = []
    for _ in range(count):
        x = rng.uniform(0, SVG_W)
        y = rng.uniform(0, SVG_H)
        r = rng.uniform(0.4, 1.8)
        op = rng.uniform(0.3, 1.0)
        elems.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" '
            f'fill="white" opacity="{op:.2f}"/>'
        )
    return elems


def export_svg(dt: datetime | None = None, path: str = "cosmos.svg") -> str:
    if dt is None:
        dt = datetime.now(timezone.utc)

    positions = get_all_positions(dt)
    jd = days_since_j2000(dt)

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{SVG_W}" height="{SVG_H}" '
        f'style="background:#050A14">'
    )

    # Defs (radial gradients, glow filters)
    parts.append("<defs>")
    parts.append("""
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="4" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="sunglow" x="-100%" y="-100%" width="300%" height="300%">
    <feGaussianBlur stdDeviation="12" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
""")
    for name, color in SVG_PLANET_COLORS.items():
        parts.append(
            f'  <radialGradient id="grad_{name}" cx="35%" cy="35%" r="65%">'
            f'<stop offset="0%" stop-color="white" stop-opacity="0.8"/>'
            f'<stop offset="100%" stop-color="{color}"/>'
            f'</radialGradient>'
        )
    parts.append("</defs>")

    # Stars
    parts.extend(star_field_svg(350))

    # Grid rings (subtle AU rings)
    cx, cy = SVG_W / 2, SVG_H / 2
    scale = (SVG_W * 0.44) / VIEW_AU
    for au_r in [5, 10, 15, 20, 25, 30]:
        r = au_r * scale
        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" '
            f'fill="none" stroke="#1a2a4a" stroke-width="0.5" stroke-dasharray="4,8"/>'
        )
        parts.append(
            f'<text x="{cx + r + 3:.1f}" y="{cy:.1f}" fill="#1a3a6a" '
            f'font-size="9" font-family="monospace">{au_r} AU</text>'
        )

    # Orbits
    for p in PLANETS:
        if p.semi_major_au <= VIEW_AU:
            parts.append(svg_orbit(p))

    # Celestial bodies
    all_bodies_info = [
        (SUN, positions.get("Sun", (0, 0))),
    ] + [(p, positions.get(p.name, (0, 0))) for p in PLANETS]

    for body, (x_au, y_au) in all_bodies_info:
        if abs(x_au) > VIEW_AU * 1.1 or abs(y_au) > VIEW_AU * 1.1:
            continue
        sx, sy = au_to_svg(x_au, y_au)
        r = SVG_PLANET_RADII.get(body.name, 7)
        color = SVG_PLANET_COLORS.get(body.name, "#FFFFFF")
        grad_id = f"grad_{body.name}"
        filt = 'filter="url(#sunglow)"' if body.name == "Sun" else (
            'filter="url(#glow)"' if body.name in GLOW_COLORS else ""
        )

        # Saturn rings
        if body.name == "Saturn":
            rr = r * 2.2
            parts.append(
                f'<ellipse cx="{sx:.1f}" cy="{sy:.1f}" '
                f'rx="{rr:.1f}" ry="{rr*0.3:.1f}" '
                f'fill="none" stroke="#D4C090" stroke-width="3" opacity="0.5"/>'
            )

        parts.append(
            f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{r}" '
            f'fill="url(#{grad_id})" {filt}/>'
        )

        # Labels
        if body.name != "Sun":
            parts.append(
                f'<text x="{sx + r + 4:.1f}" y="{sy + 4:.1f}" '
                f'fill="{color}" fill-opacity="0.85" font-size="11" '
                f'font-family="monospace">{body.name}</text>'
            )

    # Title
    title_text = f"COSMOS — {dt.strftime('%Y-%m-%d %H:%M UTC')}"
    parts.append(
        f'<text x="10" y="22" fill="#7DB9E8" font-size="14" '
        f'font-family="monospace" font-weight="bold">{title_text}</text>'
    )
    parts.append(
        f'<text x="10" y="38" fill="#3a6a9a" font-size="10" '
        f'font-family="monospace">Keplerian orbits · J2000+{jd:,.0f} days</text>'
    )

    parts.append("</svg>")

    svg_content = "\n".join(parts)
    with open(path, "w") as f:
        f.write(svg_content)
    return path
