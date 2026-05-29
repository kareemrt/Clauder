"""Terminal and text rendering for WorldForge maps."""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import World

RESET = "\033[0m"
BOLD  = "\033[1m"


def render_terminal(world: "World", use_color: bool = True) -> None:
    """Print the world to stdout."""
    for line in _build_lines(world, use_color):
        print(line)


def render_plain(world: "World") -> str:
    """Return a plain (no ANSI) string of the world map."""
    return "\n".join(_build_lines(world, use_color=False))


def render_legend(use_color: bool = True) -> str:
    """Return a formatted biome legend string."""
    from .biomes import BIOMES

    groups = [
        ("OCEAN",    ["DEEP_OCEAN", "OCEAN", "COAST", "BEACH"]),
        ("HOT",      ["DESERT", "SAVANNA", "TROPICAL_FOREST"]),
        ("TEMPERATE",["GRASSLAND", "SHRUBLAND", "TEMPERATE_FOREST"]),
        ("COLD",     ["BOREAL_FOREST", "TUNDRA", "SNOW"]),
        ("TERRAIN",  ["MOUNTAIN", "PEAK", "RIVER", "CITY"]),
    ]
    lines = []
    for label, keys in groups:
        parts = []
        for k in keys:
            b = BIOMES[k]
            ch = f"{b.ansi}{b.char}{RESET}" if use_color else b.char
            parts.append(f"{ch} {b.name}")
        lines.append(f"  [{label}]  " + "   ".join(parts))
    return "\n".join(lines)


# ------------------------------------------------------------------
# Internal helpers
# ------------------------------------------------------------------

def _build_lines(world: "World", use_color: bool) -> list[str]:
    from .biomes import BIOMES

    lines = []
    for y in range(world.size):
        row_parts = []
        for x in range(world.size):
            key = world.biome_at(y, x)
            b = BIOMES[key]
            if use_color:
                row_parts.append(f"{b.ansi}{b.char}{RESET}")
            else:
                row_parts.append(b.char)
        lines.append("".join(row_parts))
    return lines
