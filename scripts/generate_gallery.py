"""Regenerate every image in gallery/ used by the README.

Run with: python3 -m scripts.generate_gallery
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fractalis.burning_ship import render_burning_ship
from fractalis.julia import render_julia
from fractalis.lsystem import PRESETS as LSYSTEM_PRESETS
from fractalis.lsystem import render_lsystem
from fractalis.mandelbrot import SEAHORSE_VALLEY, render_mandelbrot
from fractalis.png_writer import write_png

GALLERY_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gallery")

SIZE = 480


def _write(name, pixels, size=SIZE):
    path = os.path.join(GALLERY_DIR, name)
    write_png(path, size, size, pixels)
    print(f"wrote {path} ({os.path.getsize(path) // 1024} KB)")


def main():
    os.makedirs(GALLERY_DIR, exist_ok=True)

    _write("mandelbrot_full.png",
           render_mandelbrot(SIZE, SIZE, max_iter=300, cmap="inferno"))
    _write("mandelbrot_seahorse.png",
           render_mandelbrot(SIZE, SIZE, bounds=SEAHORSE_VALLEY, max_iter=500, cmap="fire"))
    _write("julia_classic.png",
           render_julia(SIZE, SIZE, c="classic", max_iter=300, cmap="ocean"))
    _write("julia_spiral.png",
           render_julia(SIZE, SIZE, c="spiral", max_iter=300, cmap="psychedelic"))
    _write("burning_ship.png",
           render_burning_ship(SIZE, SIZE, max_iter=300, cmap="fire"))

    for name in LSYSTEM_PRESETS:
        _write(f"{name}.png", render_lsystem(name, SIZE, SIZE, stroke=2))


if __name__ == "__main__":
    main()
