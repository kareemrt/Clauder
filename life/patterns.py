import numpy as np

_GLIDER = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 1],
], dtype=np.uint8)

_BLINKER = np.array([[1, 1, 1]], dtype=np.uint8)

_TOAD = np.array([
    [0, 1, 1, 1],
    [1, 1, 1, 0],
], dtype=np.uint8)

_BEACON = np.array([
    [1, 1, 0, 0],
    [1, 1, 0, 0],
    [0, 0, 1, 1],
    [0, 0, 1, 1],
], dtype=np.uint8)

_BLOCK = np.array([[1, 1], [1, 1]], dtype=np.uint8)

_BEEHIVE = np.array([
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [0, 1, 1, 0],
], dtype=np.uint8)

_LOAF = np.array([
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [0, 1, 0, 1],
    [0, 0, 1, 0],
], dtype=np.uint8)

_PULSAR = np.array([
    [0,0,1,1,1,0,0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [0,0,1,1,1,0,0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,0],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,0],
], dtype=np.uint8)

# Gosper Glider Gun — period-30 gun producing gliders
_GLIDER_GUN = np.zeros((9, 36), dtype=np.uint8)
for r, c in [
    (4,0),(4,1),(5,0),(5,1),
    (4,10),(5,10),(6,10),(3,11),(7,11),(2,12),(8,12),(2,13),(8,13),
    (5,14),(3,15),(7,15),(4,16),(5,16),(6,16),(5,17),
    (2,20),(3,20),(4,20),(2,21),(3,21),(4,21),(1,22),(5,22),
    (0,24),(1,24),(5,24),(6,24),
    (2,34),(3,34),(2,35),(3,35),
]:
    _GLIDER_GUN[r, c] = 1

# LWSS — lightweight spaceship
_LWSS = np.array([
    [0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 0],
], dtype=np.uint8)

# Pentadecathlon — period-15 oscillator
_PENTADECATHLON = np.array([
    [0,0,1,0,0,0,0,1,0,0],
    [1,1,0,1,1,1,1,0,1,1],
    [0,0,1,0,0,0,0,1,0,0],
], dtype=np.uint8)

PATTERNS: dict[str, np.ndarray] = {
    "glider": _GLIDER,
    "blinker": _BLINKER,
    "toad": _TOAD,
    "beacon": _BEACON,
    "block": _BLOCK,
    "beehive": _BEEHIVE,
    "loaf": _LOAF,
    "pulsar": _PULSAR,
    "glider_gun": _GLIDER_GUN,
    "lwss": _LWSS,
    "pentadecathlon": _PENTADECATHLON,
}

PATTERN_INFO: dict[str, str] = {
    "glider": "Period-4 spaceship — travels diagonally across the board",
    "blinker": "Period-2 oscillator — simplest possible oscillator",
    "toad": "Period-2 oscillator — two rows of three offset by one",
    "beacon": "Period-2 oscillator — two offset 2×2 blocks",
    "block": "Still life — 2×2 square, the simplest stable pattern",
    "beehive": "Still life — hexagonal cluster, very common in random fields",
    "loaf": "Still life — slightly asymmetric hexagonal cluster",
    "pulsar": "Period-3 oscillator — one of the most common large oscillators",
    "glider_gun": "Period-30 gun — Gosper's famous infinite-glider factory",
    "lwss": "Lightweight spaceship — travels horizontally at c/2",
    "pentadecathlon": "Period-15 oscillator — ten cells in a row with tweaks",
}
