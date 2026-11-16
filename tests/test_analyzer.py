"""Tests for the analyzer module."""

import pytest
from unittest.mock import MagicMock
from datetime import date

from ecotrack.analyzer import (
    calculate_summary,
    trend_analysis,
    equivalences,
    GLOBAL_AVERAGES,
    FootprintSummary,
)


def _make_row(category: str, kg_co2e: float, logged_at: str = "2024-01-15") -> dict:
    return {"category": category, "kg_co2e": kg_co2e, "logged_at": logged_at}


class TestCalculateSummary:
    def test_empty_logs(self):
        s = calculate_summary([])
        assert s.total_kg_co2e == 0.0
        assert s.annualized_kg_co2e == 0.0

    def test_single_entry(self):
        rows = [_make_row("transport", 50.0)]
        s = calculate_summary(rows)
        assert s.total_kg_co2e == 50.0
        assert "transport" in s.by_category

    def test_multiple_categories(self):
        rows = [
            _make_row("transport", 100.0),
            _make_row("energy", 200.0),
            _make_row("food", 150.0),
        ]
        s = calculate_summary(rows)
        assert s.total_kg_co2e == 450.0
        assert len(s.by_category) == 3

    def test_annualization(self):
        # 365 kg over 365 days → 1 kg/day → 365 kg/year
        start = date(2024, 1, 1)
        end = date(2024, 12, 30)  # 364 days
        rows = [
            _make_row("transport", 100.0, "2024-01-01"),
            _make_row("transport", 100.0, "2024-12-30"),
        ]
        s = calculate_summary(rows, start=start, end=end)
        # 200 kg over 364 days → ~200.5 kg/year
        assert s.annualized_kg_co2e == pytest.approx(200 / 364 * 365, rel=0.01)

    def test_vs_average_positive_means_above(self):
        rows = [_make_row("transport", 14600)]  # exactly US average
        s = calculate_summary(rows, start=date(2024, 1, 1), end=date(2024, 12, 31))
        assert s.vs_average("usa") == pytest.approx(0.0, abs=5.0)

    def test_paris_gap(self):
        rows = [_make_row("transport", 5000)]
        s = calculate_summary(rows, start=date(2024, 1, 1), end=date(2024, 12, 31))
        gap = s.paris_gap_kg()
        assert gap == pytest.approx(5000 - GLOBAL_AVERAGES["paris_target_2030"], rel=0.01)


class TestTrendAnalysis:
    def _make_monthly(self, values: list[float]) -> list:
        months = ["2024-01", "2024-02", "2024-03", "2024-04", "2024-05"]
        return [
            {"month": months[i], "total_kg_co2e": v, "entry_count": 5}
            for i, v in enumerate(values)
        ]

    def test_insufficient_data(self):
        result = trend_analysis(self._make_monthly([100]))
        assert result["trend"] == "insufficient_data"

    def test_improving_trend(self):
        result = trend_analysis(self._make_monthly([200, 180]))
        assert result["trend"] == "improving"
        assert result["change_pct"] < 0

    def test_worsening_trend(self):
        result = trend_analysis(self._make_monthly([100, 120]))
        assert result["trend"] == "worsening"
        assert result["change_pct"] > 0

    def test_stable_trend(self):
        result = trend_analysis(self._make_monthly([100, 102]))
        assert result["trend"] == "stable"


class TestEquivalences:
    def test_zero_emissions(self):
        eq = equivalences(0)
        assert eq["miles_driven"] == 0

    def test_positive_equivalences(self):
        eq = equivalences(1000)
        assert eq["miles_driven"] > 0
        assert eq["trees_year"] > 0
        assert eq["beef_kg"] > 0

    def test_scaling(self):
        eq1 = equivalences(100)
        eq2 = equivalences(200)
        assert eq2["miles_driven"] == pytest.approx(eq1["miles_driven"] * 2, rel=0.01)
