"""Core L-system rewriting engine and turtle-graphics interpreter."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class LSystem:
    """A parametric-free Lindenmayer system definition."""

    name: str
    description: str
    axiom: str
    rules: dict[str, str]
    angle: float
    draw_chars: str = "F"
    start_heading: float = 90.0
    default_iterations: int = 4

    def expand(self, iterations: int) -> str:
        """Apply the production rules `iterations` times to the axiom."""
        if iterations < 0:
            raise ValueError("iterations must be >= 0")
        sequence = self.axiom
        for _ in range(iterations):
            sequence = "".join(self.rules.get(symbol, symbol) for symbol in sequence)
        return sequence


@dataclass(frozen=True)
class Segment:
    """A single drawn line segment, tagged with its branch depth."""

    x1: float
    y1: float
    x2: float
    y2: float
    depth: int


def interpret(instructions: str, lsystem: LSystem, step: float = 1.0) -> list[Segment]:
    """Walk a turtle through an expanded L-system string, returning segments to draw.

    Supported alphabet:
      - any char in `lsystem.draw_chars`: move forward `step`, drawing a segment
      - 'f': move forward `step` without drawing
      - '+': turn left by `lsystem.angle` degrees
      - '-': turn right by `lsystem.angle` degrees
      - '|': turn around (180 degrees)
      - '[': push current position/heading onto the stack
      - ']': pop position/heading off the stack
    """
    x, y = 0.0, 0.0
    heading = lsystem.start_heading
    stack: list[tuple[float, float, float]] = []
    segments: list[Segment] = []

    for symbol in instructions:
        if symbol in lsystem.draw_chars:
            rad = math.radians(heading)
            nx = x + step * math.cos(rad)
            ny = y + step * math.sin(rad)
            segments.append(Segment(x, y, nx, ny, len(stack)))
            x, y = nx, ny
        elif symbol == "f":
            rad = math.radians(heading)
            x += step * math.cos(rad)
            y += step * math.sin(rad)
        elif symbol == "+":
            heading += lsystem.angle
        elif symbol == "-":
            heading -= lsystem.angle
        elif symbol == "|":
            heading += 180
        elif symbol == "[":
            stack.append((x, y, heading))
        elif symbol == "]":
            x, y, heading = stack.pop()
        # any other symbol is treated as a no-op marker (e.g. "X", "A", "B")

    return segments


def bounding_box(segments: list[Segment]) -> tuple[float, float, float, float]:
    """Return (min_x, min_y, max_x, max_y) for a list of segments."""
    if not segments:
        return (0.0, 0.0, 0.0, 0.0)
    xs = [s.x1 for s in segments] + [s.x2 for s in segments]
    ys = [s.y1 for s in segments] + [s.y2 for s in segments]
    return (min(xs), min(ys), max(xs), max(ys))
