import pytest

from lsystemgarden.lsystem import LSystem


def test_zero_iterations_returns_axiom():
    system = LSystem(axiom="F", rules={"F": "F+F"}, angle=90)
    assert system.expand(0) == "F"


def test_deterministic_single_rule_expansion():
    system = LSystem(axiom="F", rules={"F": "F+F-F"}, angle=90)
    assert system.expand(1) == "F+F-F"
    assert system.expand(2) == "F+F-F+F+F-F-F+F-F"


def test_koch_curve_growth_length():
    # Each F becomes 4 symbols containing F (F+F--F+F), so symbol count
    # of F's quadruples every generation.
    system = LSystem(axiom="F", rules={"F": "F+F--F+F"}, angle=60)
    assert system.expand(1).count("F") == 4
    assert system.expand(2).count("F") == 16
    assert system.expand(3).count("F") == 64


def test_symbols_without_rules_pass_through_unchanged():
    system = LSystem(axiom="A+B", rules={"A": "AA"}, angle=90)
    assert system.expand(1) == "AA+B"


def test_negative_iterations_raises():
    system = LSystem(axiom="F", rules={}, angle=90)
    with pytest.raises(ValueError):
        system.expand(-1)


def test_stochastic_rule_only_picks_listed_replacements():
    system = LSystem(
        axiom="F",
        rules={"F": [(0.5, "FF"), (0.5, "F+F")]},
        angle=90,
        seed=0,
    )
    result = system.expand(1)
    assert result in {"FF", "F+F"}


def test_stochastic_rule_is_reproducible_with_seed():
    rules = {"F": [(0.5, "FF"), (0.5, "F+F")]}
    a = LSystem(axiom="F", rules=rules, angle=90, seed=42).expand(5)
    b = LSystem(axiom="F", rules=rules, angle=90, seed=42).expand(5)
    assert a == b


def test_stochastic_rule_varies_without_a_fixed_seed_relationship():
    # Different seeds should be capable of producing different expansions.
    rules = {"F": [(0.5, "FF"), (0.5, "F+F")]}
    outcomes = {
        LSystem(axiom="F", rules=rules, angle=90, seed=s).expand(6)
        for s in range(10)
    }
    assert len(outcomes) > 1
