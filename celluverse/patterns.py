"""Built-in pattern library — 25+ classic Life patterns.

Patterns are stored as (numpy array, description, category) named-tuples.
Categories: still | osc | ship | long | gun | misc
"""

from __future__ import annotations

from typing import Dict, NamedTuple

import numpy as np


class Pattern(NamedTuple):
    cells: np.ndarray
    description: str
    category: str


def _p(rows: list[list[int]], desc: str, cat: str = "misc") -> Pattern:
    w = max(len(r) for r in rows)
    grid = np.zeros((len(rows), w), dtype=np.uint8)
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            grid[i, j] = v
    return Pattern(grid, desc, cat)


PATTERNS: Dict[str, Pattern] = {
    # ── Still Lifes ──────────────────────────────────────────────────────────
    "block": _p(
        [[1, 1], [1, 1]],
        "Simplest still life — 2×2 square",
        "still",
    ),
    "beehive": _p(
        [[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]],
        "6-cell hexagonal still life",
        "still",
    ),
    "loaf": _p(
        [[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 0]],
        "7-cell asymmetric still life",
        "still",
    ),
    "boat": _p(
        [[1, 1, 0], [1, 0, 1], [0, 1, 0]],
        "5-cell still life shaped like a boat",
        "still",
    ),
    "tub": _p(
        [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
        "4-cell diamond still life",
        "still",
    ),

    # ── Oscillators ──────────────────────────────────────────────────────────
    "blinker": _p(
        [[1, 1, 1]],
        "Period-2 — simplest oscillator",
        "osc",
    ),
    "toad": _p(
        [[0, 1, 1, 1], [1, 1, 1, 0]],
        "Period-2 oscillator",
        "osc",
    ),
    "beacon": _p(
        [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]],
        "Period-2 oscillator",
        "osc",
    ),
    "pulsar": _p(
        [
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
        ],
        "Period-3 pulsar — most common period-3 oscillator",
        "osc",
    ),
    "pentadecathlon": _p(
        [
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
        ],
        "Period-15 oscillator — longest common period",
        "osc",
    ),

    # ── Spaceships ───────────────────────────────────────────────────────────
    "glider": _p(
        [[0, 1, 0], [0, 0, 1], [1, 1, 1]],
        "Classic glider — moves diagonally every 4 gens",
        "ship",
    ),
    "lwss": _p(
        [
            [0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 0],
        ],
        "Lightweight spaceship — period-4 horizontal mover",
        "ship",
    ),
    "mwss": _p(
        [
            [0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 1, 0],  # simplified
            [0, 0, 1, 1, 1, 1],
        ],
        "Middleweight spaceship",
        "ship",
    ),

    # ── Methuselahs (long-lived small patterns) ───────────────────────────────
    "r_pentomino": _p(
        [[0, 1, 1], [1, 1, 0], [0, 1, 0]],
        "Methuselah — stabilises after 1 103 generations",
        "long",
    ),
    "diehard": _p(
        [
            [0, 0, 0, 0, 0, 0, 1, 0],
            [1, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 1, 1],
        ],
        "Methuselah — completely vanishes after 130 generations",
        "long",
    ),
    "acorn": _p(
        [
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [1, 1, 0, 0, 1, 1, 1],
        ],
        "Methuselah — stabilises after 5 206 generations",
        "long",
    ),
    "pi_heptomino": _p(
        [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
        "Pi heptomino — lives ~173 generations",
        "long",
    ),

    # ── Guns (infinite growth) ────────────────────────────────────────────────
    "gosper_gun": _p(
        [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ],
        "Gosper Glider Gun — first pattern with unbounded growth (1970)",
        "gun",
    ),

    # ── Misc ─────────────────────────────────────────────────────────────────
    "cross": _p(
        [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        "Plus/cross — quickly forms complex structures",
        "misc",
    ),
    "diamond": _p(
        [
            [0, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [1, 0, 0, 0, 1],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 0],
        ],
        "Diamond ring pattern",
        "misc",
    ),
    "infinite_1": _p(
        [[1, 0, 1, 1, 0, 1, 1, 0]],
        "Infinite growth — expands without bound",
        "misc",
    ),
    "f_pentomino": _p(
        [[0, 1, 1], [1, 1, 0], [0, 1, 0]],
        "F-pentomino — related to R-pentomino",
        "misc",
    ),
}

CATEGORIES: dict[str, str] = {
    "still": "Still Lifes",
    "osc":   "Oscillators",
    "ship":  "Spaceships",
    "long":  "Methuselahs",
    "gun":   "Guns",
    "misc":  "Miscellaneous",
}
