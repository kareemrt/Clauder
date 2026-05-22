"""Core fractal computation engine."""

import numpy as np
from typing import Tuple, Optional


def compute_mandelbrot(
    width: int,
    height: int,
    x_min: float = -2.5,
    x_max: float = 1.0,
    y_min: float = -1.25,
    y_max: float = 1.25,
    max_iter: int = 256,
) -> np.ndarray:
    """Compute Mandelbrot set using vectorized numpy operations."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    iteration_counts = np.zeros(C.shape, dtype=float)
    mask = np.ones(C.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask] ** 2 + C[mask]
        escaped = mask & (np.abs(Z) > 2.0)
        # Smooth coloring: fractional escape count
        abs_z = np.abs(Z[escaped])
        iteration_counts[escaped] = i + 1 - np.log2(np.log2(np.maximum(abs_z, 1.0)))
        mask[escaped] = False

    iteration_counts[mask] = max_iter
    return iteration_counts


def compute_julia(
    width: int,
    height: int,
    c: complex = -0.7269 + 0.1889j,
    x_min: float = -1.8,
    x_max: float = 1.8,
    y_min: float = -1.8,
    y_max: float = 1.8,
    max_iter: int = 256,
) -> np.ndarray:
    """Compute Julia set for a given complex parameter c."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    Z = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    iteration_counts = np.zeros(Z.shape, dtype=float)
    mask = np.ones(Z.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask] ** 2 + c
        escaped = mask & (np.abs(Z) > 2.0)
        abs_z = np.abs(Z[escaped])
        iteration_counts[escaped] = i + 1 - np.log2(np.log2(np.maximum(abs_z, 1.0)))
        mask[escaped] = False

    iteration_counts[mask] = max_iter
    return iteration_counts


def compute_burning_ship(
    width: int,
    height: int,
    x_min: float = -2.5,
    x_max: float = 1.5,
    y_min: float = -2.0,
    y_max: float = 0.5,
    max_iter: int = 256,
) -> np.ndarray:
    """Compute Burning Ship fractal — a wild cousin of the Mandelbrot set."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    iteration_counts = np.zeros(C.shape, dtype=float)
    mask = np.ones(C.shape, dtype=bool)

    for i in range(max_iter):
        # Burning Ship: take absolute values of real/imag before squaring
        Z[mask] = (np.abs(Z[mask].real) + 1j * np.abs(Z[mask].imag)) ** 2 + C[mask]
        escaped = mask & (np.abs(Z) > 2.0)
        abs_z = np.abs(Z[escaped])
        iteration_counts[escaped] = i + 1 - np.log2(np.log2(np.maximum(abs_z, 1.0)))
        mask[escaped] = False

    iteration_counts[mask] = max_iter
    return iteration_counts


def compute_tricorn(
    width: int,
    height: int,
    x_min: float = -2.5,
    x_max: float = 1.5,
    y_min: float = -2.0,
    y_max: float = 2.0,
    max_iter: int = 256,
) -> np.ndarray:
    """Compute Tricorn (Mandelbar) fractal using conjugate iteration."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    iteration_counts = np.zeros(C.shape, dtype=float)
    mask = np.ones(C.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = np.conj(Z[mask]) ** 2 + C[mask]
        escaped = mask & (np.abs(Z) > 2.0)
        abs_z = np.abs(Z[escaped])
        iteration_counts[escaped] = i + 1 - np.log2(np.log2(np.maximum(abs_z, 1.0)))
        mask[escaped] = False

    iteration_counts[mask] = max_iter
    return iteration_counts


def zoom_region(
    center_x: float,
    center_y: float,
    zoom: float,
    aspect_ratio: float = 1.0,
) -> Tuple[float, float, float, float]:
    """Calculate view bounds for a zoom level centered at a point."""
    half_width = 1.5 / zoom
    half_height = half_width / aspect_ratio
    return (
        center_x - half_width,
        center_x + half_width,
        center_y - half_height,
        center_y + half_height,
    )
