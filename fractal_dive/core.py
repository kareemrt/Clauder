"""
Fractal computation engine.

Mandelbrot: iterate z = z² + c from z=0, c = pixel coordinate
Julia:      iterate z = z² + c from z = pixel coordinate, c = fixed constant

Uses smooth (continuous) coloring via escape-time + magnitude for anti-banding.
"""

import numpy as np


def _smooth_iteration_count(z: np.ndarray, iteration: np.ndarray, max_iter: int) -> np.ndarray:
    """Convert integer escape counts to smooth float values for gradient coloring."""
    mask = iteration < max_iter
    # Guard against log(log(|z|)) blowing up near |z|=1 or z=0
    mag = np.where(mask, np.abs(z), 4.0)
    mag = np.maximum(mag, 1.0001)              # |z| is always >2 at escape, but clamp defensively
    inner = np.log2(mag)
    inner = np.maximum(inner, 1e-10)
    smooth_delta = np.where(mask, np.log2(inner), 0.0)
    smooth = np.where(mask, iteration.astype(float) - smooth_delta, float(max_iter))
    return np.clip(smooth, 0, max_iter)


def mandelbrot(
    width: int,
    height: int,
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    max_iter: int = 256,
) -> np.ndarray:
    """Compute Mandelbrot set, returning a [height × width] float array of smooth escape counts."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    z = np.zeros_like(C)
    iteration = np.zeros(C.shape, dtype=np.int32)
    escaped = np.zeros(C.shape, dtype=bool)

    for i in range(max_iter):
        mask = ~escaped
        z[mask] = z[mask] ** 2 + C[mask]
        newly_escaped = mask & (np.abs(z) > 2.0)
        iteration[newly_escaped] = i
        escaped |= newly_escaped

    return _smooth_iteration_count(z, iteration, max_iter)


def julia(
    width: int,
    height: int,
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    c: complex,
    max_iter: int = 256,
) -> np.ndarray:
    """Compute Julia set for a given constant c, returning a smooth escape array."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    z = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    iteration = np.zeros(z.shape, dtype=np.int32)
    escaped = np.zeros(z.shape, dtype=bool)

    for i in range(max_iter):
        mask = ~escaped
        z[mask] = z[mask] ** 2 + c
        newly_escaped = mask & (np.abs(z) > 2.0)
        iteration[newly_escaped] = i
        escaped |= newly_escaped

    return _smooth_iteration_count(z, iteration, max_iter)
