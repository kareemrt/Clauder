"""A small gallery of classic L-system fractals."""

from __future__ import annotations

from .lsystem import LSystem

PRESETS: dict[str, LSystem] = {
    "koch-snowflake": LSystem(
        name="Koch Snowflake",
        description="The classic von Koch snowflake curve.",
        axiom="F++F++F",
        rules={"F": "F-F++F-F"},
        angle=60,
        draw_chars="F",
        start_heading=0,
        default_iterations=4,
    ),
    "sierpinski-arrowhead": LSystem(
        name="Sierpinski Arrowhead",
        description="Sierpinski triangle traced as a single continuous curve.",
        axiom="A",
        rules={"A": "B-A-B", "B": "A+B+A"},
        angle=60,
        draw_chars="AB",
        start_heading=0,
        default_iterations=6,
    ),
    "dragon-curve": LSystem(
        name="Heighway Dragon Curve",
        description="The famous paper-folding dragon curve.",
        axiom="FX",
        rules={"X": "X+YF+", "Y": "-FX-Y"},
        angle=90,
        draw_chars="F",
        start_heading=0,
        default_iterations=11,
    ),
    "fractal-plant": LSystem(
        name="Fractal Plant",
        description="Lindenmayer's original branching plant model.",
        axiom="X",
        rules={"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"},
        angle=25,
        draw_chars="F",
        start_heading=90,
        default_iterations=5,
    ),
    "fractal-tree": LSystem(
        name="Binary Fractal Tree",
        description="A symmetric binary branching tree.",
        axiom="F",
        rules={"F": "F[+F][-F]"},
        angle=27,
        draw_chars="F",
        start_heading=90,
        default_iterations=8,
    ),
    "hilbert-curve": LSystem(
        name="Hilbert Curve",
        description="A space-filling curve that visits every cell of a grid.",
        axiom="A",
        rules={"A": "-BF+AFA+FB-", "B": "+AF-BFB-FA+"},
        angle=90,
        draw_chars="F",
        start_heading=0,
        default_iterations=5,
    ),
    "levy-c-curve": LSystem(
        name="Levy C Curve",
        description="A self-similar fractal curve resembling jagged coastline.",
        axiom="F",
        rules={"F": "+F--F+"},
        angle=45,
        draw_chars="F",
        start_heading=0,
        default_iterations=14,
    ),
}


def get_preset(key: str) -> LSystem:
    try:
        return PRESETS[key]
    except KeyError as exc:
        available = ", ".join(sorted(PRESETS))
        raise KeyError(f"Unknown preset {key!r}. Available presets: {available}") from exc
