"""Live terminal rendering using plain ANSI escape codes (no curses dependency)."""

from __future__ import annotations

import sys
import time

from genesis.simulation import Simulation

CLEAR = "\033[H\033[J"
RESET = "\033[0m"
FOOD_COLOR = "\033[32m"  # green
FOOD_CHAR = "."


def _organism_color(speed: int, vision: int) -> str:
    # map vision -> hue bucket across the 256-color ramp, speed -> brightness
    base = 21 + int((vision / 8) * 9) * 6  # walks through blue->red-ish range
    base = min(base, 231)
    return f"\033[38;5;{base}m"


def render_frame(sim: Simulation) -> str:
    world = sim.world
    grid = [[" " for _ in range(world.width)] for _ in range(world.height)]

    for fx, fy in world.food:
        grid[fy][fx] = f"{FOOD_COLOR}{FOOD_CHAR}{RESET}"

    for org in world.organisms():
        g = org.genome
        glyph = "@" if g.speed >= 3 else ("o" if g.speed == 2 else "*")
        grid[org.y][org.x] = f"{_organism_color(g.speed, g.vision)}{glyph}{RESET}"

    lines = ["".join(row) for row in grid]
    header = f"tick {sim.tick_count:>5}  pop {len(world.organisms()):>4}  food {len(world.food):>4}"
    return CLEAR + header + "\n" + "\n".join(lines) + "\n"


def watch(sim: Simulation, ticks: int, fps: float = 12.0) -> None:
    delay = 1.0 / fps
    try:
        for _ in range(ticks):
            sim.tick()
            sys.stdout.write(render_frame(sim))
            sys.stdout.flush()
            if not sim.world.organisms():
                print("\nExtinction. Everyone starved.")
                break
            time.sleep(delay)
    except KeyboardInterrupt:
        pass
