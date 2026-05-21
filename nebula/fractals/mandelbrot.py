"""Mandelbrot set: z_{n+1} = z_n^2 + c"""

import numpy as np


def mandelbrot(
    width: int,
    height: int,
    x_min: float = -2.5,
    x_max: float = 1.0,
    y_min: float = -1.25,
    y_max: float = 1.25,
    max_iter: int = 256,
) -> np.ndarray:
    """
    Compute the Mandelbrot set.

    Returns a 2D array of smooth iteration counts normalized to [0, 1].
    Uses smooth (continuous) coloring via the escape-time algorithm.
    """
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    c = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    z = np.zeros_like(c)
    iterations = np.zeros(c.shape, dtype=float)
    mask = np.ones(c.shape, dtype=bool)

    for i in range(max_iter):
        z[mask] = z[mask] ** 2 + c[mask]
        escaped = mask & (np.abs(z) > 2.0)
        # Smooth coloring: fractional escape count
        if np.any(escaped):
            modulus = np.abs(z[escaped])
            log_z = np.log(np.maximum(modulus, 1.0))
            inner = np.maximum(log_z, 1e-10)
            smooth = i + 1 - np.log(np.log(inner)) / np.log(2)
            iterations[escaped] = np.clip(np.nan_to_num(smooth, nan=i), 0, max_iter)
        mask[escaped] = False
        if not np.any(mask):
            break

    # Points that never escaped stay at 0
    result = iterations / max_iter
    return result
