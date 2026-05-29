"""City placement: score land tiles by habitability and river proximity."""

import random
from .terrain import HeightMap
from .biomes import SEA_LEVEL, MOUNTAIN_LEVEL
from .rivers import RiverSystem


class CitySystem:
    """Places cities on habitable land, preferring river-adjacent tiles."""

    def __init__(self, height_map: HeightMap, river_system: RiverSystem,
                 seed: int = None):
        self.hmap = height_map
        self.rivers = river_system
        self.size = height_map.size
        self.cities: list[tuple[int, int]] = []
        self._rng = random.Random(seed)

    def generate(self, num_cities: int = 8, min_dist: int = 8) -> "CitySystem":
        s, h, r = self.size, self.hmap, self.rivers
        rng = self._rng

        low  = SEA_LEVEL + 0.06
        high = MOUNTAIN_LEVEL * 0.82

        scored: list[tuple[float, int, int]] = []
        for y in range(s):
            for x in range(s):
                hv = h.get(y, x)
                if not (low <= hv <= high):
                    continue
                near_river = any(
                    r.is_river(y + dy, x + dx)
                    for dy in range(-3, 4)
                    for dx in range(-3, 4)
                    if 0 <= y + dy < s and 0 <= x + dx < s
                )
                score = rng.random() + (0.55 if near_river else 0.0)
                scored.append((score, y, x))

        scored.sort(reverse=True)

        for _, cy, cx in scored:
            if len(self.cities) >= num_cities:
                break
            if all(
                (cy - ey) ** 2 + (cx - ex) ** 2 >= min_dist ** 2
                for ey, ex in self.cities
            ):
                self.cities.append((cy, cx))

        return self

    def is_city(self, y: int, x: int) -> bool:
        return (y, x) in self.cities
