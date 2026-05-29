"""Biome definitions and height/moisture classification (Whittaker-inspired)."""

from dataclasses import dataclass

RESET = "\033[0m"

SEA_LEVEL      = 0.38
SHORE_LEVEL    = SEA_LEVEL + 0.04
LAND_LEVEL     = SEA_LEVEL + 0.07
MOUNTAIN_LEVEL = 0.74
PEAK_LEVEL     = 0.90


@dataclass(frozen=True)
class Biome:
    name: str
    char: str
    ansi: str   # ANSI foreground escape
    walkable: bool = True


BIOMES: dict[str, Biome] = {
    "DEEP_OCEAN":       Biome("Deep Ocean",       "≈", "\033[34m",  False),
    "OCEAN":            Biome("Ocean",             "~", "\033[94m",  False),
    "COAST":            Biome("Coast",             "~", "\033[96m",  False),
    "BEACH":            Biome("Beach",             ".", "\033[93m"),
    "DESERT":           Biome("Desert",            "∙", "\033[33m"),
    "SAVANNA":          Biome("Savanna",           ",", "\033[32m"),
    "GRASSLAND":        Biome("Grassland",         '"', "\033[92m"),
    "SHRUBLAND":        Biome("Shrubland",         ";", "\033[32m"),
    "TEMPERATE_FOREST": Biome("Temperate Forest",  "♣", "\033[32m"),
    "TROPICAL_FOREST":  Biome("Tropical Forest",  "♠", "\033[92m"),
    "BOREAL_FOREST":    Biome("Boreal Forest",     "♦", "\033[36m"),
    "TUNDRA":           Biome("Tundra",            "·", "\033[37m"),
    "SNOW":             Biome("Snow",              "*", "\033[97m"),
    "MOUNTAIN":         Biome("Mountain",          "▲", "\033[90m"),
    "PEAK":             Biome("Peak",              "▲", "\033[97m"),
    "RIVER":            Biome("River",             "≈", "\033[96m",  False),
    "CITY":             Biome("City",              "★", "\033[93m"),
}


def classify(height: float, moisture: float) -> str:
    """Return biome key for a land/sea cell based on height and moisture."""
    if height < SEA_LEVEL * 0.65:
        return "DEEP_OCEAN"
    if height < SEA_LEVEL:
        return "OCEAN"
    if height < SHORE_LEVEL:
        return "COAST"
    if height < LAND_LEVEL:
        return "BEACH"
    if height > PEAK_LEVEL:
        return "PEAK"
    if height > MOUNTAIN_LEVEL:
        return "MOUNTAIN"

    # Normalise land elevation [0, 1] → temperature proxy (high = cold)
    land_t = (height - LAND_LEVEL) / (MOUNTAIN_LEVEL - LAND_LEVEL)
    temp = 1.0 - land_t * 0.85   # 1 = tropical, 0 = polar

    if temp < 0.18:
        return "TUNDRA"
    if temp < 0.35:
        return "TUNDRA" if moisture < 0.35 else "BOREAL_FOREST"
    if temp < 0.55:
        if moisture < 0.22:
            return "SHRUBLAND"
        if moisture < 0.50:
            return "GRASSLAND"
        return "TEMPERATE_FOREST"
    # Hot zone
    if moisture < 0.18:
        return "DESERT"
    if moisture < 0.42:
        return "SAVANNA"
    if moisture < 0.65:
        return "GRASSLAND"
    return "TROPICAL_FOREST"
