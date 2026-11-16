"""
Emission trend analysis and comparisons.
"""

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional
import sqlite3

# Global averages in kg CO2e per year (2023 estimates)
GLOBAL_AVERAGES = {
    "world": 4_600,
    "usa": 14_600,
    "eu": 7_300,
    "china": 8_200,
    "india": 1_900,
    "paris_target_2030": 2_500,     # ~2.5 tonnes to stay under 2°C
    "paris_target_1_5c": 1_600,     # ~1.6 tonnes for 1.5°C
}

# US category averages (kg CO2e/year)
US_CATEGORY_AVERAGES = {
    "transport": 4_600,
    "energy": 2_900,
    "food": 2_500,
    "consumption": 2_300,
    "services": 2_300,  # government, healthcare, etc.
}


@dataclass
class FootprintSummary:
    total_kg_co2e: float
    by_category: dict[str, float]
    period_days: int
    annualized_kg_co2e: float

    @property
    def annualized_tonnes(self) -> float:
        return self.annualized_kg_co2e / 1000

    def vs_average(self, region: str = "usa") -> float:
        """Return % difference vs regional average. Negative = better."""
        avg = GLOBAL_AVERAGES.get(region, GLOBAL_AVERAGES["world"])
        return round((self.annualized_kg_co2e - avg) / avg * 100, 1)

    def paris_gap_kg(self) -> float:
        """How many kg above/below the 2°C Paris target."""
        return self.annualized_kg_co2e - GLOBAL_AVERAGES["paris_target_2030"]


def calculate_summary(
    logs: list[sqlite3.Row],
    start: Optional[date] = None,
    end: Optional[date] = None,
) -> FootprintSummary:
    """Build a FootprintSummary from raw log rows."""
    if not logs:
        period_days = (end - start).days + 1 if (start and end) else 30
        return FootprintSummary(
            total_kg_co2e=0.0,
            by_category={},
            period_days=period_days,
            annualized_kg_co2e=0.0,
        )

    total = sum(row["kg_co2e"] for row in logs)
    by_cat: dict[str, float] = {}
    for row in logs:
        by_cat[row["category"]] = by_cat.get(row["category"], 0) + row["kg_co2e"]

    # Determine period
    if start and end:
        period_days = (end - start).days + 1
    else:
        dates = [row["logged_at"][:10] for row in logs]
        if len(dates) > 1:
            d0 = date.fromisoformat(min(dates))
            d1 = date.fromisoformat(max(dates))
            period_days = max((d1 - d0).days + 1, 1)
        else:
            period_days = 1

    annualized = total / period_days * 365

    return FootprintSummary(
        total_kg_co2e=round(total, 2),
        by_category={k: round(v, 2) for k, v in sorted(by_cat.items(), key=lambda x: x[1], reverse=True)},
        period_days=period_days,
        annualized_kg_co2e=round(annualized, 2),
    )


def trend_analysis(monthly_data: list[sqlite3.Row]) -> dict:
    """Analyze month-over-month trends."""
    if len(monthly_data) < 2:
        return {"trend": "insufficient_data", "change_pct": 0.0}

    values = [row["total_kg_co2e"] for row in monthly_data]
    latest = values[-1]
    previous = values[-2]
    all_avg = sum(values) / len(values)

    change_pct = ((latest - previous) / previous * 100) if previous > 0 else 0

    if change_pct < -5:
        trend = "improving"
    elif change_pct > 5:
        trend = "worsening"
    else:
        trend = "stable"

    return {
        "trend": trend,
        "change_pct": round(change_pct, 1),
        "latest_month_kg": round(latest, 2),
        "average_monthly_kg": round(all_avg, 2),
        "best_month": monthly_data[values.index(min(values))]["month"],
        "worst_month": monthly_data[values.index(max(values))]["month"],
    }


def equivalences(kg_co2e: float) -> dict:
    """
    Convert a kg CO2e amount to relatable equivalences.
    Helps people understand scale.
    """
    return {
        "miles_driven": round(kg_co2e / 0.404, 0),
        "trees_year": round(kg_co2e / 21.77, 1),  # avg tree absorbs 21.77 kg/year
        "smartphones_charged": round(kg_co2e / 0.000082, 0),
        "beef_kg": round(kg_co2e / 60.0, 2),
        "flights_nyc_la": round(kg_co2e / 303, 2),  # one-way NYC→LAX ~303 kg CO2e
        "coal_lbs": round(kg_co2e / 0.454, 1),
    }
