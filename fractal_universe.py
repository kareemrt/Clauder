#!/usr/bin/env python3
"""
Fractal Universe — ASCII/ANSI fractal art generator.

Pure Python stdlib — no dependencies required.

Usage:
    python fractal_universe.py                          # Classic Mandelbrot
    python fractal_universe.py --preset seahorse        # Seahorse Valley zoom
    python fractal_universe.py --fractal julia          # Julia set (classic)
    python fractal_universe.py --fractal julia --preset dragon
    python fractal_universe.py --fractal burning_ship   # Burning Ship fractal
    python fractal_universe.py --fractal tricorn        # Tricorn (Mandelbar)
    python fractal_universe.py --daily                  # Today's unique fractal
    python fractal_universe.py --list-presets           # Show all presets
    python fractal_universe.py --save-svg output.svg    # Export SVG
    python fractal_universe.py --no-color               # Plain ASCII (no ANSI)
"""

import sys
import math
import colorsys
import datetime
import hashlib
import argparse
import shutil


# ── ANSI Color Utilities ──────────────────────────────────────────────────────

RESET = "\033[0m"


def hsv(h, s, v):
    """Return (r, g, b) integers from HSV floats."""
    r, g, b = colorsys.hsv_to_rgb(h % 1.0, max(0.0, min(1.0, s)), max(0.0, min(1.0, v)))
    return int(r * 255), int(g * 255), int(b * 255)


# ── Color Palettes ────────────────────────────────────────────────────────────

def _fire(t):
    if t < 0.20:
        return hsv(0.00, 1.0, t * 5.0)
    elif t < 0.50:
        return hsv(0.04, 1.0, 1.0)
    elif t < 0.80:
        return hsv(0.10, 1.0 - (t - 0.50) * 1.5, 1.0)
    else:
        return hsv(0.14, 0.3, 1.0)


def _ocean(t):
    return hsv(0.52 + t * 0.13, 0.55 + t * 0.45, 0.15 + t * 0.85)


def _neon(t):
    return hsv(t * 0.88, 1.0, 0.15 + t * 0.85)


def _gold(t):
    return hsv(0.08 + t * 0.04, 1.0 - t * 0.35, 0.10 + t * 0.90)


def _aurora(t):
    return hsv(0.30 + t * 0.48, 0.60 + t * 0.40, 0.05 + t * 0.95)


def _cosmos(t):
    return hsv(0.65 + t * 0.20, 1.0, 0.08 + t * 0.92)


def _crimson(t):
    return hsv(0.95 + t * 0.05, 1.0 - t * 0.20, 0.10 + t * 0.90)


def _ice(t):
    return hsv(0.55 + t * 0.08, 0.90 - t * 0.60, 0.20 + t * 0.80)


PALETTES = {
    "fire":    _fire,
    "ocean":   _ocean,
    "neon":    _neon,
    "gold":    _gold,
    "aurora":  _aurora,
    "cosmos":  _cosmos,
    "crimson": _crimson,
    "ice":     _ice,
}

BLOCKS = " ░▒▓█"
PLAIN  = " .:-=+*#@"  # ASCII-only fallback


# ── Location Presets ──────────────────────────────────────────────────────────

MANDELBROT_PRESETS = {
    "classic":   dict(cx=-0.500000, cy=0.000000, zoom=1.0,    palette="fire"),
    "seahorse":  dict(cx=-0.745000, cy=0.100000, zoom=60.0,   palette="ocean"),
    "elephant":  dict(cx=0.275000,  cy=0.000000, zoom=8.0,    palette="gold"),
    "spiral":    dict(cx=-0.761574, cy=-0.084760, zoom=250.0, palette="aurora"),
    "lightning": dict(cx=-0.390540, cy=-0.586790, zoom=120.0, palette="neon"),
    "galaxy":    dict(cx=-0.159200, cy=1.031700,  zoom=80.0,  palette="cosmos"),
    "minibrot":  dict(cx=-1.749000, cy=0.000000,  zoom=800.0, palette="fire"),
    "valley":    dict(cx=-0.525700, cy=0.524300,  zoom=40.0,  palette="ocean"),
    "dendrite":  dict(cx=0.000000,  cy=1.000000,  zoom=4.0,   palette="ice"),
}

JULIA_PRESETS = {
    "classic":   dict(jcx=-0.70000, jcy=0.27015, palette="fire"),
    "dragon":    dict(jcx=-0.80000, jcy=0.15600, palette="neon"),
    "lightning": dict(jcx=-0.40000, jcy=0.60000, palette="gold"),
    "spiral":    dict(jcx=-0.72690, jcy=0.18890, palette="aurora"),
    "snowflake": dict(jcx=-0.38000, jcy=0.65900, palette="ice"),
    "dendrite":  dict(jcx=0.00000,  jcy=1.00000, palette="cosmos"),
    "rabbit":    dict(jcx=-0.12260, jcy=0.74490, palette="aurora"),
    "galaxy":    dict(jcx=-0.62772, jcy=0.42193, palette="cosmos"),
}


# ── Fractal Computation ───────────────────────────────────────────────────────

def _smooth_escape(n, zx, zy):
    """Smooth iteration count via the potential function (continuous coloring)."""
    try:
        return n + 1.0 - math.log2(math.log2(math.hypot(zx, zy)))
    except (ValueError, ZeroDivisionError):
        return float(n)


def mandelbrot(cx, cy, max_iter):
    x = y = 0.0
    for n in range(max_iter):
        x2, y2 = x * x, y * y
        if x2 + y2 > 4.0:
            return _smooth_escape(n, x, y)
        y = 2.0 * x * y + cy
        x = x2 - y2 + cx
    return float(max_iter)


def julia(zx, zy, cx, cy, max_iter):
    for n in range(max_iter):
        zx2, zy2 = zx * zx, zy * zy
        if zx2 + zy2 > 4.0:
            return _smooth_escape(n, zx, zy)
        zy = 2.0 * zx * zy + cy
        zx = zx2 - zy2 + cx
    return float(max_iter)


def burning_ship(cx, cy, max_iter):
    x = y = 0.0
    for n in range(max_iter):
        x2, y2 = x * x, y * y
        if x2 + y2 > 4.0:
            return _smooth_escape(n, x, y)
        x, y = x2 - y2 + cx, abs(2.0 * x * y) + cy
    return float(max_iter)


def tricorn(cx, cy, max_iter):
    """Tricorn / Mandelbar set: z → conj(z)² + c."""
    x = y = 0.0
    for n in range(max_iter):
        x2, y2 = x * x, y * y
        if x2 + y2 > 4.0:
            return _smooth_escape(n, x, y)
        x, y = x2 - y2 + cx, -2.0 * x * y + cy
    return float(max_iter)


# ── ASCII/ANSI Renderer ───────────────────────────────────────────────────────

def render(
    fractal="mandelbrot",
    width=80,
    height=40,
    cx=-0.5,
    cy=0.0,
    zoom=1.0,
    max_iter=80,
    palette="fire",
    jcx=-0.7,
    jcy=0.27015,
    color=True,
):
    """Render a fractal to a multiline string (ANSI or plain ASCII)."""
    color_fn = PALETTES.get(palette, _fire)

    # Terminal characters are ~2× taller than wide; adjust to avoid squashing
    rx = 3.5 / zoom
    ry = rx * height / (width * 0.475)
    x0 = cx - rx / 2.0
    y1 = cy + ry / 2.0
    dx = rx / width
    dy = ry / height

    _dispatch = {
        "mandelbrot":   lambda px, py: mandelbrot(px, py, max_iter),
        "julia":        lambda px, py: julia(px, py, jcx, jcy, max_iter),
        "burning_ship": lambda px, py: burning_ship(px, py, max_iter),
        "tricorn":      lambda px, py: tricorn(px, py, max_iter),
    }
    compute = _dispatch.get(fractal, _dispatch["mandelbrot"])

    lines = []
    for row in range(height):
        py = y1 - dy * row
        chars = []
        for col in range(width):
            v = compute(x0 + dx * col, py)
            if v >= max_iter:
                chars.append("\033[40m \033[0m" if color else " ")
            else:
                t = (v % max_iter) / max_iter
                if color:
                    r, g, b = color_fn(t)
                    dr = max(0, r // 7)
                    dg = max(0, g // 7)
                    db = max(0, b // 7)
                    ch = BLOCKS[int(t * (len(BLOCKS) - 1))]
                    chars.append(
                        f"\033[48;2;{dr};{dg};{db}m"
                        f"\033[38;2;{r};{g};{b}m"
                        f"{ch}\033[0m"
                    )
                else:
                    chars.append(PLAIN[int(t * (len(PLAIN) - 1))])
        lines.append("".join(chars))

    return "\n".join(lines)


# ── SVG Renderer ──────────────────────────────────────────────────────────────

def render_svg(
    fractal="mandelbrot",
    width=600,
    height=400,
    cx=-0.5,
    cy=0.0,
    zoom=1.0,
    max_iter=100,
    palette="fire",
    jcx=-0.7,
    jcy=0.27015,
):
    """Render a fractal as an SVG string (each pixel = 1×1 <rect>)."""
    color_fn = PALETTES.get(palette, _fire)

    rx = 3.5 / zoom
    ry = rx * height / width
    x0 = cx - rx / 2.0
    y1 = cy + ry / 2.0
    dx = rx / width
    dy = ry / height

    _dispatch = {
        "mandelbrot":   lambda px, py: mandelbrot(px, py, max_iter),
        "julia":        lambda px, py: julia(px, py, jcx, jcy, max_iter),
        "burning_ship": lambda px, py: burning_ship(px, py, max_iter),
        "tricorn":      lambda px, py: tricorn(px, py, max_iter),
    }
    compute = _dispatch.get(fractal, _dispatch["mandelbrot"])

    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        f'  <title>Fractal Universe — {fractal} | {palette}</title>',
        f'  <rect width="{width}" height="{height}" fill="#000"/>',
    ]

    for row in range(height):
        py = y1 - dy * row
        for col in range(width):
            v = compute(x0 + dx * col, py)
            if v >= max_iter:
                fill = "#000000"
            else:
                t = (v % max_iter) / max_iter
                r, g, b = color_fn(t)
                fill = f"#{r:02x}{g:02x}{b:02x}"
            parts.append(
                f'  <rect x="{col}" y="{row}" width="1" height="1" fill="{fill}"/>'
            )

    parts.append("</svg>")
    return "\n".join(parts)


# ── Daily Fractal ─────────────────────────────────────────────────────────────

def daily_fractal():
    """Return render params for today's unique fractal, seeded by the date."""
    seed = datetime.date.today().isoformat()
    h = hashlib.sha256(seed.encode()).hexdigest()

    all_types = ["mandelbrot", "julia", "burning_ship", "tricorn"]
    ftype = all_types[int(h[0], 16) % len(all_types)]

    palette_keys = list(PALETTES.keys())
    pal = palette_keys[int(h[1], 16) % len(palette_keys)]

    if ftype == "mandelbrot":
        presets = list(MANDELBROT_PRESETS.values())
        p = presets[int(h[2], 16) % len(presets)]
        return dict(fractal="mandelbrot", cx=p["cx"], cy=p["cy"],
                    zoom=p["zoom"], palette=pal, jcx=-0.7, jcy=0.27015)
    elif ftype == "julia":
        presets = list(JULIA_PRESETS.values())
        p = presets[int(h[2], 16) % len(presets)]
        return dict(fractal="julia", cx=0.0, cy=0.0, zoom=1.0,
                    palette=pal, jcx=p["jcx"], jcy=p["jcy"])
    elif ftype == "burning_ship":
        zooms = [0.8, 1.0, 1.5, 2.5]
        z = zooms[int(h[3], 16) % len(zooms)]
        return dict(fractal="burning_ship", cx=-0.5, cy=-0.5, zoom=z, palette=pal,
                    jcx=-0.7, jcy=0.27015)
    else:
        return dict(fractal="tricorn", cx=-0.5, cy=0.0, zoom=1.0, palette=pal,
                    jcx=-0.7, jcy=0.27015)


# ── Coloured Banner ───────────────────────────────────────────────────────────

_BANNER = (
    "\033[36m╔══════════════════════════════════════════════════════════════════╗\033[0m\n"
    "\033[36m║\033[0m   \033[35m░▒▓\033[0m  \033[1;97mF R A C T A L   U N I V E R S E\033[0m  \033[35m▓▒░\033[0m   \033[36m║\033[0m\n"
    "\033[36m║\033[0m         \033[90mInfinite mathematical beauty in your terminal\033[0m       \033[36m║\033[0m\n"
    "\033[36m╚══════════════════════════════════════════════════════════════════╝\033[0m"
)

_BANNER_PLAIN = (
    "+=================================================================+\n"
    "|         F R A C T A L   U N I V E R S E                       |\n"
    "|         Infinite mathematical beauty in your terminal          |\n"
    "+=================================================================+"
)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="fractal_universe",
        description="Fractal Universe — ASCII/ANSI fractal art generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Fractal types:
  mandelbrot     The iconic Mandelbrot set
  julia          Julia sets (parametric via --jcx / --jcy)
  burning_ship   The Burning Ship fractal
  tricorn        Tricorn / Mandelbar (z → conjugate(z)² + c)

Palettes:   fire, ocean, neon, gold, aurora, cosmos, crimson, ice

Mandelbrot presets:
  classic, seahorse, elephant, spiral, lightning, galaxy, minibrot, valley, dendrite

Julia presets:
  classic, dragon, lightning, spiral, snowflake, dendrite, rabbit, galaxy

Examples:
  python fractal_universe.py
  python fractal_universe.py --preset seahorse --palette ocean
  python fractal_universe.py --fractal julia --preset dragon
  python fractal_universe.py --fractal burning_ship --palette crimson
  python fractal_universe.py --daily
  python fractal_universe.py --cx -0.7269 --cy 0.1889 --zoom 5 --palette aurora
  python fractal_universe.py --no-color --width 60 --height 28
  python fractal_universe.py --save-svg fractal.svg
""",
    )

    parser.add_argument(
        "--fractal",
        choices=["mandelbrot", "julia", "burning_ship", "tricorn"],
        default="mandelbrot",
        help="Fractal type (default: mandelbrot)",
    )
    parser.add_argument("--preset", metavar="NAME", help="Named location preset")
    parser.add_argument("--palette", choices=list(PALETTES.keys()), help="Color palette")
    parser.add_argument("--zoom",   type=float, default=1.0,     help="Zoom level (default: 1.0)")
    parser.add_argument("--cx",     type=float, default=None,    help="Center X / real axis")
    parser.add_argument("--cy",     type=float, default=None,    help="Center Y / imaginary axis")
    parser.add_argument("--jcx",    type=float, default=-0.7,    help="Julia c (real part)")
    parser.add_argument("--jcy",    type=float, default=0.27015, help="Julia c (imaginary part)")
    parser.add_argument("--width",  type=int,   default=None,    help="Render width (chars)")
    parser.add_argument("--height", type=int,   default=None,    help="Render height (chars)")
    parser.add_argument("--iterations", type=int, default=80,   help="Max iterations (default: 80)")
    parser.add_argument("--no-color", action="store_true",       help="Plain ASCII, no ANSI color")
    parser.add_argument("--daily",    action="store_true",       help="Today's unique daily fractal")
    parser.add_argument("--list-presets", action="store_true",   help="List all named presets")
    parser.add_argument("--save-svg", metavar="FILE",            help="Export as SVG file")

    args = parser.parse_args(argv)

    # ── list presets ────────────────────────────────────────────────────────
    if args.list_presets:
        print("\n  Mandelbrot presets:")
        for k, v in MANDELBROT_PRESETS.items():
            print(f"    {k:<12} center=({v['cx']:.5f}, {v['cy']:.5f}i)  zoom={v['zoom']:.0f}x")
        print("\n  Julia presets:")
        for k, v in JULIA_PRESETS.items():
            print(f"    {k:<12} c = {v['jcx']:.5f} + {v['jcy']:.5f}i")
        print()
        return 0

    # ── resolve parameters ───────────────────────────────────────────────────
    params = dict(
        fractal=args.fractal,
        palette=args.palette or "fire",
        cx=args.cx if args.cx is not None else -0.5,
        cy=args.cy if args.cy is not None else 0.0,
        zoom=args.zoom,
        jcx=args.jcx,
        jcy=args.jcy,
    )

    daily_label = None
    if args.daily:
        today_params = daily_fractal()
        params.update(today_params)
        daily_label = f"Today's fractal ({datetime.date.today()})"
    elif args.preset:
        if args.fractal == "julia":
            pool = JULIA_PRESETS
            if args.preset not in pool:
                parser.error(f"Unknown Julia preset '{args.preset}'. Use --list-presets.")
            p = pool[args.preset]
            params["jcx"] = p["jcx"]
            params["jcy"] = p["jcy"]
            if not args.palette:
                params["palette"] = p["palette"]
        else:
            pool = MANDELBROT_PRESETS
            if args.preset not in pool:
                parser.error(f"Unknown preset '{args.preset}'. Use --list-presets.")
            p = pool[args.preset]
            params["cx"]   = p["cx"]
            params["cy"]   = p["cy"]
            params["zoom"] = p["zoom"]
            if not args.palette:
                params["palette"] = p["palette"]

    # explicit --cx / --cy override preset values
    if args.cx is not None:
        params["cx"] = args.cx
    if args.cy is not None:
        params["cy"] = args.cy

    # ── terminal size ────────────────────────────────────────────────────────
    ts = shutil.get_terminal_size((80, 40))
    w = args.width  or max(40, ts.columns - 2)
    h = args.height or max(20, ts.lines   - 8)

    # ── banner & info ────────────────────────────────────────────────────────
    use_color = not args.no_color
    print()
    print(_BANNER if use_color else _BANNER_PLAIN)
    if daily_label:
        print(f"\n  ✨  {daily_label}")
    print(
        f"\n  Fractal : {params['fractal'].upper():<15}"
        f"  Palette : {params['palette']}"
    )
    print(
        f"  Center  : ({params['cx']:.6f}, {params['cy']:.6f}i)"
        f"  Zoom    : {params['zoom']:.1f}x"
        f"  Iters   : {args.iterations}"
    )
    if params["fractal"] == "julia":
        print(f"  Julia c : {params['jcx']:.5f} + {params['jcy']:.5f}i")
    print()

    # ── render terminal art ──────────────────────────────────────────────────
    art = render(
        fractal=params["fractal"],
        width=w,
        height=h,
        cx=params["cx"],
        cy=params["cy"],
        zoom=params["zoom"],
        max_iter=args.iterations,
        palette=params["palette"],
        jcx=params["jcx"],
        jcy=params["jcy"],
        color=use_color,
    )
    print(art)

    # ── optional SVG export ──────────────────────────────────────────────────
    if args.save_svg:
        svg_w = args.width  or 600
        svg_h = args.height or 400
        print(f"\n  Rendering SVG ({svg_w}×{svg_h}) …", end="", flush=True)
        svg = render_svg(
            fractal=params["fractal"],
            width=svg_w,
            height=svg_h,
            cx=params["cx"],
            cy=params["cy"],
            zoom=params["zoom"],
            max_iter=min(args.iterations, 150),
            palette=params["palette"],
            jcx=params["jcx"],
            jcy=params["jcy"],
        )
        with open(args.save_svg, "w", encoding="utf-8") as fh:
            fh.write(svg)
        print(f"  saved → {args.save_svg}")

    print(f"\n  Run 'python fractal_universe.py --help' for all options.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
