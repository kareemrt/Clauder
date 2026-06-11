"""Escape-time fractals: Mandelbrot, Julia, and Burning Ship sets."""

import numpy as np


def _viewport(width, height, center, zoom):
    """Return (x_min, x_max, y_min, y_max) for a given center and zoom level."""
    aspect = width / height
    scale = 2.0 / zoom
    x_min = center[0] - scale * aspect
    x_max = center[0] + scale * aspect
    y_min = center[1] - scale
    y_max = center[1] + scale
    return x_min, x_max, y_min, y_max


def _smooth_escape(c, z0, max_iter, transform=None):
    """Run the escape-time iteration ``z = transform(z)**2 + c``.

    Returns a normalized array in ``[0, 1]`` where ``1.0`` means the point
    never escaped (i.e. it is considered part of the set), and values below
    ``1.0`` give a smoothly interpolated escape speed for coloring.
    """
    z = np.broadcast_to(z0, c.shape).astype(np.complex128).copy()
    div_time = np.zeros(c.shape, dtype=np.float64)
    mask = np.ones(c.shape, dtype=bool)

    for i in range(max_iter):
        zm = z[mask]
        if transform is not None:
            zm = transform(zm)
        zm = zm * zm + c[mask]
        z[mask] = zm

        escaped = np.abs(zm) > 2.0
        if np.any(escaped):
            escaped_idx = np.flatnonzero(mask)[escaped]
            magnitude = np.abs(z.flat[escaped_idx])
            # Smooth iteration count (Normalized Iteration Count algorithm).
            div_time.flat[escaped_idx] = i + 1 - np.log(np.log(magnitude)) / np.log(2)
            mask.flat[escaped_idx] = False

        if not mask.any():
            break

    div_time[mask] = max_iter
    normalized = div_time / max_iter
    np.clip(normalized, 0.0, 1.0, out=normalized)
    # Points still in `mask` never escaped: mark them as fully "inside".
    normalized[mask] = 1.0
    return normalized


def mandelbrot(width, height, max_iter=200, center=(-0.5, 0.0), zoom=1.0):
    """Compute a normalized escape-time grid for the Mandelbrot set."""
    x_min, x_max, y_min, y_max = _viewport(width, height, center, zoom)
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    cx, cy = np.meshgrid(x, y)
    c = cx + 1j * cy
    return _smooth_escape(c, 0.0, max_iter)


def julia(width, height, c_param, max_iter=200, center=(0.0, 0.0), zoom=1.0):
    """Compute a normalized escape-time grid for a Julia set with constant ``c_param``."""
    x_min, x_max, y_min, y_max = _viewport(width, height, center, zoom)
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    zx, zy = np.meshgrid(x, y)
    z0 = zx + 1j * zy
    c = np.full(z0.shape, c_param, dtype=np.complex128)
    return _smooth_escape(c, z0, max_iter)


def burning_ship(width, height, max_iter=200, center=(-0.5, -0.5), zoom=1.0):
    """Compute a normalized escape-time grid for the Burning Ship fractal."""
    x_min, x_max, y_min, y_max = _viewport(width, height, center, zoom)
    x = np.linspace(x_min, x_max, width)
    # Burning ship is conventionally rendered with the imaginary axis flipped.
    y = np.linspace(y_max, y_min, height)
    cx, cy = np.meshgrid(x, y)
    c = cx + 1j * cy
    return _smooth_escape(
        c, 0.0, max_iter, transform=lambda z: np.abs(z.real) + 1j * np.abs(z.imag)
    )
