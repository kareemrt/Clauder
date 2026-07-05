"""Celestial body data model."""

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class CelestialBody:
    name: str
    mass: float         # solar masses
    x: float            # AU
    y: float            # AU
    vx: float           # AU / year
    vy: float           # AU / year
    color: str          # Rich color string
    symbol: str         # single display character
    trail_length: int = 80
    trail: List[Tuple[float, float]] = field(default_factory=list)

    @property
    def speed(self) -> float:
        return (self.vx ** 2 + self.vy ** 2) ** 0.5

    @property
    def distance(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def record_position(self) -> None:
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)
