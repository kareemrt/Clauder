"""Seed patterns and tuned parameter presets for the Bloom automaton.

Each preset bundles a kernel/growth configuration with a seed pattern that
reliably grows into an interesting organism under that configuration. They
are original creations tuned by simulating and observing the result, not
reproductions of patterns from any particular paper.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


def blob(radius: int, sharpness: float = 4.0) -> np.ndarray:
    """A radially symmetric, soft-edged disc -- the simplest seed."""
    size = radius * 2 + 1
    y, x = np.mgrid[0:size, 0:size].astype(np.float64)
    r = np.sqrt((y - radius) ** 2 + (x - radius) ** 2) / radius
    return np.clip(1.0 - r ** sharpness, 0.0, 1.0)


def comet(radius: int, sharpness: float = 3.0) -> np.ndarray:
    """An asymmetric blob (denser on one side) that tends to glide rather than sit still."""
    size = radius * 2 + 1
    y, x = np.mgrid[0:size, 0:size].astype(np.float64)
    r = np.sqrt((y - radius) ** 2 + (x - radius) ** 2) / radius
    base = np.clip(1.0 - r ** sharpness, 0.0, 1.0)
    tail = np.clip((x - radius) / radius, 0.0, 1.0) * 0.6
    return np.clip(base - tail * base, 0.0, 1.0)


def ring(radius: int, thickness: float = 0.35) -> np.ndarray:
    """A hollow ring, which tends to pulse or split as it evolves."""
    size = radius * 2 + 1
    y, x = np.mgrid[0:size, 0:size].astype(np.float64)
    r = np.sqrt((y - radius) ** 2 + (x - radius) ** 2) / radius
    return np.exp(-((r - (1 - thickness)) ** 2) / (2 * (thickness / 2) ** 2))


@dataclass(frozen=True)
class Preset:
    name: str
    description: str
    radius: int
    shells: list[tuple[float, float, float]]
    mu: float
    sigma: float
    dt: float
    seed_kind: str  # "place" or "random"
    pattern: np.ndarray | None = field(default=None, repr=False)
    density: float = 0.4


PRESETS: dict[str, Preset] = {
    "mitosis": Preset(
        name="mitosis",
        description=(
            "A single comet-shaped seed that repeatedly divides, like a cell "
            "splitting, until the whole grid is tiled with ring-shaped organisms."
        ),
        radius=13,
        shells=[(0.5, 0.15, 1.0)],
        mu=0.15,
        sigma=0.03,
        dt=0.1,
        seed_kind="place",
        pattern=comet(18),
    ),
    "pulsar": Preset(
        name="pulsar",
        description=(
            "A ring seed grown under a two-shell kernel; it blooms outward into "
            "a tiled mosaic of pulsing diamonds."
        ),
        radius=16,
        shells=[(0.3, 0.1, 0.5), (0.8, 0.12, 1.0)],
        mu=0.19,
        sigma=0.020,
        dt=0.1,
        seed_kind="place",
        pattern=ring(20),
    ),
    "colony": Preset(
        name="colony",
        description=(
            "Random noise that self-organizes directly into an evenly spaced "
            "lattice of ring-shaped cells, no single seed required."
        ),
        radius=13,
        shells=[(0.5, 0.15, 1.0)],
        mu=0.12,
        sigma=0.035,
        dt=0.1,
        seed_kind="random",
        density=0.4,
    ),
}


def list_presets() -> list[str]:
    return sorted(PRESETS)
