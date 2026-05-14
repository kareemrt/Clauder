"""Fractal computation algorithms — pure Python, zero external dependencies."""
import math

_LOG2 = math.log(2.0)


def _smooth(n: int, zx: float, zy: float) -> float:
    """Continuous (smooth) iteration count using the standard escape-time formula."""
    log_zn = math.log(zx * zx + zy * zy) * 0.5
    nu = math.log(log_zn / _LOG2) / _LOG2
    return max(0.0, n + 1.0 - nu)


def mandelbrot(cx: float, cy: float, max_iter: int = 256) -> float:
    """Iterate z = z² + c from z=0. Returns smooth escape count (0 = interior)."""
    zx = zy = 0.0
    for n in range(max_iter):
        zx2, zy2 = zx * zx, zy * zy
        if zx2 + zy2 > 4.0:
            return _smooth(n, zx, zy)
        zy = 2.0 * zx * zy + cy
        zx = zx2 - zy2 + cx
    return 0.0


def julia(zx: float, zy: float, cx: float, cy: float, max_iter: int = 256) -> float:
    """Iterate z = z² + c from the given z₀. Returns smooth escape count."""
    for n in range(max_iter):
        zx2, zy2 = zx * zx, zy * zy
        if zx2 + zy2 > 4.0:
            return _smooth(n, zx, zy)
        zy = 2.0 * zx * zy + cy
        zx = zx2 - zy2 + cx
    return 0.0


def burning_ship(cx: float, cy: float, max_iter: int = 256) -> float:
    """Burning Ship fractal: uses |Re(z)| and |Im(z)| before squaring."""
    zx = zy = 0.0
    for n in range(max_iter):
        zx2, zy2 = zx * zx, zy * zy
        if zx2 + zy2 > 4.0:
            return _smooth(n, zx, zy)
        zy = 2.0 * abs(zx) * abs(zy) + cy
        zx = zx2 - zy2 + cx
    return 0.0


def newton_cubic(zx: float, zy: float, max_iter: int = 64, tol: float = 1e-6) -> tuple:
    """
    Newton's method for f(z) = z³ − 1.
    Returns (root_index [0..2], convergence_fraction [0..1]).
    root_index = -1 if no convergence.
    """
    roots = [
        (1.0, 0.0),
        (-0.5,  0.8660254037844387),
        (-0.5, -0.8660254037844387),
    ]
    tol2 = tol * tol

    for n in range(max_iter):
        zx2, zy2 = zx * zx, zy * zy
        # z² and z³
        z2x, z2y = zx2 - zy2, 2.0 * zx * zy
        z3x = zx * z2x - zy * z2y
        z3y = zx * z2y + zy * z2x
        # f(z) = z³ − 1,  f′(z) = 3z²
        fzx, fzy = z3x - 1.0, z3y
        denom = 3.0 * (z2x * z2x + z2y * z2y)
        if denom < 1e-14:
            break
        # Newton step: z ← z − f(z)/f′(z)
        zx -= (fzx * z2x + fzy * z2y) / denom
        zy -= (fzy * z2x - fzx * z2y) / denom

        for i, (rx, ry) in enumerate(roots):
            dx, dy = zx - rx, zy - ry
            if dx * dx + dy * dy < tol2:
                return i, n / max_iter

    return -1, 1.0
