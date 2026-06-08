"""The rewriting engine at the heart of every L-system.

A Lindenmayer system (L-system) grows a string by repeatedly replacing
symbols according to production rules. Starting from a short "axiom" like
``F`` and a rule like ``F -> F+F-F``, a handful of generations produce
strings long enough to draw entire fractal forests when interpreted by a
turtle (see :mod:`lsystem_garden.turtle`).

Stochastic rules are supported: a symbol may map to a list of
``(weight, replacement)`` pairs, in which case one is chosen at random
each time the symbol is rewritten. This is what gives plant-like presets
their organic, non-repeating silhouettes.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List, Sequence, Tuple, Union

# A rule either rewrites a symbol to a fixed string, or to one of several
# alternatives chosen by weighted random choice.
Replacement = Union[str, Sequence[Tuple[float, str]]]


@dataclass(frozen=True)
class LSystem:
    """An immutable description of an L-system grammar.

    Attributes:
        axiom: The initial string the system starts from.
        rules: Mapping of a single-character symbol to its replacement.
            A replacement is either a literal string, or a sequence of
            ``(weight, string)`` pairs for stochastic rewriting.
        angle: The default turn angle (in degrees) used when this system
            is interpreted by a turtle.
        name: A human-readable label, used in CLI listings and filenames.
        description: A short explanation of what the system represents.
    """

    axiom: str
    rules: Dict[str, Replacement]
    angle: float
    name: str = "lsystem"
    description: str = ""
    seed_color: str = "#2e7d32"
    background: str = "#0b1020"

    def expand(self, iterations: int, *, rng: random.Random | None = None) -> str:
        """Return the string produced after ``iterations`` rewrite passes."""

        return expand(self.axiom, self.rules, iterations, rng=rng)


def _choose(replacement: Replacement, rng: random.Random) -> str:
    if isinstance(replacement, str):
        return replacement

    weights = [w for w, _ in replacement]
    options = [s for _, s in replacement]
    return rng.choices(options, weights=weights, k=1)[0]


def expand(
    axiom: str,
    rules: Dict[str, Replacement],
    iterations: int,
    *,
    rng: random.Random | None = None,
) -> str:
    """Rewrite ``axiom`` ``iterations`` times according to ``rules``.

    Symbols absent from ``rules`` are left untouched (they are typically
    turtle commands like ``+``, ``-``, ``[`` and ``]`` that carry meaning
    during rendering but never expand themselves).
    """

    if iterations < 0:
        raise ValueError("iterations must be non-negative")

    rng = rng or random.Random()
    current = axiom
    for _ in range(iterations):
        pieces: List[str] = []
        for symbol in current:
            replacement = rules.get(symbol)
            if replacement is None:
                pieces.append(symbol)
            else:
                pieces.append(_choose(replacement, rng))
        current = "".join(pieces)
    return current


@dataclass
class GrowthStats:
    """Bookkeeping about a generated string, handy for CLI summaries."""

    iterations: int
    length: int
    draw_commands: int = field(default=0)


def stats_for(s: str, iterations: int, draw_symbols: str = "FGAB") -> GrowthStats:
    """Summarize a generated L-system string."""

    return GrowthStats(
        iterations=iterations,
        length=len(s),
        draw_commands=sum(1 for ch in s if ch in draw_symbols),
    )
