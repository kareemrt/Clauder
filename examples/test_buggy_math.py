"""Tests for buggy_math — use `clauder heal` to fix them automatically."""

import pytest
from examples.buggy_math import add, subtract, multiply, divide, factorial


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_subtract():
    assert subtract(10, 3) == 7
    assert subtract(0, 5) == -5


def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(0, 99) == 0


def test_divide():
    assert divide(10, 2) == 5.0
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


def test_factorial():
    assert factorial(0) == 1
    assert factorial(5) == 120
