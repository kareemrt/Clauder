"""Core fractal computation algorithms with smooth coloring."""

import math
from typing import Callable

ESCAPE_RADIUS = 2.0
ESCAPE_RADIUS_SQ = ESCAPE_RADIUS ** 2


def mandelbrot(c: complex, max_iter: int) -> tuple[float, int]:
    """
    Compute Mandelbrot set membership with smooth escape-time coloring.
    z_{n+1} = z_n^2 + c, starting from z_0 = 0.
    Returns (smooth_value, raw_iteration).
    """
    z = 0j
    for i in range(max_iter):
        if z.real * z.real + z.imag * z.imag > ESCAPE_RADIUS_SQ:
            log_zn = math.log(z.real * z.real + z.imag * z.imag) / 2.0
            nu = math.log(log_zn / math.log(2.0)) / math.log(2.0)
            return i + 1.0 - nu, i
        z = z * z + c
    return 0.0, max_iter


def julia(c: complex, max_iter: int, seed: complex = 0j) -> tuple[float, int]:
    """
    Compute Julia set for parameter c with initial point z = seed.
    Returns (smooth_value, raw_iteration).
    """
    z = seed
    for i in range(max_iter):
        if z.real * z.real + z.imag * z.imag > ESCAPE_RADIUS_SQ:
            log_zn = math.log(z.real * z.real + z.imag * z.imag) / 2.0
            nu = math.log(log_zn / math.log(2.0)) / math.log(2.0)
            return i + 1.0 - nu, i
        z = z * z + c
    return 0.0, max_iter


def burning_ship(c: complex, max_iter: int) -> tuple[float, int]:
    """
    Burning Ship fractal: z_{n+1} = (|Re(z)| + i|Im(z)|)^2 + c.
    The absolute-value fold creates the ship-like structure.
    Returns (smooth_value, raw_iteration).
    """
    z = 0j
    for i in range(max_iter):
        if z.real * z.real + z.imag * z.imag > ESCAPE_RADIUS_SQ:
            log_zn = math.log(z.real * z.real + z.imag * z.imag) / 2.0
            nu = math.log(log_zn / math.log(2.0)) / math.log(2.0)
            return i + 1.0 - nu, i
        z = complex(abs(z.real), abs(z.imag)) ** 2 + c
    return 0.0, max_iter


def newton(c: complex, max_iter: int, tol: float = 1e-6) -> tuple[float, int]:
    """
    Newton fractal for f(z) = z^3 - 1, using Newton-Raphson iteration.
    Colors pixels by which root they converge to and how fast.
    Returns (root_index + convergence_speed, raw_iteration).
    """
    _ROOTS = [1 + 0j, complex(-0.5, math.sqrt(3) / 2), complex(-0.5, -math.sqrt(3) / 2)]
    z = c
    for i in range(max_iter):
        fz = z ** 3 - 1
        if abs(fz) < tol:
            break
        fpz = 3 * z ** 2
        if abs(fpz) < 1e-12:
            break
        z = z - fz / fpz
    for root_idx, root in enumerate(_ROOTS):
        if abs(z - root) < 0.01:
            speed = i / max_iter
            return root_idx * 100.0 + speed * 80.0, i
    return 0.0, max_iter


def tricorn(c: complex, max_iter: int) -> tuple[float, int]:
    """
    Tricorn (Mandelbar) fractal: z_{n+1} = conj(z_n)^2 + c.
    Anti-Mandelbrot with pointy thorn structures.
    """
    z = 0j
    for i in range(max_iter):
        if z.real * z.real + z.imag * z.imag > ESCAPE_RADIUS_SQ:
            log_zn = math.log(z.real * z.real + z.imag * z.imag) / 2.0
            nu = math.log(log_zn / math.log(2.0)) / math.log(2.0)
            return i + 1.0 - nu, i
        z = z.conjugate() ** 2 + c
    return 0.0, max_iter


def compute_frame(
    fractal_fn: Callable,
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
    width: int,
    height: int,
    max_iter: int,
    **kwargs,
) -> list[list[tuple[float, int]]]:
    """Compute a full grid of fractal values for the given viewport."""
    dx = (xmax - xmin) / width
    dy = (ymax - ymin) / height
    frame = []
    for row in range(height):
        y = ymax - row * dy
        line = []
        for col in range(width):
            x = xmin + col * dx
            c = complex(x, y)
            line.append(fractal_fn(c, max_iter, **kwargs))
        frame.append(line)
    return frame
