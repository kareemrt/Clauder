"""Presets describing the plants and fractal curves the garden can grow.

Each :class:`Species` bundles an L-system (axiom + production rules) with
the turtle parameters and colours used to render it. New species can be
added simply by adding another entry to :data:`SPECIES`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .lsystem import RuleSet


@dataclass(frozen=True)
class Species:
    """A growable L-system species."""

    key: str
    name: str
    description: str
    axiom: str
    rules: RuleSet
    angle: float
    iterations: int
    step: float = 1.0
    step_falloff: float = 1.0
    angle_jitter: float = 0.0
    start_heading: float = 90.0
    background: str = "#0f1115"


SPECIES: dict[str, Species] = {
    "fern": Species(
        key="fern",
        name="Fractal Fern",
        description="A self-similar fern frond, the textbook Barnsley-style L-system.",
        axiom="X",
        rules={"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"},
        angle=25,
        iterations=4,
        start_heading=90,
        background="#0f1115",
    ),
    "bush": Species(
        key="bush",
        name="Wild Bush",
        description="A stochastic shrub: every branch independently rolls its own shape.",
        axiom="F",
        rules={
            "F": [
                ("F[+F]F[-F]F", 0.34),
                ("F[+F]F", 0.33),
                ("F[-F]F", 0.33),
            ]
        },
        angle=22,
        iterations=5,
        step_falloff=0.82,
        angle_jitter=6,
        start_heading=90,
        background="#0f1115",
    ),
    "sierpinski": Species(
        key="sierpinski",
        name="Sierpinski Arrowhead",
        description="The Sierpinski triangle, traced as a single continuous arrowhead curve.",
        axiom="F-G-G",
        rules={"F": "F-G+F+G-F", "G": "GG"},
        angle=120,
        iterations=4,
        start_heading=0,
        background="#0f1115",
    ),
    "koch": Species(
        key="koch",
        name="Koch Snowflake",
        description="Three Koch curves joined into the classic infinitely-jagged snowflake.",
        axiom="F--F--F",
        rules={"F": "F+F--F+F"},
        angle=60,
        iterations=4,
        start_heading=0,
        background="#0f1115",
    ),
    "dragon": Species(
        key="dragon",
        name="Dragon Curve",
        description="The Heighway dragon: fold a strip of paper in half enough times.",
        axiom="FX",
        rules={"X": "X+YF+", "Y": "-FX-Y"},
        angle=90,
        iterations=10,
        start_heading=0,
        background="#0f1115",
    ),
    "hilbert": Species(
        key="hilbert",
        name="Hilbert Curve",
        description="A space-filling curve that visits every cell of a grid exactly once.",
        axiom="A",
        rules={"A": "-BF+AFA+FB-", "B": "+AF-BFB-FA+"},
        angle=90,
        iterations=5,
        start_heading=0,
        background="#0f1115",
    ),
}


def get(key: str) -> Species:
    """Look up a species by key, raising a friendly error if unknown."""
    try:
        return SPECIES[key]
    except KeyError as exc:
        choices = ", ".join(sorted(SPECIES))
        raise ValueError(f"unknown species {key!r}; choose from: {choices}") from exc
