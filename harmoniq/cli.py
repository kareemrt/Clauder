"""Command-line interface for Harmoniq."""

import argparse
import sys
import os
from .composer import Composition
from .renderer import render_piano_roll, render_ascii_staff, render_waveform, render_summary_box

_BOLD   = "\033[1m"
_CYAN   = "\033[36m"
_YELLOW = "\033[33m"
_DIM    = "\033[2m"
_RESET  = "\033[0m"

BANNER = f"""{_CYAN}{_BOLD}
  ██╗  ██╗ █████╗ ██████╗ ███╗   ███╗ ██████╗ ███╗   ██╗██╗ ██████╗
  ██║  ██║██╔══██╗██╔══██╗████╗ ████║██╔═══██╗████╗  ██║██║██╔═══██╗
  ███████║███████║██████╔╝██╔████╔██║██║   ██║██╔██╗ ██║██║██║   ██║
  ██╔══██║██╔══██║██╔══██╗██║╚██╔╝██║██║   ██║██║╚██╗██║██║██║▄▄ ██║
  ██║  ██║██║  ██║██║  ██║██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║╚██████╔╝
  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚══▀▀╝
{_RESET}{_DIM}  Mathematical Music Composer  ·  v1.0.0{_RESET}
"""

SOURCES = {
    "fibonacci":   Composition.from_fibonacci,
    "primes":      Composition.from_primes,
    "collatz":     Composition.from_collatz,
    "mandelbrot":  Composition.from_mandelbrot,
    "golden":      Composition.from_golden_ratio,
    "lookandsay":  Composition.from_look_and_say,
}

SCALES_HELP = "major minor dorian phrygian lydian mixolydian pentatonic blues whole_tone"
ROOTS_HELP  = "C C# D D# E F F# G G# A A# B"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="harmoniq",
        description="Compose music from mathematical sequences.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
sequences:
  fibonacci   — 1,1,2,3,5,8,13 ...
  primes      — 2,3,5,7,11,13 ...
  collatz     — 3n+1 chaos sequence
  mandelbrot  — boundary iteration depths
  golden      — powers of φ (golden ratio)
  lookandsay  — Conway's look-and-say lengths

scales: {SCALES_HELP}
roots:  {ROOTS_HELP}

examples:
  harmoniq compose fibonacci --length 32 --scale pentatonic --root G
  harmoniq compose mandelbrot --output nocturne.abc
  harmoniq compose collatz --start 27 --scale minor --root A
  harmoniq demo
""",
    )
    sub = p.add_subparsers(dest="command")

    # compose
    compose = sub.add_parser("compose", help="Compose from a sequence")
    compose.add_argument("source", choices=SOURCES.keys(), help="Mathematical sequence")
    compose.add_argument("--length",  "-n", type=int, default=32,  help="Sequence length (default 32)")
    compose.add_argument("--scale",   "-s", default="major",       help=f"Scale/mode (default: major)")
    compose.add_argument("--root",    "-r", default="C",           help="Root note (default: C)")
    compose.add_argument("--start",         type=int, default=27,  help="Start value for Collatz (default 27)")
    compose.add_argument("--output",  "-o", default=None,          help="Save ABC notation to file")
    compose.add_argument("--no-colour",     action="store_true",   help="Disable terminal colours")

    # demo
    sub.add_parser("demo", help="Run all sequences and display output")

    # info
    info = sub.add_parser("info", help="Show info about a sequence")
    info.add_argument("source", choices=SOURCES.keys())

    return p


def compose_and_display(comp: Composition, output_file=None) -> None:
    print(render_summary_box(comp))
    print()
    print(render_waveform(comp))
    print()
    print(render_piano_roll(comp))
    print()
    print(render_ascii_staff(comp))

    abc = comp.to_abc()
    print(f"\n{_BOLD}{_CYAN}  ♩  ABC Notation (first 20 lines){_RESET}")
    print(_DIM + "  " + "─" * 60 + _RESET)
    for line in abc.splitlines()[:20]:
        print("  " + line)
    print(_DIM + "  ..." + _RESET if len(abc.splitlines()) > 20 else "")

    if output_file:
        with open(output_file, "w") as f:
            f.write(abc)
        print(f"\n{_CYAN}  ✓  Saved to {output_file}{_RESET}")
        print(f"{_DIM}  Open at https://abc.rectanglered.com/ or import into MuseScore{_RESET}")


def run_demo() -> None:
    print(BANNER)
    demos = [
        Composition.from_fibonacci(24),
        Composition.from_primes(24),
        Composition.from_collatz(27),
        Composition.from_mandelbrot(24),
    ]
    for comp in demos:
        print("\n" + "═" * 70)
        compose_and_display(comp)


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        print(BANNER)
        parser.print_help()
        return 0

    if args.command == "demo":
        run_demo()
        return 0

    if args.command == "info":
        print(f"\n  Source: {args.source}")
        from . import sequences as sq
        fn = getattr(sq, args.source.replace("lookandsay", "look_and_say"), None)
        if fn:
            sample = fn(16) if args.source != "collatz" else fn(27)
            print(f"  Sample (n=16): {sample}")
        return 0

    if args.command == "compose":
        fn = SOURCES[args.source]
        kwargs: dict = {"scale": args.scale, "root": args.root}
        if args.source == "collatz":
            kwargs["start"] = args.start
        elif args.source not in ("mandelbrot",):
            kwargs["length"] = args.length

        print(BANNER)
        comp = fn(**kwargs)
        compose_and_display(comp, args.output)
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
