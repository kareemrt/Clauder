import numpy as np


def mandelbrot(width: int, height: int, x_min: float, x_max: float,
               y_min: float, y_max: float, max_iter: int = 256) -> np.ndarray:
    """
    Compute smooth Mandelbrot iteration counts over a grid.

    Returns a float array of shape (height, width) with values in [0, max_iter].
    Values == max_iter indicate points inside the set.
    """
    x = np.linspace(x_min, x_max, width, dtype=np.float64)
    y = np.linspace(y_min, y_max, height, dtype=np.float64)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    iteration = np.full(C.shape, max_iter, dtype=np.float64)
    mask = np.ones(C.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask] ** 2 + C[mask]
        escaped = mask & (np.abs(Z) > 2.0)
        # Smooth iteration count using the escape-radius trick
        if escaped.any():
            absZ = np.abs(Z[escaped])
            # log(log(|Z|)) / log(2) normalises the boundary
            iteration[escaped] = i + 1 - np.log(np.log(absZ)) / np.log(2)
        mask &= ~escaped

    return iteration
