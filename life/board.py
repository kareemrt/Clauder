import numpy as np


class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.uint8)
        self.generation = 0
        self.history: list[int] = []

    def randomize(self, density: float = 0.3, seed: int | None = None) -> "Board":
        rng = np.random.default_rng(seed)
        self.grid = rng.choice(
            [0, 1], size=(self.height, self.width), p=[1 - density, density]
        ).astype(np.uint8)
        return self

    def load(self, pattern: np.ndarray, row: int = 0, col: int = 0) -> "Board":
        ph, pw = pattern.shape
        r0, c0 = row % self.height, col % self.width
        for dr in range(ph):
            for dc in range(pw):
                self.grid[(r0 + dr) % self.height][(c0 + dc) % self.width] = pattern[dr, dc]
        return self

    def step(self) -> np.ndarray:
        g = self.grid
        neighbors = sum(
            np.roll(np.roll(g, dr, 0), dc, 1)
            for dr in (-1, 0, 1)
            for dc in (-1, 0, 1)
            if (dr, dc) != (0, 0)
        )
        self.grid = np.where(
            (neighbors == 3) | ((g == 1) & (neighbors == 2)), 1, 0
        ).astype(np.uint8)
        self.generation += 1
        self.history.append(int(np.sum(self.grid)))
        return self.grid

    def population(self) -> int:
        return int(np.sum(self.grid))

    def is_dead(self) -> bool:
        return self.population() == 0

    def is_stable(self, window: int = 8) -> bool:
        if len(self.history) < window:
            return False
        tail = self.history[-window:]
        return max(tail) - min(tail) == 0

    def fingerprint(self) -> bytes:
        return self.grid.tobytes()
