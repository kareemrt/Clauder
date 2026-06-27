"""Procedural maze generation using the randomized recursive-backtracker algorithm."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

NORTH, SOUTH, EAST, WEST = "N", "S", "E", "W"
OPPOSITE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
DELTA = {NORTH: (-1, 0), SOUTH: (1, 0), EAST: (0, 1), WEST: (0, -1)}


@dataclass
class Maze:
    """A grid of cells connected by open passages (no implicit diagonal moves)."""

    rows: int
    cols: int
    start: tuple = (0, 0)
    end: tuple = field(default=None)
    passages: dict = field(default_factory=dict)  # (r, c) -> set of open directions

    def __post_init__(self):
        if self.end is None:
            self.end = (self.rows - 1, self.cols - 1)
        if not self.passages:
            self.passages = {(r, c): set() for r in range(self.rows) for c in range(self.cols)}

    def in_bounds(self, cell: tuple) -> bool:
        r, c = cell
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, cell: tuple):
        """Yield cells reachable from `cell` through an open passage, in a fixed
        N, S, E, W order so traversal order is deterministic for a given seed."""
        r, c = cell
        for direction in (NORTH, SOUTH, EAST, WEST):
            if direction in self.passages[cell]:
                dr, dc = DELTA[direction]
                yield (r + dr, c + dc)

    def carve(self, cell: tuple, direction: str) -> None:
        r, c = cell
        dr, dc = DELTA[direction]
        other = (r + dr, c + dc)
        self.passages[cell].add(direction)
        self.passages[other].add(OPPOSITE[direction])


def generate_maze(rows: int, cols: int, seed: int | None = None) -> Maze:
    """Generate a perfect maze (single unique path between any two cells)."""
    rng = random.Random(seed)
    maze = Maze(rows=rows, cols=cols)
    visited = {(0, 0)}
    stack = [(0, 0)]

    while stack:
        current = stack[-1]
        r, c = current
        candidates = []
        for direction, (dr, dc) in DELTA.items():
            nxt = (r + dr, c + dc)
            if maze.in_bounds(nxt) and nxt not in visited:
                candidates.append((direction, nxt))

        if not candidates:
            stack.pop()
            continue

        direction, nxt = rng.choice(candidates)
        maze.carve(current, direction)
        visited.add(nxt)
        stack.append(nxt)

    return maze
