"""Carbon footprint and financial impact calculations."""

import json
from pathlib import Path
from typing import Tuple

_DATA_PATH = Path(__file__).parent.parent / "data" / "emission_factors.json"


def _load_factors() -> dict:
    with open(_DATA_PATH) as f:
        return json.load(f)


def get_emission_factor(category: str) -> float:
    """Return kg CO2e per kg of food for the given category."""
    factors = _load_factors()
    cat = category.lower()
    return factors["food_categories"].get(cat, factors["food_categories"]["other"])["kg_co2_per_kg"]


def estimate_weight_kg(quantity: float, unit: str) -> float:
    """Convert quantity + unit to kg for emission calculations."""
    unit = unit.lower()
    conversions = {
        "kg": 1.0,
        "g": 0.001,
        "lb": 0.453592,
        "oz": 0.0283495,
        "l": 1.0,
        "ml": 0.001,
        "cup": 0.24,
        "tbsp": 0.015,
        "tsp": 0.005,
        "unit": 0.15,
        "item": 0.15,
        "slice": 0.03,
        "can": 0.4,
        "bag": 0.5,
        "bunch": 0.3,
        "loaf": 0.5,
        "bottle": 0.75,
        "pack": 0.5,
        "box": 0.3,
    }
    return quantity * conversions.get(unit, 0.15)


def calculate_co2_impact(quantity: float, unit: str, category: str) -> float:
    """Return kg CO2e emitted if this food is wasted."""
    weight_kg = estimate_weight_kg(quantity, unit)
    factor = get_emission_factor(category)
    return round(weight_kg * factor, 4)


def estimate_usd_value(quantity: float, unit: str, category: str) -> float:
    """Rough USD value estimate based on average prices."""
    price_per_kg = {
        "beef": 10.0, "lamb": 12.0, "pork": 7.0, "chicken": 5.5,
        "fish": 9.0, "dairy": 2.5, "eggs": 5.0, "vegetables": 3.0,
        "fruits": 3.5, "grains": 2.0, "legumes": 2.5, "bread": 4.0,
        "cheese": 11.0, "butter": 8.0, "tofu": 4.5, "nuts": 15.0,
        "other": 4.0,
    }
    weight_kg = estimate_weight_kg(quantity, unit)
    price = price_per_kg.get(category.lower(), 4.0)
    return round(weight_kg * price, 2)


def co2_to_human_equivalent(kg_co2: float) -> str:
    """Convert kg CO2 to relatable equivalents."""
    driving_km = kg_co2 / 0.21
    smartphone_charges = kg_co2 / 0.008
    if driving_km >= 1:
        return f"{driving_km:.1f} km driven by car"
    return f"{smartphone_charges:.0f} smartphone charges"
