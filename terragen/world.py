"""World data model and procedural generation pipeline."""

from __future__ import annotations

import numpy as np

from .biomes import (
    BEACH_LEVEL,
    MOUNTAIN_LEVEL,
    PEAK_LEVEL,
    SEA_LEVEL,
    Biome,
    get_biome,
)
from .names import generate_city_name, generate_world_name
from .noise import continent_mask, fractal_noise

_WATER_BIOMES = {Biome.DEEP_OCEAN, Biome.OCEAN, Biome.SHALLOW_WATER}
_CITY_BIOMES = {
    Biome.GRASSLAND,
    Biome.FOREST,
    Biome.DECIDUOUS_FOREST,
    Biome.SAVANNA,
    Biome.TROPICAL_FOREST,
}


class World:
    def __init__(self, width: int = 140, height: int = 45, seed: int | None = None):
        self.width = width
        self.height = height
        self.seed = seed if seed is not None else int(np.random.randint(1, 999_999))

        self.heightmap: np.ndarray | None = None
        self.moisture_map: np.ndarray | None = None
        self.temperature_map: np.ndarray | None = None
        self.biome_map: np.ndarray | None = None

        self.rivers: list[list[tuple[int, int]]] = []
        self.river_cells: set[tuple[int, int]] = set()
        # (row, col, is_capital, name)
        self.cities: list[tuple[int, int, bool, str]] = []
        self.world_name: str = ""

    # ------------------------------------------------------------------
    def generate(self) -> "World":
        rng = np.random.default_rng(self.seed)
        s = rng.integers(0, 2**31, size=12).tolist()

        # Height = continent shape blended with fBm detail
        base = fractal_noise(self.width, self.height, scale=38, octaves=7,
                             persistence=0.48, seed=s[0])
        mask = continent_mask(self.width, self.height, seed=s[1])
        self.heightmap = base * 0.45 + mask * 0.55
        self._normalise("heightmap")

        # Moisture
        self.moisture_map = fractal_noise(self.width, self.height, scale=55, octaves=4,
                                          persistence=0.6, seed=s[2])
        self._normalise("moisture_map")

        # Temperature: cosine latitude gradient + noise + altitude cooling
        lat = np.cos(np.linspace(-np.pi / 2, np.pi / 2, self.height))[:, np.newaxis]
        t_noise = fractal_noise(self.width, self.height, scale=70, octaves=3, seed=s[3])
        self.temperature_map = lat * 0.70 + t_noise * 0.30
        alt = np.where(self.heightmap > SEA_LEVEL,
                       (self.heightmap - SEA_LEVEL) / (1 - SEA_LEVEL), 0.0)
        self.temperature_map = (self.temperature_map - alt * 0.45).clip(0, 1)

        self._assign_biomes()
        self._generate_rivers(rng)
        self._place_cities(rng)
        self.world_name = generate_world_name(np.random.default_rng(s[10]))
        return self

    # ------------------------------------------------------------------
    def _normalise(self, attr: str) -> None:
        arr = getattr(self, attr)
        lo, hi = arr.min(), arr.max()
        setattr(self, attr, (arr - lo) / (hi - lo + 1e-9))

    def _assign_biomes(self) -> None:
        H, W = self.height, self.width
        bmap = [[None] * W for _ in range(H)]
        for y in range(H):
            for x in range(W):
                bmap[y][x] = get_biome(
                    self.heightmap[y, x],
                    self.moisture_map[y, x],
                    self.temperature_map[y, x],
                )
        self.biome_map = bmap

    # ------------------------------------------------------------------
    def _generate_rivers(self, rng: np.random.Generator) -> None:
        sources = [
            (y, x)
            for y in range(self.height)
            for x in range(self.width)
            if self.heightmap[y, x] > MOUNTAIN_LEVEL * 0.75
        ]
        if not sources:
            return

        n = min(25, max(1, len(sources) // 15))
        idxs = rng.choice(len(sources), size=n, replace=False)
        for i in idxs:
            path = self._trace_river(*sources[i])
            if len(path) > 8:
                self.rivers.append(path)
                self.river_cells.update(path)

    def _trace_river(self, y: int, x: int, max_steps: int = 600) -> list[tuple[int, int]]:
        path = [(y, x)]
        visited = {(y, x)}
        H, W = self.height, self.width

        for _ in range(max_steps):
            cur_h = self.heightmap[y, x]
            best: tuple[int, int] | None = None
            best_h = cur_h

            for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1),
                           (-1, -1), (-1, 1), (1, -1), (1, 1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < H and 0 <= nx < W and (ny, nx) not in visited:
                    h = self.heightmap[ny, nx]
                    if h < best_h:
                        best_h = h
                        best = (ny, nx)

            if best is None:
                break
            y, x = best
            path.append((y, x))
            visited.add((y, x))
            if self.heightmap[y, x] < SEA_LEVEL:
                break

        return path

    # ------------------------------------------------------------------
    def _place_cities(self, rng: np.random.Generator) -> None:
        H, W = self.height, self.width
        candidates: list[tuple[float, int, int]] = []

        for y in range(3, H - 3):
            for x in range(3, W - 3):
                if self.biome_map[y][x] not in _CITY_BIOMES:
                    continue
                score = 1.0
                # Coastal proximity bonus
                for dy in range(-5, 6):
                    for dx in range(-5, 6):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < H and 0 <= nx < W:
                            if self.biome_map[ny][nx] in _WATER_BIOMES:
                                score += 1.5
                                break
                    else:
                        continue
                    break
                if (y, x) in self.river_cells:
                    score += 2.0
                candidates.append((score, y, x))

        if not candidates:
            return

        candidates.sort(reverse=True)
        n_cities = min(14, max(3, len(candidates) // 60))
        min_dist = max(H, W) // (n_cities + 2)

        placed: list[tuple[int, int, bool]] = []
        for _, y, x in candidates:
            too_close = any(
                abs(py - y) + abs(px - x) < min_dist for py, px, _ in placed
            )
            if not too_close:
                placed.append((y, x, len(placed) == 0))
            if len(placed) >= n_cities:
                break

        name_rng = np.random.default_rng(self.seed + 7)
        self.cities = [
            (y, x, is_cap, generate_city_name(name_rng))
            for y, x, is_cap in placed
        ]

    # ------------------------------------------------------------------
    def biome_coverage(self) -> dict[str, float]:
        """Return percentage coverage for each biome."""
        from collections import Counter
        total = self.width * self.height
        counts: Counter = Counter()
        for row in self.biome_map:
            counts.update(row)
        return {b.name: round(v / total * 100, 2) for b, v in counts.items()}
