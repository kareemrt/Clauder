"""Fractal noise generation for terrain synthesis."""

import numpy as np


def _smooth_noise(rng: np.random.Generator, width: int, height: int, scale: float) -> np.ndarray:
    """Single-octave value noise with smoothstep interpolation."""
    scale = max(1.0, scale)
    gw = int(np.ceil(width / scale)) + 2
    gh = int(np.ceil(height / scale)) + 2
    grid = rng.random((gh, gw))

    xs = np.arange(width) / scale
    ys = np.arange(height) / scale

    x0 = np.floor(xs).astype(int).clip(0, gw - 2)
    y0 = np.floor(ys).astype(int).clip(0, gh - 2)
    x1 = (x0 + 1).clip(0, gw - 1)
    y1 = (y0 + 1).clip(0, gh - 1)

    xf = xs - np.floor(xs)
    yf = ys - np.floor(ys)
    # Smoothstep (3t² - 2t³)
    xf = xf * xf * (3 - 2 * xf)
    yf = yf * yf * (3 - 2 * yf)

    xf = xf[np.newaxis, :]
    yf = yf[:, np.newaxis]
    x0 = x0[np.newaxis, :]
    x1 = x1[np.newaxis, :]
    y0 = y0[:, np.newaxis]
    y1 = y1[:, np.newaxis]

    return (
        grid[y0, x0] * (1 - xf) * (1 - yf)
        + grid[y0, x1] * xf * (1 - yf)
        + grid[y1, x0] * (1 - xf) * yf
        + grid[y1, x1] * xf * yf
    )


def fractal_noise(
    width: int,
    height: int,
    scale: float = 50,
    octaves: int = 6,
    persistence: float = 0.5,
    lacunarity: float = 2.0,
    seed: int | None = None,
) -> np.ndarray:
    """Fractional Brownian motion noise — sum of noise octaves at increasing frequencies."""
    rng = np.random.default_rng(seed)
    result = np.zeros((height, width))
    amplitude = 1.0
    total = 0.0
    current_scale = scale

    for _ in range(octaves):
        result += amplitude * _smooth_noise(rng, width, height, current_scale)
        total += amplitude
        amplitude *= persistence
        current_scale /= lacunarity

    return result / total


def continent_mask(width: int, height: int, seed: int | None = None) -> np.ndarray:
    """Gaussian continent blobs blended with fBm for organic coastlines."""
    rng = np.random.default_rng(seed)
    inner_seed = int(rng.integers(0, 2**31))

    noise = fractal_noise(width, height, scale=width // 3, octaves=4, seed=inner_seed)

    x = np.linspace(-1, 1, width)
    y = np.linspace(-1, 1, height)
    X, Y = np.meshgrid(x, y)

    n_blobs = int(rng.integers(2, 5))
    land = np.zeros((height, width))
    for _ in range(n_blobs):
        cx = rng.uniform(-0.35, 0.35)
        cy = rng.uniform(-0.35, 0.35)
        rx = rng.uniform(0.25, 0.55)
        ry = rng.uniform(0.20, 0.45)
        land += np.exp(-((X - cx) ** 2 / (2 * rx**2) + (Y - cy) ** 2 / (2 * ry**2)))

    land = land / land.max()
    combined = land * 0.55 + noise * 0.45
    return (combined - combined.min()) / (combined.max() - combined.min())
