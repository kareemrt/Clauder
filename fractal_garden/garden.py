"""High-level helpers that grow a :mod:`~fractal_garden.species` into geometry."""

from __future__ import annotations

import random

from . import lsystem, turtle
from .species import Species, get
from .turtle import Segment


def grow(
    species: str | Species,
    *,
    iterations: int | None = None,
    seed: int | None = None,
    angle_jitter: float | None = None,
) -> list[Segment]:
    """Expand a species' L-system and walk a turtle through the result.

    :param species: a species key (e.g. ``"fern"``) or a :class:`Species`.
    :param iterations: override the species' default iteration count.
    :param seed: seed for the random number generator driving stochastic
        rules and angle jitter. ``None`` means non-deterministic.
    :param angle_jitter: override the species' default angle jitter (degrees).
    """
    sp = species if isinstance(species, Species) else get(species)
    rng = random.Random(seed)

    iters = sp.iterations if iterations is None else iterations
    jitter = sp.angle_jitter if angle_jitter is None else angle_jitter

    commands = lsystem.expand(sp.axiom, sp.rules, iters, rng)
    config = turtle.TurtleConfig(
        angle=sp.angle,
        step=sp.step,
        step_falloff=sp.step_falloff,
        angle_jitter=jitter,
        start_heading=sp.start_heading,
    )
    return turtle.run(commands, config, rng)
