"""Biome presets for Terrarium."""

import random
from terrarium.world import World
from terrarium.entities import Plant, Herbivore, Carnivore, WATER, ROCK


def _scatter_rocks(world: World, density: float = 0.04):
    """Randomly scatter rock cells across the world."""
    for y in range(world.height):
        for x in range(world.width):
            if world.type_grid[y][x] == 0 and random.random() < density:
                world.type_grid[y][x] = ROCK  # rocks have no entity object


def _place_n(world: World, EntityCls, count: int, etype: int):
    """Randomly place exactly `count` entities of `EntityCls` on empty cells."""
    placed = 0
    attempts = 0
    while placed < count and attempts < count * 100:
        y = random.randint(0, world.height - 1)
        x = random.randint(0, world.width - 1)
        if world.type_grid[y][x] == 0:
            world.place(y, x, EntityCls(), etype)
            placed += 1
        attempts += 1


def create_forest(width: int = 70, height: int = 28) -> World:
    """Dense forest biome: abundant plants, many herbivores, few carnivores."""
    world = World(width, height)
    for y in range(height):
        for x in range(width):
            if random.random() < 0.40:
                world.place(y, x, Plant(), 1)
    _scatter_rocks(world, density=0.02)
    _place_n(world, Herbivore, 25, 2)
    _place_n(world, Carnivore,  4, 3)
    return world


def create_savanna(width: int = 70, height: int = 28) -> World:
    """Open savanna: sparse plants, many herbivores, a few carnivores."""
    world = World(width, height)
    for y in range(height):
        for x in range(width):
            if random.random() < 0.18:
                world.place(y, x, Plant(), 1)
    _scatter_rocks(world, density=0.05)
    _place_n(world, Herbivore, 22, 2)
    _place_n(world, Carnivore,  3, 3)
    return world


def create_sparse(width: int = 70, height: int = 28) -> World:
    """Sparse world: minimal start — watch the ecosystem bootstrap itself."""
    world = World(width, height)

    # Dense central plant patch — the seed of life
    cy, cx = height // 2, width // 2
    for y in range(cy - 8, cy + 9):
        for x in range(cx - 15, cx + 15):
            if world.in_bounds(y, x) and random.random() < 0.65:
                world.place(y, x, Plant(), 1)

    _place_n(world, Herbivore, 5, 2)    # just 5 to let plants stabilize first
    _place_n(world, Carnivore, 2, 3)
    return world


def create_archipelago(width: int = 70, height: int = 28) -> World:
    """Islands of life separated by water channels."""
    world = World(width, height)

    # Carve water channels
    for y in range(height):
        for x in range(width):
            if (x % 18 < 2) or (y % 10 < 1):
                world.type_grid[y][x] = WATER

    # Fill land tiles
    for y in range(height):
        for x in range(width):
            if world.type_grid[y][x] != WATER:
                r = random.random()
                if r < 0.35:
                    world.place(y, x, Plant(), 1)
                elif r < 0.43:
                    world.place(y, x, Herbivore(), 2)
                elif r < 0.44:
                    world.place(y, x, Carnivore(), 3)

    return world


BIOMES: dict = {
    "forest":      create_forest,
    "savanna":     create_savanna,
    "sparse":      create_sparse,
    "archipelago": create_archipelago,
}
