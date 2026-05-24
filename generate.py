#!/usr/bin/env python3
"""
Fractal Universe — CLI entry point.

Usage:
    python generate.py                # render full gallery
    python generate.py mandelbrot     # render only Mandelbrot
    python generate.py julia          # render only Julia sets
    python generate.py newton         # render only Newton fractal
    python generate.py burning_ship   # render only Burning Ship
    python generate.py contact        # render contact-sheet summary
"""

import sys
import time
import numpy as np

from fractal_universe.fractals import mandelbrot, julia, newton, burning_ship
from fractal_universe.coloring import histogram_coloring, newton_coloring, PALETTES
from fractal_universe.renderer import save_rgb, render_contact_sheet

GALLERY = "gallery"
W, H = 1200, 900   # output resolution per image


def render_mandelbrot():
    print("Rendering Mandelbrot set…")
    t0 = time.time()
    data = mandelbrot(W, H, x_min=-2.5, x_max=1.0, y_min=-1.25, y_max=1.25, max_iter=512)
    rgb = histogram_coloring(data, palette_name="cosmic", max_iter=512)
    save_rgb(rgb, f"{GALLERY}/mandelbrot.png")
    print(f"  done in {time.time()-t0:.1f}s")

    # Seahorse Valley zoom
    print("Rendering Mandelbrot zoom (Seahorse Valley)…")
    t0 = time.time()
    data = mandelbrot(W, H, x_min=-0.77, x_max=-0.73, y_min=0.08, y_max=0.12, max_iter=1024)
    rgb = histogram_coloring(data, palette_name="ocean", max_iter=1024)
    save_rgb(rgb, f"{GALLERY}/mandelbrot_zoom.png")
    print(f"  done in {time.time()-t0:.1f}s")


def render_julia():
    configs = [
        # (c,                    palette,    filename,            label)
        (-0.7269 + 0.1889j,     "cosmic",   "julia_spiral",      "Spiral"),
        (-0.4 + 0.6j,           "aurora",   "julia_dendrite",    "Dendrite"),
        (0.285 + 0.01j,         "lava",     "julia_lava",        "Lava"),
        (-0.835 - 0.2321j,      "electric", "julia_electric",    "Electric"),
    ]
    for c, palette, fname, label in configs:
        print(f"Rendering Julia set ({label})…")
        t0 = time.time()
        data = julia(W, H, c=c, max_iter=512)
        rgb = histogram_coloring(data, palette_name=palette, max_iter=512)
        save_rgb(rgb, f"{GALLERY}/{fname}.png")
        print(f"  done in {time.time()-t0:.1f}s")


def render_newton():
    print("Rendering Newton fractal…")
    t0 = time.time()
    root_id, iteration = newton(W, H, max_iter=64)
    rgb = newton_coloring(root_id, iteration, max_iter=64)
    save_rgb(rgb, f"{GALLERY}/newton.png")
    print(f"  done in {time.time()-t0:.1f}s")


def render_burning_ship():
    print("Rendering Burning Ship fractal…")
    t0 = time.time()
    data = burning_ship(W, H, max_iter=256)
    rgb = histogram_coloring(data, palette_name="lava", max_iter=256)
    save_rgb(rgb, f"{GALLERY}/burning_ship.png")
    print(f"  done in {time.time()-t0:.1f}s")


def render_contact():
    from PIL import Image
    targets = [
        ("gallery/mandelbrot.png",    "Mandelbrot Set"),
        ("gallery/julia_spiral.png",  "Julia — Spiral"),
        ("gallery/newton.png",        "Newton Fractal"),
        ("gallery/burning_ship.png",  "Burning Ship"),
    ]
    thumb_w, thumb_h = 600, 450
    images = []
    for path, label in targets:
        img = Image.open(path).resize((thumb_w, thumb_h), Image.LANCZOS)
        images.append((np.array(img), label))
    render_contact_sheet(images, "gallery/contact_sheet.png", cols=2)


COMMANDS = {
    "mandelbrot":   render_mandelbrot,
    "julia":        render_julia,
    "newton":       render_newton,
    "burning_ship": render_burning_ship,
    "contact":      render_contact,
}

if __name__ == "__main__":
    requested = sys.argv[1:] or list(COMMANDS.keys())
    for cmd in requested:
        if cmd not in COMMANDS:
            print(f"Unknown command: {cmd}. Available: {', '.join(COMMANDS)}")
            sys.exit(1)
        COMMANDS[cmd]()
    print("\nAll done! Images saved to gallery/")
