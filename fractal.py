#!/usr/bin/env python3
"""
Fractal Explorer — generates Mandelbrot and Julia sets as colored terminal art
and saves them as PNG images using only the Python standard library.
"""

import os
import sys
import struct
import zlib
import argparse
import math
from typing import Tuple

# ---------------------------------------------------------------------------
# Color palettes (R, G, B triples mapped across 0..1 escape-time gradient)
# ---------------------------------------------------------------------------

def palette_fire(t: float) -> Tuple[int, int, int]:
    r = int(min(255, 255 * (t * 3)))
    g = int(min(255, 255 * max(0, t * 3 - 1)))
    b = int(min(255, 255 * max(0, t * 3 - 2)))
    return r, g, b


def palette_ocean(t: float) -> Tuple[int, int, int]:
    r = int(9 * (1 - t) * t**3 * 255)
    g = int(15 * (1 - t)**2 * t**2 * 255)
    b = int(8.5 * (1 - t)**3 * t * 255)
    return min(r, 255), min(g, 255), min(b, 255)


def palette_ice(t: float) -> Tuple[int, int, int]:
    r = int(t * 180)
    g = int(t * 220)
    b = int(128 + t * 127)
    return r, g, b


def palette_gold(t: float) -> Tuple[int, int, int]:
    r = int(min(255, t * 2 * 255))
    g = int(min(255, t * 1.5 * 200))
    b = int(t * 80)
    return r, g, b


PALETTES = {
    "fire": palette_fire,
    "ocean": palette_ocean,
    "ice": palette_ice,
    "gold": palette_gold,
}

# ---------------------------------------------------------------------------
# Core math: escape-time iteration
# ---------------------------------------------------------------------------

def mandelbrot(cx: float, cy: float, max_iter: int) -> Tuple[int, float]:
    zx, zy = 0.0, 0.0
    for i in range(max_iter):
        zx2, zy2 = zx * zx, zy * zy
        if zx2 + zy2 > 4.0:
            # Smooth colouring via log of the magnitude
            log_zn = math.log(zx2 + zy2) / 2
            nu = math.log(log_zn / math.log(2)) / math.log(2)
            return i, i + 1 - nu
        zx, zy = zx2 - zy2 + cx, 2 * zx * zy + cy
    return max_iter, float(max_iter)


def julia(zx: float, zy: float, cx: float, cy: float, max_iter: int) -> Tuple[int, float]:
    for i in range(max_iter):
        zx2, zy2 = zx * zx, zy * zy
        if zx2 + zy2 > 4.0:
            log_zn = math.log(zx2 + zy2) / 2
            nu = math.log(log_zn / math.log(2)) / math.log(2)
            return i, i + 1 - nu
        zx, zy = zx2 - zy2 + cx, 2 * zx * zy + cy
    return max_iter, float(max_iter)

# ---------------------------------------------------------------------------
# Render to a 2-D grid of RGB tuples
# ---------------------------------------------------------------------------

def render(
    mode: str,
    width: int,
    height: int,
    cx_range: Tuple[float, float],
    cy_range: Tuple[float, float],
    max_iter: int,
    palette_fn,
    julia_c: Tuple[float, float] = (-0.7, 0.27015),
) -> list:
    pixels = []
    x_min, x_max = cx_range
    y_min, y_max = cy_range

    for py in range(height):
        row = []
        cy = y_min + (y_max - y_min) * py / (height - 1)
        for px in range(width):
            cx = x_min + (x_max - x_min) * px / (width - 1)

            if mode == "mandelbrot":
                iters, smooth = mandelbrot(cx, cy, max_iter)
            else:
                iters, smooth = julia(cx, cy, julia_c[0], julia_c[1], max_iter)

            if iters == max_iter:
                row.append((0, 0, 0))
            else:
                t = (smooth % max_iter) / max_iter
                # Cycle through palette twice for richer banding
                t = (math.sin(t * math.pi * 4) * 0.5 + 0.5)
                row.append(palette_fn(t))
        pixels.append(row)
    return pixels

# ---------------------------------------------------------------------------
# PNG encoder (pure stdlib — no Pillow required)
# ---------------------------------------------------------------------------

def _png_chunk(tag: bytes, data: bytes) -> bytes:
    c = zlib.crc32(tag + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", c)


def save_png(pixels: list, path: str) -> None:
    height = len(pixels)
    width = len(pixels[0])
    raw_rows = []
    for row in pixels:
        raw = bytearray([0])  # filter type: None
        for r, g, b in row:
            raw += bytes([r, g, b])
        raw_rows.append(bytes(raw))
    compressed = zlib.compress(b"".join(raw_rows), 9)
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = (
        b"\x89PNG\r\n\x1a\n"
        + _png_chunk(b"IHDR", ihdr_data)
        + _png_chunk(b"IDAT", compressed)
        + _png_chunk(b"IEND", b"")
    )
    with open(path, "wb") as f:
        f.write(png)

# ---------------------------------------------------------------------------
# Terminal ASCII renderer (256-color ANSI)
# ---------------------------------------------------------------------------

ASCII_GRADIENT = " .:-=+*#%@"


def _ansi_bg(r: int, g: int, b: int) -> str:
    return f"\x1b[48;2;{r};{g};{b}m"


def _ansi_fg(r: int, g: int, b: int) -> str:
    return f"\x1b[38;2;{r};{g};{b}m"


RESET = "\x1b[0m"


def print_ascii(pixels: list, max_iter: int) -> None:
    height = len(pixels)
    width = len(pixels[0])
    lines = []
    for row in pixels:
        line = []
        for r, g, b in row:
            brightness = (r * 299 + g * 587 + b * 114) // (1000 * 256 // len(ASCII_GRADIENT))
            brightness = min(brightness, len(ASCII_GRADIENT) - 1)
            char = ASCII_GRADIENT[brightness]
            line.append(f"{_ansi_fg(r, g, b)}{char}")
        lines.append("".join(line) + RESET)
    print("\n".join(lines))

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Fractal Explorer — Mandelbrot & Julia set renderer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fractal.py                            # Mandelbrot, terminal art
  python fractal.py --mode julia --palette ice # Julia set, ice palette
  python fractal.py --save mandelbrot.png      # Save as PNG
  python fractal.py --mode julia --julia-c -0.4 0.6 --palette fire --save julia.png
""",
    )
    parser.add_argument("--mode", choices=["mandelbrot", "julia"], default="mandelbrot")
    parser.add_argument("--palette", choices=list(PALETTES), default="fire")
    parser.add_argument("--width", type=int, default=120, help="Terminal columns")
    parser.add_argument("--height", type=int, default=40, help="Terminal rows")
    parser.add_argument("--img-width", type=int, default=800, help="PNG pixel width")
    parser.add_argument("--img-height", type=int, default=600, help="PNG pixel height")
    parser.add_argument("--max-iter", type=int, default=256)
    parser.add_argument("--julia-c", nargs=2, type=float, default=[-0.7, 0.27015],
                        metavar=("RE", "IM"), help="Julia set constant c = RE + IM*i")
    parser.add_argument("--save", metavar="FILE.png", help="Save PNG to this path")
    parser.add_argument("--no-terminal", action="store_true", help="Skip terminal output")
    args = parser.parse_args()

    palette_fn = PALETTES[args.palette]

    if args.mode == "mandelbrot":
        cx_range = (-2.5, 1.0)
        cy_range = (-1.2, 1.2)
    else:
        cx_range = (-1.6, 1.6)
        cy_range = (-1.2, 1.2)

    julia_c = tuple(args.julia_c)

    if not args.no_terminal:
        print(f"\n  Fractal Explorer — {args.mode.capitalize()} set  |  palette: {args.palette}\n")
        terminal_pixels = render(
            args.mode, args.width, args.height,
            cx_range, cy_range, args.max_iter, palette_fn, julia_c,
        )
        print_ascii(terminal_pixels, args.max_iter)
        print()

    if args.save:
        print(f"  Rendering {args.img_width}×{args.img_height} PNG … ", end="", flush=True)
        img_pixels = render(
            args.mode, args.img_width, args.img_height,
            cx_range, cy_range, args.max_iter, palette_fn, julia_c,
        )
        save_png(img_pixels, args.save)
        size_kb = os.path.getsize(args.save) // 1024
        print(f"saved → {args.save}  ({size_kb} KB)")


if __name__ == "__main__":
    main()
