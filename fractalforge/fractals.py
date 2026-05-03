"""Core fractal computation algorithms."""


def mandelbrot(c: complex, max_iters: int) -> int:
    """Return escape iteration count for point c in the Mandelbrot set."""
    z = 0 + 0j
    for i in range(max_iters):
        if abs(z) > 2.0:
            return i
        z = z * z + c
    return max_iters


def julia(z: complex, c: complex, max_iters: int) -> int:
    """Return escape iteration count for point z with Julia parameter c."""
    for i in range(max_iters):
        if abs(z) > 2.0:
            return i
        z = z * z + c
    return max_iters


def burning_ship(c: complex, max_iters: int) -> int:
    """Return escape iteration count for the Burning Ship fractal at c."""
    z = 0 + 0j
    for i in range(max_iters):
        if abs(z) > 2.0:
            return i
        z = (abs(z.real) + abs(z.imag) * 1j) ** 2 + c
    return max_iters


def tricorn(c: complex, max_iters: int) -> int:
    """Return escape iteration count for the Tricorn (Mandelbar) fractal at c."""
    z = 0 + 0j
    for i in range(max_iters):
        if abs(z) > 2.0:
            return i
        z = z.conjugate() ** 2 + c
    return max_iters


def newton(z: complex, max_iters: int, tol: float = 1e-6) -> int:
    """Return iteration count for Newton fractal of z^3 - 1."""
    for i in range(max_iters):
        fz = z ** 3 - 1
        fpz = 3 * z ** 2
        if abs(fpz) < 1e-10:
            break
        z_new = z - fz / fpz
        if abs(z_new - z) < tol:
            return i
        z = z_new
    return max_iters


FRACTALS = {
    "mandelbrot": {
        "fn": mandelbrot,
        "default_region": (-2.5, -1.25, 1.0, 1.25),
        "args": [],
        "description": "The classic Mandelbrot set — the most famous fractal.",
    },
    "julia": {
        "fn": julia,
        "default_region": (-1.5, -1.5, 1.5, 1.5),
        "args": ["c"],
        "description": "Julia set — infinitely varied shapes from a single complex parameter.",
    },
    "burning_ship": {
        "fn": burning_ship,
        "default_region": (-2.5, -2.0, 1.5, 0.5),
        "args": [],
        "description": "Burning Ship — a fiery cousin of the Mandelbrot set.",
    },
    "tricorn": {
        "fn": tricorn,
        "default_region": (-2.5, -1.25, 1.0, 1.25),
        "args": [],
        "description": "Tricorn (Mandelbar) — a three-fold symmetric Mandelbrot variant.",
    },
    "newton": {
        "fn": newton,
        "default_region": (-1.5, -1.5, 1.5, 1.5),
        "args": [],
        "description": "Newton fractal of z³−1 — shows Newton's method basin boundaries.",
    },
}


def render_frame(
    fractal_name: str,
    width: int,
    height: int,
    region: tuple,          # (x_min, y_min, x_max, y_max)
    max_iters: int,
    julia_c: complex = -0.7 + 0.27j,
) -> list[list[int]]:
    """
    Compute a 2-D grid of iteration counts for the given fractal.
    Returns height x width list of ints.
    """
    x_min, y_min, x_max, y_max = region
    x_step = (x_max - x_min) / width
    y_step = (y_max - y_min) / height

    info = FRACTALS[fractal_name]
    fn = info["fn"]
    grid = []

    for row in range(height):
        y = y_max - row * y_step
        line = []
        for col in range(width):
            x = x_min + col * x_step
            c = complex(x, y)
            if fractal_name == "julia":
                iters = fn(c, julia_c, max_iters)
            else:
                iters = fn(c, max_iters)
            line.append(iters)
        grid.append(line)

    return grid
