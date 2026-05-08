"""ASCII canvas: draws starfield, orbital paths, and planets."""
from __future__ import annotations

import math
import random
from typing import Dict, List, Tuple

from rich.text import Text

from .solar_system import Planet


class Canvas:
    def __init__(self, width: int, height: int, seed: int = 42) -> None:
        self.width = width
        self.height = height
        self.cx = width // 2
        self.cy = height // 2
        # Largest orbit radius that fits inside the canvas given aspect compensation
        self.max_r = min(width // 2 - 3, int((height // 2 - 1) / 0.45))

        rng = random.Random(seed)
        star_count = int(width * height * 0.018)
        self.stars: List[Tuple[int, int]] = [
            (rng.randint(0, width - 1), rng.randint(0, height - 1))
            for _ in range(star_count)
        ]
        self._orbit_cache: Dict[str, List[Tuple[int, int]]] = {}

    def _orbit_points(self, planet: Planet) -> List[Tuple[int, int]]:
        pts: set[Tuple[int, int]] = set()
        r = planet.display_r * self.max_r
        # Step size: smaller radius = coarser sampling is fine; finer for large orbits
        step = max(1, int(360 / (2 * math.pi * r + 1)))
        for deg in range(0, 360, step):
            theta = math.radians(deg)
            x = int(self.cx + r * math.cos(theta))
            y = int(self.cy + r * math.sin(theta) * 0.45)
            if 0 <= x < self.width and 0 <= y < self.height:
                pts.add((x, y))
        return list(pts)

    def render(self, planets: List[Planet], t: float) -> Text:
        # 2D grid of (char, style) pairs
        grid: List[List[Tuple[str, str | None]]] = [
            [(" ", None)] * self.width for _ in range(self.height)
        ]

        def put(x: int, y: int, ch: str, style: str | None) -> None:
            if 0 <= x < self.width and 0 <= y < self.height:
                grid[y][x] = (ch, style)

        # --- Starfield ---
        for sx, sy in self.stars:
            put(sx, sy, "·", "bright_black")

        # --- Orbital paths (cached) ---
        for planet in planets:
            if planet.name not in self._orbit_cache:
                self._orbit_cache[planet.name] = self._orbit_points(planet)
            for px, py in self._orbit_cache[planet.name]:
                if grid[py][px][0] in (" ", "·"):
                    put(px, py, "·", "bright_black")

        # --- Sun ---
        put(self.cx, self.cy, "☀", "bright_yellow")

        # --- Planets + abbreviated labels ---
        for planet in planets:
            px, py = planet.position(t, self.cx, self.cy, self.max_r)
            put(px, py, planet.char, planet.color)
            for i, ch in enumerate(planet.name[:3]):
                lx = px + 2 + i
                if 0 <= lx < self.width and grid[py][lx][0] in (" ", "·"):
                    put(lx, py, ch, planet.color)

        # --- Compose Rich Text ---
        text = Text(no_wrap=True)
        for y in range(self.height):
            for x in range(self.width):
                ch, sty = grid[y][x]
                text.append(ch, style=sty or "")
            if y < self.height - 1:
                text.append("\n")
        return text
