#!/usr/bin/env python3
"""
Evolving Conway's Game of Life

Cells carry their own birth/survival rules and pass them to offspring
with random mutations. Watch Darwinian selection unfold in your terminal.

Controls:
  [P] / [Space]  Pause / Resume
  [R]            Reset with new random soup
  [C]            Clear the grid
  [+] / [-]      Increase / Decrease speed
  [Q]            Quit
"""

import curses
import random
import time
import argparse


# Classic Conway rules: B3/S23
CONWAY_BIRTH    = frozenset({3})
CONWAY_SURVIVAL = frozenset({2, 3})

MUTATION_RATE = 0.008   # probability per rule-set per step
LINEAGE_DRIFT = 0.04    # probability of color shift on reproduction

# ANSI color pairs (index 1-7)
COLORS = [
    curses.COLOR_GREEN,
    curses.COLOR_CYAN,
    curses.COLOR_BLUE,
    curses.COLOR_MAGENTA,
    curses.COLOR_YELLOW,
    curses.COLOR_RED,
    curses.COLOR_WHITE,
]

# Characters rendered by cell age (youngest → oldest)
AGE_CHARS = "·+▒▓█"


# ---------------------------------------------------------------------------
# Cell
# ---------------------------------------------------------------------------

class Cell:
    __slots__ = ("lineage", "birth", "survival", "age")

    def __init__(self, lineage: int, birth: frozenset, survival: frozenset, age: int = 0):
        self.lineage  = lineage
        self.birth    = birth
        self.survival = survival
        self.age      = age

    def offspring(self) -> "Cell":
        """Return a (possibly mutated) child cell."""
        b = set(self.birth)
        s = set(self.survival)

        if random.random() < MUTATION_RATE:
            n = random.randint(0, 8)
            b.discard(n) if n in b else b.add(n)
        if random.random() < MUTATION_RATE:
            n = random.randint(0, 8)
            s.discard(n) if n in s else s.add(n)

        # Prevent degenerate rule sets that instantly die or explode
        if not b:
            b = {3}
        if not s:
            s = {2}

        new_lineage = (self.lineage + 1) % len(COLORS) if random.random() < LINEAGE_DRIFT else self.lineage
        return Cell(new_lineage, frozenset(b), frozenset(s))


# ---------------------------------------------------------------------------
# Simulation
# ---------------------------------------------------------------------------

class EvolvingLife:
    def __init__(self, width: int, height: int):
        self.width      = width
        self.height     = height
        self.grid: dict[tuple[int, int], Cell] = {}
        self.generation = 0
        self.pop_history: list[int] = []

    def randomize(self, density: float = 0.30) -> None:
        self.grid       = {}
        self.generation = 0
        self.pop_history.clear()
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < density:
                    lineage = random.randint(0, len(COLORS) - 1)
                    self.grid[(x, y)] = Cell(lineage, CONWAY_BIRTH, CONWAY_SURVIVAL)

    # -- neighbor helpers --------------------------------------------------

    def _neighbor_count(self, x: int, y: int) -> int:
        w, h = self.width, self.height
        g = self.grid
        return sum(
            1
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
            if (dx or dy) and ((x + dx) % w, (y + dy) % h) in g
        )

    def _neighbor_cells(self, x: int, y: int) -> list[Cell]:
        w, h = self.width, self.height
        g = self.grid
        return [
            g[(nx, ny)]
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
            if (dx or dy) and (nx := (x + dx) % w, ny := (y + dy) % h) and (nx, ny) in g
        ]

    def _dominant_neighbor(self, x: int, y: int) -> Cell | None:
        neighbors = self._neighbor_cells(x, y)
        if not neighbors:
            return None
        tally: dict[int, int] = {}
        for c in neighbors:
            tally[c.lineage] = tally.get(c.lineage, 0) + 1
        dom = max(tally, key=tally.__getitem__)
        return random.choice([c for c in neighbors if c.lineage == dom])

    # -- step --------------------------------------------------------------

    def step(self) -> None:
        g = self.grid
        candidates: set[tuple[int, int]] = set()
        for x, y in g:
            candidates.add((x, y))
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    candidates.add(((x + dx) % self.width, (y + dy) % self.height))

        new_grid: dict[tuple[int, int], Cell] = {}
        for pos in candidates:
            x, y = pos
            n = self._neighbor_count(x, y)
            if pos in g:
                cell = g[pos]
                if n in cell.survival:
                    child = cell.offspring()
                    child.age = cell.age + 1
                    new_grid[pos] = child
            else:
                parent = self._dominant_neighbor(x, y)
                if parent and n in parent.birth:
                    child = parent.offspring()
                    new_grid[pos] = child

        self.grid = new_grid
        self.generation += 1
        self.pop_history.append(len(new_grid))
        if len(self.pop_history) > 120:
            self.pop_history.pop(0)


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def _pop_sparkline(history: list[int], width: int) -> str:
    if not history:
        return ""
    bars = "▁▂▃▄▅▆▇█"
    peak = max(history) or 1
    step = max(1, len(history) // width)
    line = ""
    for i in range(0, len(history), step):
        idx = int(history[i] / peak * (len(bars) - 1))
        line += bars[idx]
    return line[:width]


def run(stdscr: "curses._CursesWindow") -> None:
    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.start_color()
    curses.use_default_colors()

    for i, fg in enumerate(COLORS, start=1):
        curses.init_pair(i, fg, -1)

    height, width = stdscr.getmaxyx()
    grid_h = height - 3

    sim = EvolvingLife(width, grid_h)
    sim.randomize()

    paused = False
    delay  = 0.06   # seconds per frame

    while True:
        key = stdscr.getch()
        if key in (ord("q"), ord("Q")):
            break
        elif key in (ord("p"), ord("P"), ord(" ")):
            paused = not paused
        elif key in (ord("r"), ord("R")):
            sim.randomize()
        elif key in (ord("c"), ord("C")):
            sim.grid.clear()
        elif key in (ord("+"), ord("=")):
            delay = max(0.01, delay - 0.01)
        elif key == ord("-"):
            delay = min(0.50, delay + 0.01)

        if not paused:
            sim.step()

        stdscr.erase()

        for (x, y), cell in sim.grid.items():
            if 0 <= y < grid_h and 0 <= x < width:
                age_idx = min(cell.age // 6, len(AGE_CHARS) - 1)
                try:
                    stdscr.addstr(y, x, AGE_CHARS[age_idx], curses.color_pair(cell.lineage + 1))
                except curses.error:
                    pass

        # Status bar
        pop       = len(sim.grid)
        gen       = sim.generation
        fps       = int(1 / delay)
        status    = "PAUSED " if paused else "RUNNING"
        spark     = _pop_sparkline(sim.pop_history, 40)
        line_sep  = "─" * width
        line_stat = f" Gen {gen:7,d} │ Pop {pop:6,d} │ {fps:3d} fps │ {status}  {spark}"
        line_ctrl = " [P]ause  [R]eset  [C]lear  [+/-] Speed  [Q]uit"

        try:
            stdscr.addstr(height - 3, 0, line_sep[:width - 1])
            stdscr.addstr(height - 2, 0, line_stat[:width - 1])
            stdscr.addstr(height - 1, 0, line_ctrl[:width - 1])
        except curses.error:
            pass

        stdscr.refresh()
        time.sleep(delay)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.parse_args()

    try:
        curses.wrapper(run)
    except KeyboardInterrupt:
        pass

    print("Thanks for watching the universe evolve.")


if __name__ == "__main__":
    main()
