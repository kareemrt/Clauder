"""Core cellular automaton simulation engines.

Three distinct models of computation, each producing wildly different
emergent behavior from identical simple rules applied to a 2D grid.
"""

from collections import defaultdict
import random


class GameOfLife:
    """Conway's Game of Life — the canonical cellular automaton (1970).

    Rules (B3/S23):
      - A live cell survives with 2 or 3 live neighbors.
      - A dead cell is born with exactly 3 live neighbors.
      - All other cells die or stay dead.
    """

    NAME = "Conway's Game of Life"
    DESCRIPTION = "Classic 2D cellular automaton by John Conway (1970)"

    def __init__(self, width: int, height: int, wrap: bool = True):
        self.width = width
        self.height = height
        self.wrap = wrap
        self.generation = 0
        self.births = 0
        self.deaths = 0
        self._cells: set = set()

    # --- Cell access ---

    def set(self, x: int, y: int, alive: bool = True) -> None:
        if self.wrap:
            x, y = x % self.width, y % self.height
        elif not (0 <= x < self.width and 0 <= y < self.height):
            return
        if alive:
            self._cells.add((x, y))
        else:
            self._cells.discard((x, y))

    def get(self, x: int, y: int) -> bool:
        if self.wrap:
            x, y = x % self.width, y % self.height
        return (x, y) in self._cells

    def toggle(self, x: int, y: int) -> None:
        self.set(x, y, not self.get(x, y))

    def population(self) -> int:
        return len(self._cells)

    def cells(self):
        return frozenset(self._cells)

    # --- Lifecycle ---

    def clear(self) -> None:
        self._cells.clear()
        self.generation = 0
        self.births = 0
        self.deaths = 0

    def randomize(self, density: float = 0.3) -> None:
        self.clear()
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < density:
                    self._cells.add((x, y))

    def step(self) -> tuple:
        """Advance one generation. Returns (births, deaths)."""
        neighbor_counts: dict = defaultdict(int)

        for (x, y) in self._cells:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if self.wrap:
                        nx %= self.width
                        ny %= self.height
                    elif not (0 <= nx < self.width and 0 <= ny < self.height):
                        continue
                    neighbor_counts[(nx, ny)] += 1

        new_cells: set = set()
        births = 0
        deaths = 0

        for (x, y), count in neighbor_counts.items():
            if (x, y) in self._cells:
                if count in (2, 3):
                    new_cells.add((x, y))
                else:
                    deaths += 1
            else:
                if count == 3:
                    new_cells.add((x, y))
                    births += 1

        deaths += sum(1 for pos in self._cells if pos not in new_cells
                      and pos not in neighbor_counts)

        self.births = births
        self.deaths = deaths
        self._cells = new_cells
        self.generation += 1

        return births, deaths

    def history_snapshot(self) -> frozenset:
        return frozenset(self._cells)


class BriansBrain:
    """Brian's Brain — a 3-state cellular automaton by Brian Silverman.

    States:
      2 = Firing (on)     — drawn as bright cell
      1 = Refractory (dying) — drawn as dim cell
      0 = Dead (off)

    Rules:
      - Firing  → Refractory (always)
      - Refractory → Dead (always)
      - Dead → Firing if exactly 2 firing neighbors
    """

    NAME = "Brian's Brain"
    DESCRIPTION = "3-state automaton: firing, refractory, and dead cells"

    FIRING = 2
    REFRACTORY = 1
    DEAD = 0

    def __init__(self, width: int, height: int, wrap: bool = True):
        self.width = width
        self.height = height
        self.wrap = wrap
        self.generation = 0
        self.births = 0
        self.deaths = 0
        self._cells: dict = {}

    def set(self, x: int, y: int, state: int = 2) -> None:
        if self.wrap:
            x, y = x % self.width, y % self.height
        if state == self.DEAD:
            self._cells.pop((x, y), None)
        else:
            self._cells[(x, y)] = state

    def get(self, x: int, y: int) -> int:
        if self.wrap:
            x, y = x % self.width, y % self.height
        return self._cells.get((x, y), self.DEAD)

    def population(self) -> int:
        return sum(1 for s in self._cells.values() if s == self.FIRING)

    def cells(self):
        return dict(self._cells)

    def clear(self) -> None:
        self._cells.clear()
        self.generation = 0
        self.births = 0
        self.deaths = 0

    def randomize(self, density: float = 0.15) -> None:
        self.clear()
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < density:
                    self._cells[(x, y)] = self.FIRING

    def step(self) -> tuple:
        firing_neighbors: dict = defaultdict(int)

        for (x, y), state in self._cells.items():
            if state == self.FIRING:
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if self.wrap:
                            nx %= self.width
                            ny %= self.height
                        elif not (0 <= nx < self.width and 0 <= ny < self.height):
                            continue
                        firing_neighbors[(nx, ny)] += 1

        new_cells: dict = {}
        births = 0
        deaths = 0

        for (x, y), state in self._cells.items():
            if state == self.FIRING:
                new_cells[(x, y)] = self.REFRACTORY
            # REFRACTORY → DEAD (simply omit from new_cells)
            elif state == self.REFRACTORY:
                deaths += 1

        for (x, y), count in firing_neighbors.items():
            if (x, y) not in self._cells and count == 2:
                new_cells[(x, y)] = self.FIRING
                births += 1

        self.births = births
        self.deaths = deaths
        self._cells = new_cells
        self.generation += 1

        return births, deaths


class LangtonsAnt:
    """Langton's Ant — a Turing-complete 2D cellular automaton (1986).

    An 'ant' traverses a binary-colored grid:
      - On a WHITE cell: turn right 90°, flip cell to black, move forward
      - On a BLACK cell: turn left 90°, flip cell to white, move forward

    After ~10,000 steps the ant constructs an emergent 'highway' pattern.
    """

    NAME = "Langton's Ant"
    DESCRIPTION = "An ant traverses a grid, flipping colors and changing direction"

    NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3

    _TURN_RIGHT = {0: 1, 1: 2, 2: 3, 3: 0}
    _TURN_LEFT  = {0: 3, 3: 2, 2: 1, 1: 0}
    _DX = {0: 0, 1: 1, 2: 0, 3: -1}
    _DY = {0: -1, 1: 0, 2: 1, 3: 0}

    def __init__(self, width: int, height: int, wrap: bool = True):
        self.width = width
        self.height = height
        self.wrap = wrap
        self.generation = 0
        self.births = 0
        self.deaths = 0
        self._black: set = set()
        self.ant_x = width // 2
        self.ant_y = height // 2
        self.ant_dir = self.NORTH

    def get(self, x: int, y: int) -> bool:
        return (x, y) in self._black

    def ant_at(self, x: int, y: int) -> bool:
        return self.ant_x == x and self.ant_y == y

    def cells(self):
        return frozenset(self._black)

    def population(self) -> int:
        return len(self._black)

    def clear(self) -> None:
        self._black.clear()
        self.ant_x = self.width // 2
        self.ant_y = self.height // 2
        self.ant_dir = self.NORTH
        self.generation = 0

    def randomize(self, density: float = 0.0) -> None:
        self.clear()
        if density > 0:
            for y in range(self.height):
                for x in range(self.width):
                    if random.random() < density:
                        self._black.add((x, y))

    def step(self) -> tuple:
        x, y = self.ant_x, self.ant_y

        if (x, y) in self._black:
            self.ant_dir = self._TURN_LEFT[self.ant_dir]
            self._black.discard((x, y))
            self.deaths += 1
        else:
            self.ant_dir = self._TURN_RIGHT[self.ant_dir]
            self._black.add((x, y))
            self.births += 1

        nx = x + self._DX[self.ant_dir]
        ny = y + self._DY[self.ant_dir]

        if self.wrap:
            nx %= self.width
            ny %= self.height
        else:
            nx = max(0, min(self.width - 1, nx))
            ny = max(0, min(self.height - 1, ny))

        self.ant_x = nx
        self.ant_y = ny
        self.generation += 1

        return self.births, self.deaths
