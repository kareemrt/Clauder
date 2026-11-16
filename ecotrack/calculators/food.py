"""
Food emission calculations.

Emission factors sourced from:
- Poore & Nemecek (2018), Science: "Reducing food's environmental impacts
  through producers and consumers" - the most comprehensive lifecycle analysis
- Our World in Data: Food and Climate
- FAO: Livestock's Long Shadow
"""

from dataclasses import dataclass
from enum import Enum


class DietType(str, Enum):
    MEAT_HEAVY = "meat_heavy"
    AVERAGE = "average"
    LOW_MEAT = "low_meat"
    PESCATARIAN = "pescatarian"
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"


# kg CO2e per kg of food (lifecycle, cradle-to-plate)
EMISSION_FACTORS = {
    # Meat & Seafood
    "beef": 60.0,
    "lamb": 24.0,
    "pork": 7.6,
    "chicken": 6.9,
    "eggs": 4.5,
    "fish_farmed": 5.4,
    "fish_wild": 3.0,
    "shrimp": 12.0,
    # Dairy
    "milk": 3.2,
    "cheese": 10.0,
    "butter": 11.5,
    "yogurt": 2.2,
    # Plant proteins
    "tofu": 2.0,
    "legumes": 0.9,
    "nuts": 2.5,
    # Grains & Carbs
    "wheat_bread": 1.4,
    "rice": 4.0,
    "oats": 1.6,
    "pasta": 1.8,
    # Vegetables & Fruit
    "vegetables": 2.0,
    "root_vegetables": 0.4,
    "fruit": 0.9,
    "citrus": 0.4,
}

# Annual kg CO2e by diet type (average person, US)
DIET_ANNUAL_KG_CO2E = {
    DietType.MEAT_HEAVY: 3300,
    DietType.AVERAGE: 2500,
    DietType.LOW_MEAT: 1900,
    DietType.PESCATARIAN: 1500,
    DietType.VEGETARIAN: 1200,
    DietType.VEGAN: 900,
}

DIET_DESCRIPTIONS = {
    DietType.MEAT_HEAVY: "Meat at most meals (>100g meat/day)",
    DietType.AVERAGE: "Meat ~4x per week (average American)",
    DietType.LOW_MEAT: "Meat ~2x per week",
    DietType.PESCATARIAN: "No meat, but fish",
    DietType.VEGETARIAN: "No meat or fish",
    DietType.VEGAN: "No animal products",
}


@dataclass
class FoodEntry:
    food_item: str
    amount_kg: float
    kg_co2e: float
    description: str


class FoodCalculator:
    """Calculate CO2e emissions from food consumption."""

    def food_item(self, item: str, amount_kg: float) -> FoodEntry:
        """Calculate emissions for a specific food item."""
        if item not in EMISSION_FACTORS:
            raise ValueError(
                f"Unknown food item: {item}. Available: {', '.join(EMISSION_FACTORS.keys())}"
            )
        kg = amount_kg * EMISSION_FACTORS[item]
        return FoodEntry(
            food_item=item,
            amount_kg=amount_kg,
            kg_co2e=round(kg, 3),
            description=f"{amount_kg:.2f} kg of {item}",
        )

    def diet_annual(self, diet_type: DietType) -> float:
        """Get annual kg CO2e for a diet type."""
        return DIET_ANNUAL_KG_CO2E[diet_type]

    def diet_monthly(self, diet_type: DietType) -> float:
        """Get monthly kg CO2e for a diet type."""
        return round(DIET_ANNUAL_KG_CO2E[diet_type] / 12, 1)

    def diet_comparison(self) -> dict:
        """Return comparison of all diet types."""
        return {
            dt.value: {
                "annual_kg_co2e": DIET_ANNUAL_KG_CO2E[dt],
                "description": DIET_DESCRIPTIONS[dt],
                "vs_average_pct": round(
                    (DIET_ANNUAL_KG_CO2E[dt] - DIET_ANNUAL_KG_CO2E[DietType.AVERAGE])
                    / DIET_ANNUAL_KG_CO2E[DietType.AVERAGE]
                    * 100,
                    1,
                ),
            }
            for dt in DietType
        }

    def food_waste_impact(self, waste_fraction: float = 0.30) -> float:
        """
        Extra emissions from wasted food.
        waste_fraction: fraction of food purchased that is wasted (0-1)
        Returns: multiplier for total food emissions
        """
        return 1.0 / (1.0 - waste_fraction)

    @staticmethod
    def list_foods() -> list[tuple[str, float]]:
        """Return all food items with their emission factors."""
        return sorted(EMISSION_FACTORS.items(), key=lambda x: x[1], reverse=True)
