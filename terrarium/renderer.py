"""ANSI terminal renderer for Terrarium."""

import sys
from .world import World
from .entities import EMPTY, PLANT, HERBIVORE, CARNIVORE, WATER, ROCK

# ANSI helpers
RST = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

# Foreground 256-color
def fg(n):
    return f"\033[38;5;{n}m"

# Background 256-color
def bg(n):
    return f"\033[48;5;{n}m"

# Cell chars and colors (fancy Unicode mode)
FANCY = {
    EMPTY:     ("·", DIM + fg(236)),
    PLANT:     ("♣", fg(46)),
    HERBIVORE: ("◉", BOLD + fg(220)),
    CARNIVORE: ("◆", BOLD + fg(196)),
    WATER:     ("≈", fg(33)),
    ROCK:      ("▪", fg(244)),
}

# Plain ASCII fallback
PLAIN = {
    EMPTY:     (".", ""),
    PLANT:     ("*", fg(46)),
    HERBIVORE: ("H", BOLD + fg(220)),
    CARNIVORE: ("C", BOLD + fg(196)),
    WATER:     ("~", fg(33)),
    ROCK:      ("#", fg(244)),
}

# Sparkline block characters
SPARKS = "▁▂▃▄▅▆▇█"


class Renderer:
    def __init__(self, world: World, fancy: bool = True, history_len: int = 40):
        self.world = world
        self.cells = FANCY if fancy else PLAIN
        self.history: list[tuple[int, int, int]] = []
        self.history_len = history_len
        self._initialized = False

    def record(self, counts: tuple[int, int, int]):
        self.history.append(counts)
        if len(self.history) > self.history_len:
            self.history.pop(0)

    # ------------------------------------------------------------------
    # Public render
    # ------------------------------------------------------------------

    def render(self, tick: int, fps: float = 0.0):
        w = self.world
        counts = w.counts()
        self.record(counts)
        plants, herbs, carns = counts

        frame_lines = []

        # ── Title bar ──────────────────────────────────────────────────
        bar_width = w.width + 2
        title = " TERRARIUM — Living Ecosystem Simulator "
        pad = max(0, bar_width - len(title))
        frame_lines.append(
            BOLD + fg(46) + "╔" + "═" * (bar_width - 2) + "╗" + RST
        )
        frame_lines.append(
            BOLD + fg(46) + "║" + RST
            + BOLD + fg(46) + title + " " * pad + RST
            + BOLD + fg(46) + "║" + RST
        )
        frame_lines.append(
            BOLD + fg(46) + "╠" + "═" * (bar_width - 2) + "╣" + RST
        )

        # ── World grid ─────────────────────────────────────────────────
        for y in range(w.height):
            row = BOLD + fg(46) + "║" + RST
            for x in range(w.width):
                t = w.type_grid[y][x]
                char, color = self.cells.get(t, ("?", ""))
                row += color + char + RST
            row += BOLD + fg(46) + "║" + RST
            frame_lines.append(row)

        frame_lines.append(
            BOLD + fg(46) + "╠" + "═" * (bar_width - 2) + "╣" + RST
        )

        # ── Stats panel ────────────────────────────────────────────────
        fps_str = f"{fps:5.1f} fps" if fps > 0 else "  --- fps"
        tick_line = f" Tick {tick:>7}   {fps_str}"
        frame_lines.append(
            BOLD + fg(46) + "║" + RST
            + BOLD + tick_line.ljust(bar_width - 2) + RST
            + BOLD + fg(46) + "║" + RST
        )

        stat_rows = [
            (fg(46)  + "♣" + RST, "Plants    ", plants, 46),
            (fg(220) + "◉" + RST, "Herbivores", herbs,  220),
            (fg(196) + "◆" + RST, "Carnivores", carns,  196),
        ]
        for icon, label, count, color_n in stat_rows:
            bar = self._pop_bar(count, max(plants, herbs, carns, 1), bar_width - 20, color_n)
            line = f" {icon} {label} {count:>5}  {bar}"
            frame_lines.append(
                BOLD + fg(46) + "║" + RST
                + line.ljust(bar_width - 2 + self._ansi_len(line) - len(self._strip_ansi(line))) + RST
                + BOLD + fg(46) + "║" + RST
            )

        # ── Sparkline history ──────────────────────────────────────────
        if len(self.history) >= 4:
            frame_lines.append(
                BOLD + fg(46) + "║" + RST
                + DIM + " Population history:".ljust(bar_width - 2) + RST
                + BOLD + fg(46) + "║" + RST
            )
            for idx, (vals, color_n) in enumerate([
                ([h[0] for h in self.history], 46),
                ([h[1] for h in self.history], 220),
                ([h[2] for h in self.history], 196),
            ]):
                spark = self._sparkline(vals, color_n, bar_width - 4)
                prefix = [" ♣ ", " ◉ ", " ◆ "][idx]
                icon_colored = fg(color_n) + prefix + RST
                line = icon_colored + spark
                frame_lines.append(
                    BOLD + fg(46) + "║" + RST
                    + line + " " * max(0, bar_width - 2 - len(self._strip_ansi(line))) + RST
                    + BOLD + fg(46) + "║" + RST
                )

        # ── Footer ─────────────────────────────────────────────────────
        hint = " [Ctrl+C] exit  [--biome forest|savanna|sparse]"
        frame_lines.append(
            BOLD + fg(46) + "║" + RST
            + DIM + hint.ljust(bar_width - 2) + RST
            + BOLD + fg(46) + "║" + RST
        )
        frame_lines.append(
            BOLD + fg(46) + "╚" + "═" * (bar_width - 2) + "╝" + RST
        )

        # ── Output ─────────────────────────────────────────────────────
        if not self._initialized:
            sys.stdout.write("\033[2J\033[H\033[?25l")  # clear + hide cursor
            self._initialized = True
        else:
            sys.stdout.write("\033[H")  # move to top-left (no clear = less flicker)

        sys.stdout.write("\n".join(frame_lines) + "\n")
        sys.stdout.flush()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _pop_bar(self, value: int, max_val: int, width: int, color_n: int) -> str:
        filled = int((value / max_val) * width) if max_val > 0 else 0
        return fg(color_n) + "█" * filled + DIM + "░" * (width - filled) + RST

    def _sparkline(self, values: list[int], color_n: int, width: int) -> str:
        if not values:
            return ""
        max_v = max(values) or 1
        trimmed = values[-width:]
        chars = []
        for v in trimmed:
            idx = int((v / max_v) * (len(SPARKS) - 1))
            chars.append(fg(color_n) + SPARKS[idx] + RST)
        return "".join(chars)

    @staticmethod
    def _strip_ansi(s: str) -> str:
        import re
        return re.sub(r"\033\[[0-9;]*m", "", s)

    def _ansi_len(self, s: str) -> int:
        return len(s)
