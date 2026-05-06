"""Rule functions: each maps an (H, W) uint8 grid to the next generation."""

import numpy as np
from typing import Callable, Set


# ---------------------------------------------------------------------------
# Neighbor counting (Moore neighbourhood, toroidal wrap)
# ---------------------------------------------------------------------------

def _neighbors(cells: np.ndarray) -> np.ndarray:
    """Count live Moore-neighbourhood cells for every position."""
    n = np.zeros_like(cells, dtype=np.int32)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue
            n += np.roll(np.roll(cells > 0, dy, axis=0), dx, axis=1).astype(np.int32)
    return n


# ---------------------------------------------------------------------------
# Built-in rules
# ---------------------------------------------------------------------------

def life_rule(cells: np.ndarray) -> np.ndarray:
    """Conway's Game of Life — B3/S23."""
    n = _neighbors(cells)
    return ((n == 3) | ((cells == 1) & (n == 2))).astype(np.uint8)


def highlife_rule(cells: np.ndarray) -> np.ndarray:
    """HighLife — B36/S23.  Contains self-replicating patterns."""
    n = _neighbors(cells)
    born = (n == 3) | (n == 6)
    survive = (n == 2) | (n == 3)
    return (born | ((cells == 1) & survive)).astype(np.uint8)


def seeds_rule(cells: np.ndarray) -> np.ndarray:
    """Seeds — B2/S.  Explosive growth; every cell dies each step."""
    n = _neighbors(cells)
    return ((cells == 0) & (n == 2)).astype(np.uint8)


def day_and_night_rule(cells: np.ndarray) -> np.ndarray:
    """Day & Night — B3678/S34678.  Dead/alive are symmetric."""
    n = _neighbors(cells)
    born = np.isin(n, [3, 6, 7, 8]) & (cells == 0)
    survive = np.isin(n, [3, 4, 6, 7, 8]) & (cells == 1)
    return (born | survive).astype(np.uint8)


def maze_rule(cells: np.ndarray) -> np.ndarray:
    """Maze — B3/S12345.  Carves labyrinthine corridors."""
    n = _neighbors(cells)
    born = (n == 3) & (cells == 0)
    survive = np.isin(n, [1, 2, 3, 4, 5]) & (cells == 1)
    return (born | survive).astype(np.uint8)


def brian_brain_rule(cells: np.ndarray) -> np.ndarray:
    """Brian's Brain — 3-state CA.  Produces persistent electron-like signals.

    States: 0 = dead  |  1 = firing  |  2 = refractory
    """
    firing = (cells == 1).astype(np.int32)
    n_fire = np.zeros_like(cells, dtype=np.int32)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue
            n_fire += np.roll(np.roll(firing, dy, axis=0), dx, axis=1)

    new = np.zeros_like(cells)
    new[(cells == 0) & (n_fire == 2)] = 1   # dead → firing
    new[cells == 1] = 2                      # firing → refractory
    # refractory → dead (stays 0)
    return new


def custom_bs_rule(birth: Set[int], survive: Set[int]) -> Callable:
    """Factory that produces a B/S rule function from two neighbour-count sets."""
    b_arr = np.array(sorted(birth), dtype=np.int32)
    s_arr = np.array(sorted(survive), dtype=np.int32)

    def rule(cells: np.ndarray) -> np.ndarray:
        n = _neighbors(cells)
        born = np.isin(n, b_arr) & (cells == 0)
        survived = np.isin(n, s_arr) & (cells == 1)
        return (born | survived).astype(np.uint8)

    rule.__name__ = f"B{''.join(map(str,birth))}/S{''.join(map(str,survive))}"
    return rule


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

RULES: dict[str, Callable] = {
    "life": life_rule,
    "highlife": highlife_rule,
    "seeds": seeds_rule,
    "day_and_night": day_and_night_rule,
    "maze": maze_rule,
    "brain": brian_brain_rule,
}

RULE_DESCRIPTIONS: dict[str, str] = {
    "life":          "Conway's Game of Life (B3/S23) — the timeless classic",
    "highlife":      "HighLife (B36/S23) — harbours self-replicating patterns",
    "seeds":         "Seeds (B2/S) — explosive growth that always dies out",
    "day_and_night": "Day & Night (B3678/S34678) — dead and alive are symmetric",
    "maze":          "Maze (B3/S12345) — carves infinite labyrinthine corridors",
    "brain":         "Brian's Brain (3-state) — persistent electron-like signals",
    "ant":           "Langton's Ant — Turing-complete 2-D Turing machine",
}
