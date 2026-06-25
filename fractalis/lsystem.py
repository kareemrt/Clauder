"""L-system curve generation: string rewriting + turtle graphics + rasterization."""

import math

from . import colormaps


def expand(axiom, rules, iterations):
    """Apply L-system production rules to ``axiom`` ``iterations`` times."""
    s = axiom
    for _ in range(iterations):
        s = "".join(rules.get(ch, ch) for ch in s)
    return s


def turtle_segments(instructions, angle, step=1.0, heading=0.0):
    """Walk ``instructions`` with a turtle and return a list of line segments.

    Recognized symbols: F/G draw forward, f/g move without drawing,
    + turns left, - turns right, [ pushes state, ] pops state.
    Returns a list of (x0, y0, x1, y1) tuples in turtle-space units.
    """
    x, y = 0.0, 0.0
    stack = []
    segments = []
    for ch in instructions:
        if ch in "FG":
            nx = x + step * math.cos(math.radians(heading))
            ny = y + step * math.sin(math.radians(heading))
            segments.append((x, y, nx, ny))
            x, y = nx, ny
        elif ch in "fg":
            x += step * math.cos(math.radians(heading))
            y += step * math.sin(math.radians(heading))
        elif ch == "+":
            heading += angle
        elif ch == "-":
            heading -= angle
        elif ch == "[":
            stack.append((x, y, heading))
        elif ch == "]":
            x, y, heading = stack.pop()
    return segments


def _bresenham(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x1 >= x0 else -1
    sy = 1 if y1 >= y0 else -1
    x, y = x0, y0
    if dx >= dy:
        err = dx / 2.0
        while x != x1:
            points.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
        points.append((x1, y1))
    else:
        err = dy / 2.0
        while y != y1:
            points.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
        points.append((x1, y1))
    return points


def rasterize(segments, width, height, cmap="psychedelic", background=(8, 8, 16),
              margin=24, stroke=1):
    """Render line segments to an RGB pixel buffer, colored along path order."""
    cmap_fn = colormaps.get(cmap) if isinstance(cmap, str) else cmap

    xs = [p for seg in segments for p in (seg[0], seg[2])]
    ys = [p for seg in segments for p in (seg[1], seg[3])]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span_x = max(max_x - min_x, 1e-9)
    span_y = max(max_y - min_y, 1e-9)

    draw_w = width - 2 * margin
    draw_h = height - 2 * margin
    scale = min(draw_w / span_x, draw_h / span_y)
    off_x = margin + (draw_w - span_x * scale) / 2
    off_y = margin + (draw_h - span_y * scale) / 2

    def to_pixel(x, y):
        px = off_x + (x - min_x) * scale
        py = height - (off_y + (y - min_y) * scale)  # flip so +y is "up"
        return round(px), round(py)

    pixels = bytearray(background * (width * height))

    def plot(px, py, color):
        if 0 <= px < width and 0 <= py < height:
            offset = (py * width + px) * 3
            pixels[offset:offset + 3] = bytes(color)

    n = len(segments)
    for i, (x0, y0, x1, y1) in enumerate(segments):
        color = cmap_fn(i / max(n - 1, 1))
        p0 = to_pixel(x0, y0)
        p1 = to_pixel(x1, y1)
        for px, py in _bresenham(*p0, *p1):
            for dx in range(-(stroke // 2), stroke - stroke // 2):
                for dy in range(-(stroke // 2), stroke - stroke // 2):
                    plot(px + dx, py + dy, color)

    return pixels


# (axiom, rules, angle, heading, iterations) presets tuned to look good
# at moderate iteration counts.
PRESETS = {
    "koch_snowflake": dict(
        axiom="F++F++F", rules={"F": "F-F++F-F"}, angle=60, heading=0, iterations=4,
    ),
    "sierpinski_triangle": dict(
        axiom="F-G-G", rules={"F": "F-G+F+G-F", "G": "GG"}, angle=120, heading=0,
        iterations=6,
    ),
    "dragon_curve": dict(
        axiom="FX", rules={"X": "X+YF+", "Y": "-FX-Y"}, angle=90, heading=0,
        iterations=12,
    ),
    "fractal_plant": dict(
        axiom="X",
        rules={"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"},
        angle=25, heading=90, iterations=6,
    ),
    "levy_c_curve": dict(
        axiom="F", rules={"F": "+F--F+"}, angle=45, heading=0, iterations=14,
    ),
}


def render_lsystem(preset, width=800, height=800, cmap="psychedelic",
                    step=1.0, stroke=1, iterations=None):
    """Render a named L-system preset to an RGB pixel buffer."""
    spec = PRESETS[preset]
    n_iter = spec["iterations"] if iterations is None else iterations
    instructions = expand(spec["axiom"], spec["rules"], n_iter)
    segments = turtle_segments(instructions, spec["angle"], step=step,
                                heading=spec["heading"])
    return rasterize(segments, width, height, cmap=cmap, stroke=stroke)
