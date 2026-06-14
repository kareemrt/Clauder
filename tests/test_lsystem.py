import random

import pytest

from fractal_garden import lsystem


def test_zero_iterations_returns_axiom():
    assert lsystem.expand("F-G-G", {"F": "F-G+F+G-F", "G": "GG"}, 0) == "F-G-G"


def test_deterministic_expansion_koch():
    rules = {"F": "F+F--F+F"}
    assert lsystem.expand("F", rules, 1) == "F+F--F+F"
    assert lsystem.expand("F", rules, 2) == "F+F--F+F" + "+" + "F+F--F+F" + "--" + "F+F--F+F" + "+" + "F+F--F+F"


def test_unmatched_symbols_pass_through():
    assert lsystem.expand("XYZ", {}, 3) == "XYZ"


def test_negative_iterations_rejected():
    with pytest.raises(ValueError):
        lsystem.expand("F", {}, -1)


def test_stochastic_rule_is_seed_reproducible():
    rules = {"F": [("FF", 0.5), ("F+F", 0.5)]}
    a = lsystem.expand("F", rules, 4, random.Random(123))
    b = lsystem.expand("F", rules, 4, random.Random(123))
    assert a == b


def test_stochastic_rule_only_uses_listed_replacements():
    rules = {"F": [("FF", 0.5), ("F+F", 0.5)]}
    result = lsystem.expand("F", rules, 1, random.Random(0))
    assert result in {"FF", "F+F"}
