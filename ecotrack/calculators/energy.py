"""
Home energy emission calculations.

Emission factors sourced from:
- EPA eGRID 2022 (electricity)
- EPA: https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator
- EIA: https://www.eia.gov/environment/emissions/co2_vol_mass.php
"""

from dataclasses import dataclass


# kg CO2e per unit
EMISSION_FACTORS = {
    # Electricity (kg CO2e per kWh) - US average and regional
    "electricity_us_avg": 0.386,
    "electricity_coal_heavy": 0.700,
    "electricity_mixed": 0.450,
    "electricity_renewable": 0.020,
    # Natural gas (kg CO2e per therm)
    "natural_gas": 5.302,
    # Heating oil (kg CO2e per gallon)
    "heating_oil": 10.16,
    # Propane (kg CO2e per gallon)
    "propane": 5.74,
    # Wood (kg CO2e per cord) - net near-zero but has emissions
    "wood": 1507.0,
}

US_AVERAGE_ELECTRICITY_KWH_PER_MONTH = 886  # EIA 2022


@dataclass
class EnergyEntry:
    source: str
    amount: float
    unit: str
    kg_co2e: float
    description: str


class EnergyCalculator:
    """Calculate CO2e emissions from home energy use."""

    def electricity(
        self,
        kwh: float,
        grid_type: str = "us_avg",
    ) -> EnergyEntry:
        """
        Calculate emissions from electricity consumption.

        grid_type: us_avg, coal_heavy, mixed, renewable
        """
        key = f"electricity_{grid_type}"
        if key not in EMISSION_FACTORS:
            raise ValueError(f"Unknown grid type: {grid_type}")
        kg = kwh * EMISSION_FACTORS[key]
        return EnergyEntry(
            source="electricity",
            amount=kwh,
            unit="kWh",
            kg_co2e=round(kg, 3),
            description=f"{kwh:.1f} kWh electricity ({grid_type} grid)",
        )

    def natural_gas(self, therms: float) -> EnergyEntry:
        """Calculate emissions from natural gas consumption."""
        kg = therms * EMISSION_FACTORS["natural_gas"]
        return EnergyEntry(
            source="natural_gas",
            amount=therms,
            unit="therms",
            kg_co2e=round(kg, 3),
            description=f"{therms:.1f} therms of natural gas",
        )

    def heating_oil(self, gallons: float) -> EnergyEntry:
        """Calculate emissions from heating oil consumption."""
        kg = gallons * EMISSION_FACTORS["heating_oil"]
        return EnergyEntry(
            source="heating_oil",
            amount=gallons,
            unit="gallons",
            kg_co2e=round(kg, 3),
            description=f"{gallons:.1f} gallons of heating oil",
        )

    def propane(self, gallons: float) -> EnergyEntry:
        """Calculate emissions from propane consumption."""
        kg = gallons * EMISSION_FACTORS["propane"]
        return EnergyEntry(
            source="propane",
            amount=gallons,
            unit="gallons",
            kg_co2e=round(kg, 3),
            description=f"{gallons:.1f} gallons of propane",
        )

    def monthly_home(
        self,
        electricity_kwh: float = 886,
        natural_gas_therms: float = 0,
        heating_oil_gallons: float = 0,
        grid_type: str = "us_avg",
    ) -> list[EnergyEntry]:
        """Calculate all home energy emissions for a month."""
        entries = []
        if electricity_kwh > 0:
            entries.append(self.electricity(electricity_kwh, grid_type))
        if natural_gas_therms > 0:
            entries.append(self.natural_gas(natural_gas_therms))
        if heating_oil_gallons > 0:
            entries.append(self.heating_oil(heating_oil_gallons))
        return entries
