import numpy as np


def burning_ship(width: int, height: int,
                 x_min: float = -2.5, x_max: float = 1.5,
                 y_min: float = -2.0, y_max: float = 0.5,
                 max_iter: int = 256) -> np.ndarray:
    """
    Burning Ship fractal: z_{n+1} = (|Re(z)| + i|Im(z)|)^2 + c.

    Returns a float array of shape (height, width) with smooth iteration counts.
    """
    x = np.linspace(x_min, x_max, width, dtype=np.float64)
    y = np.linspace(y_min, y_max, height, dtype=np.float64)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    iteration = np.full(C.shape, max_iter, dtype=np.float64)
    mask = np.ones(C.shape, dtype=bool)

    for i in range(max_iter):
        r, im = Z[mask].real, Z[mask].imag
        Z[mask] = (np.abs(r) + 1j * np.abs(im)) ** 2 + C[mask]
        escaped = mask & (np.abs(Z) > 2.0)
        if escaped.any():
            absZ = np.abs(Z[escaped])
            iteration[escaped] = i + 1 - np.log(np.log(np.maximum(absZ, 1.0001))) / np.log(2)
        mask &= ~escaped

    return iteration
