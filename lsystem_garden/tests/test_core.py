import random

import pytest

from lsystem_garden.core import LSystem, expand, stats_for


def test_expand_deterministic_koch():
    result = expand("F", {"F": "F+F-F"}, iterations=2)
    # Pass 1: F+F-F
    # Pass 2: each F -> F+F-F
    assert result == "F+F-F+F+F-F-F+F-F"


def test_expand_zero_iterations_returns_axiom():
    assert expand("FX", {"F": "FF", "X": "F-X"}, iterations=0) == "FX"


def test_expand_rejects_negative_iterations():
    with pytest.raises(ValueError):
        expand("F", {"F": "FF"}, iterations=-1)


def test_expand_leaves_unknown_symbols_untouched():
    result = expand("F+F", {"F": "FF"}, iterations=1)
    assert result == "FF+FF"


def test_stochastic_expansion_is_reproducible_with_seed():
    rules = {"X": [(0.5, "F"), (0.5, "G")]}
    a = expand("XXXXXXXXXX", rules, iterations=1, rng=random.Random(42))
    b = expand("XXXXXXXXXX", rules, iterations=1, rng=random.Random(42))
    assert a == b
    assert set(a) <= {"F", "G"}


def test_stochastic_expansion_can_diverge_with_different_seeds():
    rules = {"X": [(0.5, "F"), (0.5, "G")]}
    outcomes = {
        expand("X" * 40, rules, iterations=1, rng=random.Random(seed)) for seed in range(10)
    }
    assert len(outcomes) > 1


def test_lsystem_expand_matches_module_level_function():
    system = LSystem(axiom="F", rules={"F": "F+F"}, angle=60.0)
    assert system.expand(2, rng=random.Random(0)) == expand("F", {"F": "F+F"}, 2, rng=random.Random(0))


def test_stats_for_counts_draw_commands():
    stats = stats_for("F+F-[FX]F", iterations=3)
    assert stats.iterations == 3
    assert stats.length == 9
    assert stats.draw_commands == 4  # F, F, F, F (X is not a draw symbol)
