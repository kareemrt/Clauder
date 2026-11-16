"""Tests for impact calculation module."""

import pytest
from foodsave.impact import (
    estimate_weight_kg,
    calculate_co2_impact,
    estimate_usd_value,
    co2_to_human_equivalent,
)


def test_estimate_weight_kg_basic():
    assert estimate_weight_kg(1.0, "kg") == 1.0
    assert estimate_weight_kg(1000.0, "g") == pytest.approx(1.0)
    assert estimate_weight_kg(1.0, "lb") == pytest.approx(0.453592, rel=1e-3)


def test_estimate_weight_unknown_unit():
    # Unknown units fall back to 0.15 kg per unit
    assert estimate_weight_kg(2.0, "unknown") == pytest.approx(0.30, rel=1e-3)


def test_calculate_co2_impact_beef():
    # 1 kg beef at 27 kg CO2e/kg
    co2 = calculate_co2_impact(1.0, "kg", "beef")
    assert co2 == pytest.approx(27.0, rel=1e-2)


def test_calculate_co2_impact_vegetables():
    # 500g vegetables
    co2 = calculate_co2_impact(500.0, "g", "vegetables")
    assert co2 == pytest.approx(1.0, rel=1e-2)


def test_estimate_usd_value_positive():
    usd = estimate_usd_value(1.0, "kg", "chicken")
    assert usd > 0


def test_co2_equivalent_driving():
    # 10 kg CO2 ≈ 47.6 km
    result = co2_to_human_equivalent(10.0)
    assert "km" in result or "charge" in result


def test_zero_co2_equivalent():
    result = co2_to_human_equivalent(0.001)
    assert isinstance(result, str)
