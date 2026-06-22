from __future__ import annotations

import argparse
import time

from PIL import Image

from .presets import PRESETS
from .renderer import render


def rows_to_image(rows: dict[int, list[tuple[int, int, int]]], width: int, height: int) -> Image.Image:
    flat: list[tuple[int, int, int]] = []
    for y in range(height):
        flat.extend(rows[y])
    image = Image.new("RGB", (width, height))
    image.putdata(flat)
    return image


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="pytracer", description="A from-scratch CPU ray tracer.")
    parser.add_argument("--scene", choices=sorted(PRESETS), default="showcase")
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--samples", type=int, default=4, help="Antialiasing samples per pixel")
    parser.add_argument("--depth", type=int, default=3, help="Max reflection bounce depth")
    parser.add_argument("--workers", type=int, default=4, help="Parallel worker processes")
    parser.add_argument("--out", default="render.png")
    args = parser.parse_args(argv)

    camera, scene = PRESETS[args.scene](args.width, args.height)
    start = time.time()

    def progress(done: int, total: int) -> None:
        pct = (done + 1) / total * 100
        print(f"\rRendering '{args.scene}': {pct:5.1f}%", end="", flush=True)

    rows = render(
        camera,
        scene,
        samples=args.samples,
        max_depth=args.depth,
        workers=args.workers,
        progress=progress,
    )
    print()
    image = rows_to_image(rows, args.width, args.height)
    image.save(args.out)
    elapsed = time.time() - start
    print(f"Saved {args.out} ({args.width}x{args.height}, {args.samples} spp) in {elapsed:.1f}s")


if __name__ == "__main__":
    main()
