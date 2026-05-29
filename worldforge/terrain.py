"""Fractal heightmap generation via Diamond-Square algorithm."""

import random


class HeightMap:
    """2-D heightmap generated with the Diamond-Square midpoint-displacement algorithm.

    size must be 2^k + 1 (e.g. 33, 65, 129, 257).
    """

    def __init__(self, size: int, seed: int = None):
        n = size - 1
        assert n > 0 and (n & (n - 1)) == 0, "size must be 2^k + 1"
        self.size = size
        self.data: list[list[float]] = [[0.0] * size for _ in range(size)]
        self._rng = random.Random(seed)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(self, roughness: float = 0.55) -> "HeightMap":
        s, g, rng = self.size, self.data, self._rng
        step = s - 1

        # Seed the four corners
        for cy in (0, step):
            for cx in (0, step):
                g[cy][cx] = rng.random()

        scale = 1.0
        while step > 1:
            half = step >> 1

            # Diamond step: set centre of each axis-aligned square
            for y in range(0, s - 1, step):
                for x in range(0, s - 1, step):
                    g[y + half][x + half] = (
                        g[y][x] + g[y][x + step]
                        + g[y + step][x] + g[y + step][x + step]
                    ) / 4.0 + rng.uniform(-scale, scale)

            # Square step: set midpoint of each diamond edge
            for y in range(0, s, half):
                x_off = half if (y // half) % 2 == 0 else 0
                for x in range(x_off, s, step):
                    total, count = 0.0, 0
                    for dy, dx in ((-half, 0), (half, 0), (0, -half), (0, half)):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < s and 0 <= nx < s:
                            total += g[ny][nx]
                            count += 1
                    g[y][x] = total / count + rng.uniform(-scale, scale)

            scale *= roughness
            step = half

        self._normalize()
        return self

    def get(self, y: int, x: int) -> float:
        return self.data[y][x]

    def set(self, y: int, x: int, v: float) -> None:
        self.data[y][x] = v

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _normalize(self) -> None:
        flat = [v for row in self.data for v in row]
        lo, hi = min(flat), max(flat)
        span = hi - lo or 1.0
        for y in range(self.size):
            for x in range(self.size):
                self.data[y][x] = (self.data[y][x] - lo) / span
