"""Procedural fantasy world name generator."""

from __future__ import annotations

import random

_PREFIXES = [
    "Ar", "El", "Tha", "Mor", "Sil", "Dra", "Vor", "Quel", "Bal", "Nor",
    "Eri", "Fen", "Gal", "Hra", "Iso", "Jor", "Kal", "Lun", "Myr", "Os",
    "Pyr", "Quor", "Ral", "Syl", "Tor", "Um", "Vael", "Wyn", "Xan", "Zef",
]

_MIDDLES = [
    "an", "ar", "en", "or", "in", "al", "eth", "ash", "ond", "ir",
    "ad", "om", "ul", "ys",
]

_SUFFIXES = [
    "dor", "heim", "garde", "wyn", "thas", "mir", "lon", "ria", "vale",
    "moor", "fell", "shire", "wood", "thorn", "drift", "spire", "hollow",
]

_ADJECTIVES = [
    "Sundered", "Forgotten", "Emerald", "Frozen", "Burning", "Silent",
    "Whispering", "Shattered", "Ancient", "Radiant", "Drowned", "Gilded",
    "Restless", "Hollow", "Wandering", "Eternal", "Storm-Touched", "Verdant",
]

_NOUNS = [
    "Realm", "Expanse", "Frontier", "Wilds", "Dominion", "Reach", "Isles",
    "Lands", "Continent", "Sphere", "Reaches", "Cradle", "Sprawl", "Crown",
]


def generate_world_name(seed: int) -> str:
    """Generate a deterministic fantasy world name (with epithet) from a seed."""
    rng = random.Random(seed)

    name = rng.choice(_PREFIXES)
    if rng.random() < 0.7:
        name += rng.choice(_MIDDLES)
    name += rng.choice(_SUFFIXES)
    name = name[0].upper() + name[1:]

    epithet = f"the {rng.choice(_ADJECTIVES)} {rng.choice(_NOUNS)}"
    return f"{name}, {epithet}"
