import pytest

from lsystems.core import LSystem


def test_zero_iterations_returns_axiom():
    system = LSystem(axiom="F", rules={"F": "F+F"})
    assert system.expand(0) == "F"


def test_single_iteration_applies_rule_once():
    system = LSystem(axiom="F", rules={"F": "F+F"})
    assert system.expand(1) == "F+F"


def test_multiple_iterations_compound():
    system = LSystem(axiom="F", rules={"F": "F+F"})
    assert system.expand(2) == "F+F+F+F"


def test_symbols_without_rules_are_left_unchanged():
    system = LSystem(axiom="A+B", rules={"A": "AB"})
    assert system.expand(1) == "AB+B"


def test_negative_iterations_raises():
    system = LSystem(axiom="F", rules={})
    with pytest.raises(ValueError):
        system.expand(-1)
