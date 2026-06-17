"""L-systems: string rewriting grammars interpreted as turtle graphics.

An L-system expands a starting string ("axiom") by repeatedly replacing
characters according to production rules, then a turtle walks the final
string drawing lines, turning, and branching using a push/pop stack.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from PIL import Image, ImageDraw


@dataclass(frozen=True)
class LSystem:
    axiom: str
    rules: dict[str, str]
    angle: float
    iterations: int
    name: str = "lsystem"
    start_heading: float = 90.0
    step_scale: float = 1.0


PRESETS: dict[str, LSystem] = {
    "tree": LSystem(
        axiom="X",
        rules={"X": "F-[[X]+X]+F[+FX]-X", "F": "FF"},
        angle=25.0,
        iterations=6,
        name="tree",
        step_scale=1.0,
    ),
    "bush": LSystem(
        axiom="F",
        rules={"F": "FF-[-F+F+F]+[+F-F-F]"},
        angle=22.5,
        iterations=4,
        name="bush",
        step_scale=1.0,
    ),
    "koch": LSystem(
        axiom="F",
        rules={"F": "F+F-F-F+F"},
        angle=90.0,
        iterations=4,
        name="koch",
        start_heading=0.0,
        step_scale=1.0,
    ),
    "dragon": LSystem(
        axiom="FX",
        rules={"X": "X+YF+", "Y": "-FX-Y"},
        angle=90.0,
        iterations=11,
        name="dragon",
        start_heading=0.0,
        step_scale=1.0,
    ),
    "sierpinski": LSystem(
        axiom="F-G-G",
        rules={"F": "F-G+F+G-F", "G": "GG"},
        angle=120.0,
        iterations=6,
        name="sierpinski",
        start_heading=0.0,
        step_scale=1.0,
    ),
}


def expand(system: LSystem) -> str:
    s = system.axiom
    for _ in range(system.iterations):
        s = "".join(system.rules.get(ch, ch) for ch in s)
    return s


@dataclass
class _TurtleState:
    x: float
    y: float
    heading: float


def _path_segments(system: LSystem, instructions: str) -> tuple[list[tuple[float, float, float, float]], tuple[float, float, float, float]]:
    """Walk the turtle and return line segments plus the bounding box."""
    state = _TurtleState(0.0, 0.0, system.start_heading)
    stack: list[_TurtleState] = []
    segments: list[tuple[float, float, float, float]] = []
    min_x = max_x = state.x
    min_y = max_y = state.y

    for ch in instructions:
        if ch in ("F", "G"):
            rad = math.radians(state.heading)
            nx = state.x + math.cos(rad) * system.step_scale
            ny = state.y + math.sin(rad) * system.step_scale
            segments.append((state.x, state.y, nx, ny))
            state.x, state.y = nx, ny
            min_x, max_x = min(min_x, nx), max(max_x, nx)
            min_y, max_y = min(min_y, ny), max(max_y, ny)
        elif ch == "+":
            state.heading += system.angle
        elif ch == "-":
            state.heading -= system.angle
        elif ch == "[":
            stack.append(_TurtleState(state.x, state.y, state.heading))
        elif ch == "]":
            state = stack.pop()
        # any other character is a no-op placeholder (e.g. X, Y)

    return segments, (min_x, min_y, max_x, max_y)


def render_lsystem(
    preset: str = "tree",
    width: int = 900,
    height: int = 900,
    bg: tuple[int, int, int] = (10, 12, 16),
    line_color: tuple[int, int, int] = (130, 220, 140),
    margin: float = 0.06,
) -> Image.Image:
    """Render a named L-system preset to a Pillow Image."""
    if preset not in PRESETS:
        raise ValueError(f"Unknown preset {preset!r}. Options: {sorted(PRESETS)}")
    system = PRESETS[preset]
    instructions = expand(system)
    segments, (min_x, min_y, max_x, max_y) = _path_segments(system, instructions)

    span_x = max(max_x - min_x, 1e-6)
    span_y = max(max_y - min_y, 1e-6)
    usable_w = width * (1 - 2 * margin)
    usable_h = height * (1 - 2 * margin)
    scale = min(usable_w / span_x, usable_h / span_y)

    def to_pixel(x: float, y: float) -> tuple[float, float]:
        px = (x - min_x) * scale + (width - span_x * scale) / 2
        # Flip y because image coordinates grow downward.
        py = height - ((y - min_y) * scale + (height - span_y * scale) / 2)
        return px, py

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)
    for x0, y0, x1, y1 in segments:
        p0 = to_pixel(x0, y0)
        p1 = to_pixel(x1, y1)
        draw.line([p0, p1], fill=line_color, width=1)
    return img
