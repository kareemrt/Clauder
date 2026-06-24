"""Lindenmayer-system grammar expansion.

An L-system rewrites every symbol in a string ("axiom") according to a set
of production rules, repeated for a number of generations. Rules can be
deterministic (one replacement) or stochastic (a weighted choice of
replacements), which is what gives organic-looking growth its variety.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

Replacement = str | list[tuple[float, str]]


@dataclass(frozen=True)
class LSystem:
    axiom: str
    rules: dict[str, Replacement]
    angle: float
    seed: int | None = None

    def expand(self, iterations: int) -> str:
        """Apply the production rules `iterations` times, starting from the axiom."""
        if iterations < 0:
            raise ValueError("iterations must be >= 0")
        rng = random.Random(self.seed)
        state = self.axiom
        for _ in range(iterations):
            state = "".join(self._rewrite(symbol, rng) for symbol in state)
        return state

    def _rewrite(self, symbol: str, rng: random.Random) -> str:
        rule = self.rules.get(symbol)
        if rule is None:
            return symbol
        if isinstance(rule, str):
            return rule
        weights = [weight for weight, _ in rule]
        choices = [replacement for _, replacement in rule]
        return rng.choices(choices, weights=weights, k=1)[0]
