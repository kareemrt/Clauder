"""River generation: flow downhill from mountain sources to the sea."""

import random
from .terrain import HeightMap
from .biomes import SEA_LEVEL


class RiverSystem:
    """Generates river paths by following the steepest-descent gradient."""

    def __init__(self, height_map: HeightMap, seed: int = None):
        self.hmap = height_map
        self.size = height_map.size
        self.cells: set[tuple[int, int]] = set()
        self._rng = random.Random(seed)

    def generate(self, num_rivers: int = 12) -> "RiverSystem":
        s, h = self.size, self.hmap

        # Candidate sources: mid-to-high elevations (not peaks, not ocean)
        candidates = [
            (y, x)
            for y in range(s)
            for x in range(s)
            if 0.62 < h.get(y, x) < 0.91
        ]
        self._rng.shuffle(candidates)

        spawned = 0
        for sy, sx in candidates:
            if spawned >= num_rivers:
                break
            path = self._trace(sy, sx)
            if len(path) >= 6:          # reject tiny trickles
                self.cells.update(path)
                spawned += 1

        return self

    def is_river(self, y: int, x: int) -> bool:
        return (y, x) in self.cells

    # ------------------------------------------------------------------

    def _trace(self, y: int, x: int) -> list[tuple[int, int]]:
        """Walk downhill from (y, x) until reaching the sea or a dead end."""
        s, h = self.size, self.hmap
        path: list[tuple[int, int]] = []
        seen: set[tuple[int, int]] = set()

        while True:
            if (y, x) in seen or h.get(y, x) < SEA_LEVEL:
                break
            seen.add((y, x))
            path.append((y, x))

            # Pick the steepest downhill 8-connected neighbour
            best_h, best = h.get(y, x), None
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dy == dx == 0:
                        continue
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < s and 0 <= nx < s:
                        nh = h.get(ny, nx)
                        if nh < best_h:
                            best_h, best = nh, (ny, nx)

            if best is None:
                break   # local minimum on land
            y, x = best

        return path
