"""Organism: a single living agent placed on the world grid."""

from __future__ import annotations

from itertools import count

from genesis.genome import Genome

INITIAL_ENERGY = 14.0
FOOD_ENERGY = 9.0
MAX_AGE = 400


class Organism:
    _ids = count()

    def __init__(self, genome: Genome, x: int, y: int, energy: float = INITIAL_ENERGY):
        self.id = next(Organism._ids)
        self.genome = genome
        self.x = x
        self.y = y
        self.energy = energy
        self.age = 0

    @property
    def alive(self) -> bool:
        return self.energy > 0 and self.age <= MAX_AGE

    def can_reproduce(self) -> bool:
        return self.energy >= self.genome.repro_threshold
