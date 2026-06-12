"""A small gallery of attraction-matrix rule sets.

Each preset is a square matrix ``A`` where ``A[i, j]`` is the force that species
``j`` exerts on species ``i`` in their shared "social" band (positive = pulled
together, negative = pushed apart). Tiny changes to these numbers produce wildly
different emergent behaviour -- cells, chases, chains, or chaos.
"""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Preset:
    name: str
    description: str
    matrix: np.ndarray
    colors: tuple[tuple[int, int, int], ...]
    r_max: float = 0.10
    force_factor: float = 8.0
    friction: float = 0.85


# Each type self-attracts (forms a blob) but repels its neighbour in the cycle,
# which keeps the blobs from merging and produces drifting, membrane-like cells.
_CELLS = np.array(
    [
        [0.5, -0.3, 0.0, 0.0, -0.3],
        [-0.3, 0.5, -0.3, 0.0, 0.0],
        [0.0, -0.3, 0.5, -0.3, 0.0],
        [0.0, 0.0, -0.3, 0.5, -0.3],
        [-0.3, 0.0, 0.0, -0.3, 0.5],
    ]
)

# A three-way rock-paper-scissors chase: each species flees the one ahead of it
# in the cycle and is drawn toward the one behind, producing rotating vortices.
_CHASE = np.array(
    [
        [0.0, 0.7, -1.0],
        [-1.0, 0.0, 0.7],
        [0.7, -1.0, 0.0],
    ]
)

# A dense, mostly-repulsive web of six species with no symmetry -- nothing
# settles, so the whole system stays in turbulent, swirling motion.
_CHAOS = np.array(
    [
        [0.4, 0.6, -0.7, 0.2, -0.5, 0.8],
        [-0.8, 0.3, 0.5, -0.6, 0.7, -0.2],
        [0.6, -0.4, 0.2, 0.8, -0.3, -0.6],
        [-0.5, 0.7, -0.8, 0.1, 0.6, 0.4],
        [0.3, -0.6, 0.4, -0.7, 0.2, 0.9],
        [-0.7, 0.5, -0.2, 0.6, -0.9, 0.3],
    ]
)

# Mostly repulsive with mild self-attraction -- particles spread into many tight,
# stable little clusters that occasionally drift and merge.
_SMALL_CLUSTERS = np.array(
    [
        [0.3, -0.6, -0.6, -0.6],
        [-0.6, 0.3, -0.6, -0.6],
        [-0.6, -0.6, 0.3, -0.6],
        [-0.6, -0.6, -0.6, 0.3],
    ]
)

PRESETS: dict[str, Preset] = {
    "cells": Preset(
        name="cells",
        description="Self-attracting blobs that repel their cyclic neighbour, "
        "forming drifting cell-like membranes.",
        matrix=_CELLS,
        colors=(
            (240, 80, 90),
            (240, 180, 60),
            (110, 220, 110),
            (90, 170, 240),
            (190, 110, 240),
        ),
    ),
    "chase": Preset(
        name="chase",
        description="A rock-paper-scissors of three species, each fleeing one "
        "neighbour and chasing the other -- endless rotating vortices.",
        matrix=_CHASE,
        colors=((250, 90, 90), (90, 220, 140), (90, 150, 250)),
        r_max=0.14,
        force_factor=10.0,
    ),
    "chaos": Preset(
        name="chaos",
        description="A dense, asymmetric web of six species with no fixed "
        "points -- turbulent, ever-shifting flow.",
        matrix=_CHAOS,
        colors=(
            (250, 90, 90),
            (250, 180, 70),
            (240, 240, 90),
            (110, 230, 120),
            (100, 170, 250),
            (200, 110, 250),
        ),
        r_max=0.12,
        force_factor=9.0,
        friction=0.8,
    ),
    "small_clusters": Preset(
        name="small_clusters",
        description="Mild self-attraction plus broad repulsion -- particles "
        "settle into many small, stable clusters.",
        matrix=_SMALL_CLUSTERS,
        colors=((240, 100, 120), (250, 200, 80), (120, 220, 160), (110, 170, 250)),
        r_max=0.08,
        force_factor=7.0,
    ),
}


def get_preset(name: str) -> Preset:
    try:
        return PRESETS[name]
    except KeyError as exc:
        available = ", ".join(sorted(PRESETS))
        raise KeyError(f"Unknown preset {name!r}. Available presets: {available}") from exc
