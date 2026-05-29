#!/usr/bin/env python3
"""Generate plain-text example maps used in the README."""

import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from worldforge.world import World
from worldforge.renderer import render_plain

os.makedirs("examples", exist_ok=True)

configs = [
    ("world_42.txt",       42,   65, 12, 8),
    ("world_1337.txt",     1337, 65, 14, 10),
    ("world_ocean.txt",    7,    65, 8,  5),
    ("world_small.txt",    99,   33, 6,  4),
]

for fname, seed, size, rivers, cities in configs:
    print(f"\n{'='*50}")
    world = World(size, seed=seed, num_rivers=rivers, num_cities=cities)
    path = os.path.join("examples", fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(render_plain(world))
    print(f"  → saved {path}")
    stats = world.stats()
    for biome, pct in list(stats.items())[:6]:
        print(f"    {biome:<22} {pct}%")

print("\nDone.")
