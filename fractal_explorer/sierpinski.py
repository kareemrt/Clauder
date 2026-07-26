"""Sierpinski triangle and other IFS fractals."""


def compute_sierpinski(size: int = 32) -> list[str]:
    """
    Generate a Sierpinski triangle using the XOR trick.
    Returns a list of strings (rows), each of length `size`.
    """
    rows = []
    for y in range(size):
        row = ""
        for x in range(size):
            row += "█" if (x & y) == 0 else " "
        rows.append(row)
    return rows


def compute_dragon_curve(iterations: int = 12) -> list[tuple[float, float]]:
    """
    Generate points of the dragon curve fractal using an L-system.
    Returns a list of (x, y) coordinates.
    """
    sequence = "FX"
    for _ in range(iterations):
        expanded = ""
        for ch in sequence:
            if ch == "X":
                expanded += "X+YF+"
            elif ch == "Y":
                expanded += "-FX-Y"
            else:
                expanded += ch
        sequence = expanded

    x, y = 0.0, 0.0
    angle = 0  # 0=right, 1=up, 2=left, 3=down
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    points = [(x, y)]
    for ch in sequence:
        if ch == "F":
            x += dx[angle]
            y += dy[angle]
            points.append((x, y))
        elif ch == "+":
            angle = (angle + 1) % 4
        elif ch == "-":
            angle = (angle - 1) % 4
    return points


def render_dragon_to_grid(
    points: list[tuple[float, float]], width: int = 60, height: int = 30
) -> list[list[bool]]:
    """Map dragon curve points to a boolean grid."""
    if not points:
        return [[False] * width for _ in range(height)]

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    x_range = x_max - x_min or 1
    y_range = y_max - y_min or 1

    grid = [[False] * width for _ in range(height)]
    for x, y in points:
        col = int((x - x_min) / x_range * (width - 1))
        row = int((y - y_min) / y_range * (height - 1))
        col = max(0, min(width - 1, col))
        row = max(0, min(height - 1, row))
        grid[row][col] = True
    return grid
