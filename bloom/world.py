"""The simulation grid and its update rule."""

from __future__ import annotations

import numpy as np

from .kernel import build_kernel, growth


class World:
    """A toroidal grid of cell values in ``[0, 1]`` evolving under Bloom's rule."""

    def __init__(
        self,
        height: int,
        width: int,
        radius: int = 13,
        shells: list[tuple[float, float, float]] | None = None,
        mu: float = 0.15,
        sigma: float = 0.017,
        dt: float = 0.1,
        seed: int | None = None,
    ) -> None:
        self.height = height
        self.width = width
        self.radius = radius
        self.shells = shells or [(0.5, 0.15, 1.0)]
        self.mu = mu
        self.sigma = sigma
        self.dt = dt
        self.rng = np.random.default_rng(seed)

        self.state = np.zeros((height, width), dtype=np.float64)
        self._kernel_fft = build_kernel((height, width), radius, self.shells)

    def step(self) -> None:
        """Advance the world by one timestep, in place."""
        state_fft = np.fft.fft2(self.state)
        potential = np.real(np.fft.ifft2(state_fft * self._kernel_fft))
        delta = growth(potential, self.mu, self.sigma)
        self.state = np.clip(self.state + self.dt * delta, 0.0, 1.0)

    def seed_random(self, density: float = 0.3, patch: int | None = None) -> None:
        """Fill the world (or a centered patch of it) with random noise."""
        patch = patch or min(self.height, self.width) // 2
        block = self.rng.random((patch, patch))
        block[block > density] = 0.0
        self.place(block, self.height // 2, self.width // 2)

    def place(self, pattern: np.ndarray, row: int, col: int) -> None:
        """Stamp ``pattern`` onto the grid centered at ``(row, col)``, wrapping at the edges."""
        ph, pw = pattern.shape
        rows = (np.arange(ph) - ph // 2 + row) % self.height
        cols = (np.arange(pw) - pw // 2 + col) % self.width
        self.state[np.ix_(rows, cols)] = np.maximum(
            self.state[np.ix_(rows, cols)], pattern
        )

    def mass(self) -> float:
        """Total "living" mass on the grid, useful for spotting die-offs/blow-ups."""
        return float(self.state.sum())
