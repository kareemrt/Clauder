"""Terminal rendering engines for cellular automata.

CursesRenderer  — full interactive UI with keyboard controls
SimpleRenderer  — non-interactive ASCII output for demos / testing
"""

import curses
import time
from typing import Optional


# Two-column block chars so each grid cell is visually square
CELL_STYLES = {
    "block":  ("██", "  "),
    "shade":  ("▓▓", "░░"),
    "dot":    ("● ", "  "),
    "square": ("■ ", "· "),
    "hash":   ("##", ".."),
    "cross":  ("╬╬", "  "),
}

HELP = (
    " [SPC] Pause  [R] Random  [C] Clear  [S] Step  "
    "[+/-] Speed  [←→↑↓] Pan  [Q] Quit "
)


class CursesRenderer:
    """Full interactive curses UI for any automaton."""

    def __init__(self, automaton, style: str = "block", speed: int = 10):
        self.automaton = automaton
        on_char, off_char = CELL_STYLES.get(style, CELL_STYLES["block"])
        self.on_char  = on_char
        self.off_char = off_char
        self.cell_w   = len(on_char)
        self.speed    = speed      # target steps per second
        self.paused   = False
        self.vx       = 0          # viewport offset
        self.vy       = 0
        self._screen: Optional[curses.window] = None

    # ── Public entry point ────────────────────────────────────────────────

    def run(self) -> None:
        curses.wrapper(self._loop)

    # ── Internal curses loop ──────────────────────────────────────────────

    def _loop(self, screen: curses.window) -> None:
        self._screen = screen
        self._init_colors()
        curses.curs_set(0)
        screen.nodelay(True)
        screen.keypad(True)

        last_step = time.monotonic()

        while True:
            H, W = screen.getmaxyx()
            screen.erase()
            self._draw_border(H, W)
            self._draw_grid(H, W)
            self._draw_stats(H, W)
            self._draw_help(H, W)
            screen.refresh()

            key = screen.getch()
            if key != -1 and not self._handle_key(key):
                break

            now = time.monotonic()
            interval = 1.0 / max(1, self.speed)
            if not self.paused and (now - last_step) >= interval:
                self.automaton.step()
                last_step = now

            time.sleep(0.008)

    def _init_colors(self) -> None:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN,   -1)  # alive / firing
        curses.init_pair(2, curses.COLOR_YELLOW,  -1)  # refractory
        curses.init_pair(3, curses.COLOR_RED,     -1)  # ant
        curses.init_pair(4, curses.COLOR_CYAN,    -1)  # border / UI chrome
        curses.init_pair(5, curses.COLOR_WHITE,   -1)  # help text
        curses.init_pair(6, curses.COLOR_MAGENTA, -1)  # accent / title

    # ── Drawing helpers ───────────────────────────────────────────────────

    def _put(self, y: int, x: int, text: str, pair: int, bold: bool = False) -> None:
        if self._screen is None:
            return
        H, W = self._screen.getmaxyx()
        if y < 0 or y >= H or x < 0 or x + len(text) > W:
            return
        attr = curses.color_pair(pair)
        if bold:
            attr |= curses.A_BOLD
        try:
            self._screen.addstr(y, x, text, attr)
        except curses.error:
            pass

    def _draw_border(self, H: int, W: int) -> None:
        try:
            self._screen.attron(curses.color_pair(4))
            self._screen.border()
            self._screen.attroff(curses.color_pair(4))
        except curses.error:
            pass
        title = f"  LifeSim ◆ {self.automaton.NAME}  "
        self._put(0, max(1, (W - len(title)) // 2), title, 6, bold=True)

    def _draw_grid(self, H: int, W: int) -> None:
        grid_h = H - 3   # rows inside border minus stat row
        grid_cols = (W - 2) // self.cell_w

        a = self.automaton
        has_ant   = hasattr(a, "ant_at")
        has_brain = hasattr(a, "FIRING")

        for row in range(grid_h):
            for col in range(grid_cols):
                x = col + self.vx
                y = row + self.vy
                sy = 1 + row
                sx = 1 + col * self.cell_w

                if sy >= H - 2 or sx + self.cell_w > W - 1:
                    continue

                if has_ant and a.ant_at(x, y):
                    dir_chars = {0: "↑↑", 1: "→→", 2: "↓↓", 3: "←←"}
                    ch = dir_chars.get(a.ant_dir, "@@")
                    self._put(sy, sx, ch, 3, bold=True)
                elif has_brain:
                    state = a._cells.get((x, y), 0)
                    if state == 2:
                        self._put(sy, sx, self.on_char, 1, bold=True)
                    elif state == 1:
                        self._put(sy, sx, "░░"[:self.cell_w], 2)
                elif a.get(x, y):
                    self._put(sy, sx, self.on_char, 1, bold=True)

    def _draw_stats(self, H: int, W: int) -> None:
        a = self.automaton
        status = "PAUSED ‖" if self.paused else "▶ RUN  "
        line = (
            f" {status}  "
            f"Gen: {a.generation:>7,}  "
            f"Pop: {a.population():>7,}  "
            f"B: {getattr(a, 'births', 0):>5,}  "
            f"D: {getattr(a, 'deaths', 0):>5,}  "
            f"Speed: {self.speed:>2} fps "
        )
        self._put(H - 2, 1, line[:W - 2], 4)

    def _draw_help(self, H: int, W: int) -> None:
        self._put(H - 1, 1, HELP[:W - 2], 5)

    # ── Input handler ─────────────────────────────────────────────────────

    def _handle_key(self, key: int) -> bool:
        """Return False to quit."""
        if key in (ord("q"), ord("Q"), 27):
            return False
        if key == ord(" "):
            self.paused = not self.paused
        elif key in (ord("r"), ord("R")):
            self.automaton.randomize()
        elif key in (ord("c"), ord("C")):
            self.automaton.clear()
        elif key in (ord("s"), ord("S")):
            if self.paused:
                self.automaton.step()
        elif key in (ord("+"), ord("=")):
            self.speed = min(120, self.speed + 2)
        elif key == ord("-"):
            self.speed = max(1, self.speed - 2)
        elif key == curses.KEY_LEFT:
            self.vx = max(0, self.vx - 5)
        elif key == curses.KEY_RIGHT:
            self.vx = min(self.automaton.width - 5, self.vx + 5)
        elif key == curses.KEY_UP:
            self.vy = max(0, self.vy - 3)
        elif key == curses.KEY_DOWN:
            self.vy = min(self.automaton.height - 3, self.vy + 3)
        return True


class SimpleRenderer:
    """Non-interactive ASCII renderer — useful for demos and testing."""

    def __init__(
        self,
        automaton,
        on_char: str = "█",
        off_char: str = " ",
        border: bool = True,
    ):
        self.automaton = automaton
        self.on_char  = on_char
        self.off_char = off_char
        self.border   = border

    def render(self, width: int, height: int, ox: int = 0, oy: int = 0) -> str:
        """Return an ASCII string of width×height cells starting at (ox, oy)."""
        a = self.automaton
        has_ant   = hasattr(a, "ant_at")
        has_brain = hasattr(a, "FIRING")

        rows = []
        if self.border:
            rows.append("+" + "-" * width + "+")

        for row in range(height):
            line = ""
            for col in range(width):
                x, y = col + ox, row + oy
                if has_ant and a.ant_at(x, y):
                    line += "@"
                elif has_brain:
                    state = a._cells.get((x, y), 0)
                    line += "█" if state == 2 else ("░" if state == 1 else " ")
                elif a.get(x, y):
                    line += self.on_char
                else:
                    line += self.off_char

            if self.border:
                rows.append("|" + line + "|")
            else:
                rows.append(line)

        if self.border:
            rows.append("+" + "-" * width + "+")

        return "\n".join(rows)

    def animate(
        self,
        steps: int,
        width: int = 60,
        height: int = 20,
        fps: float = 8.0,
        ox: int = 0,
        oy: int = 0,
    ) -> None:
        """Run a simple terminal animation for `steps` generations."""
        import os
        delay = 1.0 / fps

        for _ in range(steps):
            self.automaton.step()
            a = self.automaton
            # Clear screen
            print("\033[2J\033[H", end="")
            header = (
                f"LifeSim ◆ {a.NAME}  "
                f"Gen: {a.generation:,}  Pop: {a.population():,}"
            )
            print(header)
            print(self.render(width, height, ox, oy))
            time.sleep(delay)
