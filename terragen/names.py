"""Phonetic name generator for worlds and settlements."""

import numpy as np

_WORLD_PREFIX = [
    "Aer", "Cal", "Dor", "El", "Fal", "Gal", "Ith", "Jor", "Kel", "Lor",
    "Mor", "Nor", "Or", "Pal", "Ran", "Sol", "Tel", "Ul", "Val", "Wyr",
    "Xal", "Yor", "Zel", "Arath", "Ebon", "Kaer", "Thal", "Vorn",
]
_WORLD_SUFFIX = [
    "athia", "oria", "andar", "eldor", "ithon", "ander", "oras", "emor",
    "inor", "aleth", "ondra", "anthos", "eria", "idor", "amus", "ellion",
    "aros", "imor", "adris", "elund",
]

_CITY_PREFIX = [
    "Ash", "Bel", "Cal", "Dar", "Eden", "Fell", "Gar", "Hald", "Iren",
    "Jor", "Kal", "Lor", "Mar", "Nar", "Ost", "Port", "Rael", "Sand",
    "Tor", "Ul", "Var", "West", "Xar", "Yor", "Zeph", "Bram", "Dusk",
    "Iron", "Lake", "North", "Silver", "Stone", "Storm",
]
_CITY_SUFFIX = [
    "hold", "haven", "ford", "gate", "port", "wich", "burg", "stead",
    "wall", "keep", "mere", "moor", "vale", "fen", "brook", "fall",
    "crest", "reach", "watch", "marsh",
]


def generate_world_name(rng: np.random.Generator) -> str:
    return rng.choice(_WORLD_PREFIX) + rng.choice(_WORLD_SUFFIX)


def generate_city_name(rng: np.random.Generator) -> str:
    return rng.choice(_CITY_PREFIX) + rng.choice(_CITY_SUFFIX)
