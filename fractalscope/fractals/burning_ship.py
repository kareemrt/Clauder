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
    Compute the Burning Ship fractal escape-time values.

    Uses the recurrence  z -> (|Re(z)| + i|Im(z)|)² + c, which produces
    a flame-like structure that gives the fractal its name.

    Returns a (height, width) float array in [0, 1].
    """
    x = np.linspace(x_min, x_max, width)
    # Flip y axis so the "ship" appears right-side-up
    y = np.linspace(y_max, y_min, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    escaped = np.zeros(C.shape, dtype=float)
    mask = np.ones(C.shape, dtype=bool)

    for i in range(max_iter):
        re = np.abs(Z.real[mask])
        im = np.abs(Z.imag[mask])
        Z[mask] = (re + 1j * im) ** 2 + C[mask]
        newly_escaped = mask & (np.abs(Z) > 2.0)
        escaped[newly_escaped] = i + 1 - np.log2(np.log2(np.abs(Z[newly_escaped])))
        mask[newly_escaped] = False

    result = np.where(mask, 0.0, escaped / max_iter)
    return result.clip(0.0, 1.0)
