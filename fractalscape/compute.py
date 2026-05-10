"""Core fractal computation engines."""

import numpy as np
from typing import Tuple


def mandelbrot(
    width: int,
    height: int,
    x_min: float = -2.5,
    x_max: float = 1.0,
    y_min: float = -1.25,
    y_max: float = 1.25,
    max_iter: int = 256,
) -> np.ndarray:
    """Compute escape-time iteration counts for the Mandelbrot set."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    iterations = np.zeros(C.shape, dtype=np.float64)
    mask = np.ones(C.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask] ** 2 + C[mask]
        escaped = mask & (np.abs(Z) > 2.0)
        # Smooth coloring: fractional escape count
        iterations[escaped] = i + 1 - np.log2(np.log2(np.abs(Z[escaped])))
        mask[escaped] = False

    return iterations


def julia(
    width: int,
    height: int,
    c: complex = -0.7 + 0.27015j,
    x_min: float = -1.8,
    x_max: float = 1.8,
    y_min: float = -1.8,
    y_max: float = 1.8,
    max_iter: int = 256,
) -> np.ndarray:
    """Compute escape-time iteration counts for a Julia set."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    Z = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    iterations = np.zeros(Z.shape, dtype=np.float64)
    mask = np.ones(Z.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask] ** 2 + c
        escaped = mask & (np.abs(Z) > 2.0)
        iterations[escaped] = i + 1 - np.log2(np.log2(np.abs(Z[escaped])))
        mask[escaped] = False

    return iterations


def burning_ship(
    width: int,
    height: int,
    x_min: float = -2.5,
    x_max: float = 1.5,
    y_min: float = -2.0,
    y_max: float = 0.5,
    max_iter: int = 256,
) -> np.ndarray:
    """Compute the Burning Ship fractal — a haunting variant of Mandelbrot."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    iterations = np.zeros(C.shape, dtype=np.float64)
    mask = np.ones(C.shape, dtype=bool)

    for i in range(max_iter):
        # The defining characteristic: take absolute values before squaring
        Z[mask] = (np.abs(Z[mask].real) + 1j * np.abs(Z[mask].imag)) ** 2 + C[mask]
        escaped = mask & (np.abs(Z) > 2.0)
        iterations[escaped] = i + 1.0
        mask[escaped] = False

    return iterations


# Famous Julia set parameters
JULIA_PRESETS = {
    "dendrite":    -0.0 + 1.0j,
    "douady":      -0.123 + 0.745j,
    "san_marco":   -0.75 + 0.0j,
    "siegel_disk": -0.391 - 0.587j,
    "spiral":      -0.7 + 0.27015j,
    "rabbit":      -0.123 + 0.745j,
    "galaxy":      0.285 + 0.01j,
    "lightning":   -0.8 + 0.156j,
}

# Famous Mandelbrot zoom coordinates (x_min, x_max, y_min, y_max)
MANDELBROT_TOURS = {
    "full":         (-2.5,  1.0,  -1.25, 1.25),
    "seahorse":     (-0.75, -0.7,  0.1,  0.15),
    "elephant":     (0.275,  0.285, 0.006, 0.012),
    "triple_spiral": (-0.088, -0.078, 0.645, 0.655),
    "mini_mandelbrot": (-1.77, -1.74, -0.02, 0.02),
    "lightning_bolt": (-0.56, -0.50, 0.50, 0.58),
}
