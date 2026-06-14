#!/usr/bin/env python3
"""Regenerate the sample SVGs in gallery/ used by the README.

Run from the repository root:

    python3 scripts/generate_gallery.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from fractal_garden import garden, palette, species, svgrender  # noqa: E402

GALLERY = ROOT / "gallery"

# (species key, palette name, seed) — chosen for a pleasant default gallery.
SAMPLES = [
    ("fern", "spring", 1),
    ("bush", "autumn", 7),
    ("sierpinski", "ocean", 0),
    ("koch", "fire", 0),
    ("dragon", "twilight", 0),
    ("hilbert", "mono", 0),
]

GARDEN_SEED = 20240614


def main() -> None:
    GALLERY.mkdir(exist_ok=True)

    for key, palette_name, seed in SAMPLES:
        segments = garden.grow(key, seed=seed)
        svg = svgrender.render_svg(
            segments,
            palette=palette.resolve(palette_name),
            background=species.get(key).background,
        )
        out = GALLERY / f"{key}.svg"
        out.write_text(svg)
        print(f"wrote {out} ({len(svg):,} bytes, {len(segments):,} segments)")

    import random

    rng = random.Random(GARDEN_SEED)
    palette_names = list(palette.PALETTES)
    plants = []
    for key in species.SPECIES:
        seed = rng.randrange(2**32)
        pal_name = palette_names[rng.randrange(len(palette_names))]
        plants.append(svgrender.GardenPlant(garden.grow(key, seed=seed), palette.resolve(pal_name)))

    garden_svg = svgrender.render_garden(plants)
    out = GALLERY / "garden.svg"
    out.write_text(garden_svg)
    print(f"wrote {out} ({len(garden_svg):,} bytes)")


if __name__ == "__main__":
    main()
