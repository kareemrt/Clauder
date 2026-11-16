"""
Consumption and lifestyle emission calculations.

Emission factors sourced from:
- EPA: Waste Reduction Model (WARM)
- Greenpeace / WWF lifecycle analyses
- Carbon Trust product lifecycle assessments
"""

from dataclasses import dataclass
from enum import Enum


class ShoppingHabit(str, Enum):
    MINIMAL = "minimal"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


# kg CO2e per unit
EMISSION_FACTORS = {
    # Clothing (per item)
    "t_shirt": 7.0,
    "jeans": 33.4,
    "jacket": 50.0,
    "shoes": 14.0,
    # Electronics (per device)
    "smartphone": 70.0,
    "laptop": 316.0,
    "tv_55inch": 400.0,
    "tablet": 130.0,
    # Household (per item)
    "sofa": 185.0,
    "mattress": 100.0,
    # Waste management (kg CO2e per tonne of waste)
    "landfill": 467.0,
    "recycled": 21.0,
    "composted": 10.0,
    # Streaming & digital (kg CO2e per hour)
    "streaming_hd": 0.036,
    "gaming_console": 0.1,
    # Services (kg CO2e per dollar spent, rough averages)
    "hotel_night": 15.0,
    "restaurant_meal": 2.5,
}

SHOPPING_ANNUAL_KG_CO2E = {
    ShoppingHabit.MINIMAL: 400,
    ShoppingHabit.MODERATE: 1000,
    ShoppingHabit.HIGH: 2000,
    ShoppingHabit.VERY_HIGH: 4000,
}


@dataclass
class ConsumptionEntry:
    category: str
    item: str
    quantity: float
    kg_co2e: float
    description: str


class ConsumptionCalculator:
    """Calculate CO2e emissions from consumption and lifestyle choices."""

    def purchase(self, item: str, quantity: int = 1) -> ConsumptionEntry:
        """Calculate emissions for purchasing a product."""
        if item not in EMISSION_FACTORS:
            raise ValueError(f"Unknown item: {item}")
        kg = quantity * EMISSION_FACTORS[item]
        return ConsumptionEntry(
            category="purchase",
            item=item,
            quantity=quantity,
            kg_co2e=round(kg, 3),
            description=f"{quantity}× {item}",
        )

    def waste_annual(
        self,
        total_kg: float,
        recycled_fraction: float = 0.30,
        composted_fraction: float = 0.10,
    ) -> ConsumptionEntry:
        """Calculate annual household waste emissions."""
        landfill_fraction = 1.0 - recycled_fraction - composted_fraction
        kg_co2e = (
            total_kg / 1000 * (
                landfill_fraction * EMISSION_FACTORS["landfill"]
                + recycled_fraction * EMISSION_FACTORS["recycled"]
                + composted_fraction * EMISSION_FACTORS["composted"]
            )
        )
        return ConsumptionEntry(
            category="waste",
            item="household_waste",
            quantity=total_kg,
            kg_co2e=round(kg_co2e, 3),
            description=(
                f"{total_kg:.0f} kg waste/year "
                f"({recycled_fraction*100:.0f}% recycled, "
                f"{composted_fraction*100:.0f}% composted)"
            ),
        )

    def streaming(self, hours_per_day: float) -> ConsumptionEntry:
        """Calculate annual emissions from HD video streaming."""
        annual_hours = hours_per_day * 365
        kg = annual_hours * EMISSION_FACTORS["streaming_hd"]
        return ConsumptionEntry(
            category="digital",
            item="streaming",
            quantity=annual_hours,
            kg_co2e=round(kg, 3),
            description=f"{hours_per_day:.1f} hours/day HD streaming",
        )

    def shopping_annual(self, habit: ShoppingHabit) -> float:
        """Get annual kg CO2e for a shopping habit level."""
        return SHOPPING_ANNUAL_KG_CO2E[habit]
