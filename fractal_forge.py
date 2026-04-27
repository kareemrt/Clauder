#!/usr/bin/env python3
"""
FractalForge - Terminal Fractal Explorer & Renderer

Renders Mandelbrot, Julia, and Burning Ship fractals in the terminal
using colored Unicode block characters. Supports PNG export via Pillow.
"""

import argparse
import sys
import os
from typing import Optional, Tuple

# ─── Fractal Engines ─────────────────────────────────────────────────────────

def mandelbrot(c: complex, max_iter: int) -> int:
    z = 0 + 0j
    for i in range(max_iter):
        if z.real * z.real + z.imag * z.imag > 4.0:
            return i
        z = z * z + c
    return max_iter


def julia(z: complex, c: complex, max_iter: int) -> int:
    for i in range(max_iter):
        if z.real * z.real + z.imag * z.imag > 4.0:
            return i
        z = z * z + c
    return max_iter


def burning_ship(c: complex, max_iter: int) -> int:
    z = 0 + 0j
    for i in range(max_iter):
        if z.real * z.real + z.imag * z.imag > 4.0:
            return i
        z = complex(abs(z.real), abs(z.imag)) ** 2 + c
    return max_iter


def tricorn(c: complex, max_iter: int) -> int:
    z = 0 + 0j
    for i in range(max_iter):
        if z.real * z.real + z.imag * z.imag > 4.0:
            return i
        z = z.conjugate() * z.conjugate() + c
    return max_iter


FRACTAL_ENGINES = {
    'mandelbrot':   mandelbrot,
    'julia':        julia,
    'burning_ship': burning_ship,
    'tricorn':      tricorn,
}

# ─── Color Palettes (ANSI 256-color) ─────────────────────────────────────────

def _ansi(code: int) -> str:
    return f'\033[38;5;{code}m'

PALETTES = {
    'cosmic': [
        _ansi(17), _ansi(18), _ansi(19), _ansi(20), _ansi(21), _ansi(27),
        _ansi(33), _ansi(39), _ansi(45), _ansi(51), _ansi(87), _ansi(123),
        _ansi(159), _ansi(195), _ansi(231), _ansi(226), _ansi(220), _ansi(214),
        _ansi(208), _ansi(202), _ansi(196), _ansi(197), _ansi(198), _ansi(165),
        _ansi(129), _ansi(93), _ansi(57), _ansi(21), _ansi(18), _ansi(17),
    ],
    'fire': [
        _ansi(232), _ansi(52), _ansi(88), _ansi(124), _ansi(160), _ansi(196),
        _ansi(202), _ansi(208), _ansi(214), _ansi(220), _ansi(226), _ansi(227),
        _ansi(228), _ansi(229), _ansi(230), _ansi(231),
    ],
    'ocean': [
        _ansi(17), _ansi(18), _ansi(19), _ansi(20), _ansi(21), _ansi(26),
        _ansi(31), _ansi(36), _ansi(41), _ansi(46), _ansi(47), _ansi(48),
        _ansi(49), _ansi(50), _ansi(51), _ansi(87), _ansi(123), _ansi(159),
        _ansi(195), _ansi(231),
    ],
    'neon': [
        _ansi(232), _ansi(55), _ansi(56), _ansi(57), _ansi(93), _ansi(129),
        _ansi(165), _ansi(201), _ansi(200), _ansi(199), _ansi(198), _ansi(197),
        _ansi(196), _ansi(202), _ansi(208), _ansi(214), _ansi(220), _ansi(226),
        _ansi(231),
    ],
    'matrix': [
        _ansi(232), _ansi(22), _ansi(28), _ansi(34), _ansi(40), _ansi(46),
        _ansi(47), _ansi(48), _ansi(49), _ansi(50), _ansi(51), _ansi(231),
    ],
    'ice': [
        _ansi(232), _ansi(17), _ansi(18), _ansi(19), _ansi(20), _ansi(21),
        _ansi(27), _ansi(33), _ansi(39), _ansi(45), _ansi(51), _ansi(87),
        _ansi(123), _ansi(159), _ansi(195), _ansi(231),
    ],
}

RESET  = '\033[0m'
BLACK  = '\033[38;5;232m'
BLOCKS = ' ░▒▓█'

PRESETS = {
    'seahorse':  {'fractal': 'mandelbrot', 'cx': -0.745,   'cy': 0.1,     'zoom': 80.0},
    'elephant':  {'fractal': 'mandelbrot', 'cx': 0.3,      'cy': 0.0,     'zoom': 40.0},
    'star':      {'fractal': 'julia',      'cx': 0.0,      'cy': 0.0,     'zoom': 1.0,
                  'jc_real': -0.4,         'jc_imag': 0.6},
    'dendrite':  {'fractal': 'julia',      'cx': 0.0,      'cy': 0.0,     'zoom': 1.0,
                  'jc_real': 0.0,          'jc_imag': 1.0},
    'swirl':     {'fractal': 'julia',      'cx': 0.0,      'cy': 0.0,     'zoom': 1.0,
                  'jc_real': -0.7269,      'jc_imag': 0.1889},
    'ship':      {'fractal': 'burning_ship', 'cx': -0.5,   'cy': -0.5,   'zoom': 1.0},
}

# ─── Rendering ────────────────────────────────────────────────────────────────

def _compute_grid(
    fractal_type: str,
    width: int,
    height: int,
    cx: float,
    cy: float,
    zoom: float,
    max_iter: int,
    julia_c: complex,
) -> list[list[int]]:
    engine = FRACTAL_ENGINES[fractal_type]
    x_half = 2.0 / zoom
    y_half = 1.0 / zoom

    x_min, x_max = cx - x_half, cx + x_half
    y_min, y_max = cy - y_half, cy + y_half

    grid = []
    for row in range(height):
        y = y_max - (row / height) * (y_max - y_min)
        line = []
        for col in range(width):
            x = x_min + (col / width) * (x_max - x_min)
            c = complex(x, y)
            if fractal_type == 'julia':
                iters = engine(c, julia_c, max_iter)
            else:
                iters = engine(c, max_iter)
            line.append(iters)
        grid.append(line)
    return grid


def render_terminal(
    fractal_type: str,
    width: int,
    height: int,
    cx: float,
    cy: float,
    zoom: float,
    max_iter: int,
    palette_name: str,
    julia_c: complex,
    show_info: bool = False,
) -> None:
    palette = PALETTES.get(palette_name, PALETTES['cosmic'])
    grid = _compute_grid(fractal_type, width, height, cx, cy, zoom, max_iter, julia_c)

    lines = []
    for row in grid:
        parts = []
        for iters in row:
            if iters == max_iter:
                parts.append(f'{BLACK} ')
            else:
                t = iters / max_iter
                char_idx  = min(int(t * (len(BLOCKS) - 1)), len(BLOCKS) - 1)
                color_idx = min(int(t * (len(palette) - 1)), len(palette) - 1)
                parts.append(f'{palette[color_idx]}{BLOCKS[char_idx]}')
        lines.append(''.join(parts) + RESET)

    print('\n'.join(lines))

    if show_info:
        _print_info(fractal_type, cx, cy, zoom, max_iter, julia_c, palette_name)


def _print_info(fractal_type, cx, cy, zoom, max_iter, julia_c, palette):
    bar = '─' * 48
    print(f'\n╭{bar}╮')
    print(f'│{"  FractalForge  —  Render Info":^48}│')
    print(f'├{bar}┤')
    print(f'│  Fractal : {fractal_type.replace("_", " ").title():<36}│')
    print(f'│  Center  : ({cx:.6f}, {cy:.6f}){"":<20}│')
    print(f'│  Zoom    : {zoom:<37.4f}│')
    print(f'│  Iter    : {max_iter:<37}│')
    print(f'│  Palette : {palette:<37}│')
    if fractal_type == 'julia':
        print(f'│  Julia c : {julia_c!s:<37}│')
    print(f'╰{bar}╯')


def save_png(
    fractal_type: str,
    width: int,
    height: int,
    cx: float,
    cy: float,
    zoom: float,
    max_iter: int,
    output_path: str,
    julia_c: complex,
) -> None:
    try:
        from PIL import Image
        import colorsys
    except ImportError:
        sys.exit('Pillow is required for PNG export. Run: pip install Pillow')

    print(f'Rendering {width}×{height} PNG…')
    grid = _compute_grid(fractal_type, width, height, cx, cy, zoom, max_iter, julia_c)
    img = Image.new('RGB', (width, height))
    pixels = img.load()

    for row_idx, row in enumerate(grid):
        for col_idx, iters in enumerate(row):
            if iters == max_iter:
                pixels[col_idx, row_idx] = (0, 0, 0)
            else:
                # Smooth HSV gradient — cycles through hues as iterations increase
                t = iters / max_iter
                hue = (0.65 + t * 2.8) % 1.0
                r, g, b = colorsys.hsv_to_rgb(hue, 0.85, 1.0)
                pixels[col_idx, row_idx] = (int(r * 255), int(g * 255), int(b * 255))

    img.save(output_path)
    print(f'Saved → {output_path}')


def list_presets() -> None:
    print('\n  Available Presets\n  ' + '─' * 40)
    for name, cfg in PRESETS.items():
        frac = cfg['fractal'].replace('_', ' ').title()
        print(f'  {name:<12} {frac:<20} zoom={cfg.get("zoom", 1.0)}')
    print()


# ─── CLI ──────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog='fractal_forge',
        description='FractalForge — Terminal Fractal Explorer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python fractal_forge.py
  python fractal_forge.py --fractal julia --palette fire
  python fractal_forge.py --preset seahorse --palette cosmic
  python fractal_forge.py --fractal mandelbrot --cx -0.745 --cy 0.1 --zoom 80
  python fractal_forge.py --output fractal.png --png-width 3840 --png-height 2160
  python fractal_forge.py --list-presets
        """,
    )
    p.add_argument('--fractal', choices=list(FRACTAL_ENGINES), default='mandelbrot',
                   metavar='TYPE', help='mandelbrot | julia | burning_ship | tricorn')
    p.add_argument('--preset', choices=list(PRESETS),
                   help='Use a named zoom preset (overrides cx/cy/zoom/fractal)')
    p.add_argument('--list-presets', action='store_true', help='List available presets and exit')

    p.add_argument('--width',  type=int,   default=120,  help='Terminal width  (default: 120)')
    p.add_argument('--height', type=int,   default=42,   help='Terminal height (default: 42)')
    p.add_argument('--cx',     type=float, default=-0.5, help='Center X (default: -0.5)')
    p.add_argument('--cy',     type=float, default=0.0,  help='Center Y (default:  0.0)')
    p.add_argument('--zoom',   type=float, default=1.0,  help='Zoom level (default: 1.0)')
    p.add_argument('--iter',   type=int,   default=128,  help='Max iterations (default: 128)')

    p.add_argument('--palette', choices=list(PALETTES), default='cosmic',
                   help='Color palette: ' + ' | '.join(PALETTES))
    p.add_argument('--jc-real', type=float, default=-0.7,     help='Julia c — real part')
    p.add_argument('--jc-imag', type=float, default=0.27015,  help='Julia c — imaginary part')

    p.add_argument('--output',     type=str, default=None, help='Save PNG to this path')
    p.add_argument('--png-width',  type=int, default=1920, help='PNG width  (default: 1920)')
    p.add_argument('--png-height', type=int, default=1080, help='PNG height (default: 1080)')
    p.add_argument('--info', action='store_true', help='Show render info after drawing')
    return p


def main() -> None:
    args = build_parser().parse_args()

    if args.list_presets:
        list_presets()
        return

    # Apply preset (overrides individual flags)
    if args.preset:
        cfg = PRESETS[args.preset]
        args.fractal  = cfg.get('fractal', args.fractal)
        args.cx       = cfg.get('cx',      args.cx)
        args.cy       = cfg.get('cy',      args.cy)
        args.zoom     = cfg.get('zoom',    args.zoom)
        args.jc_real  = cfg.get('jc_real', args.jc_real)
        args.jc_imag  = cfg.get('jc_imag', args.jc_imag)

    julia_c = complex(args.jc_real, args.jc_imag)

    if args.output:
        save_png(
            args.fractal, args.png_width, args.png_height,
            args.cx, args.cy, args.zoom, args.iter,
            args.output, julia_c,
        )
    else:
        render_terminal(
            args.fractal, args.width, args.height,
            args.cx, args.cy, args.zoom, args.iter,
            args.palette, julia_c, show_info=args.info,
        )


if __name__ == '__main__':
    main()
