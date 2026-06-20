"""Core L-system string-rewriting engine."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class LSystem:
    """A Lindenmayer system: an axiom rewritten by per-symbol production rules.

    Each iteration replaces every symbol in the current string with its rule
    output (symbols with no rule are left unchanged), so the string length
    typically grows exponentially with the number of iterations.
    """

    axiom: str
    rules: dict[str, str] = field(default_factory=dict)

    def expand(self, iterations: int) -> str:
        if iterations < 0:
            raise ValueError("iterations must be >= 0")
        state = self.axiom
        for _ in range(iterations):
            state = "".join(self.rules.get(symbol, symbol) for symbol in state)
        return state
