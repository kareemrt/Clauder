"""
Mathematical computations for various fractal types.
All done in pure Python — no dependencies required.
"""

import math
from typing import Tuple


def mandelbrot(cx: float, cy: float, max_iter: int = 256) -> Tuple[int, float]:
    """
    Classic Mandelbrot set: z_{n+1} = z_n^2 + c, starting at z=0.
    Returns (raw_iteration, smooth_value) using the smooth escape-time algorithm.
    """
    zx, zy = 0.0, 0.0
    for i in range(max_iter):
        zx2, zy2 = zx * zx, zy * zy
        if zx2 + zy2 > 256.0:  # high bailout radius improves smooth coloring
            log_zn = math.log(zx2 + zy2) * 0.5
            nu = math.log(log_zn / math.log(2.0)) / math.log(2.0)
            return i, i + 1.0 - nu
        zy = 2.0 * zx * zy + cy
        zx = zx2 - zy2 + cx
    return max_iter, float(max_iter)


def julia(zx: float, zy: float, cx: float, cy: float, max_iter: int = 256) -> Tuple[int, float]:
    """
    Julia set: z_{n+1} = z_n^2 + c with fixed parameter (cx, cy).
    Some beautiful c values:
      Dragon wing: (-0.7269, 0.1889)
      Douady rabbit: (-0.123, 0.745)
      San Marco: (-0.75, 0.0)
      Siegel disk: (-0.391, -0.587)
    """
    for i in range(max_iter):
        zx2, zy2 = zx * zx, zy * zy
        if zx2 + zy2 > 256.0:
            log_zn = math.log(zx2 + zy2) * 0.5
            nu = math.log(log_zn / math.log(2.0)) / math.log(2.0)
            return i, i + 1.0 - nu
        zy = 2.0 * zx * zy + cy
        zx = zx2 - zy2 + cx
    return max_iter, float(max_iter)


def burning_ship(cx: float, cy: float, max_iter: int = 256) -> Tuple[int, float]:
    """
    Burning Ship fractal: z_{n+1} = (|Re(z)| + i|Im(z)|)^2 + c
    Produces a ship-like structure at the bottom of its parameter space.
    """
    zx, zy = 0.0, 0.0
    for i in range(max_iter):
        zx2, zy2 = zx * zx, zy * zy
        if zx2 + zy2 > 256.0:
            log_zn = math.log(zx2 + zy2) * 0.5
            nu = math.log(log_zn / math.log(2.0)) / math.log(2.0)
            return i, i + 1.0 - nu
        zy = 2.0 * abs(zx) * abs(zy) + cy
        zx = zx2 - zy2 + cx
    return max_iter, float(max_iter)


def tricorn(cx: float, cy: float, max_iter: int = 256) -> Tuple[int, float]:
    """
    Tricorn / Mandelbar: z_{n+1} = conj(z)^2 + c
    Named for its characteristic three-fold symmetry.
    """
    zx, zy = 0.0, 0.0
    for i in range(max_iter):
        zx2, zy2 = zx * zx, zy * zy
        if zx2 + zy2 > 256.0:
            log_zn = math.log(zx2 + zy2) * 0.5
            nu = math.log(log_zn / math.log(2.0)) / math.log(2.0)
            return i, i + 1.0 - nu
        zy = -2.0 * zx * zy + cy   # conjugate squares negative imaginary
        zx = zx2 - zy2 + cx
    return max_iter, float(max_iter)


def multibrot(cx: float, cy: float, power: int = 3, max_iter: int = 256) -> Tuple[int, float]:
    """
    Multibrot set: z_{n+1} = z_n^d + c for arbitrary integer power d.
    d=2 → Mandelbrot, d=3 → three-fold symmetry, d=4 → four-fold, etc.
    """
    zx, zy = 0.0, 0.0
    for i in range(max_iter):
        zx2, zy2 = zx * zx, zy * zy
        if zx2 + zy2 > 256.0:
            log_zn = math.log(zx2 + zy2) * 0.5
            nu = math.log(log_zn / math.log(2.0)) / math.log(2.0)
            return i, i + 1.0 - nu
        # Compute z^power in polar form: r^p * e^(p*theta)
        r = math.sqrt(zx2 + zy2)
        theta = math.atan2(zy, zx) * power
        rp = r ** power
        zx = rp * math.cos(theta) + cx
        zy = rp * math.sin(theta) + cy
    return max_iter, float(max_iter)


# Pre-baked famous locations in the Mandelbrot set
LANDMARKS = {
    "Full View":         {"cx": -0.5,       "cy":  0.0,      "zoom":  0.75,  "max_iter": 100},
    "Seahorse Valley":   {"cx": -0.74529,   "cy":  0.11307,  "zoom":  320,   "max_iter": 300},
    "Elephant Valley":   {"cx":  0.3010,    "cy":  0.0,      "zoom":   14,   "max_iter": 200},
    "Dragon Spiral":     {"cx": -0.72689,   "cy":  0.18857,  "zoom":  800,   "max_iter": 500},
    "Mini-Brot":         {"cx": -1.7499,    "cy":  0.0,      "zoom":  250,   "max_iter": 400},
    "Triple Spiral":     {"cx": -0.08800,   "cy":  0.65400,  "zoom":   45,   "max_iter": 300},
    "Antenna":           {"cx": -1.25506,   "cy":  0.38050,  "zoom":  100,   "max_iter": 350},
    "Deep Zoom":         {"cx": -0.77568377, "cy": 0.13646737, "zoom": 50000, "max_iter": 800},
}
