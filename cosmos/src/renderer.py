"""
Terminal renderer for the Cosmos solar system visualizer.
Draws the solar system on a 2D grid using ANSI/Unicode art.
"""

import math
import random
from datetime import datetime

from .orbital import PLANETS, SUN, get_all_positions, days_since_j2000, OrbitalElements

# --- Canvas helpers ----------------------------------------------------------

CANVAS_W = 120
CANVAS_H = 50
VIEW_AU   = 32.0   # AU visible from center to edge (for full solar system)
INNER_AU  = 1.8    # AU for inner-system zoom

ORBIT_CHARS = "·∘○◌"
STAR_CHARS  = "·✦✧⊹*"

ANSI_RESET  = "\033[0m"
ANSI_BOLD   = "\033[1m"
ANSI_DIM    = "\033[2m"

PLANET_COLORS = {
    "Sun":     "\033[1;93m",  # bold bright yellow
    "Mercury": "\033[0;33m",  # yellow
    "Venus":   "\033[1;97m",  # bright white
    "Earth":   "\033[1;34m",  # bright blue
    "Mars":    "\033[0;31m",  # red
    "Jupiter": "\033[0;33m",  # yellow
    "Saturn":  "\033[1;33m",  # bold yellow
    "Uranus":  "\033[1;36m",  # cyan
    "Neptune": "\033[0;34m",  # blue
}

ORBIT_COLORS = {
    "Mercury": "\033[2;33m",
    "Venus":   "\033[2;37m",
    "Earth":   "\033[2;34m",
    "Mars":    "\033[2;31m",
    "Jupiter": "\033[2;33m",
    "Saturn":  "\033[2;33m",
    "Uranus":  "\033[2;36m",
    "Neptune": "\033[2;34m",
}


def au_to_pixel(x_au: float, y_au: float, view_au: float, w: int, h: int):
    """Convert AU coordinates to canvas pixel (col, row), y-axis inverted for terminal."""
    scale_x = (w - 2) / (2 * view_au)
    scale_y = (h - 2) / (2 * view_au) * 2.0  # compensate for terminal char aspect ratio
    col = int(w / 2 + x_au * scale_x)
    row = int(h / 2 - y_au * scale_y)
    return col, row


def make_star_field(w: int, h: int, seed: int = 42, density: float = 0.03) -> list[tuple[int, int, str]]:
    """Generate a random star field."""
    rng = random.Random(seed)
    stars = []
    for row in range(h):
        for col in range(w):
            if rng.random() < density:
                ch = rng.choice(STAR_CHARS)
                stars.append((row, col, ch))
    return stars


STARS = make_star_field(CANVAS_W, CANVAS_H)


def draw_orbit(canvas: list[list[str]], planet: OrbitalElements, view_au: float,
               w: int, h: int, color: str) -> None:
    """Draw an elliptical orbit on the canvas."""
    a = planet.semi_major_au
    e = planet.eccentricity
    b = a * math.sqrt(1 - e * e)
    cx_offset = -a * e  # center of ellipse is offset from focus (Sun)

    steps = max(200, int(2 * math.pi * a / view_au * 400))
    for i in range(steps):
        theta = 2 * math.pi * i / steps
        # Ellipse in orbital plane centered at focus
        r = a * (1 - e * e) / (1 + e * math.cos(theta))
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        col, row = au_to_pixel(x, y, view_au, w, h)
        if 0 <= row < h and 0 <= col < w:
            if canvas[row][col] == " ":
                canvas[row][col] = f"{color}·{ANSI_RESET}"


def render_frame(
    dt: datetime | None = None,
    view_au: float = VIEW_AU,
    w: int = CANVAS_W,
    h: int = CANVAS_H,
    show_labels: bool = True,
    show_orbits: bool = True,
    show_stars: bool = True,
) -> str:
    """
    Render the solar system at datetime dt (default: now).
    Returns a string ready to be printed to the terminal.
    """
    positions = get_all_positions(dt)
    jd = days_since_j2000(dt)

    # Initialize canvas
    canvas: list[list[str]] = [[" "] * w for _ in range(h)]

    # Star field
    if show_stars:
        for row, col, ch in STARS:
            if 0 <= row < h and 0 <= col < w:
                canvas[row][col] = f"\033[2;37m{ch}{ANSI_RESET}"

    # Draw orbits
    if show_orbits:
        for p in PLANETS:
            if p.semi_major_au <= view_au * 1.1:
                color = ORBIT_COLORS.get(p.name, "\033[2;37m")
                draw_orbit(canvas, p, view_au, w, h, color)

    # Draw celestial bodies
    all_bodies = [SUN] + PLANETS
    for body in all_bodies:
        if body.name not in positions:
            continue
        x_au, y_au = positions[body.name]
        if abs(x_au) > view_au or abs(y_au) > view_au:
            continue
        col, row = au_to_pixel(x_au, y_au, view_au, w, h)
        if not (0 <= row < h and 0 <= col < w):
            continue

        color = PLANET_COLORS.get(body.name, "\033[0;37m")

        # Sun gets a special glow
        if body.name == "Sun":
            canvas[row][col] = f"{color}☀{ANSI_RESET}"
            # Glow ring
            for dr, dc, gc in [(-1,0,"·"),(1,0,"·"),(0,-1,"·"),(0,1,"·")]:
                nr, nc = row+dr, col+dc
                if 0<=nr<h and 0<=nc<w:
                    canvas[nr][nc] = f"\033[2;93m{gc}{ANSI_RESET}"
        else:
            canvas[row][col] = f"{color}{body.symbol}{ANSI_RESET}"

            # Label
            if show_labels and 0 <= row < h and col + 2 < w:
                label = body.name
                for i, ch in enumerate(label):
                    lc = col + 2 + i
                    if 0 <= lc < w and canvas[row][lc] == " ":
                        canvas[row][lc] = f"\033[2;37m{ch}{ANSI_RESET}"

    # Assemble rows
    lines = ["".join(row) for row in canvas]
    return "\n".join(lines)


def render_data_panel(dt: datetime | None = None) -> str:
    """Render a text panel with planetary data."""
    from datetime import timezone
    if dt is None:
        dt = datetime.now(timezone.utc)

    jd = days_since_j2000(dt)
    positions = get_all_positions(dt)

    lines = []
    lines.append(f"\033[1;97m{'─' * 52}\033[0m")
    lines.append(f"\033[1;93m  ☀  COSMOS — Solar System Monitor\033[0m")
    lines.append(f"\033[0;37m  {dt.strftime('%Y-%m-%d %H:%M UTC')}  |  JD+{jd:,.1f} since J2000\033[0m")
    lines.append(f"\033[1;97m{'─' * 52}\033[0m")
    lines.append(f"\033[2;37m  {'Planet':<10} {'Distance (AU)':>14} {'X':>8} {'Y':>8}\033[0m")
    lines.append(f"\033[2;37m  {'──────':<10} {'────────────':>14} {'──':>8} {'──':>8}\033[0m")

    for p in PLANETS:
        x, y = positions[p.name]
        dist = math.sqrt(x*x + y*y)
        color = PLANET_COLORS.get(p.name, "\033[0;37m")
        lines.append(
            f"  {color}{p.symbol} {p.name:<9}{ANSI_RESET}"
            f"\033[0;37m {dist:>13.4f} {x:>8.3f} {y:>8.3f}\033[0m"
        )

    lines.append(f"\033[1;97m{'─' * 52}\033[0m")
    return "\n".join(lines)


def full_render(dt: datetime | None = None, view_au: float = VIEW_AU,
                w: int = CANVAS_W, h: int = CANVAS_H) -> str:
    """Full combined render: map + data panel."""
    border_h = f"\033[1;34m╔{'═' * w}╗\033[0m"
    border_f = f"\033[1;34m╚{'═' * w}╝\033[0m"
    border_v = "\033[1;34m║\033[0m"

    frame = render_frame(dt, view_au, w, h)
    rows = frame.split("\n")
    boxed = [f"{border_v}{row}{border_v}" for row in rows]
    map_section = f"{border_h}\n" + "\n".join(boxed) + f"\n{border_f}"

    data = render_data_panel(dt)
    return f"{map_section}\n\n{data}"
