"""
Fractal computation engine.
Supports Mandelbrot, Julia, Burning Ship, and Tricorn fractals.
Uses NumPy vectorization when available (100x speedup over pure Python).
"""
import math
from typing import Callable, List, Optional, Tuple

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

# ---------------------------------------------------------------------------
# Pure-Python pixel functions (fallback and for exotic fractal types)
# ---------------------------------------------------------------------------

def _smooth_escape(iteration: int, x: float, y: float) -> float:
    """Continuous (smooth) iteration count using the normalized escape formula."""
    mag_sq = x * x + y * y
    if mag_sq < 1.0:
        return float(iteration)
    log_zn = math.log(mag_sq) * 0.5
    nu = math.log(max(log_zn / math.log(2), 1e-10)) / math.log(2)
    return iteration + 1.0 - nu


def mandelbrot_pixel(cx: float, cy: float, max_iter: int) -> float:
    """z_{n+1} = z_n^2 + c, z_0 = 0"""
    x = y = 0.0
    for i in range(max_iter):
        x2, y2 = x * x, y * y
        if x2 + y2 > 4.0:
            return _smooth_escape(i, x, y)
        y = 2.0 * x * y + cy
        x = x2 - y2 + cx
    return float(max_iter)


def julia_pixel(zx: float, zy: float, cx: float, cy: float, max_iter: int) -> float:
    """z_{n+1} = z_n^2 + c, z_0 = pixel coordinate"""
    x, y = zx, zy
    for i in range(max_iter):
        x2, y2 = x * x, y * y
        if x2 + y2 > 4.0:
            return _smooth_escape(i, x, y)
        y = 2.0 * x * y + cy
        x = x2 - y2 + cx
    return float(max_iter)


def burning_ship_pixel(cx: float, cy: float, max_iter: int) -> float:
    """z_{n+1} = (|Re(z)| + i|Im(z)|)^2 + c — the terrifying ship"""
    x = y = 0.0
    for i in range(max_iter):
        x2, y2 = x * x, y * y
        if x2 + y2 > 4.0:
            return _smooth_escape(i, x, y)
        y = abs(2.0 * x * y) + cy
        x = x2 - y2 + cx
    return float(max_iter)


def tricorn_pixel(cx: float, cy: float, max_iter: int) -> float:
    """z_{n+1} = conj(z_n)^2 + c — three-fold anti-symmetry"""
    x = y = 0.0
    for i in range(max_iter):
        x2, y2 = x * x, y * y
        if x2 + y2 > 4.0:
            return _smooth_escape(i, x, y)
        new_x = x2 - y2 + cx
        y = -2.0 * x * y + cy  # conjugation flips imaginary sign
        x = new_x
    return float(max_iter)


def newton_pixel(cx: float, cy: float, max_iter: int, tolerance: float = 1e-6) -> float:
    """Newton fractal for z^3 - 1: basin of attraction coloring."""
    roots = [1.0 + 0j, -0.5 + 0.8660254j, -0.5 - 0.8660254j]
    z = complex(cx, cy)
    for i in range(max_iter):
        fz = z * z * z - 1.0
        dfz = 3.0 * z * z
        if abs(dfz) < 1e-10:
            break
        z -= fz / dfz
        for idx, root in enumerate(roots):
            if abs(z - root) < tolerance:
                # Encode root index into the value with smooth shading
                return float(idx * max_iter // 3) + i * 0.1
    return float(max_iter)


# ---------------------------------------------------------------------------
# NumPy-accelerated implementations
# ---------------------------------------------------------------------------

def _numpy_standard(C: "np.ndarray", Z_init: "np.ndarray",
                    max_iter: int) -> "np.ndarray":
    """Vectorized escape-time algorithm for z = z^2 + c variants."""
    Z = Z_init.copy()
    result = np.full(C.shape, float(max_iter))
    active = np.ones(C.shape, dtype=bool)

    for i in range(1, max_iter + 1):
        if not active.any():
            break
        Z[active] = Z[active] ** 2 + C[active]
        abs_sq = Z.real ** 2 + Z.imag ** 2
        escaped = active & (abs_sq > 4.0)
        if escaped.any():
            abs_z = np.sqrt(abs_sq[escaped])
            log_zn = np.log(abs_z)
            nu = np.log(np.maximum(log_zn / math.log(2), 1e-10)) / math.log(2)
            result[escaped] = i + 1.0 - nu
            active[escaped] = False

    return result


def _numpy_burning_ship(C: "np.ndarray", max_iter: int) -> "np.ndarray":
    """Vectorized Burning Ship fractal."""
    Z = np.zeros_like(C)
    result = np.full(C.shape, float(max_iter))
    active = np.ones(C.shape, dtype=bool)

    for i in range(1, max_iter + 1):
        if not active.any():
            break
        Z_bs = np.abs(Z.real) + 1j * np.abs(Z.imag)
        Z = np.where(active, Z_bs ** 2 + C, Z)
        abs_sq = Z.real ** 2 + Z.imag ** 2
        escaped = active & (abs_sq > 4.0)
        if escaped.any():
            abs_z = np.sqrt(abs_sq[escaped])
            log_zn = np.log(abs_z)
            nu = np.log(np.maximum(log_zn / math.log(2), 1e-10)) / math.log(2)
            result[escaped] = i + 1.0 - nu
            active[escaped] = False

    return result


def _numpy_tricorn(C: "np.ndarray", max_iter: int) -> "np.ndarray":
    """Vectorized Tricorn (Mandelbar) fractal."""
    Z = np.zeros_like(C)
    result = np.full(C.shape, float(max_iter))
    active = np.ones(C.shape, dtype=bool)

    for i in range(1, max_iter + 1):
        if not active.any():
            break
        Z = np.where(active, Z.conj() ** 2 + C, Z)
        abs_sq = Z.real ** 2 + Z.imag ** 2
        escaped = active & (abs_sq > 4.0)
        if escaped.any():
            abs_z = np.sqrt(abs_sq[escaped])
            log_zn = np.log(abs_z)
            nu = np.log(np.maximum(log_zn / math.log(2), 1e-10)) / math.log(2)
            result[escaped] = i + 1.0 - nu
            active[escaped] = False

    return result


def _compute_numpy(
    width: int, height: int,
    x_min: float, x_max: float, y_min: float, y_max: float,
    fractal_type: str, max_iter: int,
    julia_c: Tuple[float, float],
) -> List[List[float]]:
    x = np.linspace(x_min, x_max, width, dtype=np.float64)
    y = np.linspace(y_min, y_max, height, dtype=np.float64)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]  # (height, width)

    if fractal_type == "mandelbrot":
        result = _numpy_standard(C, np.zeros_like(C), max_iter)
    elif fractal_type == "julia":
        jc = complex(julia_c[0], julia_c[1])
        result = _numpy_standard(np.full_like(C, jc), C.copy(), max_iter)
    elif fractal_type == "burning_ship":
        result = _numpy_burning_ship(C, max_iter)
    elif fractal_type == "tricorn":
        result = _numpy_tricorn(C, max_iter)
    else:
        result = _numpy_standard(C, np.zeros_like(C), max_iter)

    return result.tolist()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def compute_fractal(
    width: int,
    height: int,
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    fractal_type: str = "mandelbrot",
    max_iter: int = 256,
    julia_c: Tuple[float, float] = (-0.7, 0.27015),
    progress_callback: Optional[Callable[[float], None]] = None,
) -> List[List[float]]:
    """
    Compute fractal iteration values for every pixel.

    Returns a (height × width) list-of-lists where:
      - value == max_iter  →  point is inside the set (rendered black)
      - value < max_iter   →  smooth escape count for coloring

    Args:
        width, height:   Pixel dimensions.
        x_min … y_max:   Complex-plane viewport bounds.
        fractal_type:    One of 'mandelbrot', 'julia', 'burning_ship',
                         'tricorn', 'newton'.
        max_iter:        Iteration cap (higher = more detail, slower).
        julia_c:         Fixed complex constant for Julia sets (cx, cy).
        progress_callback: Called with float in [0, 1] during Python fallback.
    """
    if NUMPY_AVAILABLE and fractal_type != "newton":
        return _compute_numpy(width, height, x_min, x_max, y_min, y_max,
                               fractal_type, max_iter, julia_c)

    # Pure-Python fallback (also used for Newton fractal)
    dx = (x_max - x_min) / width
    dy = (y_max - y_min) / height
    result: List[List[float]] = []

    pixel_fn = {
        "mandelbrot":   lambda cx, cy: mandelbrot_pixel(cx, cy, max_iter),
        "julia":        lambda cx, cy: julia_pixel(cx, cy, julia_c[0], julia_c[1], max_iter),
        "burning_ship": lambda cx, cy: burning_ship_pixel(cx, cy, max_iter),
        "tricorn":      lambda cx, cy: tricorn_pixel(cx, cy, max_iter),
        "newton":       lambda cx, cy: newton_pixel(cx, cy, max_iter),
    }.get(fractal_type, lambda cx, cy: mandelbrot_pixel(cx, cy, max_iter))

    for row in range(height):
        cy = y_min + row * dy
        line = [pixel_fn(x_min + col * dx, cy) for col in range(width)]
        result.append(line)
        if progress_callback and row % 4 == 0:
            progress_callback((row + 1) / height)

    return result
