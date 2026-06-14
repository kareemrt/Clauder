"""Turtle-graphics interpreter for L-system strings.

Converts an expanded L-system string into a list of :class:`Segment`
line segments by walking a virtual turtle across the plane. The supported
alphabet is the classic one used throughout the L-system literature:

============  =================================================
Symbol        Meaning
============  =================================================
``F`` ``G``   Move forward one step, drawing a line
``f``         Move forward one step without drawing
``+``         Turn left by the system's angle
``-``         Turn right by the system's angle
``[``         Push the current state (position, heading, depth)
``]``         Pop the most recently pushed state
anything else Ignored (structural symbols like ``X``, ``A``, ``B``)
============  =================================================
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

DRAW_CHARS = "FG"
MOVE_CHARS = "f"


@dataclass(frozen=True)
class Segment:
    """A single drawn line, with the bracket-nesting ``depth`` it was drawn at."""

    x1: float
    y1: float
    x2: float
    y2: float
    depth: int


@dataclass(frozen=True)
class TurtleConfig:
    """Parameters controlling how a command string is turned into geometry."""

    angle: float
    step: float = 1.0
    step_falloff: float = 1.0
    angle_jitter: float = 0.0
    start_heading: float = 90.0


def run(commands: str, config: TurtleConfig, rng: random.Random | None = None) -> list[Segment]:
    """Walk the turtle through ``commands`` and return the drawn segments."""
    rng = rng or random.Random()

    x = y = 0.0
    heading = config.start_heading
    depth = 0
    step = config.step
    stack: list[tuple[float, float, float, int, float]] = []
    segments: list[Segment] = []

    for ch in commands:
        if ch in DRAW_CHARS or ch in MOVE_CHARS:
            rad = math.radians(heading)
            nx = x + step * math.cos(rad)
            ny = y + step * math.sin(rad)
            if ch in DRAW_CHARS:
                segments.append(Segment(x, y, nx, ny, depth))
            x, y = nx, ny
        elif ch == "+":
            heading += config.angle + rng.uniform(-config.angle_jitter, config.angle_jitter)
        elif ch == "-":
            heading -= config.angle + rng.uniform(-config.angle_jitter, config.angle_jitter)
        elif ch == "[":
            stack.append((x, y, heading, depth, step))
            depth += 1
            step *= config.step_falloff
        elif ch == "]":
            if not stack:
                raise ValueError("unbalanced ']' in command string")
            x, y, heading, depth, step = stack.pop()
        # everything else (X, A, B, ...) is a structural symbol only

    return segments
