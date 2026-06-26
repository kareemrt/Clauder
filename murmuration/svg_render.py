"""Render flock state to SVG. Pure stdlib, no image libraries required."""

from __future__ import annotations

import math

from .flock import Flock

_BG = "#0b1021"
_PREY_COLOR_SLOW = (90, 200, 255)
_PREY_COLOR_FAST = (255, 120, 220)
_PREDATOR_COLOR = "#ff4d4d"


def _lerp_color(c1, c2, t: float) -> str:
    t = max(0.0, min(1.0, t))
    r = round(c1[0] + (c2[0] - c1[0]) * t)
    g = round(c1[1] + (c2[1] - c1[1]) * t)
    b = round(c1[2] + (c2[2] - c1[2]) * t)
    return f"rgb({r},{g},{b})"


def _boid_triangle(x: float, y: float, heading: float, size: float) -> str:
    tip = (x + size * math.cos(heading), y + size * math.sin(heading))
    left = (
        x + size * 0.5 * math.cos(heading + 2.5),
        y + size * 0.5 * math.sin(heading + 2.5),
    )
    right = (
        x + size * 0.5 * math.cos(heading - 2.5),
        y + size * 0.5 * math.sin(heading - 2.5),
    )
    return f"{tip[0]:.2f},{tip[1]:.2f} {left[0]:.2f},{left[1]:.2f} {right[0]:.2f},{right[1]:.2f}"


def render_snapshot(flock: Flock, scale: float = 8.0) -> str:
    """Render the current flock state as a single static SVG frame."""
    cfg = flock.config
    w, h = cfg.width * scale, cfg.height * scale
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" '
        f'viewBox="0 0 {w:.0f} {h:.0f}">',
        f'<rect width="{w:.0f}" height="{h:.0f}" fill="{_BG}"/>',
    ]
    for boid in flock.prey:
        t = min(boid.speed() / cfg.max_speed, 1.0)
        color = _lerp_color(_PREY_COLOR_SLOW, _PREY_COLOR_FAST, t)
        pts = _boid_triangle(boid.position.x * scale, boid.position.y * scale, boid.heading(), size=scale * 1.1)
        parts.append(f'<polygon points="{pts}" fill="{color}"/>')
    for pred in flock.predators:
        pts = _boid_triangle(pred.position.x * scale, pred.position.y * scale, pred.heading(), size=scale * 1.8)
        parts.append(f'<polygon points="{pts}" fill="{_PREDATOR_COLOR}"/>')
    parts.append("</svg>")
    return "\n".join(parts)


def render_trail(flock: Flock, steps: int, scale: float = 8.0, sample_every: int = 1) -> str:
    """Step the flock forward, recording a fading trail per boid, then
    render one composite SVG: ghost trails plus the final positions.
    """
    cfg = flock.config
    w, h = cfg.width * scale, cfg.height * scale
    history: dict[int, list[tuple[float, float, bool]]] = {id(b): [] for b in flock.boids}

    for step in range(steps):
        if step % sample_every == 0:
            for boid in flock.boids:
                history[id(boid)].append((boid.position.x, boid.position.y, boid.is_predator))
        flock.step()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" '
        f'viewBox="0 0 {w:.0f} {h:.0f}">',
        f'<rect width="{w:.0f}" height="{h:.0f}" fill="{_BG}"/>',
    ]

    for boid in flock.boids:
        points = history[id(boid)]
        if len(points) < 2:
            continue
        color = _PREDATOR_COLOR if boid.is_predator else "#5ac8ff"
        n = len(points)
        # Draw the trail as short fading segments to avoid a single
        # polyline jumping across the toroidal wrap-around edges.
        for i in range(1, n):
            (x0, y0, _), (x1, y1, _) = points[i - 1], points[i]
            if abs(x1 - x0) > cfg.width / 2 or abs(y1 - y0) > cfg.height / 2:
                continue  # wrapped around the edge; don't draw a false long segment
            opacity = (i / n) * (0.55 if not boid.is_predator else 0.85)
            parts.append(
                f'<line x1="{x0 * scale:.2f}" y1="{y0 * scale:.2f}" '
                f'x2="{x1 * scale:.2f}" y2="{y1 * scale:.2f}" '
                f'stroke="{color}" stroke-width="{1.4 if not boid.is_predator else 2.2}" '
                f'stroke-opacity="{opacity:.3f}" stroke-linecap="round"/>'
            )

    for boid in flock.prey:
        t = min(boid.speed() / cfg.max_speed, 1.0)
        color = _lerp_color(_PREY_COLOR_SLOW, _PREY_COLOR_FAST, t)
        pts = _boid_triangle(boid.position.x * scale, boid.position.y * scale, boid.heading(), size=scale * 1.1)
        parts.append(f'<polygon points="{pts}" fill="{color}"/>')
    for pred in flock.predators:
        pts = _boid_triangle(pred.position.x * scale, pred.position.y * scale, pred.heading(), size=scale * 1.8)
        parts.append(f'<polygon points="{pts}" fill="{_PREDATOR_COLOR}"/>')

    parts.append("</svg>")
    return "\n".join(parts)
