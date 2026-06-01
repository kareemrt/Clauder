"""
Core fractal mathematics.

Each function returns a smooth real-valued escape time using the
log-log normalization trick, except newton() which returns
(convergence_speed, root_index).
"""

import math


def mandelbrot(cx: float, cy: float, max_iter: int) -> float:
    """Smooth escape time for Mandelbrot set at c = cx + cy*i."""
    zr, zi = 0.0, 0.0
    for i in range(max_iter):
        zr2, zi2 = zr * zr, zi * zi
        if zr2 + zi2 > 4.0:
            mag = math.sqrt(zr2 + zi2)
            return i + 1.0 - math.log(math.log(mag)) / math.log(2)
        zr, zi = zr2 - zi2 + cx, 2.0 * zr * zi + cy
    return float(max_iter)


def julia(zr: float, zi: float, cr: float, ci: float, max_iter: int) -> float:
    """Smooth escape time for Julia set at z = zr + zi*i with constant c = cr + ci*i."""
    for i in range(max_iter):
        zr2, zi2 = zr * zr, zi * zi
        if zr2 + zi2 > 4.0:
            mag = math.sqrt(zr2 + zi2)
            return i + 1.0 - math.log(math.log(mag)) / math.log(2)
        zr, zi = zr2 - zi2 + cr, 2.0 * zr * zi + ci
    return float(max_iter)


def burning_ship(cx: float, cy: float, max_iter: int) -> float:
    """Smooth escape time for Burning Ship fractal at (cx, cy)."""
    zr, zi = 0.0, 0.0
    for i in range(max_iter):
        zr, zi = abs(zr), abs(zi)
        zr2, zi2 = zr * zr, zi * zi
        if zr2 + zi2 > 4.0:
            mag = math.sqrt(zr2 + zi2)
            return i + 1.0 - math.log(math.log(mag)) / math.log(2)
        # Negated cy to orient the "ship" right-side up
        zr, zi = zr2 - zi2 + cx, 2.0 * zr * zi - cy
    return float(max_iter)


def newton(zr: float, zi: float, max_iter: int) -> tuple:
    """
    Newton's method for f(z) = z^3 - 1.

    Returns (convergence_t, root_index) where convergence_t is in [0,1]
    (lower = faster convergence = brighter) and root_index identifies
    which of the three cube roots of unity was reached.
    """
    # The three cube roots of unity
    roots = [(1.0, 0.0), (-0.5, 0.8660254037844387), (-0.5, -0.8660254037844387)]
    tol2 = 1e-12

    for i in range(max_iter):
        zr2, zi2 = zr * zr, zi * zi
        zm2 = zr2 + zi2
        if zm2 < 1e-30:
            break

        # z^3 = (zr + zi*i)^3
        zr3 = zr * (zr2 - 3.0 * zi2)
        zi3 = zi * (3.0 * zr2 - zi2)

        # 3*z^2
        d_re = 3.0 * (zr2 - zi2)
        d_im = 6.0 * zr * zi

        # f(z) = z^3 - 1
        f_re, f_im = zr3 - 1.0, zi3

        denom = d_re * d_re + d_im * d_im
        if denom < 1e-30:
            break

        # Newton step: z -= f(z) / f'(z)
        zr -= (f_re * d_re + f_im * d_im) / denom
        zi -= (f_im * d_re - f_re * d_im) / denom

        for j, (rx, ry) in enumerate(roots):
            dr, di = zr - rx, zi - ry
            if dr * dr + di * di < tol2:
                return (i / max_iter, j)

    return (1.0, 0)
