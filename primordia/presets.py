"""Named, hand-tuned configurations that reliably produce interesting
emergent behaviour.

Each preset returns a fresh :class:`~primordia.simulation.SimulationConfig`.
A ``seed`` may be supplied to override the preset's default, e.g. to get a
different starting arrangement while keeping the same interaction rules.
"""

from __future__ import annotations

import numpy as np

from primordia.simulation import SimulationConfig

# Display colors (hex) for up to 6 particle types, used by primordia.render.
PALETTE = ["#ff595e", "#ffca3a", "#8ac926", "#1982c4", "#6a4c93", "#f4a261"]


def _cyclic_chase(num_types: int, attract: float, repel: float, self_attract: float) -> np.ndarray:
    """Build a rock-paper-scissors style rule matrix.

    Each type is attracted to the "next" type (its prey) and repelled by
    the "previous" type (its predator), with mild self-cohesion. This
    cyclic asymmetry produces rotating chase patterns.
    """
    rules = np.zeros((num_types, num_types))
    for i in range(num_types):
        rules[i, i] = self_attract
        rules[i, (i + 1) % num_types] = attract
        rules[i, (i - 1) % num_types] = repel
    return rules


def cells(seed: int | None = 1) -> SimulationConfig:
    """A few species that separate into soft, slowly drifting blobs."""
    rules = np.array(
        [
            [0.6, -0.2, 0.1],
            [-0.2, 0.6, -0.2],
            [0.1, -0.2, 0.6],
        ]
    )
    return SimulationConfig(
        num_particles=300,
        num_types=3,
        rules=rules,
        r_max=0.10,
        beta=0.35,
        friction=0.88,
        force_factor=1.0,
        seed=seed,
    )


def chase(seed: int | None = 2) -> SimulationConfig:
    """Five species locked in a rock-paper-scissors chase, forming
    swirling, comet-like trails that chase one another around the
    arena."""
    rules = _cyclic_chase(num_types=5, attract=0.7, repel=-0.4, self_attract=0.15)
    return SimulationConfig(
        num_particles=450,
        num_types=5,
        rules=rules,
        r_max=0.07,
        beta=0.3,
        friction=0.9,
        force_factor=1.2,
        seed=seed,
    )


def chaos(seed: int | None = 3) -> SimulationConfig:
    """A fully random rule matrix with many species and low friction,
    producing turbulent, ever-shifting filaments."""
    rng = np.random.default_rng(seed)
    rules = rng.uniform(-1.0, 1.0, size=(6, 6))
    return SimulationConfig(
        num_particles=600,
        num_types=6,
        rules=rules,
        r_max=0.06,
        beta=0.25,
        friction=0.93,
        force_factor=1.4,
        seed=seed,
    )


def symbiosis(seed: int | None = 4) -> SimulationConfig:
    """Two mutually-attracting species wrapped in a third species that
    repels both, producing nested, pulsating clusters."""
    rules = np.array(
        [
            [0.4, 0.6, -0.5],
            [0.6, 0.4, -0.5],
            [-0.3, -0.3, 0.2],
        ]
    )
    return SimulationConfig(
        num_particles=350,
        num_types=3,
        rules=rules,
        r_max=0.09,
        beta=0.3,
        friction=0.87,
        force_factor=1.1,
        seed=seed,
    )


PRESETS = {
    "cells": cells,
    "chase": chase,
    "chaos": chaos,
    "symbiosis": symbiosis,
}


def get_preset(name: str, seed: int | None = None) -> SimulationConfig:
    """Look up a preset by name and build its configuration.

    If ``seed`` is given it overrides the preset's default seed.
    """
    try:
        builder = PRESETS[name]
    except KeyError as exc:
        available = ", ".join(sorted(PRESETS))
        raise KeyError(f"Unknown preset {name!r}. Available presets: {available}") from exc

    config = builder() if seed is None else builder(seed)
    return config
