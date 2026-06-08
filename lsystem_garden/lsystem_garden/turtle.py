"""Turtle-graphics interpreter that turns an L-system string into line segments.

The turtle understands the conventional alphabet used throughout the
L-system literature (Prusinkiewicz & Lindenmayer, *The Algorithmic Beauty
of Plants*):

``F`` ``G`` ``A`` ``B``
    Move forward one step, drawing a line.
``f``
    Move forward one step without drawing (a "pen up" move).
``+`` / ``-``
    Turn left / right by the system's angle (optionally scaled by a
    leading integer, e.g. ``+(2)`` turns twice as far).
``[`` / ``]``
    Push / pop the turtle's position, heading and pen depth — this is
    what allows a single string to describe branching structures.
``|``
    Reverse direction (turn by 180 degrees).

Anything else is treated as a no-op symbol (common for systems that use
placeholder letters such as ``X`` purely to drive grammar expansion).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Segment:
    """A single drawn line, annotated with branching ``depth``.

    ``depth`` is the size of the turtle's stack at the time the segment
    was drawn — branches deeper in the structure get a larger depth,
    which renderers use to taper width and shift color (mimicking how
    real plants thin and lighten toward their tips).
    """

    x1: float
    y1: float
    x2: float
    y2: float
    depth: int


@dataclass
class _State:
    x: float
    y: float
    heading: float  # degrees, 0 = pointing "up" (negative-y in screen space)


def walk(
    instructions: str,
    *,
    angle: float,
    step: float = 1.0,
    start_heading: float = 90.0,
) -> List[Segment]:
    """Interpret ``instructions`` and return the list of drawn segments.

    Args:
        instructions: The expanded L-system string.
        angle: Default turning angle in degrees for ``+``/``-``.
        step: Length of one forward move.
        start_heading: Initial heading in degrees (90 = "up" in the usual
            screen coordinate system, where y grows downward).
    """

    state = _State(x=0.0, y=0.0, heading=start_heading)
    stack: List[Tuple[_State, int]] = []
    depth = 0
    segments: List[Segment] = []

    i = 0
    n = len(instructions)
    while i < n:
        symbol = instructions[i]
        i += 1

        if symbol in "FGAB":
            rad = math.radians(state.heading)
            nx = state.x + step * math.cos(rad)
            ny = state.y - step * math.sin(rad)
            segments.append(Segment(state.x, state.y, nx, ny, depth))
            state = _State(nx, ny, state.heading)
        elif symbol == "f":
            rad = math.radians(state.heading)
            state = _State(
                state.x + step * math.cos(rad),
                state.y - step * math.sin(rad),
                state.heading,
            )
        elif symbol in "+-":
            turn, i = _read_scaled_angle(instructions, i, angle)
            state = _State(state.x, state.y, state.heading + (turn if symbol == "+" else -turn))
        elif symbol == "|":
            state = _State(state.x, state.y, state.heading + 180.0)
        elif symbol == "[":
            stack.append((state, depth))
            depth += 1
        elif symbol == "]":
            if not stack:
                raise ValueError("unbalanced ']' in L-system output")
            state, depth = stack.pop()
        # Any other symbol (X, Y, letters used purely for grammar shaping,
        # stochastic markers, etc.) is a structural no-op for the turtle.

    return segments


def _read_scaled_angle(s: str, i: int, base_angle: float) -> Tuple[float, int]:
    """Support an optional ``(N)`` multiplier after a turn symbol, e.g. ``+(3)``."""

    if i < len(s) and s[i] == "(":
        close = s.find(")", i)
        if close != -1:
            try:
                multiplier = float(s[i + 1 : close])
            except ValueError:
                return base_angle, i
            return base_angle * multiplier, close + 1
    return base_angle, i


def bounds(segments: List[Segment]) -> Tuple[float, float, float, float]:
    """Return ``(min_x, min_y, max_x, max_y)`` covering all segments."""

    if not segments:
        return (0.0, 0.0, 0.0, 0.0)

    xs = [v for seg in segments for v in (seg.x1, seg.x2)]
    ys = [v for seg in segments for v in (seg.y1, seg.y2)]
    return (min(xs), min(ys), max(xs), max(ys))
