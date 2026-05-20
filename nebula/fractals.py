"""Fractal computation engine using numpy for vectorised rendering."""

import numpy as np


def mandelbrot(width: int, height: int, x_min: float, x_max: float,
               y_min: float, y_max: float, max_iter: int = 256) -> np.ndarray:
    """Compute Mandelbrot set with smooth (continuous) escape-time colouring."""
    x = np.linspace(x_min, x_max, width, dtype=np.float64)
    y = np.linspace(y_min, y_max, height, dtype=np.float64)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    smooth = np.zeros(C.shape, dtype=np.float64)
    escaped = np.zeros(C.shape, dtype=bool)

    for i in range(max_iter):
        mask = ~escaped
        Z[mask] = Z[mask] ** 2 + C[mask]
        newly_escaped = mask & (np.abs(Z) > 2)
        if newly_escaped.any():
            # Smooth colouring: fractional escape count
            log_z = np.log(np.abs(Z[newly_escaped]))
            nu = np.log(log_z / np.log(2)) / np.log(2)
            smooth[newly_escaped] = i + 1 - nu
        escaped |= newly_escaped

    # Points that never escaped get 0
    smooth[~escaped] = 0
    return smooth


def julia(width: int, height: int, x_min: float, x_max: float,
          y_min: float, y_max: float, c: complex,
          max_iter: int = 256) -> np.ndarray:
    """Compute Julia set for a given complex parameter c."""
    x = np.linspace(x_min, x_max, width, dtype=np.float64)
    y = np.linspace(y_min, y_max, height, dtype=np.float64)
    Z = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    smooth = np.zeros(Z.shape, dtype=np.float64)
    escaped = np.zeros(Z.shape, dtype=bool)

    for i in range(max_iter):
        mask = ~escaped
        Z[mask] = Z[mask] ** 2 + c
        newly_escaped = mask & (np.abs(Z) > 2)
        if newly_escaped.any():
            log_z = np.log(np.abs(Z[newly_escaped]))
            nu = np.log(log_z / np.log(2)) / np.log(2)
            smooth[newly_escaped] = i + 1 - nu
        escaped |= newly_escaped

    smooth[~escaped] = 0
    return smooth


def burning_ship(width: int, height: int, x_min: float, x_max: float,
                 y_min: float, y_max: float, max_iter: int = 256) -> np.ndarray:
    """Compute the Burning Ship fractal."""
    x = np.linspace(x_min, x_max, width, dtype=np.float64)
    y = np.linspace(y_min, y_max, height, dtype=np.float64)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    smooth = np.zeros(C.shape, dtype=np.float64)
    escaped = np.zeros(C.shape, dtype=bool)

    for i in range(max_iter):
        mask = ~escaped
        Zm = np.abs(Z[mask].real) + 1j * np.abs(Z[mask].imag)
        Z[mask] = Zm ** 2 + C[mask]
        newly_escaped = mask & (np.abs(Z) > 2)
        if newly_escaped.any():
            log_z = np.log(np.abs(Z[newly_escaped]))
            nu = np.log(log_z / np.log(2)) / np.log(2)
            smooth[newly_escaped] = i + 1 - nu
        escaped |= newly_escaped

    smooth[~escaped] = 0
    return smooth
