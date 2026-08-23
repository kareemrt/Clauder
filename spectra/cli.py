"""Command-line interface for Spectra fractal explorer."""

import argparse
import sys
from . import __version__
from .fractals import mandelbrot, julia, burning_ship, newton
from .palettes import list_palettes
from .renderer import to_ascii, to_ascii_newton, save_image, save_newton_image


JULIA_PRESETS = {
    "dendrite":     -0.7269 + 0.1889j,
    "spiral":       -0.4 + 0.6j,
    "galaxy":       0.285 + 0.013j,
    "lightning":    -0.8 + 0.156j,
    "san-marco":    -0.75 + 0.0j,
    "double-spiral": 0.45 + 0.1428j,
    "rabbit":       -0.123 + 0.745j,
    "airplane":     -1.755 + 0j,
}

FRACTAL_BOUNDS = {
    "mandelbrot":    (-2.5, 1.0, -1.25, 1.25),
    "burning-ship":  (-2.5, 1.5, -2.0, 0.5),
    "julia":         (-2.0, 2.0, -2.0, 2.0),
    "newton":        (-2.0, 2.0, -2.0, 2.0),
}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="spectra",
        description="Spectra — Terminal Fractal Explorer  v" + __version__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  spectra mandelbrot                          # ASCII art in terminal
  spectra mandelbrot -o mandelbrot.png        # save high-res PNG
  spectra julia --preset spiral -o spiral.png
  spectra julia --c="-0.4+0.6j" -o custom.png
  spectra burning-ship --palette fire -o ship.png
  spectra newton -o newton.png
  spectra mandelbrot --zoom -0.7 0.0 0.01    # zoom to point
""",
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    sub = p.add_subparsers(dest="fractal", required=True)

    # Shared options factory
    def add_shared(sp):
        sp.add_argument("-W", "--width",   type=int, default=800,  help="image width in pixels")
        sp.add_argument("-H", "--height",  type=int, default=600,  help="image height in pixels")
        sp.add_argument("-i", "--max-iter", type=int, default=256,  help="maximum iterations")
        sp.add_argument("-p", "--palette", choices=list_palettes(), default="inferno")
        sp.add_argument("-o", "--output",  type=str, default=None,
                        help="save to PNG file (omit for ASCII terminal output)")
        sp.add_argument("--zoom", nargs=3, type=float, metavar=("CX", "CY", "RADIUS"),
                        help="zoom into (cx, cy) with given radius")
        return sp

    add_shared(sub.add_parser("mandelbrot", help="Classic Mandelbrot set"))
    add_shared(sub.add_parser("burning-ship", help="Burning Ship fractal"))

    jp = add_shared(sub.add_parser("julia", help="Julia set for a complex constant c"))
    jp.add_argument("--preset", choices=list(JULIA_PRESETS.keys()), default="spiral",
                    help="named Julia set preset")
    jp.add_argument("--c", type=complex, default=None,
                    help="explicit complex constant, e.g. -0.4+0.6j")

    np_ = sub.add_parser("newton", help="Newton fractal for z³ − 1 = 0")
    np_.add_argument("-W", "--width",   type=int, default=800)
    np_.add_argument("-H", "--height",  type=int, default=600)
    np_.add_argument("-i", "--max-iter", type=int, default=64)
    np_.add_argument("-o", "--output",  type=str, default=None)
    np_.add_argument("--zoom", nargs=3, type=float, metavar=("CX", "CY", "RADIUS"))

    sp2 = sub.add_parser("gallery", help="Generate a gallery PNG with all fractal types")
    sp2.add_argument("-o", "--output", type=str, default="gallery/spectra_gallery.png")
    sp2.add_argument("-s", "--size",   type=int, default=400, help="thumbnail size")

    return p


def compute_bounds(fractal: str, zoom: list | None) -> tuple[float, float, float, float]:
    x_min, x_max, y_min, y_max = FRACTAL_BOUNDS[fractal]
    if zoom:
        cx, cy, r = zoom
        x_min, x_max = cx - r, cx + r
        y_min, y_max = cy - r, cy + r
    return x_min, x_max, y_min, y_max


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.fractal == "gallery":
        _run_gallery(args)
        return

    x_min, x_max, y_min, y_max = compute_bounds(args.fractal, args.zoom)

    if args.fractal == "mandelbrot":
        data = mandelbrot(args.width, args.height,
                          x_min, x_max, y_min, y_max, args.max_iter)
        _output(data, args, is_newton=False)

    elif args.fractal == "burning-ship":
        data = burning_ship(args.width, args.height,
                            x_min, x_max, y_min, y_max, args.max_iter)
        _output(data, args, is_newton=False)

    elif args.fractal == "julia":
        c = args.c if args.c is not None else JULIA_PRESETS[args.preset]
        data = julia(args.width, args.height,
                     x_min, x_max, y_min, y_max, args.max_iter, c)
        _output(data, args, is_newton=False)

    elif args.fractal == "newton":
        root_map, speed_map = newton(args.width, args.height,
                                     x_min, x_max, y_min, y_max, args.max_iter)
        if args.output:
            path = save_newton_image(root_map, speed_map, args.output)
            print(f"Saved → {path}")
        else:
            print(to_ascii_newton(root_map, speed_map, width=100, height=40))


def _output(data, args, is_newton: bool):
    if args.output:
        path = save_image(data, args.output, palette=args.palette, max_iter=args.max_iter)
        print(f"Saved → {path}")
    else:
        print(to_ascii(data, max_iter=args.max_iter, width=100, height=40))


def _run_gallery(args):
    from .fractals import mandelbrot, julia, burning_ship, newton
    from .renderer import create_contact_sheet
    print("Generating gallery…")
    items = [
        ("mandelbrot",   mandelbrot(args.size, args.size, -2.5, 1.0, -1.25, 1.25, 256)),
        ("julia/spiral", julia(args.size, args.size, -2, 2, -2, 2, 256, JULIA_PRESETS["spiral"])),
        ("julia/galaxy", julia(args.size, args.size, -2, 2, -2, 2, 256, JULIA_PRESETS["galaxy"])),
        ("burning-ship", burning_ship(args.size, args.size, -2.5, 1.5, -2.0, 0.5, 256)),
        ("julia/rabbit", julia(args.size, args.size, -2, 2, -2, 2, 256, JULIA_PRESETS["rabbit"])),
        ("newton",       newton(args.size, args.size, -2, 2, -2, 2, 64)),
    ]
    create_contact_sheet(items, args.output, palette="inferno",
                         max_iter=256, cols=3, thumb_size=args.size)
    print(f"Gallery saved → {args.output}")
