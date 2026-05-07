"""Core fractal computation using vectorized numpy operations."""

import numpy as np


def mandelbrot(width: int, height: int, x_min: float, x_max: float,
               y_min: float, y_max: float, max_iter: int) -> np.ndarray:
    """Compute the Mandelbrot set with smooth (continuous) escape-time coloring."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    smooth = np.zeros(C.shape, dtype=np.float64)
    escaped = np.zeros(C.shape, dtype=bool)

    for i in range(1, max_iter + 1):
        mask = ~escaped
        Z[mask] = Z[mask] ** 2 + C[mask]
        newly_escaped = mask & (np.abs(Z) > 2.0)
        # Smooth coloring: fractional escape count
        abs_z = np.abs(Z[newly_escaped])
        smooth[newly_escaped] = i - np.log2(np.log2(np.maximum(abs_z, 1.0001)))
        escaped |= newly_escaped

    # Points that never escaped get 0
    smooth[~escaped] = 0.0
    return smooth


def julia(width: int, height: int, c_real: float, c_imag: float,
          x_min: float, x_max: float, y_min: float, y_max: float,
          max_iter: int) -> np.ndarray:
    """Compute a Julia set for constant c = c_real + c_imag*i."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    Z = x[np.newaxis, :] + 1j * y[:, np.newaxis]
    c = complex(c_real, c_imag)

    smooth = np.zeros(Z.shape, dtype=np.float64)
    escaped = np.zeros(Z.shape, dtype=bool)

    for i in range(1, max_iter + 1):
        mask = ~escaped
        Z[mask] = Z[mask] ** 2 + c
        newly_escaped = mask & (np.abs(Z) > 2.0)
        abs_z = np.abs(Z[newly_escaped])
        smooth[newly_escaped] = i - np.log2(np.log2(np.maximum(abs_z, 1.0001)))
        escaped |= newly_escaped

    smooth[~escaped] = 0.0
    return smooth


def burning_ship(width: int, height: int, x_min: float, x_max: float,
                 y_min: float, y_max: float, max_iter: int) -> np.ndarray:
    """Compute the Burning Ship fractal — like Mandelbrot but with abs() trick."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    smooth = np.zeros(C.shape, dtype=np.float64)
    escaped = np.zeros(C.shape, dtype=bool)

    for i in range(1, max_iter + 1):
        mask = ~escaped
        Z[mask] = (np.abs(Z[mask].real) + 1j * np.abs(Z[mask].imag)) ** 2 + C[mask]
        newly_escaped = mask & (np.abs(Z) > 2.0)
        abs_z = np.abs(Z[newly_escaped])
        smooth[newly_escaped] = i - np.log2(np.log2(np.maximum(abs_z, 1.0001)))
        escaped |= newly_escaped

    smooth[~escaped] = 0.0
    return smooth


# Curated presets: (name, fractal_type, params, description)
PRESETS = {
    "classic": {
        "type": "mandelbrot",
        "bounds": (-2.5, 1.0, -1.25, 1.25),
        "max_iter": 256,
        "description": "Classic Mandelbrot set — the full picture",
    },
    "seahorse": {
        "type": "mandelbrot",
        "bounds": (-0.76, -0.72, 0.06, 0.10),
        "max_iter": 512,
        "description": "Seahorse Valley — intricate spiral tendrils",
    },
    "elephant": {
        "type": "mandelbrot",
        "bounds": (0.27, 0.29, 0.0048, 0.0148),
        "max_iter": 512,
        "description": "Elephant Valley — curling proboscis shapes",
    },
    "spiral": {
        "type": "mandelbrot",
        "bounds": (-0.7269, -0.7259, 0.1889, 0.1899),
        "max_iter": 1024,
        "description": "Deep spiral — hypnotic infinite zoom",
    },
    "julia_spiral": {
        "type": "julia",
        "c": (-0.7269, 0.1889),
        "bounds": (-1.5, 1.5, -1.5, 1.5),
        "max_iter": 256,
        "description": "Julia set c≈−0.727+0.189i — swirling galaxy",
    },
    "julia_dragon": {
        "type": "julia",
        "c": (-0.4, 0.6),
        "bounds": (-1.5, 1.5, -1.5, 1.5),
        "max_iter": 256,
        "description": "Julia set c=−0.4+0.6i — dragon wings",
    },
    "julia_snowflake": {
        "type": "julia",
        "c": (0.285, 0.01),
        "bounds": (-1.5, 1.5, -1.5, 1.5),
        "max_iter": 256,
        "description": "Julia set c=0.285+0.01i — delicate snowflake",
    },
    "burning_ship": {
        "type": "burning_ship",
        "bounds": (-2.5, 1.5, -2.0, 0.5),
        "max_iter": 256,
        "description": "Burning Ship fractal — jagged, flame-like structure",
    },
}
