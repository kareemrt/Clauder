"""Burning Ship fractal: z_{n+1} = (|Re(z)| + i|Im(z)|)^2 + c"""

import numpy as np


def burning_ship(
    width: int,
    height: int,
    x_min: float = -2.5,
    x_max: float = 1.5,
    y_min: float = -2.0,
    y_max: float = 0.5,
    max_iter: int = 256,
) -> np.ndarray:
    """
    Compute the Burning Ship fractal.

    The distinctive flame-like shapes emerge from folding the real and
    imaginary parts into absolute values before squaring.

    Returns a 2D array of smooth iteration counts normalized to [0, 1].
    """
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    c = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    z = np.zeros_like(c)
    iterations = np.zeros(c.shape, dtype=float)
    mask = np.ones(c.shape, dtype=bool)

    for i in range(max_iter):
        # The burning ship twist: fold before squaring
        zr = np.abs(z[mask].real)
        zi = np.abs(z[mask].imag)
        z[mask] = (zr + 1j * zi) ** 2 + c[mask]

        escaped = mask & (np.abs(z) > 2.0)
        if np.any(escaped):
            modulus = np.abs(z[escaped])
            log_z = np.log(np.maximum(modulus, 1.0))
            inner = np.maximum(log_z, 1e-10)
            smooth = i + 1 - np.log(np.log(inner)) / np.log(2)
            iterations[escaped] = np.clip(np.nan_to_num(smooth, nan=i), 0, max_iter)
        mask[escaped] = False
        if not np.any(mask):
            break

    return iterations / max_iter
