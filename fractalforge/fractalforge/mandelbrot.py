"""Mandelbrot set computation."""

import math


def compute(
    width: int,
    height: int,
    x_min: float = -2.5,
    x_max: float = 1.0,
    y_min: float = -1.2,
    y_max: float = 1.2,
    max_iter: int = 256,
) -> list[list[float]]:
    """Return a 2-D grid of smooth iteration counts (0.0 = in-set)."""
    result = []
    x_scale = (x_max - x_min) / width
    y_scale = (y_max - y_min) / height

    for row in range(height):
        line = []
        cy = y_min + row * y_scale
        for col in range(width):
            cx = x_min + col * x_scale
            zx, zy = 0.0, 0.0
            i = 0
            while i < max_iter and zx * zx + zy * zy < 4.0:
                zx, zy = zx * zx - zy * zy + cx, 2.0 * zx * zy + cy
                i += 1
            if i == max_iter:
                line.append(0.0)
            else:
                # Smooth coloring via renormalization
                log_zn = math.log(zx * zx + zy * zy) / 2.0
                nu = math.log(log_zn / math.log(2.0)) / math.log(2.0)
                smooth = (i + 1 - nu) / max_iter
                line.append(max(0.0, min(1.0, smooth)))
        result.append(line)

    return result


PRESETS = {
    "classic": {
        "x_min": -2.5, "x_max": 1.0,
        "y_min": -1.2, "y_max": 1.2,
        "max_iter": 256,
    },
    "seahorse": {
        "x_min": -0.77, "x_max": -0.74,
        "y_min": 0.085, "y_max": 0.115,
        "max_iter": 512,
    },
    "elephant": {
        "x_min": 0.2549, "x_max": 0.2555,
        "y_min": -0.0005, "y_max": 0.0005,
        "max_iter": 1024,
    },
    "spiral": {
        "x_min": -0.748, "x_max": -0.746,
        "y_min": 0.099, "y_max": 0.101,
        "max_iter": 768,
    },
    "lightning": {
        "x_min": -1.787, "x_max": -1.784,
        "y_min": -0.002, "y_max": 0.002,
        "max_iter": 512,
    },
}
