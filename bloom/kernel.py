"""Convolution kernels and growth mappings for the Bloom automaton.

Bloom belongs to the same family as Lenia and SmoothLife: a single real-valued
grid is repeatedly convolved with a radial kernel, the convolution result is
passed through a bell-shaped "growth" function, and the result nudges each
cell up or down. Unlike Conway's Game of Life, every quantity is continuous,
which is what lets stable, organism-like blobs emerge and glide around.
"""

from __future__ import annotations

import numpy as np


def ring_kernel(size: int, shells: list[tuple[float, float, float]]) -> np.ndarray:
    """Build a radial kernel as a sum of Gaussian "shells".

    Each shell is ``(radius, width, weight)`` where ``radius`` and ``width``
    are expressed as a fraction of the kernel's half-size. The kernel is
    normalized so its values sum to 1, which keeps the convolution result
    (the "neighborhood potential") in a predictable range.
    """
    half = (size - 1) / 2.0
    y, x = np.mgrid[0:size, 0:size].astype(np.float64)
    r = np.sqrt((y - half) ** 2 + (x - half) ** 2) / half

    k = np.zeros((size, size), dtype=np.float64)
    for radius, width, weight in shells:
        k += weight * np.exp(-((r - radius) ** 2) / (2 * width ** 2))

    k[r > 1.0] = 0.0
    total = k.sum()
    if total > 0:
        k /= total
    return k


def build_kernel(
    world_shape: tuple[int, int],
    radius: int,
    shells: list[tuple[float, float, float]],
) -> np.ndarray:
    """Build the FFT of a ring kernel, padded and centered for a given world.

    Returns the kernel already transformed with ``np.fft.fft2`` so that
    :class:`bloom.world.World` only has to multiply spectra each step.
    """
    size = radius * 2 + 1
    k = ring_kernel(size, shells)

    padded = np.zeros(world_shape, dtype=np.float64)
    padded[:size, :size] = k
    # Center the kernel on (0, 0) using a toroidal shift so convolution via
    # FFT lines up with the world's wrap-around boundary.
    padded = np.roll(padded, (-radius, -radius), axis=(0, 1))
    return np.fft.fft2(padded)


def growth(u: np.ndarray, mu: float, sigma: float) -> np.ndarray:
    """Map neighborhood potential ``u`` to a growth rate in [-1, 1].

    A Gaussian bump centered at ``mu``: cells whose neighborhood potential is
    near ``mu`` grow, cells far from it shrink.
    """
    return 2.0 * np.exp(-((u - mu) ** 2) / (2.0 * sigma ** 2)) - 1.0
