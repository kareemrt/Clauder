"""Core fractal computation engines using vectorized numpy operations."""

import numpy as np


def mandelbrot(width: int, height: int, x_min: float, x_max: float,
               y_min: float, y_max: float, max_iter: int) -> np.ndarray:
    """Compute the Mandelbrot set escape-time values."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    iteration_map = np.zeros(C.shape, dtype=float)
    mask = np.ones(C.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask] ** 2 + C[mask]
        escaped = mask & (np.abs(Z) > 2.0)
        # Smooth colouring: fractional escape count
        iteration_map[escaped] = i + 1 - np.log2(np.log2(np.abs(Z[escaped])))
        mask[escaped] = False

    return iteration_map


def julia(width: int, height: int, x_min: float, x_max: float,
          y_min: float, y_max: float, max_iter: int,
          c: complex) -> np.ndarray:
    """Compute a Julia set for a given constant c."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    Z = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    iteration_map = np.zeros(Z.shape, dtype=float)
    mask = np.ones(Z.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask] ** 2 + c
        escaped = mask & (np.abs(Z) > 2.0)
        iteration_map[escaped] = i + 1 - np.log2(np.log2(np.abs(Z[escaped])))
        mask[escaped] = False

    return iteration_map


def burning_ship(width: int, height: int, x_min: float, x_max: float,
                 y_min: float, y_max: float, max_iter: int) -> np.ndarray:
    """Compute the Burning Ship fractal — abs of real & imaginary before squaring."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    iteration_map = np.zeros(C.shape, dtype=float)
    mask = np.ones(C.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = (np.abs(Z[mask].real) + 1j * np.abs(Z[mask].imag)) ** 2 + C[mask]
        escaped = mask & (np.abs(Z) > 2.0)
        iteration_map[escaped] = float(i)
        mask[escaped] = False

    return iteration_map


def newton(width: int, height: int, x_min: float, x_max: float,
           y_min: float, y_max: float, max_iter: int,
           poly: str = "z3-1") -> tuple[np.ndarray, np.ndarray]:
    """
    Newton fractal for a polynomial root-finding iteration.
    Returns (root_map, convergence_speed) arrays.
    poly options: 'z3-1', 'z4-1', 'z6-1'
    """
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    Z = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    roots_map = np.full(Z.shape, -1, dtype=int)
    speed_map = np.zeros(Z.shape, dtype=float)

    degrees = {"z3-1": 3, "z4-1": 4, "z6-1": 6}
    n = degrees.get(poly, 3)
    roots = np.array([np.exp(2j * np.pi * k / n) for k in range(n)])

    active = np.ones(Z.shape, dtype=bool)
    for i in range(max_iter):
        Zn = Z[active]
        # Newton step: z - f(z)/f'(z) = z - (z^n - 1)/(n*z^(n-1)) = ((n-1)*z^n + 1)/n
        Z[active] = ((n - 1) * Zn**n + 1) / (n * Zn**(n - 1))

        for k, root in enumerate(roots):
            converged = active & (np.abs(Z - root) < 1e-6)
            roots_map[converged] = k
            speed_map[converged] = i / max_iter
            active[converged] = False

        if not active.any():
            break

    return roots_map, speed_map
