"""A small museum of classic L-systems, ready to grow.

Each preset is an :class:`~lsystem_garden.core.LSystem` carrying its own
axiom, rules, turning angle, and a suggested color palette — so
``lsystem-garden grow fern`` looks right without any extra flags.

References for the grammars below: Prusinkiewicz & Lindenmayer, *The
Algorithmic Beauty of Plants* (1990), and the classic fractal-curve
literature (Koch 1904, Sierpinski 1915, Hilbert 1891, Heighway et al.).
"""

from __future__ import annotations

from typing import Dict

from .core import LSystem

PRESETS: Dict[str, LSystem] = {
    "fractal-plant": LSystem(
        name="fractal-plant",
        description="Classic Lindenmayer branching plant (deterministic).",
        axiom="X",
        rules={
            "X": "F+[[X]-X]-F[-FX]+X",
            "F": "FF",
        },
        angle=25.0,
        seed_color="#8d6e63",
        background="#0b1020",
    ),
    "fern": LSystem(
        name="fern",
        description="Barnsley-style asymmetric fern with stochastic fronds.",
        axiom="X",
        rules={
            "X": [
                (0.85, "F-[[X]+X]+F[+FX]-X"),
                (0.15, "F+[[X]-X]-F[-FX]+X"),
            ],
            "F": "FF",
        },
        angle=22.5,
        seed_color="#33691e",
        background="#0a1a12",
    ),
    "bush": LSystem(
        name="bush",
        description="Dense, stochastic shrub — every render is a little different.",
        axiom="A",
        rules={
            "A": [
                (0.4, "F[+A][-A]FA"),
                (0.3, "F[+A]FA"),
                (0.3, "F[-A]FA"),
            ],
            "F": "FF",
        },
        angle=20.0,
        seed_color="#4e342e",
        background="#10140b",
    ),
    "koch-snowflake": LSystem(
        name="koch-snowflake",
        description="Koch snowflake — a curve of infinite length around a finite area.",
        axiom="F++F++F",
        rules={"F": "F-F++F-F"},
        angle=60.0,
        seed_color="#80deea",
        background="#0b1020",
    ),
    "sierpinski": LSystem(
        name="sierpinski",
        description="Sierpinski triangle drawn as a single space-filling arrowhead curve.",
        axiom="F-G-G",
        rules={"F": "F-G+F+G-F", "G": "GG"},
        angle=120.0,
        seed_color="#ce93d8",
        background="#10081a",
    ),
    "dragon-curve": LSystem(
        name="dragon-curve",
        description="Heighway dragon — folded paper made infinitely thin.",
        axiom="FX",
        rules={"X": "X+YF+", "Y": "-FX-Y"},
        angle=90.0,
        seed_color="#ff8a65",
        background="#0b1020",
    ),
    "hilbert-curve": LSystem(
        name="hilbert-curve",
        description="Hilbert space-filling curve, beloved of locality-preserving indexes.",
        axiom="A",
        rules={
            "A": "-BF+AFA+FB-",
            "B": "+AF-BFB-FA+",
        },
        angle=90.0,
        seed_color="#4fc3f7",
        background="#071019",
    ),
    "levy-curve": LSystem(
        name="levy-curve",
        description="Lévy C curve — a self-similar zigzag with a fractal boundary.",
        axiom="F",
        rules={"F": "+F--F+"},
        angle=45.0,
        seed_color="#fff176",
        background="#0b1020",
    ),
}


def get(name: str) -> LSystem:
    """Look up a preset by name, raising a friendly error if it's unknown."""

    try:
        return PRESETS[name]
    except KeyError as exc:
        available = ", ".join(sorted(PRESETS))
        raise KeyError(f"unknown preset {name!r} — choose from: {available}") from exc


def names() -> list[str]:
    """Return preset names in a stable, display-friendly order."""

    return sorted(PRESETS)
