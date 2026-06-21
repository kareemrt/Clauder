"""Genome: the heritable traits that drive natural selection in the simulation."""

from __future__ import annotations

import random
from dataclasses import dataclass

# Valid ranges for each trait. Mutation always clamps back into these bounds
# so genomes can't drift into nonsensical territory (e.g. negative speed).
SPEED_RANGE = (1, 3)
VISION_RANGE = (1, 8)
METABOLISM_RANGE = (0.4, 1.6)
REPRO_THRESHOLD_RANGE = (8.0, 30.0)

MUTATION_RATE = 0.15
MUTATION_STRENGTH = 0.2


@dataclass(frozen=True)
class Genome:
    """A small set of traits with built-in tradeoffs.

    Higher speed and vision help an organism find food faster, but both
    raise its metabolic cost per tick -- so evolution has to balance
    perception and mobility against energy efficiency.
    """

    speed: int
    vision: int
    metabolism: float
    repro_threshold: float

    @classmethod
    def random(cls, rng: random.Random) -> "Genome":
        return cls(
            speed=rng.randint(*SPEED_RANGE),
            vision=rng.randint(*VISION_RANGE),
            metabolism=rng.uniform(*METABOLISM_RANGE),
            repro_threshold=rng.uniform(*REPRO_THRESHOLD_RANGE),
        )

    def mutate(self, rng: random.Random) -> "Genome":
        """Return a child genome: each trait independently has a chance to drift."""

        def jitter_int(value: int, bounds: tuple[int, int]) -> int:
            if rng.random() < MUTATION_RATE:
                value += rng.choice((-1, 1))
            return max(bounds[0], min(bounds[1], value))

        def jitter_float(value: float, bounds: tuple[float, float]) -> float:
            if rng.random() < MUTATION_RATE:
                span = bounds[1] - bounds[0]
                value += rng.gauss(0, MUTATION_STRENGTH * span)
            return max(bounds[0], min(bounds[1], value))

        return Genome(
            speed=jitter_int(self.speed, SPEED_RANGE),
            vision=jitter_int(self.vision, VISION_RANGE),
            metabolism=jitter_float(self.metabolism, METABOLISM_RANGE),
            repro_threshold=jitter_float(self.repro_threshold, REPRO_THRESHOLD_RANGE),
        )

    def upkeep_cost(self) -> float:
        """Energy spent per tick just for having this body plan."""
        return self.metabolism * (1.0 + 0.35 * self.speed + 0.15 * self.vision)
