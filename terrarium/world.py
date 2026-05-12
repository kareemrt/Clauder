"""Grid world and spatial operations for Terrarium."""

import random
from collections import deque
from .entities import Plant, Herbivore, Carnivore, EMPTY, PLANT, HERBIVORE, CARNIVORE, WATER, ROCK


class World:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # grid[y][x] = entity object or None
        self.grid = [[None] * width for _ in range(height)]
        # type_grid[y][x] = cell type constant for fast lookup
        self.type_grid = [[EMPTY] * width for _ in range(height)]

    def in_bounds(self, y: int, x: int) -> bool:
        return 0 <= y < self.height and 0 <= x < self.width

    def get(self, y: int, x: int):
        return self.grid[y][x]

    def place(self, y: int, x: int, entity, entity_type: int):
        self.grid[y][x] = entity
        self.type_grid[y][x] = entity_type

    def remove(self, y: int, x: int):
        self.grid[y][x] = None
        self.type_grid[y][x] = EMPTY

    def move(self, src_y: int, src_x: int, dst_y: int, dst_x: int):
        entity = self.grid[src_y][src_x]
        etype = self.type_grid[src_y][src_x]
        self.grid[src_y][src_x] = None
        self.type_grid[src_y][src_x] = EMPTY
        self.grid[dst_y][dst_x] = entity
        self.type_grid[dst_y][dst_x] = etype

    def neighbors4(self, y: int, x: int):
        """Cardinal direction neighbors."""
        result = []
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ny, nx = y + dy, x + dx
            if self.in_bounds(ny, nx):
                result.append((ny, nx))
        return result

    def neighbors8(self, y: int, x: int):
        """All 8-directional neighbors."""
        result = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                ny, nx = y + dy, x + dx
                if self.in_bounds(ny, nx):
                    result.append((ny, nx))
        return result

    def empty_neighbors(self, y: int, x: int):
        return [(ny, nx) for ny, nx in self.neighbors8(y, x)
                if self.type_grid[ny][nx] == EMPTY]

    def plant_neighbors(self, y: int, x: int):
        return [(ny, nx) for ny, nx in self.neighbors8(y, x)
                if self.type_grid[ny][nx] == PLANT]

    def herbivore_neighbors(self, y: int, x: int):
        return [(ny, nx) for ny, nx in self.neighbors8(y, x)
                if self.type_grid[ny][nx] == HERBIVORE]

    def find_nearest(self, y: int, x: int, target_type: int, max_range: int = 7):
        """BFS to find nearest cell of target_type. Returns (ny, nx) or None."""
        visited = {(y, x)}
        queue = deque([(y, x, 0)])
        passable = {EMPTY, PLANT, HERBIVORE, target_type}

        while queue:
            cy, cx, dist = queue.popleft()
            if dist > max_range:
                return None
            if dist > 0 and self.type_grid[cy][cx] == target_type:
                return cy, cx
            for ny, nx in self.neighbors8(cy, cx):
                if (ny, nx) not in visited and self.type_grid[ny][nx] in passable:
                    visited.add((ny, nx))
                    queue.append((ny, nx, dist + 1))
        return None

    def step_toward(self, y: int, x: int, ty: int, tx: int):
        """Return one step from (y,x) toward (ty,tx), preferring empty cells."""
        dy = 0 if ty == y else (1 if ty > y else -1)
        dx = 0 if tx == x else (1 if tx > x else -1)

        candidates = []
        if dy != 0 and dx != 0:
            candidates = [(y + dy, x + dx), (y + dy, x), (y, x + dx)]
        elif dy != 0:
            candidates = [(y + dy, x)]
        else:
            candidates = [(y, x + dx)]

        for ny, nx in candidates:
            if self.in_bounds(ny, nx):
                t = self.type_grid[ny][nx]
                if t in (EMPTY, HERBIVORE):
                    return ny, nx
        return None

    def counts(self):
        plants = herbs = carns = 0
        for row in self.type_grid:
            for t in row:
                if t == PLANT:
                    plants += 1
                elif t == HERBIVORE:
                    herbs += 1
                elif t == CARNIVORE:
                    carns += 1
        return plants, herbs, carns
