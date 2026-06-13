"""Core world generation: elevation, moisture, biomes, and rivers."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .names import generate_world_name
from .noise import PerlinNoise, normalize

SEA_LEVEL = 0.38
BEACH_LEVEL = 0.42

# Biome ids, in the order checked by classify().
BIOMES = [
    "ocean",
    "beach",
    "desert",
    "grassland",
    "forest",
    "rainforest",
    "taiga",
    "rock",
    "mountain",
    "snow",
    "river",
]

BIOME_INDEX = {name: i for i, name in enumerate(BIOMES)}

_NEIGHBORS_8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


@dataclass
class World:
    """A generated world: grids of elevation, moisture, biomes, and rivers."""

    seed: int
    width: int
    height: int
    name: str
    elevation: np.ndarray
    moisture: np.ndarray
    biome_ids: np.ndarray
    river_mask: np.ndarray
    biome_names: list[str] = field(default_factory=lambda: BIOMES)

    def biome_at(self, x: int, y: int) -> str:
        return self.biome_names[self.biome_ids[y, x]]

    def biome_counts(self) -> dict[str, int]:
        counts = {name: 0 for name in BIOMES}
        ids, freqs = np.unique(self.biome_ids, return_counts=True)
        for biome_id, freq in zip(ids, freqs):
            counts[BIOMES[biome_id]] += int(freq)
        # Rivers are overlaid separately and counted on top of land biomes.
        counts["river"] = int(self.river_mask.sum())
        return counts


def _classify_biomes(elevation: np.ndarray, moisture: np.ndarray) -> np.ndarray:
    """Assign a biome id to every cell based on elevation and moisture."""
    biome_ids = np.full(elevation.shape, BIOME_INDEX["grassland"], dtype=np.int64)

    is_ocean = elevation < SEA_LEVEL
    is_beach = (~is_ocean) & (elevation < BEACH_LEVEL)
    is_lowland = (~is_ocean) & (~is_beach) & (elevation < 0.6)
    is_highland = (~is_ocean) & (~is_beach) & (elevation >= 0.6) & (elevation < 0.8)
    is_mountain = (~is_ocean) & (~is_beach) & (elevation >= 0.8) & (elevation < 0.92)
    is_peak = elevation >= 0.92

    # Lowlands: dry -> wet
    biome_ids[is_lowland & (moisture < 0.2)] = BIOME_INDEX["desert"]
    biome_ids[is_lowland & (moisture >= 0.2) & (moisture < 0.5)] = BIOME_INDEX["grassland"]
    biome_ids[is_lowland & (moisture >= 0.5) & (moisture < 0.75)] = BIOME_INDEX["forest"]
    biome_ids[is_lowland & (moisture >= 0.75)] = BIOME_INDEX["rainforest"]

    # Highlands: dry -> wet
    biome_ids[is_highland & (moisture < 0.3)] = BIOME_INDEX["rock"]
    biome_ids[is_highland & (moisture >= 0.3) & (moisture < 0.6)] = BIOME_INDEX["taiga"]
    biome_ids[is_highland & (moisture >= 0.6)] = BIOME_INDEX["forest"]

    biome_ids[is_mountain] = BIOME_INDEX["mountain"]
    biome_ids[is_peak] = BIOME_INDEX["snow"]
    biome_ids[is_beach] = BIOME_INDEX["beach"]
    biome_ids[is_ocean] = BIOME_INDEX["ocean"]

    return biome_ids


def _apply_island_mask(elevation: np.ndarray, strength: float) -> np.ndarray:
    """Push elevation down near the map edges so landmasses form islands/continents."""
    h, w = elevation.shape
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = (w - 1) / 2, (h - 1) / 2
    dx = (xx - cx) / cx
    dy = (yy - cy) / cy
    dist = np.sqrt(dx * dx + dy * dy)
    dist = np.clip(dist, 0, 1)
    return elevation - strength * (dist ** 3)


def _generate_rivers(
    elevation: np.ndarray,
    rng: np.random.Generator,
    river_count: int,
) -> np.ndarray:
    """Trace rivers from random highland sources downhill to the sea."""
    h, w = elevation.shape
    river_mask = np.zeros((h, w), dtype=bool)

    sources = np.argwhere(elevation > 0.72)
    if len(sources) == 0 or river_count <= 0:
        return river_mask

    count = min(river_count, len(sources))
    chosen = sources[rng.choice(len(sources), size=count, replace=False)]

    max_steps = h + w
    for start_y, start_x in chosen:
        cy, cx = int(start_y), int(start_x)
        visited: set[tuple[int, int]] = set()
        for _ in range(max_steps):
            if (cy, cx) in visited:
                break
            visited.add((cy, cx))
            river_mask[cy, cx] = True

            if elevation[cy, cx] < SEA_LEVEL:
                break

            best_pos = None
            best_elev = elevation[cy, cx]
            for dy, dx in _NEIGHBORS_8:
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < h and 0 <= nx < w and elevation[ny, nx] < best_elev:
                    best_elev = elevation[ny, nx]
                    best_pos = (ny, nx)

            if best_pos is None:
                break
            cy, cx = best_pos

    return river_mask


def generate_world(
    seed: int | None = None,
    width: int = 256,
    height: int = 256,
    octaves: int = 6,
    persistence: float = 0.5,
    lacunarity: float = 2.0,
    scale: float = 4.0,
    island_strength: float = 0.9,
    river_count: int = 10,
) -> World:
    """Generate a new procedural world.

    Args:
        seed: Random seed. A random seed is chosen if None.
        width: Map width in cells.
        height: Map height in cells.
        octaves: Number of fBm octaves for elevation/moisture noise.
        persistence: Amplitude falloff per octave.
        lacunarity: Frequency growth per octave.
        scale: Number of base noise periods spanning the map.
        island_strength: How strongly edges are pulled toward ocean (0 = none).
        river_count: Number of rivers to carve from highland sources.
    """
    if seed is None:
        seed = int(np.random.default_rng().integers(0, 2**31 - 1))

    rng = np.random.default_rng(seed)

    xs = np.linspace(0, scale, width, endpoint=False)
    ys = np.linspace(0, scale, height, endpoint=False)
    xx, yy = np.meshgrid(xs, ys)

    elevation_noise = PerlinNoise(seed=seed)
    moisture_noise = PerlinNoise(seed=seed + 1)

    elevation = elevation_noise.fbm(xx, yy, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
    moisture = moisture_noise.fbm(xx, yy, octaves=octaves, persistence=persistence, lacunarity=lacunarity)

    if island_strength > 0:
        elevation = _apply_island_mask(elevation, island_strength)

    elevation = normalize(elevation)
    moisture = normalize(moisture)

    biome_ids = _classify_biomes(elevation, moisture)
    river_mask = _generate_rivers(elevation, rng, river_count)

    return World(
        seed=seed,
        width=width,
        height=height,
        name=generate_world_name(seed),
        elevation=elevation,
        moisture=moisture,
        biome_ids=biome_ids,
        river_mask=river_mask,
    )
