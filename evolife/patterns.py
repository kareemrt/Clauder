"""Classic Game of Life patterns library."""

import numpy as np
from typing import Dict

# fmt: off
LIBRARY: Dict[str, np.ndarray] = {
    "glider": np.array([
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1],
    ], dtype=np.uint8),

    "lwss": np.array([  # Lightweight spaceship
        [0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 0],
    ], dtype=np.uint8),

    "pulsar": np.array([
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
    ], dtype=np.uint8),

    "blinker": np.array([
        [1, 1, 1],
    ], dtype=np.uint8),

    "toad": np.array([
        [0, 1, 1, 1],
        [1, 1, 1, 0],
    ], dtype=np.uint8),

    "beacon": np.array([
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 1, 1],
        [0, 0, 1, 1],
    ], dtype=np.uint8),

    "r_pentomino": np.array([
        [0, 1, 1],
        [1, 1, 0],
        [0, 1, 0],
    ], dtype=np.uint8),

    "acorn": np.array([
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [1, 1, 0, 0, 1, 1, 1],
    ], dtype=np.uint8),

    "diehard": np.array([
        [0, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 1, 1],
    ], dtype=np.uint8),

    "random_5x5": None,  # Placeholder, generated at runtime
}
# fmt: on


def get_pattern(name: str, seed: int = 42) -> np.ndarray:
    if name == "random_5x5":
        rng = np.random.default_rng(seed)
        return rng.integers(0, 2, size=(5, 5), dtype=np.uint8)
    if name not in LIBRARY:
        raise ValueError(f"Unknown pattern: '{name}'. Available: {list(LIBRARY)}")
    return LIBRARY[name].copy()


def random_genome(size: int = 10, rng: np.random.Generator = None) -> np.ndarray:
    """Generate a random genome (NxN binary pattern)."""
    if rng is None:
        rng = np.random.default_rng()
    return rng.integers(0, 2, size=(size, size), dtype=np.uint8)


def list_patterns() -> list:
    return list(LIBRARY.keys())
