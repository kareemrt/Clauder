"""
Transport emission calculations.

Emission factors sourced from:
- EPA: https://www.epa.gov/greenvehicles/greenhouse-gas-emissions-typical-passenger-vehicle
- ICAO Carbon Emissions Calculator methodology
- UK BEIS Greenhouse Gas Reporting Factors 2023
"""

from dataclasses import dataclass
from typing import Optional


# kg CO2e per unit
EMISSION_FACTORS = {
    # Cars (kg CO2e per mile)
    "car_gasoline": 0.404,
    "car_diesel": 0.374,
    "car_hybrid": 0.202,
    "car_electric": 0.096,  # US average grid
    # Public transit (kg CO2e per mile per passenger)
    "bus": 0.089,
    "subway": 0.041,
    "rail_commuter": 0.100,
    "rail_intercity": 0.065,
    # Flights (kg CO2e per passenger mile, includes radiative forcing)
    "flight_short": 0.255,   # < 500 miles
    "flight_medium": 0.195,  # 500–2000 miles
    "flight_long": 0.150,    # > 2000 miles
    # Motorcycle (kg CO2e per mile)
    "motorcycle": 0.221,
    # Cycling/walking
    "cycling": 0.0,
    "walking": 0.0,
}

FLIGHT_MULTIPLIER = 2.7  # Radiative forcing multiplier for high-altitude emissions


@dataclass
class TransportEntry:
    mode: str
    distance_miles: float
    kg_co2e: float
    description: str


class TransportCalculator:
    """Calculate CO2e emissions from transportation activities."""

    def car_trip(
        self,
        miles: float,
        fuel_type: str = "gasoline",
        passengers: int = 1,
    ) -> TransportEntry:
        """Calculate emissions for a car trip."""
        key = f"car_{fuel_type}"
        if key not in EMISSION_FACTORS:
            raise ValueError(f"Unknown fuel type: {fuel_type}. Choose from: gasoline, diesel, hybrid, electric")
        factor = EMISSION_FACTORS[key]
        kg = (miles * factor) / max(passengers, 1)
        return TransportEntry(
            mode=f"car ({fuel_type})",
            distance_miles=miles,
            kg_co2e=round(kg, 3),
            description=f"{miles:.1f} miles by {fuel_type} car with {passengers} passenger(s)",
        )

    def public_transit(self, miles: float, mode: str = "bus") -> TransportEntry:
        """Calculate emissions for public transit."""
        if mode not in ("bus", "subway", "rail_commuter", "rail_intercity"):
            raise ValueError(f"Unknown transit mode: {mode}")
        kg = miles * EMISSION_FACTORS[mode]
        return TransportEntry(
            mode=mode,
            distance_miles=miles,
            kg_co2e=round(kg, 3),
            description=f"{miles:.1f} miles by {mode}",
        )

    def flight(self, miles: float) -> TransportEntry:
        """Calculate emissions for a flight (one way)."""
        if miles < 500:
            factor = EMISSION_FACTORS["flight_short"]
            category = "short-haul"
        elif miles < 2000:
            factor = EMISSION_FACTORS["flight_medium"]
            category = "medium-haul"
        else:
            factor = EMISSION_FACTORS["flight_long"]
            category = "long-haul"
        kg = miles * factor
        return TransportEntry(
            mode="flight",
            distance_miles=miles,
            kg_co2e=round(kg, 3),
            description=f"{miles:.0f}-mile {category} flight",
        )

    def commute_annual(
        self,
        daily_miles: float,
        work_days: int = 250,
        mode: str = "car_gasoline",
        passengers: int = 1,
    ) -> TransportEntry:
        """Calculate annual commute emissions."""
        total_miles = daily_miles * work_days * 2  # round trip
        if mode.startswith("car"):
            fuel_type = mode.replace("car_", "") if "_" in mode else "gasoline"
            entry = self.car_trip(total_miles, fuel_type, passengers)
        else:
            entry = self.public_transit(total_miles, mode)
        entry.description = f"Annual commute: {daily_miles:.1f} mi/day × {work_days} days"
        return entry
