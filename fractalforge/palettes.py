"""Color palettes for fractal rendering."""

from dataclasses import dataclass
from typing import List, Tuple


Color = Tuple[int, int, int]


@dataclass
class Palette:
    name: str
    colors: List[Color]
    background: Color = (0, 0, 0)

    def get_color(self, t: float) -> Color:
        """Map t in [0,1] to a color via smooth interpolation."""
        if t >= 1.0:
            return self.background
        scaled = t * (len(self.colors) - 1)
        idx = int(scaled)
        frac = scaled - idx
        c0 = self.colors[idx]
        c1 = self.colors[min(idx + 1, len(self.colors) - 1)]
        return (
            int(c0[0] + frac * (c1[0] - c0[0])),
            int(c0[1] + frac * (c1[1] - c0[1])),
            int(c0[2] + frac * (c1[2] - c0[2])),
        )


PALETTES = {
    "electric": Palette(
        name="electric",
        colors=[
            (0, 0, 20),
            (0, 0, 128),
            (0, 100, 255),
            (0, 220, 255),
            (100, 255, 255),
            (255, 255, 200),
            (255, 200, 50),
            (255, 100, 0),
            (200, 0, 0),
            (100, 0, 50),
        ],
        background=(0, 0, 0),
    ),
    "fire": Palette(
        name="fire",
        colors=[
            (0, 0, 0),
            (30, 0, 0),
            (100, 0, 0),
            (200, 50, 0),
            (255, 150, 0),
            (255, 220, 50),
            (255, 255, 200),
        ],
        background=(0, 0, 0),
    ),
    "ice": Palette(
        name="ice",
        colors=[
            (0, 0, 0),
            (0, 10, 50),
            (0, 50, 150),
            (0, 150, 220),
            (100, 200, 255),
            (200, 230, 255),
            (255, 255, 255),
        ],
        background=(0, 0, 0),
    ),
    "psychedelic": Palette(
        name="psychedelic",
        colors=[
            (255, 0, 100),
            (255, 150, 0),
            (200, 255, 0),
            (0, 255, 100),
            (0, 200, 255),
            (100, 0, 255),
            (255, 0, 200),
        ],
        background=(0, 0, 0),
    ),
    "gold": Palette(
        name="gold",
        colors=[
            (0, 0, 0),
            (20, 10, 0),
            (80, 40, 0),
            (180, 120, 0),
            (255, 200, 50),
            (255, 240, 180),
            (255, 255, 255),
        ],
        background=(0, 0, 0),
    ),
    "ocean": Palette(
        name="ocean",
        colors=[
            (0, 0, 20),
            (0, 20, 80),
            (0, 80, 160),
            (0, 160, 200),
            (50, 200, 180),
            (150, 230, 200),
            (220, 255, 240),
        ],
        background=(0, 0, 10),
    ),
}
