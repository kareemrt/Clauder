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
    Compute the Mandelbrot set escape-time values.

    Returns a (height, width) float array in [0, 1] where 1.0 means the
    point never escaped (inside the set).
    """
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    escaped = np.zeros(C.shape, dtype=float)
    mask = np.ones(C.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask] ** 2 + C[mask]
        newly_escaped = mask & (np.abs(Z) > 2.0)
        # Smooth colouring: fractional escape count
        escaped[newly_escaped] = i + 1 - np.log2(np.log2(np.abs(Z[newly_escaped])))
        mask[newly_escaped] = False

    # Points still in the set get value 0; everything else normalised to (0, 1]
    result = np.where(mask, 0.0, escaped / max_iter)
    return result.clip(0.0, 1.0)
