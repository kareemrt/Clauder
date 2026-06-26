"""Live terminal animation of the flock using plain ANSI escape codes.

No ``curses`` dependency: just clear-and-redraw with ``\\x1b[H`` so it
also works when piped through tools that don't allocate a real tty.
"""

from __future__ import annotations

import sys
import time

from .flock import Flock

_HEADING_CHARS = "→↗↑↖←↙↓↘"
_PREDATOR_CHAR = "✕"


def _heading_char(angle: float) -> str:
    import math
    index = round(angle / (math.tau / 8)) % 8
    return _HEADING_CHARS[index]


def render_frame(flock: Flock, cols: int, rows: int) -> str:
    cfg = flock.config
    grid = [[" "] * cols for _ in range(rows)]
    for boid in flock.prey:
        gx = int(boid.position.x / cfg.width * cols) % cols
        gy = int(boid.position.y / cfg.height * rows) % rows
        grid[gy][gx] = _heading_char(boid.heading())
    for pred in flock.predators:
        gx = int(pred.position.x / cfg.width * cols) % cols
        gy = int(pred.position.y / cfg.height * rows) % rows
        grid[gy][gx] = _PREDATOR_CHAR
    border = "+" + "-" * cols + "+"
    lines = [border] + ["|" + "".join(row) + "|" for row in grid] + [border]
    return "\n".join(lines)


def run_live(flock: Flock, frames: int, cols: int = 80, rows: int = 30, fps: float = 15.0,
             out=sys.stdout) -> None:
    delay = 1.0 / fps if fps > 0 else 0.0
    out.write("\x1b[2J")
    for frame in range(frames):
        out.write("\x1b[H")
        out.write(render_frame(flock, cols, rows))
        out.write(f"\nframe {frame + 1}/{frames}   boids={len(flock.prey)}   predators={len(flock.predators)}\n")
        out.flush()
        flock.step()
        if delay:
            time.sleep(delay)
