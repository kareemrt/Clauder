"""Command-line interface for FractalForge."""

import argparse
import sys
from colorama import Fore, Style

from .fractals import FRACTALS
from .palettes import list_palettes
from .renderer import render_terminal, render_to_file, demo_gallery


BANNER = f"""
{Fore.CYAN}
  ███████╗██████╗  █████╗  ██████╗████████╗ █████╗ ██╗
  ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║
  █████╗  ██████╔╝███████║██║        ██║   ███████║██║
  ██╔══╝  ██╔══██╗██╔══██║██║        ██║   ██╔══██║██║
  ██║     ██║  ██║██║  ██║╚██████╗   ██║   ██║  ██║███████╗
  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝

{Fore.YELLOW}  ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
  ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
  █████╗  ██║   ██║██████╔╝██║  ███╗█████╗
  ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝
  ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
  ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
{Style.RESET_ALL}
  {Fore.WHITE}Terminal Fractal Art Generator  {Fore.CYAN}v1.0.0{Style.RESET_ALL}
"""


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="fractalforge",
        description="FractalForge — Terminal Fractal Art Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Fractals:
  {', '.join(FRACTALS.keys())}

Palettes:
  {', '.join(list_palettes())}

Examples:
  python main.py                                   # Mandelbrot, fire palette
  python main.py -f julia -p neon -a               # Animated Julia set, neon palette
  python main.py -f burning_ship -p ocean -W 140   # Wide Burning Ship
  python main.py -f mandelbrot --zoom -0.5 0 0.4   # Zoom into spiral region
  python main.py --gallery                         # Demo all fractals
  python main.py -f julia -o my_julia.txt          # Save to file
        """,
    )

    p.add_argument("-f", "--fractal",
                   choices=list(FRACTALS.keys()),
                   default="mandelbrot",
                   help="Fractal type (default: mandelbrot)")

    p.add_argument("-p", "--palette",
                   choices=list_palettes(),
                   default="fire",
                   help="Color palette (default: fire)")

    p.add_argument("-W", "--width",
                   type=int, default=120,
                   help="Terminal width in characters (default: 120)")

    p.add_argument("-H", "--height",
                   type=int, default=40,
                   help="Terminal height in lines (default: 40)")

    p.add_argument("-i", "--max-iters",
                   type=int, default=80,
                   help="Maximum iteration depth (default: 80)")

    p.add_argument("--zoom",
                   nargs=3, metavar=("CX", "CY", "RADIUS"),
                   type=float,
                   help="Zoom to center (cx, cy) with given radius")

    p.add_argument("-c", "--julia-c",
                   nargs=2, metavar=("RE", "IM"),
                   type=float, default=[-0.7, 0.27],
                   help="Julia set parameter c = RE + IM*i (default: -0.7+0.27i)")

    p.add_argument("-a", "--animate",
                   action="store_true",
                   help="Animate iteration depth build-up")

    p.add_argument("--frames",
                   type=int, default=20,
                   help="Number of animation frames (default: 20)")

    p.add_argument("-o", "--output",
                   metavar="FILE",
                   help="Save plain-text output to FILE")

    p.add_argument("--gallery",
                   action="store_true",
                   help="Render a gallery of all fractals")

    p.add_argument("--list",
                   action="store_true",
                   help="List available fractals and palettes")

    return p


def run():
    print(BANNER)
    parser = build_parser()
    args = parser.parse_args()

    if args.list:
        print(f"{Fore.CYAN}Fractals:{Style.RESET_ALL}")
        for name, info in FRACTALS.items():
            print(f"  {Fore.YELLOW}{name:<14}{Style.RESET_ALL} {info['description']}")
        print(f"\n{Fore.CYAN}Palettes:{Style.RESET_ALL}")
        for name in list_palettes():
            print(f"  {Fore.YELLOW}{name}{Style.RESET_ALL}")
        return

    if args.gallery:
        demo_gallery()
        return

    region = None
    if args.zoom:
        cx, cy, r = args.zoom
        region = (cx - r, cy - r, cx + r, cy + r)

    julia_c = complex(args.julia_c[0], args.julia_c[1])

    if args.output:
        render_to_file(
            fractal_name=args.fractal,
            filepath=args.output,
            width=args.width,
            height=args.height,
            max_iters=args.max_iters,
            region=region,
            julia_c=julia_c,
        )
    else:
        render_terminal(
            fractal_name=args.fractal,
            width=args.width,
            height=args.height,
            max_iters=args.max_iters,
            palette=args.palette,
            region=region,
            julia_c=julia_c,
            animate=args.animate,
            frames=args.frames,
        )
