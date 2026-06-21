"""Simulation: ties the world, organisms and genetics together tick by tick."""

from __future__ import annotations

import random
from dataclasses import dataclass

from genesis.genome import Genome
from genesis.organism import FOOD_ENERGY, Organism
from genesis.world import World

DEFAULT_FOOD_DENSITY = 0.12


@dataclass
class Stats:
    tick: int
    population: int
    food_count: int
    avg_speed: float
    avg_vision: float
    avg_metabolism: float
    avg_repro_threshold: float
    avg_energy: float


def _avg(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


class Simulation:
    def __init__(
        self,
        width: int = 60,
        height: int = 30,
        population: int = 80,
        food_density: float = DEFAULT_FOOD_DENSITY,
        seed: int | None = None,
    ):
        self.width = width
        self.height = height
        self.food_density = food_density
        self.rng = random.Random(seed)
        self.world = World(width, height, self.rng)
        self.tick_count = 0
        self._seed_population(population)

    def _seed_population(self, population: int) -> None:
        for _ in range(population):
            x = self.rng.randrange(self.width)
            y = self.rng.randrange(self.height)
            if (x, y) in self.world.occupied:
                continue
            genome = Genome.random(self.rng)
            self.world.place(Organism(genome, x, y))

    def tick(self) -> Stats:
        self.tick_count += 1
        world = self.world
        world.spawn_food(self.food_density)

        living = world.organisms()
        self.rng.shuffle(living)

        for org in living:
            if (org.x, org.y) not in world.occupied:
                continue  # already removed earlier this tick (eaten its own cell, etc.)

            genome = org.genome
            target = world.nearest_food(org.x, org.y, genome.vision)
            if target is not None:
                new_pos = world.step_toward(org.x, org.y, target, genome.speed)
            else:
                new_pos = world.random_step(org.x, org.y, genome.speed)
            world.move(org, new_pos)

            org.energy -= genome.upkeep_cost()
            if world.take_food((org.x, org.y)):
                org.energy += FOOD_ENERGY
            org.age += 1

            if not org.alive:
                world.remove(org)
                continue

            if org.can_reproduce():
                spot = world.free_neighbor(org.x, org.y)
                if spot is not None:
                    share = org.energy / 2
                    org.energy -= share
                    child = Organism(genome.mutate(self.rng), spot[0], spot[1], energy=share)
                    world.place(child)

        return self._snapshot_stats()

    def _snapshot_stats(self) -> Stats:
        orgs = self.world.organisms()
        return Stats(
            tick=self.tick_count,
            population=len(orgs),
            food_count=len(self.world.food),
            avg_speed=_avg([o.genome.speed for o in orgs]),
            avg_vision=_avg([o.genome.vision for o in orgs]),
            avg_metabolism=_avg([o.genome.metabolism for o in orgs]),
            avg_repro_threshold=_avg([o.genome.repro_threshold for o in orgs]),
            avg_energy=_avg([o.energy for o in orgs]),
        )

    def run(self, ticks: int, record_every: int = 1) -> list[Stats]:
        history = []
        for _ in range(ticks):
            stats = self.tick()
            if stats.tick % record_every == 0:
                history.append(stats)
            if stats.population == 0:
                break
        return history
