"""A small gallery of named L-system presets, ready to render."""

from __future__ import annotations

from dataclasses import dataclass

from .lsystem import Replacement
from .turtle import DEFAULT_DRAW_CHARS


@dataclass(frozen=True)
class Preset:
    axiom: str
    rules: dict[str, Replacement]
    angle: float
    iterations: int
    step: float = 5.0
    start_heading: float = 90.0
    draw_chars: frozenset[str] = DEFAULT_DRAW_CHARS
    start_color: str = "#7ee787"
    end_color: str = "#58a6ff"
    seed: int | None = None
    description: str = ""


PRESETS: dict[str, Preset] = {
    "koch_snowflake": Preset(
        axiom="F++F++F",
        rules={"F": "F-F++F-F"},
        angle=60,
        iterations=4,
        step=6,
        start_color="#ffd166",
        end_color="#ef476f",
        description="The classic Koch snowflake, grown from an equilateral triangle.",
    ),
    "sierpinski_triangle": Preset(
        axiom="F-G-G",
        rules={"F": "F-G+F+G-F", "G": "GG"},
        angle=120,
        iterations=6,
        step=6,
        draw_chars=frozenset({"F", "G"}),
        start_color="#06d6a0",
        end_color="#118ab2",
        description="Sierpinski's triangle, traced as a single Lindenmayer curve.",
    ),
    "dragon_curve": Preset(
        axiom="FX",
        rules={"X": "X+YF+", "Y": "-FX-Y"},
        angle=90,
        iterations=11,
        step=6,
        draw_chars=frozenset({"F"}),
        start_color="#9b5de5",
        end_color="#f15bb5",
        description="The Heighway dragon curve, folded eleven generations deep.",
    ),
    "binary_tree": Preset(
        axiom="F",
        rules={"F": "F[+F]F[-F]F"},
        angle=25,
        iterations=4,
        step=10,
        start_color="#caf0f8",
        end_color="#03045e",
        description="A symmetric branching tree, three new shoots per generation.",
    ),
    "fractal_plant": Preset(
        axiom="X",
        rules={
            "X": "F-[[X]+X]+F[+FX]-X",
            "F": "FF",
        },
        angle=25,
        iterations=6,
        step=3,
        draw_chars=frozenset({"F"}),
        start_color="#80ed99",
        end_color="#1b4332",
        description="Prusinkiewicz's fern-like plant, from The Algorithmic Beauty of Plants.",
    ),
    "wild_bush": Preset(
        axiom="F",
        rules={
            "F": [
                (0.35, "F[+F]F[-F]F"),
                (0.35, "F[+F]F"),
                (0.30, "F[-F]F"),
            ]
        },
        angle=22,
        iterations=4,
        step=10,
        seed=7,
        start_color="#ffadad",
        end_color="#6a040f",
        description="A stochastic shrub: every branch independently rolls its own shape.",
    ),
}
