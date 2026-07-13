"""Built-in pattern library for Conway's Game of Life.

Patterns are stored as lists of (col, row) offsets. Use place_pattern()
to stamp them onto a GameOfLife instance at any position.

Categories:
  Still Lifes  — stable configurations that never change
  Oscillators  — patterns that cycle through states
  Spaceships   — patterns that translate across the grid
  Guns         — patterns that periodically emit spaceships
  Methuselahs  — small seeds that evolve for many generations
"""

from typing import List, Tuple, Optional

Cell = Tuple[int, int]

PATTERNS: dict = {
    # ── Still lifes ──────────────────────────────────────────────────────
    "block": {
        "cells": [(0,0),(1,0),(0,1),(1,1)],
        "category": "Still Life",
        "description": "2×2 block — simplest stable pattern",
    },
    "beehive": {
        "cells": [(1,0),(2,0),(0,1),(3,1),(1,2),(2,2)],
        "category": "Still Life",
        "description": "Beehive — hexagonal stable shape",
    },
    "loaf": {
        "cells": [(1,0),(2,0),(0,1),(3,1),(1,2),(3,2),(2,3)],
        "category": "Still Life",
        "description": "Loaf — asymmetric stable pattern",
    },
    "boat": {
        "cells": [(0,0),(1,0),(0,1),(2,1),(1,2)],
        "category": "Still Life",
        "description": "Boat — 5-cell stable pattern",
    },
    "tub": {
        "cells": [(1,0),(0,1),(2,1),(1,2)],
        "category": "Still Life",
        "description": "Tub — diamond stable pattern",
    },

    # ── Oscillators ───────────────────────────────────────────────────────
    "blinker": {
        "cells": [(0,1),(1,1),(2,1)],
        "category": "Oscillator",
        "description": "Blinker — period-2, simplest oscillator",
        "period": 2,
    },
    "toad": {
        "cells": [(1,0),(2,0),(3,0),(0,1),(1,1),(2,1)],
        "category": "Oscillator",
        "description": "Toad — period-2 oscillator",
        "period": 2,
    },
    "beacon": {
        "cells": [(0,0),(1,0),(0,1),(3,2),(2,3),(3,3)],
        "category": "Oscillator",
        "description": "Beacon — period-2 oscillator (two blocks)",
        "period": 2,
    },
    "pulsar": {
        "cells": [
            (2,0),(3,0),(4,0),(8,0),(9,0),(10,0),
            (0,2),(5,2),(7,2),(12,2),
            (0,3),(5,3),(7,3),(12,3),
            (0,4),(5,4),(7,4),(12,4),
            (2,5),(3,5),(4,5),(8,5),(9,5),(10,5),
            (2,7),(3,7),(4,7),(8,7),(9,7),(10,7),
            (0,8),(5,8),(7,8),(12,8),
            (0,9),(5,9),(7,9),(12,9),
            (0,10),(5,10),(7,10),(12,10),
            (2,12),(3,12),(4,12),(8,12),(9,12),(10,12),
        ],
        "category": "Oscillator",
        "description": "Pulsar — period-3, large symmetric oscillator",
        "period": 3,
    },
    "pentadecathlon": {
        "cells": [
            (1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),
            (0,1),(9,1),
            (1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(8,2),
        ],
        "category": "Oscillator",
        "description": "Pentadecathlon — period-15 oscillator",
        "period": 15,
    },
    "clock": {
        "cells": [(1,0),(3,1),(0,2),(2,2),(1,3),(3,3),(2,4)],
        "category": "Oscillator",
        "description": "Clock — period-2 oscillator",
        "period": 2,
    },

    # ── Spaceships ────────────────────────────────────────────────────────
    "glider": {
        "cells": [(1,0),(2,1),(0,2),(1,2),(2,2)],
        "category": "Spaceship",
        "description": "Glider — diagonal c/4 spaceship, the icon of Life",
        "speed": "c/4 diagonal",
    },
    "lwss": {
        "cells": [
            (1,0),(4,0),
            (0,1),
            (0,2),(4,2),
            (0,3),(1,3),(2,3),(3,3),
        ],
        "category": "Spaceship",
        "description": "Lightweight Spaceship (LWSS) — horizontal c/2",
        "speed": "c/2",
    },
    "mwss": {
        "cells": [
            (2,0),
            (0,1),(4,1),
            (5,2),
            (0,3),(5,3),
            (1,4),(2,4),(3,4),(4,4),(5,4),
        ],
        "category": "Spaceship",
        "description": "Middleweight Spaceship (MWSS) — horizontal c/2",
        "speed": "c/2",
    },
    "hwss": {
        "cells": [
            (2,0),(3,0),
            (0,1),(5,1),
            (6,2),
            (0,3),(6,3),
            (1,4),(2,4),(3,4),(4,4),(5,4),(6,4),
        ],
        "category": "Spaceship",
        "description": "Heavyweight Spaceship (HWSS) — horizontal c/2",
        "speed": "c/2",
    },

    # ── Guns ──────────────────────────────────────────────────────────────
    "gosper_glider_gun": {
        "cells": [
            (24,0),
            (22,1),(24,1),
            (12,2),(13,2),(20,2),(21,2),(34,2),(35,2),
            (11,3),(15,3),(20,3),(21,3),(34,3),(35,3),
            (0,4),(1,4),(10,4),(16,4),(20,4),(21,4),
            (0,5),(1,5),(10,5),(14,5),(16,5),(17,5),(22,5),(24,5),
            (10,6),(16,6),(24,6),
            (11,7),(15,7),
            (12,8),(13,8),
        ],
        "category": "Gun",
        "description": "Gosper Glider Gun — infinite glider stream (period 30)",
        "period": 30,
    },

    # ── Methuselahs ───────────────────────────────────────────────────────
    "r_pentomino": {
        "cells": [(1,0),(2,0),(0,1),(1,1),(1,2)],
        "category": "Methuselah",
        "description": "R-pentomino — 5 cells, stabilizes at generation 1103",
        "lifespan": 1103,
    },
    "acorn": {
        "cells": [(1,0),(3,1),(0,2),(1,2),(4,2),(5,2),(6,2)],
        "category": "Methuselah",
        "description": "Acorn — 7 cells, stabilizes at generation 5206",
        "lifespan": 5206,
    },
    "diehard": {
        "cells": [(6,0),(0,1),(1,1),(1,2),(5,2),(6,2),(7,2)],
        "category": "Methuselah",
        "description": "Diehard — vanishes completely at generation 130",
        "lifespan": 130,
    },
    "pi_heptomino": {
        "cells": [(0,0),(1,0),(2,0),(0,1),(2,1),(0,2),(1,2),(2,2)],
        "category": "Methuselah",
        "description": "Pi heptomino — stabilizes at generation 173",
        "lifespan": 173,
    },

    # ── Fun / Novelty ─────────────────────────────────────────────────────
    "infinite_growth": {
        "cells": [
            (0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),
            (0,1),
            (9,2),
            (1,3),(2,3),(9,3),
            (0,4),(3,4),(9,4),
            (0,5),(9,5),
            (0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6),(8,6),(9,6),
        ],
        "category": "Novelty",
        "description": "Switch engine — triggers unbounded population growth",
    },
}

CATEGORIES = sorted(set(p["category"] for p in PATTERNS.values()))


def get_pattern(name: str) -> Optional[List[Cell]]:
    """Return list of (x, y) cells for the named pattern, or None."""
    info = PATTERNS.get(name)
    return info["cells"] if info else None


def list_patterns() -> dict:
    """Return {name: description} for all patterns."""
    return {name: info["description"] for name, info in PATTERNS.items()}


def patterns_by_category() -> dict:
    """Return {category: [name, ...]} grouped by category."""
    result: dict = {}
    for name, info in PATTERNS.items():
        cat = info.get("category", "Other")
        result.setdefault(cat, []).append(name)
    return result


def place_pattern(
    automaton,
    pattern_name: str,
    cx: int,
    cy: int,
    clear_first: bool = False,
) -> bool:
    """Place a named pattern centered at (cx, cy) on the automaton.

    Returns True on success, False if pattern name is unknown.
    """
    cells = get_pattern(pattern_name)
    if cells is None:
        return False

    if clear_first:
        automaton.clear()

    if not cells:
        return True

    min_x = min(x for x, _ in cells)
    max_x = max(x for x, _ in cells)
    min_y = min(y for _, y in cells)
    max_y = max(y for _, y in cells)

    off_x = cx - (min_x + max_x) // 2
    off_y = cy - (min_y + max_y) // 2

    for x, y in cells:
        automaton.set(x + off_x, y + off_y, True)

    return True
