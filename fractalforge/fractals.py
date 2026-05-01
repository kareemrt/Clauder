"""Fractal computation engines using pure Python + optional NumPy acceleration."""

import math
from typing import Tuple, Optional
import numpy as np


def _smooth_iteration(n: int, z: complex, max_iter: int) -> float:
    """Smooth (continuous) iteration count to eliminate band artifacts."""
    if n == max_iter:
        return 1.0
    log_zn = math.log(abs(z)) if abs(z) > 0 else 0
    nu = math.log(log_zn / math.log(2)) / math.log(2)
    return (n + 1 - nu) / max_iter


def mandelbrot(
    width: int,
    height: int,
    center: Tuple[float, float] = (-0.5, 0.0),
    zoom: float = 1.0,
    max_iter: int = 256,
) -> np.ndarray:
    """Render the Mandelbrot set. Returns float array [0,1] of shape (height, width)."""
    cx, cy = center
    scale = 3.0 / zoom

    x = np.linspace(cx - scale * width / height / 2, cx + scale * width / height / 2, width)
    y = np.linspace(cy - scale / 2, cy + scale / 2, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    result = np.ones((height, width), dtype=np.float64)
    escaped = np.zeros((height, width), dtype=bool)

    for i in range(max_iter):
        mask = ~escaped
        Z[mask] = Z[mask] ** 2 + C[mask]
        newly_escaped = mask & (np.abs(Z) > 2.0)
        if newly_escaped.any():
            abs_z = np.abs(Z[newly_escaped])
            log_zn = np.log(np.maximum(abs_z, 1e-10))
            nu = np.log(log_zn / math.log(2)) / math.log(2)
            smooth = (i + 1 - nu) / max_iter
            result[newly_escaped] = np.clip(smooth, 0.0, 1.0)
            escaped |= newly_escaped

    result[~escaped] = 1.0
    return result


def julia(
    width: int,
    height: int,
    c: complex = complex(-0.7269, 0.1889),
    center: Tuple[float, float] = (0.0, 0.0),
    zoom: float = 1.0,
    max_iter: int = 256,
) -> np.ndarray:
    """Render a Julia set for parameter c. Returns float array [0,1]."""
    cx, cy = center
    scale = 3.0 / zoom

    x = np.linspace(cx - scale * width / height / 2, cx + scale * width / height / 2, width)
    y = np.linspace(cy - scale / 2, cy + scale / 2, height)
    Z = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    result = np.ones((height, width), dtype=np.float64)
    escaped = np.zeros((height, width), dtype=bool)

    for i in range(max_iter):
        mask = ~escaped
        Z[mask] = Z[mask] ** 2 + c
        newly_escaped = mask & (np.abs(Z) > 2.0)
        if newly_escaped.any():
            abs_z = np.abs(Z[newly_escaped])
            log_zn = np.log(np.maximum(abs_z, 1e-10))
            nu = np.log(log_zn / math.log(2)) / math.log(2)
            smooth = (i + 1 - nu) / max_iter
            result[newly_escaped] = np.clip(smooth, 0.0, 1.0)
            escaped |= newly_escaped

    result[~escaped] = 1.0
    return result


def burning_ship(
    width: int,
    height: int,
    center: Tuple[float, float] = (-0.5, -0.5),
    zoom: float = 1.0,
    max_iter: int = 256,
) -> np.ndarray:
    """Render the Burning Ship fractal. Returns float array [0,1]."""
    cx, cy = center
    scale = 3.0 / zoom

    x = np.linspace(cx - scale * width / height / 2, cx + scale * width / height / 2, width)
    y = np.linspace(cy - scale / 2, cy + scale / 2, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    result = np.ones((height, width), dtype=np.float64)
    escaped = np.zeros((height, width), dtype=bool)

    for i in range(max_iter):
        mask = ~escaped
        Zm = np.abs(Z[mask].real) + 1j * np.abs(Z[mask].imag)
        Z[mask] = Zm ** 2 + C[mask]
        newly_escaped = mask & (np.abs(Z) > 2.0)
        if newly_escaped.any():
            abs_z = np.abs(Z[newly_escaped])
            log_zn = np.log(np.maximum(abs_z, 1e-10))
            nu = np.log(log_zn / math.log(2)) / math.log(2)
            smooth = (i + 1 - nu) / max_iter
            result[newly_escaped] = np.clip(smooth, 0.0, 1.0)
            escaped |= newly_escaped

    result[~escaped] = 1.0
    return result


def tricorn(
    width: int,
    height: int,
    center: Tuple[float, float] = (0.0, 0.0),
    zoom: float = 1.0,
    max_iter: int = 256,
) -> np.ndarray:
    """Render the Tricorn (Mandelbar) fractal. Returns float array [0,1]."""
    cx, cy = center
    scale = 3.0 / zoom

    x = np.linspace(cx - scale * width / height / 2, cx + scale * width / height / 2, width)
    y = np.linspace(cy - scale / 2, cy + scale / 2, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    result = np.ones((height, width), dtype=np.float64)
    escaped = np.zeros((height, width), dtype=bool)

    for i in range(max_iter):
        mask = ~escaped
        Z[mask] = np.conj(Z[mask]) ** 2 + C[mask]
        newly_escaped = mask & (np.abs(Z) > 2.0)
        if newly_escaped.any():
            abs_z = np.abs(Z[newly_escaped])
            log_zn = np.log(np.maximum(abs_z, 1e-10))
            nu = np.log(log_zn / math.log(2)) / math.log(2)
            smooth = (i + 1 - nu) / max_iter
            result[newly_escaped] = np.clip(smooth, 0.0, 1.0)
            escaped |= newly_escaped

    result[~escaped] = 1.0
    return result


FRACTAL_REGISTRY = {
    "mandelbrot": mandelbrot,
    "julia": julia,
    "burning_ship": burning_ship,
    "tricorn": tricorn,
}
