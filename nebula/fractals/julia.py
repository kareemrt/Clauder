"""Julia sets: z_{n+1} = z_n^2 + c (fixed c, variable z0)"""

import numpy as np


# Famous Julia set constants
JULIA_PRESETS = {
    "spiral": (-0.7269 + 0.1889j),
    "dendrite": (0.0 + 1.0j),
    "rabbit": (-0.123 + 0.745j),
    "san_marco": (-0.75 + 0.0j),
    "douady_rabbit": (-0.1226 + 0.7449j),
    "siegel_disk": (-0.3905407 - 0.5867879j),
    "lightning": (0.285 + 0.01j),
    "galaxy": (-0.4 + 0.6j),
}


def julia(
    width: int,
    height: int,
    c: complex = (-0.7269 + 0.1889j),
    x_min: float = -1.5,
    x_max: float = 1.5,
    y_min: float = -1.5,
    y_max: float = 1.5,
    max_iter: int = 256,
) -> np.ndarray:
    """
    Compute a Julia set for a given complex constant c.

    Returns a 2D array of smooth iteration counts normalized to [0, 1].
    """
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    z = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    iterations = np.zeros(z.shape, dtype=float)
    mask = np.ones(z.shape, dtype=bool)

    for i in range(max_iter):
        z[mask] = z[mask] ** 2 + c
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
