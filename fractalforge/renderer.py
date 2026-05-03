"""Rendering: terminal ANSI output and plain-text file export."""

import sys
import time
from colorama import init, Fore, Style

from .fractals import render_frame, FRACTALS
from .palettes import color_for_iters, list_palettes

init(autoreset=True)


def render_terminal(
    fractal_name: str,
    width: int = 120,
    height: int = 40,
    max_iters: int = 80,
    palette: str = "fire",
    region: tuple | None = None,
    julia_c: complex = -0.7 + 0.27j,
    animate: bool = False,
    frames: int = 20,
) -> None:
    """Render fractal to terminal with ANSI colors."""
    if region is None:
        region = FRACTALS[fractal_name]["default_region"]

    _print_header(fractal_name, width, max_iters, palette, region)

    if animate:
        _animate(fractal_name, width, height, max_iters, palette, region, julia_c, frames)
    else:
        grid = render_frame(fractal_name, width, height, region, max_iters, julia_c)
        _print_grid(grid, max_iters, palette)

    _print_footer(fractal_name)


def render_to_file(
    fractal_name: str,
    filepath: str,
    width: int = 120,
    height: int = 40,
    max_iters: int = 80,
    region: tuple | None = None,
    julia_c: complex = -0.7 + 0.27j,
) -> None:
    """Render fractal to a plain-text file (no ANSI)."""
    if region is None:
        region = FRACTALS[fractal_name]["default_region"]

    chars = " .:-=+*#%@"
    grid = render_frame(fractal_name, width, height, region, max_iters, julia_c)

    lines = []
    for row in grid:
        line = ""
        for iters in row:
            if iters == max_iters:
                line += " "
            else:
                ratio = iters / max_iters
                idx = min(int(ratio * (len(chars) - 1)), len(chars) - 1)
                line += chars[idx]
        lines.append(line)

    with open(filepath, "w") as f:
        f.write(f"# FractalForge — {fractal_name.title()}\n")
        f.write(f"# Region: {region}  Max iters: {max_iters}\n\n")
        f.write("\n".join(lines))
        f.write("\n")

    print(f"{Fore.GREEN}Saved to {filepath}{Style.RESET_ALL}")


def _print_grid(grid, max_iters, palette):
    for row in grid:
        line = ""
        for iters in row:
            color, char = color_for_iters(iters, max_iters, palette)
            line += f"{color}{char}"
        print(line + Style.RESET_ALL)


def _animate(fractal_name, width, height, max_iters, palette, region, julia_c, frames):
    """Animate by gradually increasing max_iters."""
    step = max(1, max_iters // frames)
    for f in range(frames):
        current_iters = max(8, step * (f + 1))
        sys.stdout.write(f"\033[{height + 1}A")  # move cursor up
        grid = render_frame(fractal_name, width, height, region, current_iters, julia_c)
        for row in grid:
            line = ""
            for iters in row:
                color, char = color_for_iters(iters, current_iters, palette)
                line += f"{color}{char}"
            print(line + Style.RESET_ALL)
        print(f"\r{Fore.CYAN}  Iteration depth: {current_iters:4d}{Style.RESET_ALL}", end="", flush=True)
        time.sleep(0.05)
    print()


def _print_header(fractal_name, width, max_iters, palette, region):
    info = FRACTALS[fractal_name]
    bar = "─" * width
    print(f"\n{Fore.CYAN}{bar}")
    print(f"  {Fore.WHITE}FractalForge  {Fore.YELLOW}✦  {Fore.GREEN}{fractal_name.title()}")
    print(f"  {Fore.WHITE}{info['description']}")
    print(f"  {Fore.CYAN}Palette:{Style.RESET_ALL} {palette}  "
          f"{Fore.CYAN}Iterations:{Style.RESET_ALL} {max_iters}  "
          f"{Fore.CYAN}Region:{Style.RESET_ALL} {tuple(round(v,3) for v in region)}")
    print(f"{Fore.CYAN}{bar}{Style.RESET_ALL}\n")


def _print_footer(fractal_name):
    print(f"\n{Fore.CYAN}  FractalForge · github.com/kareemrt/clauder · "
          f"Run {Fore.YELLOW}python main.py --help{Fore.CYAN} for options{Style.RESET_ALL}\n")


def demo_gallery():
    """Render a quick gallery of all fractals at low resolution."""
    configs = [
        ("mandelbrot", "fire",     None,         80),
        ("julia",      "neon",     None,         80),
        ("burning_ship","ocean",   None,         80),
        ("tricorn",    "rainbow",  None,         80),
        ("newton",     "matrix",   None,         60),
    ]
    for name, pal, region, mi in configs:
        render_terminal(name, width=100, height=28, max_iters=mi,
                        palette=pal, region=region)
        print()
