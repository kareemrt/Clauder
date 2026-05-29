"""World: orchestrates all generation systems into a single coherent map."""

from __future__ import annotations
from .terrain import HeightMap
from .moisture import MoistureMap
from .biomes import classify, SEA_LEVEL
from .rivers import RiverSystem
from .cities import CitySystem


class World:
    """A fully generated procedural world.

    Parameters
    ----------
    size      : map edge length; must be 2^k + 1 (33, 65, 129, 257 …)
    seed      : integer seed for reproducible generation
    num_rivers: target number of river paths
    num_cities: target number of city sites
    verbose   : print progress lines during generation
    """

    def __init__(
        self,
        size: int = 65,
        seed: int = 42,
        num_rivers: int = 12,
        num_cities: int = 8,
        verbose: bool = True,
    ):
        self.size = size
        self.seed = seed

        def _log(msg: str) -> None:
            if verbose:
                print(f"  {msg}", flush=True)

        _log(f"Generating terrain  (seed={seed}, {size}×{size})")
        self.height   = HeightMap(size, seed=seed).generate(roughness=0.55)

        _log("Simulating moisture …")
        self.moisture = MoistureMap(size, self.height, seed=seed ^ 0xDEAD).generate()

        _log(f"Carving {num_rivers} rivers …")
        self.rivers   = RiverSystem(self.height, seed=seed ^ 0xBEEF).generate(num_rivers)

        _log(f"Placing {num_cities} cities …")
        self.cities   = CitySystem(self.height, self.rivers, seed=seed ^ 0xCAFE).generate(num_cities)

        _log("Classifying biomes …")
        self._biomes: list[list[str]] = [[""] * size for _ in range(size)]
        for y in range(size):
            for x in range(size):
                if self.cities.is_city(y, x):
                    self._biomes[y][x] = "CITY"
                elif self.rivers.is_river(y, x) and self.height.get(y, x) >= SEA_LEVEL:
                    self._biomes[y][x] = "RIVER"
                else:
                    self._biomes[y][x] = classify(
                        self.height.get(y, x),
                        self.moisture.get(y, x),
                    )

    # ------------------------------------------------------------------

    def biome_at(self, y: int, x: int) -> str:
        return self._biomes[y][x]

    def stats(self) -> dict[str, float]:
        from collections import Counter
        counts: Counter[str] = Counter(
            self._biomes[y][x] for y in range(self.size) for x in range(self.size)
        )
        total = self.size * self.size
        return {k: round(100 * v / total, 1) for k, v in counts.most_common()}
