"""Langton's Ant — a Turing-complete 2-D Turing machine.

After ~10 000 steps a single ant spontaneously builds an infinite 'highway'.
Multiple ants produce chaotic, beautiful interference patterns.
"""

import numpy as np
from typing import List, Optional


class LangtonsAnt:
    # Cardinal directions: N E S W  (dx, dy)
    _DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def __init__(
        self,
        width: int,
        height: int,
        num_ants: int = 1,
        seed: Optional[int] = None,
    ):
        self.width = width
        self.height = height
        self.cells = np.zeros((height, width), dtype=np.uint8)
        self.generation = 0
        self._pop_history: List[int] = []

        rng = np.random.default_rng(seed)
        self.ants: List[List[int]] = []   # [x, y, direction_index]
        for _ in range(num_ants):
            x = int(rng.integers(width // 4, 3 * width // 4))
            y = int(rng.integers(height // 4, 3 * height // 4))
            d = int(rng.integers(4))
            self.ants.append([x, y, d])

    # ------------------------------------------------------------------
    # Grid protocol (same interface as Grid so callers are rule-agnostic)
    # ------------------------------------------------------------------

    def step(self, _rule_fn=None) -> None:
        for ant in self.ants:
            x, y, d = ant
            if self.cells[y, x] == 0:      # white cell → turn right, flip, advance
                ant[2] = (d + 1) % 4
                self.cells[y, x] = 1
            else:                           # black cell → turn left, flip, advance
                ant[2] = (d - 1) % 4
                self.cells[y, x] = 0
            dx, dy = self._DIRS[ant[2]]
            ant[0] = (ant[0] + dx) % self.width
            ant[1] = (ant[1] + dy) % self.height

        self.generation += 1
        self._pop_history.append(self.population)

    def snapshot(self) -> np.ndarray:
        """Return the grid with ant positions marked as state 2."""
        view = self.cells.copy()
        for ant in self.ants:
            view[ant[1], ant[0]] = 2
        return view

    @property
    def population(self) -> int:
        return int(np.sum(self.cells))

    @property
    def density(self) -> float:
        return self.population / (self.width * self.height)

    @property
    def population_delta(self) -> int:
        if len(self._pop_history) < 2:
            return 0
        return self._pop_history[-1] - self._pop_history[-2]

    # Langton's Ant is never truly stable or oscillating
    is_stable = False
    is_oscillating = False
