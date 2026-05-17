"""Biome definitions and elevation/climate assignment."""

from enum import Enum


class Biome(Enum):
    DEEP_OCEAN = 0
    OCEAN = 1
    SHALLOW_WATER = 2
    BEACH = 3
    DESERT = 4
    SAVANNA = 5
    GRASSLAND = 6
    TROPICAL_FOREST = 7
    RAINFOREST = 8
    SHRUBLAND = 9
    FOREST = 10
    DECIDUOUS_FOREST = 11
    BOREAL_FOREST = 12
    TUNDRA = 13
    SNOW = 14
    MOUNTAIN = 15
    MOUNTAIN_SNOW = 16


# (character, fg_color, bg_color, display_name)
BIOME_DISPLAY: dict[Biome, tuple[str, str, str, str]] = {
    Biome.DEEP_OCEAN:       ("≋", "blue3",            "navy_blue",          "Deep Ocean"),
    Biome.OCEAN:            ("≈", "deep_sky_blue1",    "blue3",              "Ocean"),
    Biome.SHALLOW_WATER:    ("~", "sky_blue1",         "dodger_blue2",       "Shallow Water"),
    Biome.BEACH:            ("░", "khaki1",            "dark_goldenrod",     "Beach"),
    Biome.DESERT:           ("∴", "gold1",             "orange4",            "Desert"),
    Biome.SAVANNA:          ("⁚", "yellow3",           "dark_goldenrod",     "Savanna"),
    Biome.GRASSLAND:        ("·", "green3",            "dark_green",         "Grassland"),
    Biome.TROPICAL_FOREST:  ("♦", "green1",            "dark_green",         "Tropical Forest"),
    Biome.RAINFOREST:       ("♠", "bright_green",      "green4",             "Rainforest"),
    Biome.SHRUBLAND:        ("∵", "dark_khaki",        "grey30",             "Shrubland"),
    Biome.FOREST:           ("♣", "spring_green3",     "dark_green",         "Forest"),
    Biome.DECIDUOUS_FOREST: ("♧", "dark_sea_green2",   "dark_green",         "Deciduous Forest"),
    Biome.BOREAL_FOREST:    ("▴", "dark_sea_green4",   "grey23",             "Boreal Forest"),
    Biome.TUNDRA:           ("▫", "light_steel_blue",  "grey23",             "Tundra"),
    Biome.SNOW:             ("❄", "white",             "light_steel_blue1",  "Snow"),
    Biome.MOUNTAIN:         ("▲", "grey74",            "grey42",             "Mountain"),
    Biome.MOUNTAIN_SNOW:    ("△", "white",             "grey58",             "Snowy Peak"),
}

SEA_LEVEL      = 0.40
BEACH_LEVEL    = 0.44
MOUNTAIN_LEVEL = 0.72
PEAK_LEVEL     = 0.86


def get_biome(height: float, moisture: float, temperature: float) -> Biome:
    """Map elevation + climate values to a biome."""
    if height < SEA_LEVEL * 0.60:
        return Biome.DEEP_OCEAN
    if height < SEA_LEVEL:
        return Biome.OCEAN
    if height < SEA_LEVEL + 0.025:
        return Biome.SHALLOW_WATER
    if height < BEACH_LEVEL:
        return Biome.BEACH
    if height > PEAK_LEVEL:
        return Biome.MOUNTAIN_SNOW
    if height > MOUNTAIN_LEVEL:
        return Biome.MOUNTAIN

    # Land biomes — temperature × moisture table
    if temperature < 0.15:
        return Biome.SNOW
    if temperature < 0.28:
        return Biome.TUNDRA if moisture < 0.5 else Biome.BOREAL_FOREST
    if temperature < 0.42:
        if moisture < 0.30:
            return Biome.SHRUBLAND
        if moisture < 0.62:
            return Biome.FOREST
        return Biome.BOREAL_FOREST
    if temperature < 0.65:
        if moisture < 0.25:
            return Biome.DESERT
        if moisture < 0.45:
            return Biome.GRASSLAND
        if moisture < 0.70:
            return Biome.DECIDUOUS_FOREST
        return Biome.FOREST
    # Hot zone
    if moisture < 0.22:
        return Biome.DESERT
    if moisture < 0.42:
        return Biome.SAVANNA
    if moisture < 0.65:
        return Biome.TROPICAL_FOREST
    return Biome.RAINFOREST
