"""Command-line interface for Lumina."""
import argparse
import sys
import time
from pathlib import Path

from .composer import generate_scene
from .nebula import PALETTES
from .planets import PLANET_THEMES


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="lumina",
        description="Lumina — Generative Cosmic Art Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  lumina                                  # random 1920×1080 scene
  lumina --seed 7 --output cosmos.png     # reproducible scene
  lumina --width 3840 --height 2160 --seed 42   # 4K render
  lumina --nebula rosette --planet lava_world    # specific style
  lumina --batch 5 --output-dir ./gallery        # generate 5 scenes
        """,
    )
    parser.add_argument("--seed", type=int, default=None,
                        help="Random seed (default: random)")
    parser.add_argument("--width", type=int, default=1920,
                        help="Output width in pixels (default: 1920)")
    parser.add_argument("--height", type=int, default=1080,
                        help="Output height in pixels (default: 1080)")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Output file path (default: lumina_<seed>.png)")
    parser.add_argument("--nebula", choices=list(PALETTES.keys()), default=None,
                        help="Nebula color palette")
    parser.add_argument("--planet", choices=list(PLANET_THEMES.keys()), default=None,
                        help="Planet surface theme")
    parser.add_argument("--stars", type=int, default=2200,
                        help="Number of stars (default: 2200)")
    parser.add_argument("--planets", type=int, default=2,
                        choices=range(0, 4),
                        help="Number of planets 0-3 (default: 2)")
    parser.add_argument("--batch", type=int, default=1,
                        help="Generate N scenes with sequential seeds")
    parser.add_argument("--output-dir", type=str, default=".",
                        help="Directory for batch output (default: .)")
    parser.add_argument("--no-preview", action="store_true",
                        help="Suppress preview opening")

    args = parser.parse_args(argv)

    import numpy as np
    base_seed = args.seed if args.seed is not None else int(time.time()) % 100000

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for i in range(args.batch):
        seed = base_seed + i
        out_path = (
            Path(args.output) if (args.output and args.batch == 1)
            else output_dir / f"lumina_{seed}.png"
        )

        print(f"  Rendering scene  [seed={seed}  {args.width}×{args.height}]")
        t0 = time.time()
        img = generate_scene(
            width=args.width,
            height=args.height,
            seed=seed,
            nebula_palette=args.nebula,
            planet_theme=args.planet,
            star_count=args.stars,
            n_planets=args.planets,
        )
        elapsed = time.time() - t0
        img.save(out_path, format="PNG", optimize=False)
        print(f"  Saved → {out_path}  ({elapsed:.1f}s)")

    print("\nDone.")


if __name__ == "__main__":
    main()
