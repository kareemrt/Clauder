from __future__ import annotations
import numpy as np
from dataclasses import dataclass, field
from typing import List


@dataclass
class Body:
    name: str
    mass: float
    pos: np.ndarray
    vel: np.ndarray
    color: str          # full ANSI escape sequence
    symbol: str         # single display character
    trail: List[np.ndarray] = field(default_factory=list)
    max_trail: int = 40

    def record_trail(self) -> None:
        self.trail.append(self.pos.copy())
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)
