"""Turtle-graphics interpreter that walks an expanded L-system string and
produces line segments.

Coordinates use a standard math orientation (positive y is "up"); the SVG
writer is responsible for flipping to screen space.
"""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Segment:
    x1: float
    y1: float
    x2: float
    y2: float


class TurtleInterpreter:
    """Interprets L-system symbols as turtle movements.

    Recognized symbols:
        F, G   draw forward one step
        f      move forward one step without drawing
        +      turn left by `angle` degrees
        -      turn right by `angle` degrees
        [      push current position and heading
        ]      pop position and heading
    Any other symbol is ignored (it exists only to drive rule expansion).
    """

    MOVE_CHARS = frozenset("f")
    TURN_LEFT = "+"
    TURN_RIGHT = "-"
    PUSH = "["
    POP = "]"

    def __init__(
        self,
        angle: float,
        step: float = 1.0,
        start_heading: float = 90.0,
        draw_chars: str = "FG",
    ):
        self.angle = angle
        self.step = step
        self.start_heading = start_heading
        self.draw_chars = frozenset(draw_chars)

    def interpret(self, instructions: str) -> list[Segment]:
        x, y = 0.0, 0.0
        heading = self.start_heading
        stack: list[tuple[float, float, float]] = []
        segments: list[Segment] = []

        for symbol in instructions:
            if symbol in self.draw_chars or symbol in self.MOVE_CHARS:
                rad = math.radians(heading)
                nx = x + self.step * math.cos(rad)
                ny = y + self.step * math.sin(rad)
                if symbol in self.draw_chars:
                    segments.append(Segment(x, y, nx, ny))
                x, y = nx, ny
            elif symbol == self.TURN_LEFT:
                heading += self.angle
            elif symbol == self.TURN_RIGHT:
                heading -= self.angle
            elif symbol == self.PUSH:
                stack.append((x, y, heading))
            elif symbol == self.POP:
                if not stack:
                    raise ValueError("unbalanced ']' with no matching '['")
                x, y, heading = stack.pop()
            # all other symbols (e.g. X, A, B) are no-ops for the turtle

        if stack:
            raise ValueError("unbalanced '[' with no matching ']'")

        return segments
