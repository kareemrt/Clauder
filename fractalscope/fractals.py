"""Core fractal computation engines."""

import math
from typing import List, Tuple, Optional


def mandelbrot_iter(cx: float, cy: float, max_iters: int) -> int:
    x, y = 0.0, 0.0
    for i in range(max_iters):
        x2, y2 = x * x, y * y
        if x2 + y2 > 4.0:
            return i
        x, y = x2 - y2 + cx, 2.0 * x * y + cy
    return max_iters


def julia_iter(zx: float, zy: float, cx: float, cy: float, max_iters: int) -> int:
    for i in range(max_iters):
        zx2, zy2 = zx * zx, zy * zy
        if zx2 + zy2 > 4.0:
            return i
        zx, zy = zx2 - zy2 + cx, 2.0 * zx * zy + cy
    return max_iters


def burning_ship_iter(cx: float, cy: float, max_iters: int) -> int:
    x, y = 0.0, 0.0
    for i in range(max_iters):
        x2, y2 = x * x, y * y
        if x2 + y2 > 4.0:
            return i
        x, y = abs(x2 - y2) + cx, abs(2.0 * x * y) + cy
    return max_iters


def render_mandelbrot(
    width: int,
    height: int,
    cx: float = -0.5,
    cy: float = 0.0,
    zoom: float = 1.0,
    max_iters: int = 100,
) -> List[List[int]]:
    aspect = width / (height * 2.0)
    x_range = 3.5 / zoom
    y_range = x_range / aspect

    grid = []
    for row in range(height):
        line = []
        for col in range(width):
            real = cx + (col / width - 0.5) * x_range
            imag = cy + (0.5 - row / height) * y_range
            line.append(mandelbrot_iter(real, imag, max_iters))
        grid.append(line)
    return grid


def render_julia(
    width: int,
    height: int,
    cx: float = -0.7,
    cy: float = 0.27015,
    zoom: float = 1.0,
    max_iters: int = 100,
) -> List[List[int]]:
    aspect = width / (height * 2.0)
    x_range = 3.5 / zoom
    y_range = x_range / aspect

    grid = []
    for row in range(height):
        line = []
        for col in range(width):
            zx = (col / width - 0.5) * x_range
            zy = (0.5 - row / height) * y_range
            line.append(julia_iter(zx, zy, cx, cy, max_iters))
        grid.append(line)
    return grid


def render_burning_ship(
    width: int,
    height: int,
    cx: float = -0.4,
    cy: float = -0.6,
    zoom: float = 1.0,
    max_iters: int = 100,
) -> List[List[int]]:
    aspect = width / (height * 2.0)
    x_range = 3.5 / zoom
    y_range = x_range / aspect

    grid = []
    for row in range(height):
        line = []
        for col in range(width):
            real = cx + (col / width - 0.5) * x_range
            imag = cy + (0.5 - row / height) * y_range
            line.append(burning_ship_iter(real, imag, max_iters))
        grid.append(line)
    return grid


def render_sierpinski(size: int, depth: int) -> List[str]:
    """Render Sierpinski triangle as a list of strings."""
    n = 2 ** depth
    rows = []
    for y in range(n):
        row = []
        for x in range(2 * n):
            # Sierpinski rule: a point (x, y) is filled iff (x & y) == 0
            # in the triangular grid
            if (y & (n - 1 - (abs(x - n) if x >= n else (n - 1 - x)))) == 0:
                row.append("*")
            else:
                row.append(" ")
        rows.append("".join(row))

    # More reliable Sierpinski using Pascal's triangle parity
    rows = []
    for row_i in range(n):
        # Build the row using binomial coefficients mod 2
        line = [" "] * (2 * n - 1)
        coeff = 1
        for k in range(row_i + 1):
            if coeff % 2 == 1:
                pos = n - 1 - row_i + 2 * k
                if 0 <= pos < len(line):
                    line[pos] = "▲"
            if k < row_i:
                coeff = coeff * (row_i - k) // (k + 1)
        rows.append("".join(line))
    return rows


def render_newton(
    width: int,
    height: int,
    zoom: float = 1.0,
    max_iters: int = 50,
) -> List[List[Tuple[int, float]]]:
    """Newton fractal for z^3 - 1 = 0. Returns (root_index, convergence)."""
    # Roots of z^3 = 1
    roots = [
        (1.0, 0.0),
        (-0.5, math.sqrt(3) / 2),
        (-0.5, -math.sqrt(3) / 2),
    ]
    tol = 1e-6
    x_range = 4.0 / zoom
    y_range = 4.0 / zoom

    grid = []
    for row in range(height):
        line = []
        for col in range(width):
            zr = (col / width - 0.5) * x_range
            zi = (0.5 - row / height) * y_range
            iters = 0
            for iters in range(max_iters):
                zr2, zi2 = zr * zr, zi * zi
                denom = 3 * ((zr2 - zi2) ** 2 + (2 * zr * zi) ** 2)
                if denom < 1e-12:
                    break
                nr2m1 = zr2 * zr - 3 * zr * zi2 - 1
                ni = 3 * zr2 * zi - zi2 * zi
                dr = zr2 - zi2
                di = 2 * zr * zi
                denom2 = dr * dr + di * di
                if denom2 < 1e-12:
                    break
                zr -= (nr2m1 * dr + ni * di) / denom2 / 3
                zi -= (ni * dr - nr2m1 * di) / denom2 / 3
                # Check convergence to a root
                for idx, (rx, ry) in enumerate(roots):
                    if (zr - rx) ** 2 + (zi - ry) ** 2 < tol:
                        line.append((idx, iters / max_iters))
                        break
                else:
                    continue
                break
            else:
                line.append((0, 1.0))
        grid.append(line)
    return grid
