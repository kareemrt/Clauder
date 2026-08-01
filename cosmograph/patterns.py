"""
Mathematical pattern generators for Cosmograph.
Each function returns either a 2D numpy array of iteration counts
or a set of (x, y) coordinate pairs depending on the pattern type.
"""

import numpy as np
import math


def mandelbrot(width: int, height: int, x_min: float = -2.5, x_max: float = 1.0,
               y_min: float = -1.25, y_max: float = 1.25, max_iter: int = 256) -> np.ndarray:
    """Compute the Mandelbrot set using smooth iteration count."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]
    Z = np.zeros_like(C, dtype=complex)
    iterations = np.zeros(C.shape, dtype=float)
    mask = np.ones(C.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask] ** 2 + C[mask]
        escaped = mask & (np.abs(Z) > 2.0)
        # Smooth coloring: fractional escape count
        if np.any(escaped):
            abs_z = np.abs(Z[escaped])
            iterations[escaped] = i + 1 - np.log2(np.log2(np.maximum(abs_z, 1.0)))
        mask[escaped] = False

    # Interior points get max_iter
    iterations[mask] = max_iter
    return np.clip(iterations, 0, max_iter)


def julia(width: int, height: int, c: complex = -0.7 + 0.27j,
          x_range: tuple = (-1.8, 1.8), y_range: tuple = (-1.8, 1.8),
          max_iter: int = 256) -> np.ndarray:
    """Compute a Julia set for a given parameter c."""
    x = np.linspace(x_range[0], x_range[1], width)
    y = np.linspace(y_range[0], y_range[1], height)
    Z = x[np.newaxis, :] + 1j * y[:, np.newaxis]
    iterations = np.zeros(Z.shape, dtype=float)
    mask = np.ones(Z.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask] ** 2 + c
        escaped = mask & (np.abs(Z) > 2.0)
        if np.any(escaped):
            abs_z = np.abs(Z[escaped])
            iterations[escaped] = i + 1 - np.log2(np.log2(np.maximum(abs_z, 1.0)))
        mask[escaped] = False

    iterations[mask] = max_iter
    return np.clip(iterations, 0, max_iter)


def burning_ship(width: int, height: int, x_min: float = -2.5, x_max: float = 1.5,
                 y_min: float = -2.0, y_max: float = 0.5, max_iter: int = 256) -> np.ndarray:
    """Compute the Burning Ship fractal — a fiery sibling of the Mandelbrot set."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]
    Z = np.zeros_like(C, dtype=complex)
    iterations = np.zeros(C.shape, dtype=float)
    mask = np.ones(C.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = (np.abs(Z[mask].real) + 1j * np.abs(Z[mask].imag)) ** 2 + C[mask]
        escaped = mask & (np.abs(Z) > 2.0)
        if np.any(escaped):
            abs_z = np.abs(Z[escaped])
            iterations[escaped] = i + 1 - np.log2(np.log2(np.maximum(abs_z, 1.0)))
        mask[escaped] = False

    iterations[mask] = max_iter
    return np.clip(iterations, 0, max_iter)


def ulam_spiral(size: int) -> np.ndarray:
    """
    Generate an Ulam spiral — integers arranged in a clockwise spiral with
    prime numbers highlighted, revealing mysterious diagonal alignments.
    Returns a binary grid: 1 = prime, 0 = composite.
    """
    n = size * size

    # Sieve of Eratosthenes
    is_prime = np.ones(n + 1, dtype=bool)
    is_prime[0:2] = False
    for p in range(2, int(n ** 0.5) + 1):
        if is_prime[p]:
            is_prime[p * p::p] = False

    # Spiral mapping: start at center, go right then spiral
    grid = np.zeros((size, size), dtype=np.uint8)
    x, y = size // 2, size // 2
    dx, dy = 1, 0   # start moving right
    num = 1
    steps = 1
    step_count = 0
    turns = 0

    for _ in range(n):
        if 0 <= x < size and 0 <= y < size and num <= n:
            if is_prime[num]:
                grid[y][x] = 1
        num += 1
        x += dx
        step_count += 1
        if step_count == steps:
            step_count = 0
            dx, dy = -dy, dx  # turn left
            turns += 1
            if turns % 2 == 0:
                steps += 1

    return grid


def fibonacci_sunflower(n_seeds: int, canvas_size: int) -> list:
    """
    Generate Fibonacci sunflower seed positions using the golden angle.
    Returns list of (x, y, radius) tuples for each seed.
    """
    golden_angle = math.pi * (3 - math.sqrt(5))  # ~137.508°
    center = canvas_size / 2
    scale = canvas_size * 0.45 / math.sqrt(n_seeds)
    seeds = []
    for i in range(n_seeds):
        r = math.sqrt(i) * scale
        theta = i * golden_angle
        x = center + r * math.cos(theta)
        y = center + r * math.sin(theta)
        seed_radius = max(0.8, scale * 0.5)
        seeds.append((x, y, seed_radius, i))
    return seeds


def lissajous(a: int = 3, b: int = 4, delta: float = math.pi / 4,
              n_points: int = 10000) -> tuple:
    """
    Generate a Lissajous figure — the interference pattern of two perpendicular
    sinusoidal oscillations. Returns (x_array, y_array) normalized to [0, 1].
    """
    t = np.linspace(0, 2 * math.pi, n_points)
    x = np.sin(a * t + delta)
    y = np.sin(b * t)
    # Normalize to [0, 1]
    x = (x + 1) / 2
    y = (y + 1) / 2
    return x, y


def dragon_curve(iterations: int = 14) -> list:
    """
    Generate the Dragon Curve fractal via paper-fold unfolding.
    Returns a list of (x, y) vertices.
    """
    # Start with a single fold sequence
    folds = [1]  # 1 = turn right, 0 = turn left
    for _ in range(iterations - 1):
        folds = folds + [1] + [1 - f for f in reversed(folds)]

    # Walk the curve
    x, y = 0.0, 0.0
    dx, dy = 1.0, 0.0
    vertices = [(x, y)]

    for fold in folds:
        x += dx
        y += dy
        vertices.append((x, y))
        if fold == 1:  # turn right
            dx, dy = dy, -dx
        else:           # turn left
            dx, dy = -dy, dx

    return vertices


JULIA_PRESETS = {
    "dendrite":     -0.0 + 1.0j,
    "spiral":       -0.7269 + 0.1889j,
    "douady_rabbit": -0.123 + 0.745j,
    "san_marco":    -0.75 + 0.0j,
    "siegel_disk":  -0.3905407802 + 0.5867879073j,
    "classic":      -0.7 + 0.27j,
    "lightning":    0.285 + 0.01j,
}
