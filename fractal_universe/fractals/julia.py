import numpy as np


def julia(width: int, height: int, c: complex,
          x_min: float = -1.8, x_max: float = 1.8,
          y_min: float = -1.8, y_max: float = 1.8,
          max_iter: int = 256) -> np.ndarray:
    """
    Compute smooth Julia set iteration counts for a given parameter c.

    Returns a float array of shape (height, width).
    """
    x = np.linspace(x_min, x_max, width, dtype=np.float64)
    y = np.linspace(y_min, y_max, height, dtype=np.float64)
    Z = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    iteration = np.full(Z.shape, max_iter, dtype=np.float64)
    mask = np.ones(Z.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask] ** 2 + c
        escaped = mask & (np.abs(Z) > 2.0)
        if escaped.any():
            absZ = np.abs(Z[escaped])
            iteration[escaped] = i + 1 - np.log(np.log(absZ)) / np.log(2)
        mask &= ~escaped

    return iteration
