"""ANSI terminal renderer for EvoLife."""

from __future__ import annotations

import sys
import time
import os
import numpy as np
from typing import List, Optional


# ANSI color codes
class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_WHITE = "\033[97m"

    BG_BLACK = "\033[40m"
    BG_BLUE = "\033[44m"
    BG_CYAN = "\033[46m"

    @staticmethod
    def rgb(r: int, g: int, b: int) -> str:
        return f"\033[38;2;{r};{g};{b}m"

    @staticmethod
    def bg_rgb(r: int, g: int, b: int) -> str:
        return f"\033[48;2;{r};{g};{b}m"


CELL_GLYPHS = {
    "block": "██",
    "dot": " ●",
    "square": "■ ",
    "circle": "◉ ",
    "diamond": "◆ ",
    "plus": "✚ ",
    "ascii": "##",
    "ascii_dot": "* ",
}

DEAD_GLYPH = "  "

THEMES = {
    "matrix": {"alive": Color.BRIGHT_GREEN, "dead": Color.DIM + Color.GREEN, "border": Color.GREEN},
    "ocean": {"alive": Color.BRIGHT_CYAN, "dead": Color.DIM + Color.BLUE, "border": Color.CYAN},
    "fire": {"alive": Color.BRIGHT_YELLOW, "dead": Color.DIM + Color.RED, "border": Color.RED},
    "mono": {"alive": Color.BRIGHT_WHITE, "dead": Color.DIM + Color.WHITE, "border": Color.WHITE},
    "plasma": {"alive": Color.MAGENTA, "dead": Color.DIM + Color.BLUE, "border": Color.MAGENTA},
}


class Renderer:
    def __init__(self, theme: str = "matrix", glyph: str = "block", use_color: bool = True):
        self.theme_name = theme
        self.theme = THEMES.get(theme, THEMES["matrix"])
        self.glyph = CELL_GLYPHS.get(glyph, CELL_GLYPHS["block"])
        self.use_color = use_color

    def _c(self, code: str) -> str:
        return code if self.use_color else ""

    def clear(self) -> None:
        print("\033[2J\033[H", end="", flush=True)

    def move_home(self) -> None:
        print("\033[H", end="", flush=True)

    def hide_cursor(self) -> None:
        print("\033[?25l", end="", flush=True)

    def show_cursor(self) -> None:
        print("\033[?25h", end="", flush=True)

    def render_grid(self, cells: np.ndarray, title: str = "") -> str:
        h, w = cells.shape
        alive_c = self._c(self.theme["alive"])
        dead_c = self._c(self.theme["dead"])
        border_c = self._c(self.theme["border"])
        reset = self._c(Color.RESET)
        bold = self._c(Color.BOLD)

        lines = []
        # Top border
        top = border_c + "╔" + "═" * (w * 2) + "╗" + reset
        lines.append(top)

        for row in cells:
            line = border_c + "║" + reset
            for cell in row:
                if cell:
                    line += alive_c + self.glyph + reset
                else:
                    line += dead_c + DEAD_GLYPH + reset
            line += border_c + "║" + reset
            lines.append(line)

        bot = border_c + "╚" + "═" * (w * 2) + "╝" + reset
        lines.append(bot)
        return "\n".join(lines)

    def render_stats_bar(
        self,
        generation: int,
        population: int,
        born: int,
        died: int,
        evo_gen: Optional[int] = None,
        best_fitness: Optional[float] = None,
        best_lifespan: Optional[int] = None,
    ) -> str:
        bold = self._c(Color.BOLD)
        cyan = self._c(Color.BRIGHT_CYAN)
        yellow = self._c(Color.BRIGHT_YELLOW)
        green = self._c(Color.BRIGHT_GREEN)
        red = self._c(Color.RED)
        reset = self._c(Color.RESET)

        parts = [
            f"{bold}Gen:{reset} {cyan}{generation:>4}{reset}",
            f"{bold}Pop:{reset} {green}{population:>5}{reset}",
            f"{bold}Born:{reset} {green}+{born:<4}{reset}",
            f"{bold}Died:{reset} {red}-{died:<4}{reset}",
        ]
        if evo_gen is not None:
            parts.append(f"{bold}EvoGen:{reset} {yellow}{evo_gen:>3}{reset}")
        if best_fitness is not None:
            parts.append(f"{bold}Fitness:{reset} {yellow}{best_fitness:>7.1f}{reset}")
        if best_lifespan is not None:
            parts.append(f"{bold}Lifespan:{reset} {cyan}{best_lifespan:>4}{reset}")

        return "  ".join(parts)

    def render_evolution_chart(self, history: list, width: int = 50) -> str:
        """ASCII bar chart of fitness over evolution generations."""
        if not history:
            return ""
        bold = self._c(Color.BOLD)
        yellow = self._c(Color.BRIGHT_YELLOW)
        green = self._c(Color.BRIGHT_GREEN)
        reset = self._c(Color.RESET)

        fitnesses = [h["best_fitness"] for h in history]
        max_fit = max(fitnesses) if fitnesses else 1
        chart_height = 8

        lines = [f"{bold}Evolution Progress (Best Fitness){reset}"]
        bar_lines = [""] * chart_height
        recent = history[-width:]

        for entry in recent:
            val = entry["best_fitness"]
            bar_h = int((val / max_fit) * chart_height) if max_fit > 0 else 0
            for row in range(chart_height):
                idx = chart_height - 1 - row
                if idx < bar_h:
                    bar_lines[row] += yellow + "▄" + reset
                else:
                    bar_lines[row] += " "

        for i, bl in enumerate(bar_lines):
            label = f"{max_fit * (chart_height - i) / chart_height:>6.1f} │"
            lines.append(self._c(Color.DIM) + label + reset + bl)

        lines.append("       └" + "─" * len(recent))
        lines.append(f"       Gen 1{'':>{max(0, len(recent)-10)}}Gen {len(history)}")
        return "\n".join(lines)

    def render_genome(self, genome: np.ndarray, label: str = "Best Genome") -> str:
        """Display the genome as a small grid."""
        bold = self._c(Color.BOLD)
        green = self._c(Color.BRIGHT_GREEN)
        reset = self._c(Color.RESET)
        lines = [f"{bold}{label}{reset}"]
        for row in genome:
            lines.append("".join(green + "█" + reset if c else "·" for c in row))
        return "\n".join(lines)

    def render_logo(self) -> str:
        green = self._c(Color.BRIGHT_GREEN)
        yellow = self._c(Color.BRIGHT_YELLOW)
        cyan = self._c(Color.BRIGHT_CYAN)
        bold = self._c(Color.BOLD)
        reset = self._c(Color.RESET)
        return f"""{bold}{green}
  ███████╗██╗   ██╗ ██████╗     ██╗     ██╗███████╗███████╗
  ██╔════╝██║   ██║██╔═══██╗    ██║     ██║██╔════╝██╔════╝
  █████╗  ██║   ██║██║   ██║    ██║     ██║█████╗  █████╗
  ██╔══╝  ╚██╗ ██╔╝██║   ██║    ██║     ██║██╔══╝  ██╔══╝
  ███████╗ ╚████╔╝ ╚██████╔╝    ███████╗██║██║     ███████╗
  ╚══════╝  ╚═══╝   ╚═════╝     ╚══════╝╚═╝╚═╝     ╚══════╝
{reset}{cyan}  Conway's Game of Life + Genetic Evolution Simulator{reset}
  {yellow}Life finds a way.{reset}
"""
