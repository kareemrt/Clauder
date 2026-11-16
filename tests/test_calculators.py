"""Tests for emission calculators."""

import pytest
from ecotrack.calculators import (
    TransportCalculator,
    EnergyCalculator,
    FoodCalculator,
    ConsumptionCalculator,
)
from ecotrack.calculators.food import DietType
from ecotrack.calculators.consumption import ShoppingHabit


class TestTransportCalculator:
    def test_car_gasoline(self):
        calc = TransportCalculator()
        entry = calc.car_trip(100, "gasoline")
        assert entry.kg_co2e == pytest.approx(40.4, rel=0.01)
        assert entry.mode == "car (gasoline)"

    def test_car_electric_lower_than_gas(self):
        calc = TransportCalculator()
        ev = calc.car_trip(100, "electric")
        gas = calc.car_trip(100, "gasoline")
        assert ev.kg_co2e < gas.kg_co2e

    def test_car_carpooling_reduces_emissions(self):
        calc = TransportCalculator()
        solo = calc.car_trip(50, "gasoline", passengers=1)
        shared = calc.car_trip(50, "gasoline", passengers=4)
        assert shared.kg_co2e == pytest.approx(solo.kg_co2e / 4, rel=0.01)

    def test_public_transit_lower_than_car(self):
        calc = TransportCalculator()
        car = calc.car_trip(20, "gasoline")
        bus = calc.public_transit(20, "bus")
        assert bus.kg_co2e < car.kg_co2e

    def test_flight_short_haul(self):
        calc = TransportCalculator()
        entry = calc.flight(300)  # short haul
        assert entry.kg_co2e > 0
        assert "short-haul" in entry.description

    def test_flight_long_haul(self):
        calc = TransportCalculator()
        short = calc.flight(400)
        long = calc.flight(5000)
        # Long haul emits more in absolute terms
        assert long.kg_co2e > short.kg_co2e

    def test_invalid_fuel_type(self):
        with pytest.raises(ValueError, match="Unknown fuel type"):
            TransportCalculator().car_trip(100, "jet_fuel")

    def test_cycling_zero_emissions(self):
        from ecotrack.calculators.transport import EMISSION_FACTORS
        assert EMISSION_FACTORS["cycling"] == 0.0


class TestEnergyCalculator:
    def test_electricity_us_avg(self):
        calc = EnergyCalculator()
        entry = calc.electricity(886)  # US monthly average
        assert entry.kg_co2e == pytest.approx(342.0, rel=0.05)

    def test_renewable_lower_than_coal(self):
        calc = EnergyCalculator()
        coal = calc.electricity(1000, "coal_heavy")
        renewable = calc.electricity(1000, "renewable")
        assert renewable.kg_co2e < coal.kg_co2e

    def test_natural_gas(self):
        calc = EnergyCalculator()
        entry = calc.natural_gas(50)  # 50 therms
        assert entry.kg_co2e == pytest.approx(265.1, rel=0.01)

    def test_heating_oil(self):
        calc = EnergyCalculator()
        entry = calc.heating_oil(100)
        assert entry.kg_co2e > 0

    def test_monthly_home_multiple(self):
        calc = EnergyCalculator()
        entries = calc.monthly_home(electricity_kwh=500, natural_gas_therms=20)
        assert len(entries) == 2
        assert sum(e.kg_co2e for e in entries) > 0


class TestFoodCalculator:
    def test_beef_high_emissions(self):
        calc = FoodCalculator()
        beef = calc.food_item("beef", 1.0)
        chicken = calc.food_item("chicken", 1.0)
        assert beef.kg_co2e > chicken.kg_co2e

    def test_vegetables_low_emissions(self):
        calc = FoodCalculator()
        veg = calc.food_item("vegetables", 1.0)
        beef = calc.food_item("beef", 1.0)
        assert veg.kg_co2e < beef.kg_co2e

    def test_diet_vegan_less_than_average(self):
        calc = FoodCalculator()
        vegan = calc.diet_annual(DietType.VEGAN)
        avg = calc.diet_annual(DietType.AVERAGE)
        assert vegan < avg

    def test_diet_meat_heavy_more_than_average(self):
        calc = FoodCalculator()
        heavy = calc.diet_annual(DietType.MEAT_HEAVY)
        avg = calc.diet_annual(DietType.AVERAGE)
        assert heavy > avg

    def test_food_waste_multiplier(self):
        calc = FoodCalculator()
        multiplier = calc.food_waste_impact(0.30)
        assert multiplier > 1.0

    def test_invalid_food_raises(self):
        with pytest.raises(ValueError):
            FoodCalculator().food_item("unicorn_steak", 1.0)

    def test_list_foods_sorted(self):
        items = FoodCalculator.list_foods()
        factors = [f for _, f in items]
        assert factors == sorted(factors, reverse=True)


class TestConsumptionCalculator:
    def test_laptop_has_emissions(self):
        calc = ConsumptionCalculator()
        entry = calc.purchase("laptop")
        assert entry.kg_co2e > 0

    def test_multiple_items(self):
        calc = ConsumptionCalculator()
        one = calc.purchase("smartphone", 1)
        two = calc.purchase("smartphone", 2)
        assert two.kg_co2e == pytest.approx(one.kg_co2e * 2, rel=0.01)

    def test_recycling_reduces_emissions(self):
        calc = ConsumptionCalculator()
        no_recycle = calc.waste_annual(1000, recycled_fraction=0.0, composted_fraction=0.0)
        with_recycle = calc.waste_annual(1000, recycled_fraction=0.5, composted_fraction=0.1)
        assert with_recycle.kg_co2e < no_recycle.kg_co2e

    def test_invalid_item_raises(self):
        with pytest.raises(ValueError):
            ConsumptionCalculator().purchase("gold_bar")
