"""Quick showcase script — runs all fractals at reduced resolution."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fractalforge import mandelbrot, julia, sierpinski, renderer
from fractalforge.palettes import PALETTE_NAMES

W, H = 80, 28


def divider(title: str) -> None:
    renderer.print_header("✦ FractalForge ✦", title)


print("\n" + "=" * 80)
print("  FractalForge — Fractal Art Engine Showcase".center(80))
print("=" * 80 + "\n")

divider("Mandelbrot Set — Fire Palette")
grid = mandelbrot.compute(W, H, **{k: v for k, v in mandelbrot.PRESETS["classic"].items() if k != "max_iter"}, max_iter=128)
print(renderer.render_smooth(grid, "fire", "block"))
renderer.print_legend("fire", "block")

print()

divider("Mandelbrot — Seahorse Valley — Ocean Palette")
grid = mandelbrot.compute(W, H, **{k: v for k, v in mandelbrot.PRESETS["seahorse"].items() if k != "max_iter"}, max_iter=256)
print(renderer.render_smooth(grid, "ocean", "block"))
renderer.print_legend("ocean", "block")

print()

divider("Julia Set — Dragon — Plasma Palette")
grid = julia.compute(W, H, **julia.PRESETS["dragon"], max_iter=128)
print(renderer.render_smooth(grid, "plasma", "block"))
renderer.print_legend("plasma", "block")

print()

divider("Julia Set — Galaxy — Neon Palette")
grid = julia.compute(W, H, **julia.PRESETS["galaxy"], max_iter=128)
print(renderer.render_smooth(grid, "neon", "dots"))
renderer.print_legend("neon", "dots")

print()

divider("Sierpiński Triangle — Matrix Palette")
grid = sierpinski.triangle(W, H, depth=5)
print(renderer.render_bool(grid, "matrix", "block"))
renderer.print_legend("matrix", "block")

print()

divider("Barnsley Fern — Matrix Palette")
grid = sierpinski.barnsley_fern(W, H, iterations=60000)
print(renderer.render_bool(grid, "matrix", "dots"))
renderer.print_legend("matrix", "dots")

print()
print("  Run `fractalforge --help` for interactive options".center(80))
print()
