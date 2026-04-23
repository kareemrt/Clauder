"""Core Conway's Game of Life grid logic."""

import numpy as np
from typing import Tuple, List


class Grid:
    """Infinite-boundary Conway's Game of Life grid."""

    DEAD = 0
    ALIVE = 1

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cells = np.zeros((height, width), dtype=np.uint8)
        self.generation = 0
        self._history: List[np.ndarray] = []

    def seed(self, pattern: np.ndarray, offset_x: int = 0, offset_y: int = 0) -> None:
        """Place a pattern on the grid at the given offset."""
        self.cells[:] = 0
        self.generation = 0
        ph, pw = pattern.shape
        for y in range(min(ph, self.height - offset_y)):
            for x in range(min(pw, self.width - offset_x)):
                self.cells[offset_y + y, offset_x + x] = pattern[y, x]

    def step(self) -> Tuple[int, int]:
        """Advance one generation. Returns (born, died) counts."""
        neighbors = self._count_neighbors()
        alive = self.cells == self.ALIVE
        born_mask = (~alive) & ((neighbors == 3))
        survive_mask = alive & ((neighbors == 2) | (neighbors == 3))
        died_mask = alive & ~survive_mask

        new_cells = np.zeros_like(self.cells)
        new_cells[born_mask] = self.ALIVE
        new_cells[survive_mask] = self.ALIVE

        born = int(born_mask.sum())
        died = int(died_mask.sum())

        self._history.append(self.cells.copy())
        if len(self._history) > 10:
            self._history.pop(0)

        self.cells = new_cells
        self.generation += 1
        return born, died

    def _count_neighbors(self) -> np.ndarray:
        """Count live neighbors for each cell using convolution."""
        from scipy.ndimage import convolve
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]], dtype=np.uint8)
        return convolve(self.cells, kernel, mode='wrap')

    @property
    def population(self) -> int:
        return int(self.cells.sum())

    @property
    def density(self) -> float:
        return self.population / (self.width * self.height)

    def is_stable(self, window: int = 4) -> bool:
        """Return True if population hasn't changed in `window` generations."""
        if len(self._history) < window:
            return False
        pops = [int(h.sum()) for h in self._history[-window:]]
        return len(set(pops)) == 1

    def is_extinct(self) -> bool:
        return self.population == 0

    def clone(self) -> "Grid":
        g = Grid(self.width, self.height)
        g.cells = self.cells.copy()
        g.generation = self.generation
        return g
