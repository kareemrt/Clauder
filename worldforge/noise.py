"""Vectorized 2D Perlin noise and fractal Brownian motion (fBm)."""

from __future__ import annotations

import numpy as np


class PerlinNoise:
    """A seedable, vectorized 2D Perlin noise generator."""

    def __init__(self, seed: int = 0):
        rng = np.random.default_rng(seed)

        perm = rng.permutation(256).astype(np.int64)
        self._perm = np.concatenate([perm, perm])

        angles = rng.uniform(0, 2 * np.pi, size=256)
        gradients = np.stack([np.cos(angles), np.sin(angles)], axis=1)
        self._gradients = np.concatenate([gradients, gradients])

    @staticmethod
    def _fade(t: np.ndarray) -> np.ndarray:
        return t * t * t * (t * (t * 6 - 15) + 10)

    def _grad_dot(self, ix: np.ndarray, iy: np.ndarray, dx: np.ndarray, dy: np.ndarray) -> np.ndarray:
        idx = self._perm[(self._perm[ix] + iy) & 511]
        g = self._gradients[idx]
        return g[..., 0] * dx + g[..., 1] * dy

    def noise(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Sample noise at the given coordinates. Returns values roughly in [-1, 1]."""
        xi = np.floor(x).astype(np.int64)
        yi = np.floor(y).astype(np.int64)
        xf = x - xi
        yf = y - yi

        xi0, yi0 = xi & 255, yi & 255
        xi1, yi1 = (xi + 1) & 255, (yi + 1) & 255

        u = self._fade(xf)
        v = self._fade(yf)

        n00 = self._grad_dot(xi0, yi0, xf, yf)
        n10 = self._grad_dot(xi1, yi0, xf - 1, yf)
        n01 = self._grad_dot(xi0, yi1, xf, yf - 1)
        n11 = self._grad_dot(xi1, yi1, xf - 1, yf - 1)

        nx0 = n00 + u * (n10 - n00)
        nx1 = n01 + u * (n11 - n01)
        return nx0 + v * (nx1 - nx0)

    def fbm(
        self,
        x: np.ndarray,
        y: np.ndarray,
        octaves: int = 6,
        persistence: float = 0.5,
        lacunarity: float = 2.0,
    ) -> np.ndarray:
        """Fractal Brownian motion: a sum of noise octaves, normalized to [-1, 1]."""
        total = np.zeros_like(x, dtype=np.float64)
        amplitude = 1.0
        frequency = 1.0
        max_amplitude = 0.0

        for _ in range(octaves):
            total += self.noise(x * frequency, y * frequency) * amplitude
            max_amplitude += amplitude
            amplitude *= persistence
            frequency *= lacunarity

        return total / max_amplitude


def normalize(array: np.ndarray) -> np.ndarray:
    """Rescale an array to the [0, 1] range."""
    lo, hi = array.min(), array.max()
    if hi - lo < 1e-12:
        return np.zeros_like(array)
    return (array - lo) / (hi - lo)
