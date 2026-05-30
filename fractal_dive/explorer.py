"""
Interactive curses-based fractal explorer.

Controls:
  Arrow keys   — pan
  + / -        — zoom in / out
  T            — cycle through color themes
  J            — toggle Julia / Mandelbrot mode
  M            — toggle max iteration depth
  R            — reset to default view
  S            — save current view as ASCII art .txt file
  H            — toggle help overlay
  Q / Esc      — quit
"""

import curses
import os
import time
import numpy as np
from datetime import datetime

from .core import mandelbrot, julia
from .renderer import render_frame, HIDE_CURSOR, SHOW_CURSOR, RESET, CLEAR
from .themes import THEMES, THEME_ORDER

# Default Mandelbrot viewport
DEFAULT_CENTER = (-0.5, 0.0)
DEFAULT_ZOOM = 0.35           # half-width of the viewport in complex-plane units
DEFAULT_MAX_ITER = 256
JULIA_C_PRESETS = [
    -0.7 + 0.27015j,
    -0.4 + 0.6j,
    0.285 + 0.01j,
    -0.70176 - 0.3842j,
    -0.835 - 0.2321j,
    0.45 + 0.1428j,
]
MAX_ITER_LEVELS = [64, 128, 256, 512, 1024]


class Explorer:
    def __init__(self, stdscr):
        self.scr = stdscr
        self.cx, self.cy = DEFAULT_CENTER
        self.zoom = DEFAULT_ZOOM
        self.max_iter = DEFAULT_MAX_ITER
        self.theme_idx = 0
        self.julia_mode = False
        self.julia_preset_idx = 0
        self.show_help = False
        self.dirty = True
        self._data: np.ndarray | None = None

    # ── Properties ──────────────────────────────────────────────────────────

    @property
    def theme_name(self) -> str:
        return THEME_ORDER[self.theme_idx]

    @property
    def palette(self):
        return THEMES[self.theme_name][1]

    @property
    def julia_c(self) -> complex:
        return JULIA_C_PRESETS[self.julia_preset_idx % len(JULIA_C_PRESETS)]

    # ── Viewport helpers ─────────────────────────────────────────────────────

    def _bounds(self, width: int, height: int):
        aspect = (width / 2) / (height / 2)  # half-block trick halves height
        hw = self.zoom
        hh = self.zoom / aspect
        return (
            self.cx - hw, self.cx + hw,
            self.cy - hh, self.cy + hh,
        )

    # ── Render ───────────────────────────────────────────────────────────────

    def _compute(self, width: int, height: int) -> np.ndarray:
        x_min, x_max, y_min, y_max = self._bounds(width, height)
        # We render 2 × terminal_rows pixels per column for the half-block trick
        if self.julia_mode:
            return julia(width, height, x_min, x_max, y_min, y_max,
                         self.julia_c, self.max_iter)
        return mandelbrot(width, height, x_min, x_max, y_min, y_max,
                          self.max_iter)

    def _draw(self):
        rows, cols = self.scr.getmaxyx()
        # Terminal lines available (leave 1 row for status bar)
        term_rows = rows - 1
        pixel_height = term_rows * 2   # 2 pixels per terminal row
        pixel_width = cols

        data = self._compute(pixel_width, pixel_height)
        self._data = data

        frame = render_frame(data, self.max_iter, self.palette)

        # Write frame character by character via curses
        self.scr.erase()
        lines = frame.split("\n")
        for i, line in enumerate(lines[:term_rows]):
            try:
                self.scr.addstr(i, 0, line)
            except curses.error:
                pass

        self._draw_statusbar(rows, cols)
        if self.show_help:
            self._draw_help(rows, cols)

        self.scr.refresh()

    def _draw_statusbar(self, rows: int, cols: int):
        mode = f"Julia  c={self.julia_c:.4f}" if self.julia_mode else "Mandelbrot"
        theme_label = THEMES[self.theme_name][0]
        status = (
            f" {mode}  |  center ({self.cx:.6f}, {self.cy:.6f})  |  "
            f"zoom {1/self.zoom:.1f}×  |  iter {self.max_iter}  |  "
            f"theme: {theme_label}  |  [H]elp  [Q]uit "
        )
        status = status[:cols - 1].ljust(cols - 1)
        try:
            self.scr.addstr(rows - 1, 0, status, curses.A_REVERSE)
        except curses.error:
            pass

    def _draw_help(self, rows: int, cols: int):
        lines = [
            "┌─────────────────────────────────┐",
            "│        FractalDive  Help         │",
            "├─────────────────────────────────┤",
            "│  Arrows    Pan                  │",
            "│  + / -     Zoom in / out        │",
            "│  T         Cycle theme          │",
            "│  J         Toggle Julia mode    │",
            "│  N         Next Julia preset    │",
            "│  M         Cycle max iterations │",
            "│  R         Reset view           │",
            "│  S         Save snapshot        │",
            "│  H         Toggle this help     │",
            "│  Q / Esc   Quit                 │",
            "└─────────────────────────────────┘",
        ]
        start_row = max(0, rows // 2 - len(lines) // 2)
        start_col = max(0, cols // 2 - 18)
        for i, line in enumerate(lines):
            try:
                self.scr.addstr(start_row + i, start_col, line, curses.A_BOLD)
            except curses.error:
                pass

    # ── Save snapshot ────────────────────────────────────────────────────────

    def _save_snapshot(self):
        if self._data is None:
            return
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"fractal_{ts}.txt"
        rows, cols = self._data.shape
        chars = " ░▒▓█"
        lines = []
        for row in range(rows):
            line = ""
            for col in range(cols):
                v = self._data[row, col]
                if v >= self.max_iter:
                    line += " "
                else:
                    idx = int((v / self.max_iter) * (len(chars) - 1))
                    line += chars[idx]
            lines.append(line)
        with open(fname, "w") as f:
            f.write(f"FractalDive Snapshot — {datetime.now().isoformat()}\n")
            f.write(f"Mode: {'Julia  c=' + str(self.julia_c) if self.julia_mode else 'Mandelbrot'}\n")
            f.write(f"Center: ({self.cx:.8f}, {self.cy:.8f})  Zoom: {1/self.zoom:.2f}×\n\n")
            f.write("\n".join(lines))
        return fname

    # ── Main loop ────────────────────────────────────────────────────────────

    def run(self):
        curses.curs_set(0)
        self.scr.nodelay(False)
        self.scr.timeout(50)

        while True:
            if self.dirty:
                self._draw()
                self.dirty = False

            key = self.scr.getch()
            if key == curses.ERR:
                continue

            pan = self.zoom * 0.3
            redraw = True

            if key in (ord("q"), ord("Q"), 27):
                break
            elif key == curses.KEY_LEFT:
                self.cx -= pan
            elif key == curses.KEY_RIGHT:
                self.cx += pan
            elif key == curses.KEY_UP:
                self.cy -= pan
            elif key == curses.KEY_DOWN:
                self.cy += pan
            elif key in (ord("+"), ord("=")):
                self.zoom *= 0.6
            elif key in (ord("-"), ord("_")):
                self.zoom /= 0.6
            elif key in (ord("t"), ord("T")):
                self.theme_idx = (self.theme_idx + 1) % len(THEME_ORDER)
            elif key in (ord("j"), ord("J")):
                self.julia_mode = not self.julia_mode
            elif key in (ord("n"), ord("N")):
                self.julia_preset_idx += 1
            elif key in (ord("m"), ord("M")):
                idx = MAX_ITER_LEVELS.index(self.max_iter) if self.max_iter in MAX_ITER_LEVELS else 2
                self.max_iter = MAX_ITER_LEVELS[(idx + 1) % len(MAX_ITER_LEVELS)]
            elif key in (ord("r"), ord("R")):
                self.cx, self.cy = DEFAULT_CENTER
                self.zoom = DEFAULT_ZOOM
                self.max_iter = DEFAULT_MAX_ITER
            elif key in (ord("h"), ord("H")):
                self.show_help = not self.show_help
            elif key in (ord("s"), ord("S")):
                fname = self._save_snapshot()
                if fname:
                    rows, cols = self.scr.getmaxyx()
                    msg = f" Saved → {fname} "
                    try:
                        self.scr.addstr(rows - 2, 2, msg, curses.A_REVERSE)
                        self.scr.refresh()
                        time.sleep(1.5)
                    except curses.error:
                        pass
            elif key == curses.KEY_RESIZE:
                pass
            else:
                redraw = False

            if redraw:
                self.dirty = True


def launch(start_julia: bool = False):
    """Entry point for the curses explorer."""
    def _main(stdscr):
        exp = Explorer(stdscr)
        exp.julia_mode = start_julia
        exp.run()

    curses.wrapper(_main)
