"""Shared smooth-coloring escape-time renderer.

Each fractal (Mandelbrot, Julia, Burning Ship) only needs to supply an
``iterate`` function that advances z one step; this module handles the
pixel grid walk, smooth normalized coloring, and PNG-ready buffer.
"""

import math


def render(width, height, x_min, x_max, y_min, y_max, max_iter, step, seed, cmap):
    """Render an escape-time fractal.

    ``step(z, c)`` returns the next z given current z and the per-pixel
    constant c. ``seed(c)`` returns the initial z for a given c (so
    Mandelbrot can seed z=0 while Julia seeds z=pixel coordinate).
    """
    pixels = bytearray(width * height * 3)
    log2 = math.log(2)

    for py in range(height):
        y = y_min + (y_max - y_min) * py / (height - 1) if height > 1 else y_min
        row_offset = py * width * 3
        for px in range(width):
            x = x_min + (x_max - x_min) * px / (width - 1) if width > 1 else x_min
            c = complex(x, y)
            z = seed(c)

            n = 0
            while n < max_iter and (z.real * z.real + z.imag * z.imag) <= 4.0:
                z = step(z, c)
                n += 1

            offset = row_offset + px * 3
            if n >= max_iter:
                pixels[offset:offset + 3] = bytes((0, 0, 0))
            else:
                mag = abs(z)
                smooth_n = n + 1 - math.log(math.log(max(mag, 1.0000001))) / log2
                t = max(0.0, min(1.0, smooth_n / max_iter))
                pixels[offset:offset + 3] = bytes(cmap(t))

    return pixels
