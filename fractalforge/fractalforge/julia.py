"""Julia set computation."""

import math


def compute(
    width: int,
    height: int,
    cx: float = -0.7,
    cy: float = 0.27,
    x_min: float = -1.8,
    x_max: float = 1.8,
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
        zy = y_min + row * y_scale
        for col in range(width):
            zx = x_min + col * x_scale
            i = 0
            while i < max_iter and zx * zx + zy * zy < 4.0:
                zx, zy = zx * zx - zy * zy + cx, 2.0 * zx * zy + cy
                i += 1
            if i == max_iter:
                line.append(0.0)
            else:
                log_zn = math.log(zx * zx + zy * zy) / 2.0
                nu = math.log(log_zn / math.log(2.0)) / math.log(2.0)
                smooth = (i + 1 - nu) / max_iter
                line.append(max(0.0, min(1.0, smooth)))
        result.append(line)

    return result


PRESETS = {
    "dragon":     {"cx": -0.7269, "cy": 0.1889},
    "galaxy":     {"cx": -0.4,    "cy": 0.6},
    "dendrite":   {"cx": 0.0,     "cy": 1.0},
    "snowflake":  {"cx": -0.7,    "cy": 0.27},
    "lightning":  {"cx": 0.285,   "cy": 0.01},
    "spiral":     {"cx": -0.835,  "cy": -0.2321},
    "rabbit":     {"cx": -0.123,  "cy": 0.745},
    "douady":     {"cx": -0.1,    "cy": 0.651},
}
