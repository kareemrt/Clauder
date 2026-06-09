#!/usr/bin/env python3
"""
Fractals — Terminal Fractal Explorer
A zero-dependency interactive fractal renderer for your terminal.

Usage:
    python main.py                  # interactive mode
    python main.py --fractal m      # start with Mandelbrot
    python main.py --fractal j      # start with Julia set
    python main.py --fractal f      # start with Barnsley Fern
    python main.py --palette fire   # choose color palette
    python main.py --width 120 --height 40
    python main.py --export out.txt # export single frame to text file
    python main.py --demo           # cycle through all fractals automatically
"""
from __future__ import annotations

import argparse
import os
import sys
import time
import termios
import tty
import select
import signal

from fractals import (
    render_fractal,
    render_fern,
    clear_screen,
    hide_cursor,
    show_cursor,
    PALETTES,
)
from fractals.mandelbrot import compute_mandelbrot
from fractals.julia import compute_julia, JULIA_SEEDS
from fractals.barnsley import barnsley_fern, IFS_SYSTEMS
from fractals.renderer import render_splash, terminal_size


PALETTE_KEYS = list(PALETTES.keys())
JULIA_SEED_KEYS = list(JULIA_SEEDS.keys())
IFS_KEYS = list(IFS_SYSTEMS.keys())


class FractalState:
    def __init__(self) -> None:
        self.mode: str = "mandelbrot"     # mandelbrot | julia | fern
        self.cx: float = -0.5
        self.cy: float = 0.0
        self.zoom: float = 1.0
        self.max_iter: int = 80
        self.palette_idx: int = 0
        self.julia_seed_idx: int = 2      # dragon
        self.ifs_idx: int = 0             # fern
        self.dirty: bool = True

    @property
    def palette(self) -> str:
        return PALETTE_KEYS[self.palette_idx % len(PALETTE_KEYS)]

    @property
    def julia_seed(self) -> str:
        return JULIA_SEED_KEYS[self.julia_seed_idx % len(JULIA_SEED_KEYS)]

    @property
    def ifs_name(self) -> str:
        return IFS_KEYS[self.ifs_idx % len(IFS_KEYS)]

    def reset(self) -> None:
        self.cx = -0.5 if self.mode == "mandelbrot" else 0.0
        self.cy = 0.0
        self.zoom = 1.0
        self.max_iter = 80
        self.dirty = True


def _getchar_nonblocking(fd: int, timeout: float = 0.05) -> str | None:
    """Read a single keypress without blocking, returning None if none available."""
    r, _, _ = select.select([fd], [], [], timeout)
    if r:
        ch = os.read(fd, 32)
        return ch.decode("utf-8", errors="ignore")
    return None


def _handle_key(key: str, state: FractalState, width: int, height: int) -> bool:
    """
    Process a keypress, update state.
    Returns True to continue, False to quit.
    """
    pan = 0.15 / state.zoom
    state.dirty = True

    # Quit
    if key in ("q", "Q", "\x1b\x1b", "\x03"):
        return False

    # Fractal mode switch
    elif key in ("m", "M"):
        state.mode = "mandelbrot"
        state.reset()
    elif key in ("j", "J"):
        state.mode = "julia"
        state.cx = 0.0
        state.cy = 0.0
        state.zoom = 1.0
        state.dirty = True
    elif key in ("f", "F"):
        state.mode = "fern"
        state.dirty = True

    # Palette switch
    elif key in ("1", "2", "3", "4", "5", "6"):
        state.palette_idx = int(key) - 1
    elif key in ("p", "P"):
        state.palette_idx = (state.palette_idx + 1) % len(PALETTE_KEYS)

    # Zoom
    elif key in ("+", "="):
        state.zoom *= 1.5
    elif key in ("-", "_"):
        state.zoom /= 1.5
        if state.zoom < 0.01:
            state.zoom = 0.01

    # Pan — WASD and arrow keys
    elif key in ("w", "W") or key == "\x1b[A":
        state.cy -= pan
    elif key in ("s", "S") or key == "\x1b[B":
        state.cy += pan
    elif key in ("a", "A") or key == "\x1b[D":
        state.cx -= pan
    elif key in ("d", "D") or key == "\x1b[C":
        state.cx += pan

    # Iteration depth
    elif key in ("i", "I"):
        state.max_iter = min(512, state.max_iter + 20)
    elif key in ("o", "O"):
        state.max_iter = max(20, state.max_iter - 20)

    # Reset view
    elif key in ("r", "R"):
        state.reset()

    # Cycle Julia seeds (only in Julia mode)
    elif key in ("n", "N") and state.mode == "julia":
        state.julia_seed_idx = (state.julia_seed_idx + 1) % len(JULIA_SEED_KEYS)

    # Cycle IFS type (only in fern mode)
    elif key in ("n", "N") and state.mode == "fern":
        state.ifs_idx = (state.ifs_idx + 1) % len(IFS_KEYS)

    # Save current frame
    elif key in ("S",):
        _save_frame(state, width, height)
        state.dirty = False
        return True

    else:
        state.dirty = False  # unknown key — no redraw needed

    return True


def _compute_and_render(state: FractalState, width: int, height: int) -> None:
    """Compute and render the current fractal."""
    t0 = time.perf_counter()
    render_h = height - 2  # reserve 2 lines for status/help bars

    if state.mode == "mandelbrot":
        grid = compute_mandelbrot(width, render_h, state.cx, state.cy, state.zoom, state.max_iter)
        elapsed = time.perf_counter() - t0
        render_fractal(
            grid, state.palette, width, render_h,
            "Mandelbrot", state.cx, state.cy, state.zoom, state.max_iter, elapsed,
        )

    elif state.mode == "julia":
        grid = compute_julia(
            width, render_h, state.cx, state.cy, state.zoom, state.max_iter, state.julia_seed
        )
        elapsed = time.perf_counter() - t0
        render_fractal(
            grid, state.palette, width, render_h,
            f"Julia/{state.julia_seed}", state.cx, state.cy, state.zoom, state.max_iter, elapsed,
        )

    elif state.mode == "fern":
        fern_grid = barnsley_fern(width, render_h, iterations=150_000, ifs_name=state.ifs_name)
        elapsed = time.perf_counter() - t0
        render_fern(fern_grid, state.palette, width, render_h, state.ifs_name, elapsed)


def _save_frame(state: FractalState, width: int, height: int) -> None:
    """Save the current frame as a plain-text file (no ANSI codes)."""
    from fractals.mandelbrot import compute_mandelbrot
    from fractals.julia import compute_julia
    from fractals.barnsley import barnsley_fern
    from fractals.colormap import PALETTES

    render_h = height - 2
    p = PALETTES[state.palette]
    chars = p["chars"]
    filename = f"fractal_{state.mode}_{int(time.time())}.txt"

    lines: list[str] = []
    if state.mode in ("mandelbrot", "julia"):
        if state.mode == "mandelbrot":
            grid = compute_mandelbrot(width, render_h, state.cx, state.cy, state.zoom, state.max_iter)
        else:
            grid = compute_julia(width, render_h, state.cx, state.cy, state.zoom, state.max_iter, state.julia_seed)
        for row in grid:
            line = []
            for t in row:
                if t == 0.0:
                    line.append(" ")
                else:
                    n = len(chars)
                    line.append(chars[min(int(t * n), n - 1)])
            lines.append("".join(line))
    else:
        fg_grid = barnsley_fern(width, render_h, ifs_name=state.ifs_name)
        for row in fg_grid:
            lines.append("".join("*" if c else " " for c in row))

    with open(filename, "w") as fh:
        fh.write(f"# Fractal Terminal Explorer — {state.mode}\n")
        fh.write(f"# cx={state.cx} cy={state.cy} zoom={state.zoom} iter={state.max_iter}\n\n")
        fh.write("\n".join(lines))


def demo_mode(width: int, height: int) -> None:
    """Cycle through all fractals automatically."""
    state = FractalState()
    hide_cursor()
    clear_screen()

    demos = [
        ("mandelbrot", -0.5, 0.0, 1.0, 80, "cosmic"),
        ("mandelbrot", -0.7269, 0.1889, 80.0, 200, "fire"),
        ("mandelbrot", -1.4011551891, 0.0, 500.0, 300, "neon"),
        ("julia", 0.0, 0.0, 1.0, 80, "ocean"),
        ("julia", 0.0, 0.0, 1.5, 120, "gold"),
        ("fern", 0.0, 0.0, 1.0, 80, "matrix"),
    ]

    try:
        for mode, cx, cy, zoom, iters, palette in demos:
            state.mode = mode
            state.cx = cx
            state.cy = cy
            state.zoom = zoom
            state.max_iter = iters
            state.palette_idx = PALETTE_KEYS.index(palette)
            _compute_and_render(state, width, height)
            time.sleep(3.0)
    finally:
        show_cursor()


def interactive_mode(args: argparse.Namespace) -> None:
    """Full interactive TUI loop."""
    w, h = terminal_size()
    if args.width:
        w = args.width
    if args.height:
        h = args.height

    state = FractalState()

    # Apply CLI args
    mode_map = {"m": "mandelbrot", "j": "julia", "f": "fern",
                "mandelbrot": "mandelbrot", "julia": "julia", "fern": "fern"}
    state.mode = mode_map.get(args.fractal, "mandelbrot")
    if args.palette in PALETTE_KEYS:
        state.palette_idx = PALETTE_KEYS.index(args.palette)

    # Show splash
    render_splash(w, h)
    input()  # wait for enter / any key (blocking is fine for splash)

    hide_cursor()
    clear_screen()

    # Save terminal settings
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    def _cleanup(sig=None, frame=None):
        try:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except Exception:
            pass
        show_cursor()
        clear_screen()
        print("Thanks for exploring fractals! 🌀")
        sys.exit(0)

    signal.signal(signal.SIGINT, _cleanup)
    signal.signal(signal.SIGTERM, _cleanup)

    try:
        tty.setraw(fd)
        while True:
            # Recompute if dirty
            if state.dirty:
                _compute_and_render(state, w, h)
                state.dirty = False

            # Non-blocking key read
            key = _getchar_nonblocking(fd, timeout=0.1)
            if key is None:
                continue

            running = _handle_key(key, state, w, h)
            if not running:
                break

            # Handle terminal resize
            new_w, new_h = terminal_size()
            if args.width:
                new_w = args.width
            if args.height:
                new_h = args.height
            if new_w != w or new_h != h:
                w, h = new_w, new_h
                clear_screen()
                state.dirty = True

    finally:
        _cleanup()


def export_mode(args: argparse.Namespace) -> None:
    """Export a single frame to a text file."""
    w = args.width or 120
    h = args.height or 40

    state = FractalState()
    mode_map = {"m": "mandelbrot", "j": "julia", "f": "fern"}
    state.mode = mode_map.get(args.fractal, "mandelbrot")
    if args.palette in PALETTE_KEYS:
        state.palette_idx = PALETTE_KEYS.index(args.palette)

    print(f"Rendering {state.mode} fractal ({w}x{h})...")
    _save_frame(state, w, h)
    print(f"Exported to fractal_{state.mode}_*.txt")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fractal Terminal Explorer — render fractals in your terminal.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--fractal", "-F", default="m",
        choices=["m", "j", "f", "mandelbrot", "julia", "fern"],
        help="Starting fractal (default: m = Mandelbrot)",
    )
    parser.add_argument(
        "--palette", "-p", default="cosmic",
        choices=PALETTE_KEYS,
        help="Color palette (default: cosmic)",
    )
    parser.add_argument("--width", "-W", type=int, default=0, help="Override terminal width")
    parser.add_argument("--height", "-H", type=int, default=0, help="Override terminal height")
    parser.add_argument("--export", "-e", metavar="FILE", help="Export one frame to text file and exit")
    parser.add_argument("--demo", action="store_true", help="Auto-cycle demo mode")
    args = parser.parse_args()

    if args.demo:
        w, h = terminal_size()
        demo_mode(w, h)
    elif args.export:
        export_mode(args)
    else:
        interactive_mode(args)


if __name__ == "__main__":
    main()
