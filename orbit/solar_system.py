"""Planet data and orbital mechanics using circular orbit approximation."""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Planet:
    name: str
    char: str
    color: str
    period: float     # Orbital period in Earth years
    display_r: float  # Normalized display radius (0-1)
    angle0: float     # Initial angle offset in radians

    def position(self, t: float, cx: int, cy: int, max_r: float) -> Tuple[int, int]:
        """Return (col, row) screen position at simulation time t (years)."""
        theta = self.angle0 + (2 * math.pi / self.period) * t
        r = self.display_r * max_r
        # 0.45 compensates for terminal char aspect ratio (~2:1 h:w)
        x = cx + r * math.cos(theta)
        y = cy + r * math.sin(theta) * 0.45
        return round(x), round(y)


# Orbital periods from NASA Fact Sheets; display radii log-scaled for clarity.
PLANETS: list[Planet] = [
    Planet("Mercury", "·",  "white",          0.241,  0.13, 0.00),
    Planet("Venus",   "●",  "yellow",         0.615,  0.21, 1.05),
    Planet("Earth",   "◉",  "bright_blue",    1.000,  0.30, 2.50),
    Planet("Mars",    "●",  "red",            1.881,  0.39, 0.80),
    Planet("Jupiter", "◎",  "bright_yellow", 11.862,  0.53, 4.00),
    Planet("Saturn",  "⊕",  "yellow",        29.457,  0.65, 2.00),
    Planet("Uranus",  "○",  "cyan",          84.011,  0.76, 5.50),
    Planet("Neptune", "◦",  "blue",         164.795,  0.87, 3.00),
]
