"""Fractal computation engines using vectorized numpy operations."""

import numpy as np


def mandelbrot(width: int, height: int, x_min: float, x_max: float,
               y_min: float, y_max: float, max_iter: int) -> np.ndarray:
    """Compute the Mandelbrot set with smooth escape-time coloring."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    iteration_map = np.zeros((height, width), dtype=float)
    escaped = np.zeros((height, width), dtype=bool)

    for i in range(max_iter):
        mask = ~escaped
        Z[mask] = Z[mask] ** 2 + C[mask]
        newly_escaped = mask & (np.abs(Z) > 2.0)
        # Smooth iteration count for anti-banding
        abs_z = np.abs(Z[newly_escaped])
        iteration_map[newly_escaped] = i + 1 - np.log2(np.log2(np.maximum(abs_z, 1.0)))
        escaped |= newly_escaped

    return iteration_map


def julia(width: int, height: int, x_min: float, x_max: float,
          y_min: float, y_max: float, max_iter: int, c: complex) -> np.ndarray:
    """Compute a Julia set for constant c with smooth coloring."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    Z = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    iteration_map = np.zeros((height, width), dtype=float)
    escaped = np.zeros((height, width), dtype=bool)

    for i in range(max_iter):
        mask = ~escaped
        Z[mask] = Z[mask] ** 2 + c
        newly_escaped = mask & (np.abs(Z) > 2.0)
        abs_z = np.abs(Z[newly_escaped])
        iteration_map[newly_escaped] = i + 1 - np.log2(np.log2(np.maximum(abs_z, 1.0)))
        escaped |= newly_escaped

    return iteration_map


def burning_ship(width: int, height: int, x_min: float, x_max: float,
                 y_min: float, y_max: float, max_iter: int) -> np.ndarray:
    """Compute the Burning Ship fractal (absolute value variant of Mandelbrot)."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    iteration_map = np.zeros((height, width), dtype=float)
    escaped = np.zeros((height, width), dtype=bool)

    for i in range(max_iter):
        mask = ~escaped
        Z[mask] = (np.abs(Z[mask].real) + 1j * np.abs(Z[mask].imag)) ** 2 + C[mask]
        newly_escaped = mask & (np.abs(Z) > 2.0)
        abs_z = np.abs(Z[newly_escaped])
        iteration_map[newly_escaped] = i + 1 - np.log2(np.log2(np.maximum(abs_z, 1.0)))
        escaped |= newly_escaped

    return iteration_map


def newton(width: int, height: int, x_min: float, x_max: float,
           y_min: float, y_max: float, max_iter: int,
           tolerance: float = 1e-6) -> tuple[np.ndarray, np.ndarray]:
    """
    Newton fractal for f(z) = z^3 - 1.
    Returns (root_index, convergence_speed) arrays for coloring.
    """
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    Z = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    roots = np.array([1.0, -0.5 + 0.866025j, -0.5 - 0.866025j])
    root_map = np.full((height, width), -1, dtype=int)
    speed_map = np.zeros((height, width), dtype=float)
    converged = np.zeros((height, width), dtype=bool)

    for i in range(max_iter):
        mask = ~converged
        if not np.any(mask):
            break
        denom = 3 * Z[mask] ** 2
        safe = np.abs(denom) > 1e-10
        Z_new = Z[mask].copy()
        Z_new[safe] -= (Z_new[safe] ** 3 - 1) / denom[safe]
        Z[mask] = Z_new

        for ri, root in enumerate(roots):
            close = mask & (np.abs(Z - root) < tolerance) & ~converged
            root_map[close] = ri
            speed_map[close] = i
            converged |= close

    # Normalize speed for coloring
    max_speed = speed_map.max()
    if max_speed > 0:
        speed_map = speed_map / max_speed

    return root_map, speed_map
