"""Moisture map: secondary Diamond-Square pass blended with ocean-proximity diffusion."""

import random
from .terrain import HeightMap


class MoistureMap:
    """Combines a noise-based base layer with coastal humidity diffusion."""

    def __init__(self, size: int, height_map: HeightMap,
                 seed: int = None, sea_level: float = 0.38):
        self.size = size
        self.sea_level = sea_level
        self._hmap = height_map
        self._rng = random.Random(seed)
        self.data: list[list[float]] = [[0.0] * size for _ in range(size)]

    def generate(self, roughness: float = 0.60) -> "MoistureMap":
        # Base layer: independent Diamond-Square pass
        base = HeightMap(self.size, seed=self._rng.randint(0, 2 ** 31))
        base.generate(roughness)
        for y in range(self.size):
            self.data[y] = base.data[y][:]

        # Ocean-proximity layer: diffuse humidity outward from sea tiles
        ocean = self._build_ocean_layer()
        self._blur(ocean, passes=10)

        # Blend: 55% fractal noise + 45% coastal influence
        for y in range(self.size):
            for x in range(self.size):
                self.data[y][x] = 0.55 * self.data[y][x] + 0.45 * ocean[y][x]

        self._normalize()
        return self

    def get(self, y: int, x: int) -> float:
        return self.data[y][x]

    # ------------------------------------------------------------------

    def _build_ocean_layer(self) -> list[list[float]]:
        s = self.size
        layer = [[0.0] * s for _ in range(s)]
        for y in range(s):
            for x in range(s):
                if self._hmap.get(y, x) < self.sea_level:
                    layer[y][x] = 1.0
        return layer

    def _blur(self, grid: list[list[float]], passes: int) -> None:
        s = self.size
        for _ in range(passes):
            new = [[0.0] * s for _ in range(s)]
            for y in range(s):
                for x in range(s):
                    total, count = 0.0, 0
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < s and 0 <= nx < s:
                                total += grid[ny][nx]
                                count += 1
                    new[y][x] = total / count
            for y in range(s):
                grid[y] = new[y]

    def _normalize(self) -> None:
        flat = [v for row in self.data for v in row]
        lo, hi = min(flat), max(flat)
        span = hi - lo or 1.0
        for y in range(self.size):
            for x in range(self.size):
                self.data[y][x] = (self.data[y][x] - lo) / span
