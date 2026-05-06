"""Grid: the core state container for 2-state cellular automata."""

import numpy as np
from typing import Callable, List, Optional


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.generation = 0
        self.cells = np.zeros((height, width), dtype=np.uint8)
        self._pop_history: List[int] = []
        self._cell_history: List[np.ndarray] = []

    def clear(self) -> None:
        self.cells[:] = 0
        self.generation = 0
        self._pop_history.clear()
        self._cell_history.clear()

    def randomize(self, density: float = 0.3, seed: Optional[int] = None) -> None:
        rng = np.random.default_rng(seed)
        self.cells = (rng.random((self.height, self.width)) < density).astype(np.uint8)

    def place_pattern(
        self, pattern: np.ndarray, cx: int, cy: int, center: bool = True
    ) -> None:
        ph, pw = pattern.shape
        x = (cx - pw // 2) if center else cx
        y = (cy - ph // 2) if center else cy
        x = max(0, min(x, self.width - pw))
        y = max(0, min(y, self.height - ph))
        self.cells[y : y + ph, x : x + pw] = pattern

    def step(self, rule_fn: Callable[[np.ndarray], np.ndarray]) -> None:
        self._cell_history.append(self.cells.copy())
        if len(self._cell_history) > 8:
            self._cell_history.pop(0)
        self.cells = rule_fn(self.cells)
        self.generation += 1
        self._pop_history.append(self.population)

    def snapshot(self) -> np.ndarray:
        return self.cells.copy()

    @property
    def population(self) -> int:
        return int(np.sum(self.cells > 0))

    @property
    def density(self) -> float:
        total = self.width * self.height
        return self.population / total if total else 0.0

    @property
    def population_delta(self) -> int:
        if len(self._pop_history) < 2:
            return 0
        return self._pop_history[-1] - self._pop_history[-2]

    @property
    def is_stable(self) -> bool:
        if len(self._cell_history) < 1:
            return False
        return bool(np.array_equal(self.cells, self._cell_history[-1]))

    @property
    def is_oscillating(self) -> bool:
        for prev in reversed(self._cell_history[:-1]):
            if np.array_equal(self.cells, prev):
                return True
        return False
