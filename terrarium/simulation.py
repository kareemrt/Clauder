"""Simulation step logic for Terrarium."""

import random
from .world import World
from .entities import Plant, Herbivore, Carnivore, EMPTY, PLANT, HERBIVORE, CARNIVORE


def step(world: World) -> dict:
    """Advance the world by one tick. Returns event counts."""
    stats = {
        "plants_born": 0, "plants_died": 0,
        "herbivores_born": 0, "herbivores_died": 0,
        "carnivores_born": 0, "carnivores_died": 0,
    }

    # Snapshot entity positions at tick start so each entity acts once
    snapshot = []
    for y in range(world.height):
        for x in range(world.width):
            t = world.type_grid[y][x]
            if t in (PLANT, HERBIVORE, CARNIVORE):
                snapshot.append((y, x, t, world.grid[y][x]))

    random.shuffle(snapshot)

    for orig_y, orig_x, etype, entity in snapshot:
        # Skip if entity was consumed or already moved this tick
        if world.grid[orig_y][orig_x] is not entity:
            continue

        entity.age += 1

        if etype == PLANT:
            _tick_plant(world, orig_y, orig_x, entity, stats)
        elif etype == HERBIVORE:
            _tick_herbivore(world, orig_y, orig_x, entity, stats)
        elif etype == CARNIVORE:
            _tick_carnivore(world, orig_y, orig_x, entity, stats)

    return stats


# ---------------------------------------------------------------------------
# Plant logic
# ---------------------------------------------------------------------------

def _tick_plant(world: World, y: int, x: int, plant: Plant, stats: dict):
    # Age / random death
    if plant.age > Plant.MAX_AGE or random.random() < Plant.DEATH_CHANCE:
        world.remove(y, x)
        stats["plants_died"] += 1
        return

    # Spread to a random empty neighbor
    if random.random() < Plant.SPREAD_CHANCE:
        empty = world.empty_neighbors(y, x)
        if empty:
            ny, nx = random.choice(empty)
            new_plant = Plant()
            world.place(ny, nx, new_plant, PLANT)
            stats["plants_born"] += 1


# ---------------------------------------------------------------------------
# Herbivore logic
# ---------------------------------------------------------------------------

def _tick_herbivore(world: World, y: int, x: int, herb: Herbivore, stats: dict):
    herb.energy -= Herbivore.IDLE_COST

    if herb.energy <= 0 or herb.age > Herbivore.MAX_AGE:
        world.remove(y, x)
        stats["herbivores_died"] += 1
        return

    # Reproduce before moving if energy is high
    if herb.energy >= Herbivore.REPRODUCE_THRESHOLD:
        empty = world.empty_neighbors(y, x)
        if empty:
            ny, nx = random.choice(empty)
            baby = Herbivore(energy=Herbivore.REPRODUCE_COST / 2)
            world.place(ny, nx, baby, HERBIVORE)
            herb.energy -= Herbivore.REPRODUCE_COST
            stats["herbivores_born"] += 1
            return  # used the action for reproduction

    # Prefer moving onto an adjacent plant cell (eats it)
    plants = world.plant_neighbors(y, x)
    if plants:
        ny, nx = random.choice(plants)
        # Plant might have been consumed already this tick
        if world.type_grid[ny][nx] == PLANT:
            world.remove(ny, nx)
            stats["plants_died"] += 1
            herb.energy = min(herb.energy + Herbivore.EAT_GAIN, Herbivore.MAX_ENERGY)
            world.move(y, x, ny, nx)
            return

    # Navigate toward nearest plant, otherwise wander
    target = world.find_nearest(y, x, PLANT, max_range=Herbivore.VISION)
    if target:
        step = world.step_toward(y, x, *target)
        if step:
            ny, nx = step
            if world.type_grid[ny][nx] == PLANT:
                world.remove(ny, nx)
                stats["plants_died"] += 1
                herb.energy = min(herb.energy + Herbivore.EAT_GAIN / 2, Herbivore.MAX_ENERGY)
            herb.energy -= Herbivore.MOVE_COST
            world.move(y, x, ny, nx)
            return

    empty = world.empty_neighbors(y, x)
    if empty:
        ny, nx = random.choice(empty)
        herb.energy -= Herbivore.MOVE_COST
        world.move(y, x, ny, nx)


# ---------------------------------------------------------------------------
# Carnivore logic
# ---------------------------------------------------------------------------

def _tick_carnivore(world: World, y: int, x: int, carn: Carnivore, stats: dict):
    carn.energy -= Carnivore.IDLE_COST

    if carn.energy <= 0 or carn.age > Carnivore.MAX_AGE:
        world.remove(y, x)
        stats["carnivores_died"] += 1
        return

    # Reproduce if energy is high
    if carn.energy >= Carnivore.REPRODUCE_THRESHOLD:
        empty = world.empty_neighbors(y, x)
        if empty:
            ny, nx = random.choice(empty)
            baby = Carnivore(energy=Carnivore.REPRODUCE_COST / 2)
            world.place(ny, nx, baby, CARNIVORE)
            carn.energy -= Carnivore.REPRODUCE_COST
            stats["carnivores_born"] += 1
            return

    # Eat adjacent herbivore if possible
    herbs_adj = world.herbivore_neighbors(y, x)
    if herbs_adj:
        ny, nx = random.choice(herbs_adj)
        if world.type_grid[ny][nx] == HERBIVORE:
            world.remove(ny, nx)
            stats["herbivores_died"] += 1
            carn.energy = min(carn.energy + Carnivore.EAT_GAIN, Carnivore.MAX_ENERGY)
            world.move(y, x, ny, nx)
            return

    # Hunt: navigate toward nearest herbivore
    target = world.find_nearest(y, x, HERBIVORE, max_range=Carnivore.HUNT_RANGE)
    if target:
        step = world.step_toward(y, x, *target)
        if step:
            ny, nx = step
            if world.type_grid[ny][nx] == HERBIVORE:
                world.remove(ny, nx)
                stats["herbivores_died"] += 1
                carn.energy = min(carn.energy + Carnivore.EAT_GAIN, Carnivore.MAX_ENERGY)
            carn.energy -= Carnivore.MOVE_COST
            world.move(y, x, ny, nx)
            return

    # Wander
    empty = world.empty_neighbors(y, x)
    if empty:
        ny, nx = random.choice(empty)
        carn.energy -= Carnivore.MOVE_COST
        world.move(y, x, ny, nx)
