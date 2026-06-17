"""Regenerate the sample images embedded in README.md.

Run with: python3 scripts/generate_gallery.py
"""

from pathlib import Path

from PIL import Image

from fracta.chaos_game import render_chaos_game
from fracta.escape_fractals import render_julia, render_mandelbrot
from fracta.lsystem import render_lsystem

OUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "gallery"


def save(array_or_image, name: str) -> None:
    img = array_or_image if isinstance(array_or_image, Image.Image) else Image.fromarray(array_or_image)
    path = OUT_DIR / name
    img.save(path)
    print(f"wrote {path}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    save(
        render_mandelbrot(width=900, height=700, max_iter=400, palette="ocean"),
        "mandelbrot_ocean.png",
    )
    save(
        render_mandelbrot(
            width=700,
            height=700,
            center=(-0.7453, 0.1127),
            scale=0.01,
            max_iter=600,
            palette="ultraviolet",
        ),
        "mandelbrot_zoom.png",
    )
    save(
        render_julia(width=700, height=700, max_iter=400, palette="fire"),
        "julia_fire.png",
    )
    save(render_lsystem(preset="tree", width=800, height=800), "lsystem_tree.png")
    save(render_lsystem(preset="dragon", width=800, height=800), "lsystem_dragon.png")
    save(
        render_chaos_game(preset="barnsley_fern", width=700, height=900, n_points=400_000, palette="forest"),
        "chaos_fern.png",
    )
    save(
        render_chaos_game(preset="sierpinski_triangle", width=800, height=800, n_points=300_000, palette="mono"),
        "chaos_sierpinski.png",
    )


if __name__ == "__main__":
    main()
