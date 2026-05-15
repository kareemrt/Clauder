#!/usr/bin/env python3
"""
Fractopia - Terminal Fractal Explorer
Renders mathematical fractals as colorized ASCII art in your terminal.
"""

import math
import sys
import argparse
from typing import List, Tuple, Optional

# ANSI color codes
RESET  = '\033[0m'
BOLD   = '\033[1m'
COLORS = [
    '\033[38;5;196m',  # red
    '\033[38;5;202m',  # orange
    '\033[38;5;226m',  # yellow
    '\033[38;5;46m',   # green
    '\033[38;5;51m',   # cyan
    '\033[38;5;21m',   # blue
    '\033[38;5;129m',  # purple
    '\033[38;5;201m',  # magenta
    '\033[38;5;231m',  # white
]
GRADIENT = ' .,·:;+=o*O$#@░▒▓█'


# ─── Math kernels ─────────────────────────────────────────────────────────────

def _mandelbrot(c: complex, max_iter: int) -> int:
    z = 0j
    for n in range(max_iter):
        if z.real * z.real + z.imag * z.imag > 4:
            return n
        z = z * z + c
    return max_iter


def _julia(z: complex, c: complex, max_iter: int) -> int:
    for n in range(max_iter):
        if z.real * z.real + z.imag * z.imag > 4:
            return n
        z = z * z + c
    return max_iter


def _smooth_color(n: int, z: complex, max_iter: int) -> float:
    """Smooth iteration count to eliminate color banding."""
    if n == max_iter:
        return float(max_iter)
    log_zn = math.log(z.real * z.real + z.imag * z.imag) / 2
    nu = math.log(log_zn / math.log(2)) / math.log(2)
    return n + 1 - nu


# ─── Renderers ────────────────────────────────────────────────────────────────

def render_mandelbrot(
    width: int = 80,
    height: int = 40,
    max_iter: int = 128,
    color: bool = True,
    x_center: float = -0.75,
    y_center: float = 0.0,
    zoom: float = 1.0,
) -> str:
    x_range = 3.5 / zoom
    y_range = 2.0 / zoom
    x_min = x_center - x_range / 2
    x_max = x_center + x_range / 2
    y_min = y_center - y_range / 2
    y_max = y_center + y_range / 2

    rows: List[str] = []
    for row in range(height):
        cols: List[str] = []
        for col in range(width):
            cx = x_min + (x_max - x_min) * col / (width - 1)
            cy = y_min + (y_max - y_min) * row / (height - 1)
            c = complex(cx, cy)
            z = 0j
            n = 0
            for n in range(max_iter):
                if z.real * z.real + z.imag * z.imag > 4:
                    break
                z = z * z + c
            else:
                n = max_iter

            t = n / max_iter
            char_idx = min(int(t * (len(GRADIENT) - 1)), len(GRADIENT) - 1)
            char = GRADIENT[char_idx]

            if color and n < max_iter:
                c_idx = int(t * len(COLORS) * 3) % len(COLORS)
                cols.append(f"{COLORS[c_idx]}{char}{RESET}")
            else:
                cols.append(char)
        rows.append(''.join(cols))
    return '\n'.join(rows)


def render_julia(
    width: int = 80,
    height: int = 40,
    max_iter: int = 128,
    color: bool = True,
    c_real: float = -0.7,
    c_imag: float = 0.27015,
    zoom: float = 1.0,
) -> str:
    c = complex(c_real, c_imag)
    x_range = 3.0 / zoom
    y_range = 3.0 / zoom

    rows: List[str] = []
    for row in range(height):
        cols: List[str] = []
        for col in range(width):
            zx = -x_range / 2 + x_range * col / (width - 1)
            zy = -y_range / 2 + y_range * row / (height - 1)
            z = complex(zx, zy)
            n = 0
            for n in range(max_iter):
                if z.real * z.real + z.imag * z.imag > 4:
                    break
                z = z * z + c
            else:
                n = max_iter

            t = n / max_iter
            char_idx = min(int(t * (len(GRADIENT) - 1)), len(GRADIENT) - 1)
            char = GRADIENT[char_idx]

            if color and n < max_iter:
                c_idx = int(t * len(COLORS) * 3) % len(COLORS)
                cols.append(f"{COLORS[c_idx]}{char}{RESET}")
            else:
                cols.append(char)
        rows.append(''.join(cols))
    return '\n'.join(rows)


def _sierpinski_lines(order: int) -> List[str]:
    if order == 0:
        return ['▲']
    prev = _sierpinski_lines(order - 1)
    pad = ' ' * (2 ** (order - 1))
    top    = [pad + line + pad for line in prev]
    bottom = [line + ' ' + line for line in prev]
    return top + bottom


def render_sierpinski(order: int = 5, color: bool = True) -> str:
    lines = _sierpinski_lines(order)
    if not color:
        return '\n'.join(lines)
    result: List[str] = []
    num_colors = len(COLORS)
    for i, line in enumerate(lines):
        depth = int(math.log2(i + 1)) if i > 0 else 0
        c_idx = depth % num_colors
        result.append(f"{COLORS[c_idx]}{line}{RESET}")
    return '\n'.join(result)


def _dragon_sequence(iterations: int) -> List[int]:
    seq = [1]
    for _ in range(iterations - 1):
        seq = seq + [1] + [1 - x for x in reversed(seq)]
    return seq


def render_dragon(iterations: int = 13, color: bool = True) -> str:
    turns = _dragon_sequence(iterations)
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    direction = 0
    x, y = 0, 0
    points: List[Tuple[int, int]] = [(x, y)]

    for turn in turns:
        direction = (direction + (1 if turn == 1 else -1)) % 4
        x += dx[direction]
        y += dy[direction]
        points.append((x, y))

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    w = max_x - min_x + 1
    h = max_y - min_y + 1

    grid = [[False] * w for _ in range(h)]
    for px, py in points:
        grid[py - min_y][px - min_x] = True

    rows: List[str] = []
    for i, row in enumerate(grid):
        line = ''.join('█' if cell else ' ' for cell in row)
        if color:
            c_idx = (i * 3 // max(h, 1)) % len(COLORS)
            rows.append(f"{COLORS[c_idx]}{line}{RESET}")
        else:
            rows.append(line)
    return '\n'.join(rows)


def render_burning_ship(
    width: int = 80,
    height: int = 40,
    max_iter: int = 100,
    color: bool = True,
) -> str:
    x_min, x_max = -2.5, 1.5
    y_min, y_max = -2.0, 0.5

    rows: List[str] = []
    for row in range(height):
        cols: List[str] = []
        for col in range(width):
            cx = x_min + (x_max - x_min) * col / (width - 1)
            cy = y_min + (y_max - y_min) * row / (height - 1)
            zx, zy = 0.0, 0.0
            n = 0
            for n in range(max_iter):
                if zx * zx + zy * zy > 4:
                    break
                zx2 = zx * zx - zy * zy + cx
                zy  = abs(2 * zx * zy) + cy
                zx  = zx2
            else:
                n = max_iter

            t = n / max_iter
            char_idx = min(int(t * (len(GRADIENT) - 1)), len(GRADIENT) - 1)
            char = GRADIENT[char_idx]

            if color and n < max_iter:
                c_idx = int(t * len(COLORS) * 4) % len(COLORS)
                cols.append(f"{COLORS[c_idx]}{char}{RESET}")
            else:
                cols.append(char)
        rows.append(''.join(cols))
    return '\n'.join(rows)


# ─── Gallery mode ─────────────────────────────────────────────────────────────

JULIA_PRESETS = [
    (-0.7,    0.27015, "Classic spiral"),
    (-0.4,    0.6,     "Douady rabbit"),
    (0.285,   0.01,    "Dendrite"),
    (-0.70176,-0.3842, "Sea horse valley"),
    (0.45,    0.1428,  "Feather"),
    (-0.835, -0.2321,  "Fat rabbit"),
]


def gallery(width: int = 80, height: int = 20, color: bool = True) -> None:
    _header("Fractopia Gallery", width, color)
    fractals = [
        ("Mandelbrot Set", render_mandelbrot(width, height, color=color)),
        ("Burning Ship",   render_burning_ship(width, height, color=color)),
        ("Sierpinski Triangle", render_sierpinski(5, color=color)),
    ]
    for cr, ci, name in JULIA_PRESETS[:2]:
        fractals.append((
            f"Julia Set — {name} (c = {cr:+.4f}{ci:+.4f}i)",
            render_julia(width, height, color=color, c_real=cr, c_imag=ci),
        ))
    fractals.append(("Dragon Curve (13 iter)", render_dragon(13, color=color)))

    for title, art in fractals:
        _header(title, width, color)
        print(art)
        print()


# ─── UI helpers ───────────────────────────────────────────────────────────────

def _header(title: str, width: int = 80, color: bool = True) -> None:
    bar = '═' * width
    if color:
        print(f"\n{BOLD}\033[38;5;201m{bar}{RESET}")
        print(f"{BOLD}\033[38;5;201m{title.center(width)}{RESET}")
        print(f"{BOLD}\033[38;5;201m{bar}{RESET}\n")
    else:
        print(f"\n{bar}")
        print(title.center(width))
        print(f"{bar}\n")


BANNER = r"""
  ___               _              _
 | __| _ __ _  __  | |_  ___  _ __(_) __ _
 | _| | '_/ _|/ _| |  _|/ _ \| '_ \ |/ _` |
 |_|  |_| \__\__|   \__|\___/| .__/_|\__,_|
                              |_|
"""


def print_banner(color: bool = True) -> None:
    if color:
        print(f"{BOLD}\033[38;5;129m{BANNER}{RESET}")
        print(f"\033[38;5;245m  Terminal Fractal Explorer  •  pure Python  •  zero dependencies{RESET}\n")
    else:
        print(BANNER)
        print("  Terminal Fractal Explorer  •  pure Python  •  zero dependencies\n")


# ─── CLI ──────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog='fractopia',
        description='Fractopia — render mathematical fractals in your terminal',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
fractal types:
  mandelbrot   Classic Mandelbrot set
  julia        Julia set  (tweak with --c-real / --c-imag)
  sierpinski   Sierpinski triangle  (tweak with --order)
  dragon       Dragon curve  (tweak with --iterations)
  burning      Burning Ship fractal
  gallery      Render all fractals back-to-back

examples:
  fractopia mandelbrot
  fractopia julia --c-real -0.4 --c-imag 0.6
  fractopia sierpinski --order 6
  fractopia dragon --iterations 14
  fractopia mandelbrot --zoom 8 --x-center -0.75 --y-center 0.1
  fractopia gallery --width 100 --height 30
        """,
    )
    p.add_argument('fractal',
                   choices=['mandelbrot', 'julia', 'sierpinski', 'dragon', 'burning', 'gallery'],
                   nargs='?', default='gallery',
                   help='Fractal to render (default: gallery)')
    p.add_argument('--width',       type=int,   default=80,      help='Output width in characters')
    p.add_argument('--height',      type=int,   default=40,      help='Output height in characters')
    p.add_argument('--max-iter',    type=int,   default=128,     help='Max iteration depth')
    p.add_argument('--order',       type=int,   default=5,       help='Sierpinski order (1-7)')
    p.add_argument('--iterations',  type=int,   default=13,      help='Dragon curve fold count')
    p.add_argument('--c-real',      type=float, default=-0.7,    help='Julia c real part')
    p.add_argument('--c-imag',      type=float, default=0.27015, help='Julia c imaginary part')
    p.add_argument('--zoom',        type=float, default=1.0,     help='Zoom factor')
    p.add_argument('--x-center',    type=float, default=-0.75,   help='Mandelbrot viewport X center')
    p.add_argument('--y-center',    type=float, default=0.0,     help='Mandelbrot viewport Y center')
    p.add_argument('--preset',      type=int,   default=None,
                   help='Julia preset 0-5 (overrides --c-real/--c-imag)')
    p.add_argument('--no-color',    action='store_true',         help='Disable ANSI colors')
    return p


def main(argv: Optional[List[str]] = None) -> None:
    args = build_parser().parse_args(argv)
    color = not args.no_color

    print_banner(color)

    if args.preset is not None:
        idx = max(0, min(args.preset, len(JULIA_PRESETS) - 1))
        args.c_real, args.c_imag, preset_name = JULIA_PRESETS[idx]
        print(f"  Using Julia preset {idx}: {preset_name}\n")

    dispatch = {
        'mandelbrot': lambda: render_mandelbrot(
            args.width, args.height, args.max_iter, color,
            args.x_center, args.y_center, args.zoom),
        'julia':      lambda: render_julia(
            args.width, args.height, args.max_iter, color,
            args.c_real, args.c_imag, args.zoom),
        'sierpinski': lambda: render_sierpinski(args.order, color),
        'dragon':     lambda: render_dragon(args.iterations, color),
        'burning':    lambda: render_burning_ship(args.width, args.height, args.max_iter, color),
    }

    if args.fractal == 'gallery':
        gallery(args.width, args.height, color)
        return

    title_map = {
        'mandelbrot': 'Mandelbrot Set',
        'julia':      f'Julia Set  c = {args.c_real:+.5f} {args.c_imag:+.5f}i',
        'sierpinski': f'Sierpinski Triangle  (order {args.order})',
        'dragon':     f'Dragon Curve  ({args.iterations} iterations)',
        'burning':    'Burning Ship',
    }

    _header(title_map[args.fractal], args.width, color)
    print(dispatch[args.fractal]())
    print()


if __name__ == '__main__':
    main()
