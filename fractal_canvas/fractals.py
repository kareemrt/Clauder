"""
Fractal computation algorithms.
All functions return smooth float iteration counts for gradient coloring.
"""

import math
from typing import Tuple


def mandelbrot(c: complex, max_iter: int) -> float:
    """Smooth iteration count for the Mandelbrot set: z → z² + c, z₀ = 0."""
    z = 0.0 + 0.0j
    for i in range(max_iter):
        if z.real * z.real + z.imag * z.imag > 4.0:
            log_zn = math.log(z.real * z.real + z.imag * z.imag) / 2.0
            nu = math.log(log_zn / math.log(2.0)) / math.log(2.0)
            return i + 1.0 - nu
        z = z * z + c
    return float(max_iter)


def julia(z: complex, c: complex, max_iter: int) -> float:
    """Smooth iteration count for a Julia set with fixed parameter c."""
    for i in range(max_iter):
        if z.real * z.real + z.imag * z.imag > 4.0:
            log_zn = math.log(z.real * z.real + z.imag * z.imag) / 2.0
            nu = math.log(log_zn / math.log(2.0)) / math.log(2.0)
            return i + 1.0 - nu
        z = z * z + c
    return float(max_iter)


def burning_ship(c: complex, max_iter: int) -> float:
    """Burning Ship fractal: z → (|Re(z)| + i|Im(z)|)² + c."""
    z = 0.0 + 0.0j
    for i in range(max_iter):
        if z.real * z.real + z.imag * z.imag > 4.0:
            return float(i)
        z = complex(abs(z.real), abs(z.imag)) ** 2 + c
    return float(max_iter)


def newton(z: complex, max_iter: int) -> Tuple[float, int]:
    """
    Newton fractal for f(z) = z³ - 1 using Newton's method.
    Returns (iteration_count, root_index) — root index drives colorization.
    """
    roots = [
        1.0 + 0.0j,
        complex(-0.5,  math.sqrt(3) / 2.0),
        complex(-0.5, -math.sqrt(3) / 2.0),
    ]
    for i in range(max_iter):
        z3 = z * z * z
        fz = z3 - 1.0
        if abs(fz) < 1e-6:
            dists = [abs(z - r) for r in roots]
            return float(i), dists.index(min(dists))
        z = z - fz / (3.0 * z * z)
    dists = [abs(z - r) for r in roots]
    return float(max_iter), dists.index(min(dists))


def tricorn(c: complex, max_iter: int) -> float:
    """Tricorn (Mandelbar) fractal: z → conj(z)² + c."""
    z = 0.0 + 0.0j
    for i in range(max_iter):
        if z.real * z.real + z.imag * z.imag > 4.0:
            return float(i)
        z = z.conjugate() ** 2 + c
    return float(max_iter)


# Curated Julia set parameters — each produces a visually distinct pattern
JULIA_PRESETS: dict = {
    "rabbit":    complex(-0.1230,  0.7450),
    "dragon":    complex(-0.7269,  0.1889),
    "spiral":    complex(-0.4000,  0.6000),
    "dendrite":  complex( 0.0000,  1.0000),
    "galaxy":    complex(-0.8000,  0.1560),
    "lightning": complex(-0.7000,  0.2702),
    "frost":     complex(-0.4251,  0.1630),
    "coral":     complex( 0.2850,  0.0100),
}
