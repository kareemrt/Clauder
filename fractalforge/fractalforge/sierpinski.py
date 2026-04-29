"""Sierpinski triangle and carpet fractals."""


def triangle(width: int, height: int, depth: int = 6) -> list[list[bool]]:
    """Return a boolean grid for the Sierpinski triangle."""
    grid = [[False] * width for _ in range(height)]

    def _fill(x: int, y: int, size: int, level: int) -> None:
        if level == 0 or size < 2:
            # Fill a solid triangle
            for row in range(size):
                if y + row >= height:
                    break
                start = x - row
                end = x + row + 1
                for col in range(start, end):
                    if 0 <= col < width:
                        grid[y + row][col] = True
            return

        half = size // 2
        _fill(x, y, half, level - 1)
        _fill(x - half, y + half, half, level - 1)
        _fill(x + half, y + half, half, level - 1)

    size = min(width // 2, height) - 1
    _fill(width // 2, 0, size, depth)
    return grid


def carpet(width: int, height: int, depth: int = 4) -> list[list[bool]]:
    """Return a boolean grid for the Sierpinski carpet."""
    side = min(width, height)
    # Round down to nearest power of 3
    s = 1
    while s * 3 <= side:
        s *= 3

    grid = [[True] * width for _ in range(height)]

    def _cut(x: int, y: int, size: int) -> None:
        if size < 3:
            return
        third = size // 3
        cx = x + third
        cy = y + third
        for row in range(cy, cy + third):
            if row >= height:
                break
            for col in range(cx, cx + third):
                if col >= width:
                    break
                grid[row][col] = False
        for dy in range(3):
            for dx in range(3):
                if dx == 1 and dy == 1:
                    continue
                _cut(x + dx * third, y + dy * third, third)

    _cut(0, 0, s)
    return grid


def barnsley_fern(width: int, height: int, iterations: int = 50000) -> list[list[bool]]:
    """Return a boolean grid for the Barnsley fern via IFS chaos game."""
    import random

    grid = [[False] * width for _ in range(height)]
    x, y = 0.0, 0.0

    for _ in range(iterations):
        r = random.random()
        if r < 0.01:
            x, y = 0.0, 0.16 * y
        elif r < 0.86:
            x, y = 0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6
        elif r < 0.93:
            x, y = 0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6
        else:
            x, y = -0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44

        col = int((x + 3.0) / 6.0 * width)
        row = int((10.0 - y) / 10.0 * height)
        if 0 <= col < width and 0 <= row < height:
            grid[row][col] = True

    return grid
