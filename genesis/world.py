"""World: a toroidal grid holding food and organisms."""

from __future__ import annotations

import random
from typing import Optional

from genesis.organism import Organism

Coord = tuple[int, int]


class World:
    def __init__(self, width: int, height: int, rng: random.Random):
        self.width = width
        self.height = height
        self.rng = rng
        self.food: set[Coord] = set()
        self.occupied: dict[Coord, Organism] = {}

    def wrap(self, x: int, y: int) -> Coord:
        return x % self.width, y % self.height

    def organisms(self) -> list[Organism]:
        return list(self.occupied.values())

    # -- food -----------------------------------------------------------

    def spawn_food(self, target_density: float) -> None:
        """Top up food until it covers roughly `target_density` of empty cells."""
        capacity = int(self.width * self.height * target_density)
        deficit = capacity - len(self.food)
        for _ in range(max(0, deficit)):
            x = self.rng.randrange(self.width)
            y = self.rng.randrange(self.height)
            if (x, y) not in self.occupied:
                self.food.add((x, y))

    def take_food(self, coord: Coord) -> bool:
        if coord in self.food:
            self.food.remove(coord)
            return True
        return False

    # -- spatial queries --------------------------------------------------

    def cells_within(self, x: int, y: int, radius: int) -> list[Coord]:
        cells = []
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue
                cells.append(self.wrap(x + dx, y + dy))
        return cells

    def nearest_food(self, x: int, y: int, radius: int) -> Optional[Coord]:
        best: Optional[Coord] = None
        best_dist = radius + 1
        for fx, fy in self.food:
            dx = min(abs(fx - x), self.width - abs(fx - x))
            dy = min(abs(fy - y), self.height - abs(fy - y))
            dist = max(dx, dy)
            if dist <= radius and dist < best_dist:
                best = (fx, fy)
                best_dist = dist
        return best

    def step_toward(self, x: int, y: int, target: Coord, steps: int) -> Coord:
        tx, ty = target
        for _ in range(steps):
            dx = ((tx - x + self.width // 2) % self.width) - self.width // 2
            dy = ((ty - y + self.height // 2) % self.height) - self.height // 2
            x, y = self.wrap(x + (dx and (1 if dx > 0 else -1)), y + (dy and (1 if dy > 0 else -1)))
        return x, y

    def random_step(self, x: int, y: int, steps: int) -> Coord:
        for _ in range(steps):
            x, y = self.wrap(x + self.rng.choice((-1, 0, 1)), y + self.rng.choice((-1, 0, 1)))
        return x, y

    def free_neighbor(self, x: int, y: int) -> Optional[Coord]:
        candidates = self.cells_within(x, y, 1)
        self.rng.shuffle(candidates)
        for c in candidates:
            if c not in self.occupied:
                return c
        return None

    # -- mutation of occupancy ------------------------------------------

    def place(self, org: Organism) -> None:
        self.occupied[(org.x, org.y)] = org

    def move(self, org: Organism, new_coord: Coord) -> None:
        if new_coord == (org.x, org.y):
            return
        if new_coord in self.occupied:
            return  # cell taken this tick; stay put
        del self.occupied[(org.x, org.y)]
        org.x, org.y = new_coord
        self.occupied[new_coord] = org

    def remove(self, org: Organism) -> None:
        self.occupied.pop((org.x, org.y), None)
