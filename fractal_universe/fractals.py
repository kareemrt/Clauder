"""
Fractal computation engines.

Each fractal returns a 2D numpy array of iteration counts (float for smooth coloring).
"""

import numpy as np


def _escape_time(c: np.ndarray, max_iter: int, radius: float = 2.0) -> np.ndarray:
    """Core escape-time algorithm with smooth iteration count (real-valued)."""
    z = np.zeros_like(c)
    counts = np.zeros(c.shape, dtype=np.float64)
    active = np.ones(c.shape, dtype=bool)

    for i in range(max_iter):
        z[active] = z[active] ** 2 + c[active]
        escaped = active & (np.abs(z) > radius)
        # Smooth iteration count: nu = n - log2(log2(|z|))
        log_z = np.log(np.abs(z[escaped]) + 1e-10)
        counts[escaped] = i + 1 - np.log2(np.maximum(log_z, 1e-10))
        active &= ~escaped

    # Interior points get max_iter
    counts[active] = max_iter
    return counts


def mandelbrot(
    width: int,
    height: int,
    x_min: float = -2.5,
    x_max: float = 1.0,
    y_min: float = -1.25,
    y_max: float = 1.25,
    max_iter: int = 256,
) -> np.ndarray:
    """Classic Mandelbrot set: z = z² + c, where c varies over the plane."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]
    return _escape_time(C, max_iter)


def julia(
    width: int,
    height: int,
    c_real: float = -0.7269,
    c_imag: float = 0.1889,
    x_min: float = -1.5,
    x_max: float = 1.5,
    y_min: float = -1.5,
    y_max: float = 1.5,
    max_iter: int = 256,
) -> np.ndarray:
    """Julia set: z = z² + c, where c is fixed and z varies over the plane."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    Z = x[np.newaxis, :] + 1j * y[:, np.newaxis]
    C = np.full_like(Z, c_real + 1j * c_imag)
    return _escape_time(C, max_iter)


def burning_ship(
    width: int,
    height: int,
    x_min: float = -2.5,
    x_max: float = 1.5,
    y_min: float = -2.0,
    y_max: float = 0.5,
    max_iter: int = 256,
) -> np.ndarray:
    """Burning Ship fractal: z = (|Re(z)| + i|Im(z)|)² + c."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]
    z = np.zeros_like(C)
    counts = np.zeros(C.shape, dtype=np.float64)
    active = np.ones(C.shape, dtype=bool)

    for i in range(max_iter):
        z[active] = (np.abs(z[active].real) + 1j * np.abs(z[active].imag)) ** 2 + C[active]
        escaped = active & (np.abs(z) > 2.0)
        log_z = np.log(np.abs(z[escaped]) + 1e-10)
        counts[escaped] = i + 1 - np.log2(np.maximum(log_z, 1e-10))
        active &= ~escaped

    counts[active] = max_iter
    return counts


def tricorn(
    width: int,
    height: int,
    x_min: float = -2.5,
    x_max: float = 1.0,
    y_min: float = -1.5,
    y_max: float = 1.5,
    max_iter: int = 256,
) -> np.ndarray:
    """Tricorn (Mandelbar): z = conj(z)² + c."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]
    z = np.zeros_like(C)
    counts = np.zeros(C.shape, dtype=np.float64)
    active = np.ones(C.shape, dtype=bool)

    for i in range(max_iter):
        z[active] = np.conj(z[active]) ** 2 + C[active]
        escaped = active & (np.abs(z) > 2.0)
        log_z = np.log(np.abs(z[escaped]) + 1e-10)
        counts[escaped] = i + 1 - np.log2(np.maximum(log_z, 1e-10))
        active &= ~escaped

    counts[active] = max_iter
    return counts


# Famous Julia set parameters worth exploring
JULIA_PRESETS = {
    "dragon":      (-0.7269,  0.1889),
    "dendrite":    ( 0.0,     1.0),
    "spiral":      (-0.4,     0.6),
    "lightning":   (-0.8,     0.156),
    "galaxy":      (-0.12,    0.77),
    "douady":      (-0.123,   0.745),
    "rabbit":      (-0.1226,  0.7449),
    "seahorse":    (-0.7436,  0.1319),
}
