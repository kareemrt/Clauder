#!/usr/bin/env python3
"""
ASCII Ray Tracer — entry point.

Usage:
  python main.py                     # one-shot render (classic scene, 80×38)
  python main.py --scene solar       # solar system
  python main.py --scene disco       # disco floor
  python main.py --animate           # looping animation
  python main.py --width 120 --height 50 --depth 6
  python main.py --export render.png # save PNG (requires Pillow)
"""

import argparse
import math
import sys
import time

from raytracer import Renderer
from raytracer.display import AsciiDisplay
from scenes import build_classic_scene, build_solar_scene, build_disco_scene

_BUILDERS = {
    "classic": build_classic_scene,
    "solar": build_solar_scene,
    "disco": build_disco_scene,
}


def parse_args():
    p = argparse.ArgumentParser(
        description="ASCII Ray Tracer — 3D rendering in your terminal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--scene", choices=list(_BUILDERS), default="classic",
                   help="Which scene to render (default: classic)")
    p.add_argument("--width",  type=int, default=80,
                   help="Output width in characters (default: 80)")
    p.add_argument("--height", type=int, default=38,
                   help="Output height in lines (default: 38)")
    p.add_argument("--depth",  type=int, default=4,
                   help="Max reflection depth (default: 4)")
    p.add_argument("--animate", action="store_true",
                   help="Run a continuous animation loop")
    p.add_argument("--frames",  type=int, default=60,
                   help="Number of animation frames (default: 60)")
    p.add_argument("--fps",     type=float, default=8.0,
                   help="Target frame rate (default: 8)")
    p.add_argument("--no-color", action="store_true",
                   help="Disable ANSI colour output")
    p.add_argument("--export", metavar="FILE",
                   help="Export a single frame to PNG (requires Pillow)")
    p.add_argument("--t", type=float, default=0.0,
                   help="Animation parameter for single frame (default: 0)")
    return p.parse_args()


def render_frame(builder, t, width, height, depth):
    scene, camera = builder(t, width, height)
    renderer = Renderer(max_depth=depth)
    return renderer.render(scene, camera, width, height)


def export_png(pixels, path: str):
    try:
        from PIL import Image
    except ImportError:
        print("Pillow is not installed. Run:  pip install Pillow", file=sys.stderr)
        sys.exit(1)

    height = len(pixels)
    width = len(pixels[0])
    img = Image.new("RGB", (width * 2, height))  # doubled for aspect ratio
    px_data = []
    for row in pixels:
        for pixel in row:
            from raytracer.display import _gamma_correct, GAMMA
            g = _gamma_correct(pixel)
            r = int(g.x * 255)
            g_val = int(g.y * 255)
            b = int(g.z * 255)
            px_data.append((r, g_val, b))
            px_data.append((r, g_val, b))  # double horizontally
    img.putdata(px_data)
    img.save(path)
    print(f"Saved {path} ({width * 2}×{height})")


def main():
    args = parse_args()
    builder = _BUILDERS[args.scene]
    display = AsciiDisplay(color=not args.no_color)

    if args.export:
        pixels = render_frame(builder, args.t, args.width, args.height, args.depth)
        export_png(pixels, args.export)
        return

    if not args.animate:
        pixels = render_frame(builder, args.t, args.width, args.height, args.depth)
        display.print_frame(pixels)
        return

    # ── animation loop ─────────────────────────────────────────────────────
    frame_time = 1.0 / args.fps
    first = True
    loop_count = 0

    try:
        while True:
            for i in range(args.frames):
                t0 = time.monotonic()
                t_param = (i / args.frames) * 2 * math.pi
                pixels = render_frame(builder, t_param, args.width, args.height, args.depth)
                display.print_frame(pixels, clear=not first)
                first = False
                elapsed = time.monotonic() - t0
                sleep = frame_time - elapsed
                if sleep > 0:
                    time.sleep(sleep)
            loop_count += 1
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()
