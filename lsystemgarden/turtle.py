"""Turtle-graphics interpreter for L-system command strings.

Supported symbols:
    F, G   move forward one step, drawing a line
    f      move forward one step without drawing
    +      turn left by the system's angle
    -      turn right by the system's angle
    [      push the current position/heading onto a stack
    ]      pop the stack, restoring position/heading
    other  ignored (grammar-only symbols, e.g. X/Y placeholders)
"""

from __future__ import annotations

import math
from dataclasses import dataclass

DEFAULT_DRAW_CHARS = frozenset({"F", "G"})


@dataclass(frozen=True)
class Segment:
    x1: float
    y1: float
    x2: float
    y2: float
    depth: int  # branch nesting depth at the time this segment was drawn


def interpret(
    commands: str,
    *,
    angle: float,
    step: float = 1.0,
    start_heading: float = 90.0,
    draw_chars: frozenset[str] = DEFAULT_DRAW_CHARS,
) -> list[Segment]:
    """Walk a turtle through an L-system command string, returning drawn segments."""
    x, y = 0.0, 0.0
    heading = start_heading
    stack: list[tuple[float, float, float]] = []
    segments: list[Segment] = []

    for char in commands:
        if char in draw_chars:
            radians = math.radians(heading)
            nx = x + step * math.cos(radians)
            ny = y + step * math.sin(radians)
            segments.append(Segment(x, y, nx, ny, len(stack)))
            x, y = nx, ny
        elif char == "f":
            radians = math.radians(heading)
            x += step * math.cos(radians)
            y += step * math.sin(radians)
        elif char == "+":
            heading += angle
        elif char == "-":
            heading -= angle
        elif char == "[":
            stack.append((x, y, heading))
        elif char == "]":
            if not stack:
                raise ValueError("unbalanced ']' with no matching '[' in command string")
            x, y, heading = stack.pop()
        # any other symbol is grammar-only and has no turtle effect

    if stack:
        raise ValueError(f"unbalanced '[': {len(stack)} branch(es) never closed")
    return segments


def bounding_box(segments: list[Segment]) -> tuple[float, float, float, float]:
    """Return (min_x, min_y, max_x, max_y) spanning all segments."""
    if not segments:
        raise ValueError("cannot compute a bounding box for zero segments")
    xs = [s.x1 for s in segments] + [s.x2 for s in segments]
    ys = [s.y1 for s in segments] + [s.y2 for s in segments]
    return min(xs), min(ys), max(xs), max(ys)
