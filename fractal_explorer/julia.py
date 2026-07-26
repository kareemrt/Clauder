"""Julia set computation."""


def compute_julia(
    width: int,
    height: int,
    cx: float = -0.7,
    cy: float = 0.27015,
    x_min: float = -1.6,
    x_max: float = 1.6,
    y_min: float = -1.0,
    y_max: float = 1.0,
    max_iter: int = 80,
) -> list[list[int]]:
    """
    Compute a Julia set for constant c = cx + cy*i.
    Returns a 2D grid of iteration counts (0 = inside the set).
    """
    grid = []
    for row in range(height):
        line = []
        for col in range(width):
            zx = x_min + (x_max - x_min) * col / (width - 1)
            zy = y_min + (y_max - y_min) * row / (height - 1)
            line.append(_escape_count(zx, zy, cx, cy, max_iter))
        grid.append(line)
    return grid


def _escape_count(zx: float, zy: float, cx: float, cy: float, max_iter: int) -> int:
    """Return iteration count before escape, or 0 if inside the set."""
    for i in range(1, max_iter + 1):
        zx, zy = zx * zx - zy * zy + cx, 2 * zx * zy + cy
        if zx * zx + zy * zy > 4.0:
            return i
    return 0


# Famous Julia set constants: (cx, cy, name, description)
JULIA_PRESETS = [
    (-0.7,    0.27015, "Dragon",         "Classic dragon-like spirals"),
    (-0.835, -0.2321,  "Dendrite",       "Tree-like branching structure"),
    (-0.8,    0.156,   "Rabbit",         "Douady's rabbit — three lobes"),
    (0.285,   0.01,    "Symmetric",      "Symmetric filaments"),
    (-0.4,    0.6,     "Spiral Galaxy",  "Galactic spiral arms"),
    (0.0,     0.8,     "Rings",          "Concentric ring structure"),
    (-0.7269, 0.1889,  "Feather",        "Delicate feather-like pattern"),
    (-0.12,   0.74,    "San Marco",      "San Marco fractal dragon"),
]
