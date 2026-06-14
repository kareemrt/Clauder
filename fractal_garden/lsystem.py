"""L-system string rewriting engine.

An L-system rewrites every character of a string in parallel according to a
set of production rules. Repeating this a handful of times turns a tiny
"axiom" like ``"X"`` into a long instruction string that, when fed to a
turtle interpreter, traces out a fractal plant or curve.

Rules may be deterministic (a plain replacement string) or stochastic (a
list of ``(replacement, weight)`` pairs), which is what gives organic
species like :data:`fractal_garden.species.SPECIES`'s ``"bush"`` its
irregular, hand-grown look.
"""

from __future__ import annotations

import random
from typing import Mapping, Sequence, Union

WeightedRule = Sequence[tuple[str, float]]
Rule = Union[str, WeightedRule]
RuleSet = Mapping[str, Rule]


def expand(axiom: str, rules: RuleSet, iterations: int, rng: random.Random | None = None) -> str:
    """Apply ``rules`` to ``axiom`` ``iterations`` times and return the result.

    Characters with no matching rule are copied through unchanged, so
    "drawing" commands (``F``, ``+``, ``-``, ``[``, ``]``, ...) can be mixed
    freely with structural symbols (``X``, ``A``, ``B``, ...).
    """
    if iterations < 0:
        raise ValueError("iterations must be >= 0")

    rng = rng or random.Random()
    current = axiom
    for _ in range(iterations):
        pieces: list[str] = []
        for ch in current:
            rule = rules.get(ch)
            if rule is None:
                pieces.append(ch)
            elif isinstance(rule, str):
                pieces.append(rule)
            else:
                replacements, weights = zip(*rule)
                pieces.append(rng.choices(replacements, weights=weights)[0])
        current = "".join(pieces)
    return current
