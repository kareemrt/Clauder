"""
Personalized carbon reduction recommendations.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Recommendation:
    priority: int  # 1 = highest
    category: str
    action: str
    potential_saving_kg_annual: float
    effort: str  # low / medium / high
    cost_impact: str  # saves_money / neutral / costs_more
    description: str


# Action library with estimated savings
ACTIONS = [
    Recommendation(
        priority=1,
        category="transport",
        action="Switch to electric vehicle",
        potential_saving_kg_annual=2400,
        effort="high",
        cost_impact="saves_money",
        description="Replace a gas car with an EV. With the US average grid, EVs emit ~76% less per mile. Federal tax credits up to $7,500 available.",
    ),
    Recommendation(
        priority=2,
        category="transport",
        action="Work from home 2 days/week",
        potential_saving_kg_annual=600,
        effort="low",
        cost_impact="saves_money",
        description="Eliminating 2 commute days reduces transport emissions ~40% and saves fuel costs.",
    ),
    Recommendation(
        priority=3,
        category="transport",
        action="Take the train instead of flying for trips under 500 miles",
        potential_saving_kg_annual=500,
        effort="medium",
        cost_impact="neutral",
        description="Rail emits ~80% less CO2 than flying. For 2–3 short flights/year, switching to rail saves ~400–600 kg CO2e.",
    ),
    Recommendation(
        priority=4,
        category="food",
        action="Reduce beef consumption by 50%",
        potential_saving_kg_annual=460,
        effort="low",
        cost_impact="saves_money",
        description="Beef produces 60 kg CO2e per kg — 9× more than chicken. Cutting beef in half is one of the highest-impact diet changes.",
    ),
    Recommendation(
        priority=5,
        category="food",
        action="Adopt a plant-rich diet",
        potential_saving_kg_annual=900,
        effort="medium",
        cost_impact="saves_money",
        description="Shifting from an average American diet to vegetarian saves ~1,300 kg CO2e/year. Even partial shifts make a big difference.",
    ),
    Recommendation(
        priority=6,
        category="energy",
        action="Switch to renewable electricity plan",
        potential_saving_kg_annual=1800,
        effort="low",
        cost_impact="neutral",
        description="Switching to a certified renewable energy plan can reduce home electricity emissions by ~95%. Many utilities offer green tariffs.",
    ),
    Recommendation(
        priority=7,
        category="energy",
        action="Install a heat pump",
        potential_saving_kg_annual=1200,
        effort="high",
        cost_impact="saves_money",
        description="Heat pumps are 2–4× more efficient than gas furnaces. Federal 30% tax credit (Inflation Reduction Act) available.",
    ),
    Recommendation(
        priority=8,
        category="energy",
        action="Improve home insulation",
        potential_saving_kg_annual=600,
        effort="high",
        cost_impact="saves_money",
        description="Proper insulation reduces heating/cooling needs by 15–25%. Federal credits cover up to $1,200 in upgrades.",
    ),
    Recommendation(
        priority=9,
        category="energy",
        action="Install a smart thermostat",
        potential_saving_kg_annual=180,
        effort="low",
        cost_impact="saves_money",
        description="Smart thermostats reduce heating/cooling by ~15%, saving ~$150/year on energy bills.",
    ),
    Recommendation(
        priority=10,
        category="consumption",
        action="Buy second-hand clothing",
        potential_saving_kg_annual=200,
        effort="low",
        cost_impact="saves_money",
        description="The fashion industry accounts for ~10% of global CO2. Buying used clothing avoids ~95% of production emissions.",
    ),
    Recommendation(
        priority=11,
        category="consumption",
        action="Reduce food waste to under 10%",
        potential_saving_kg_annual=300,
        effort="medium",
        cost_impact="saves_money",
        description="The average American wastes ~30% of food purchased. Planning meals and proper storage can save $1,500+/year while cutting waste.",
    ),
    Recommendation(
        priority=12,
        category="transport",
        action="Bike or walk for trips under 3 miles",
        potential_saving_kg_annual=350,
        effort="medium",
        cost_impact="saves_money",
        description="60% of car trips are under 6 miles. Switching to active transport for short trips eliminates those emissions entirely.",
    ),
]


class Advisor:
    """Generate personalized carbon reduction recommendations."""

    def top_recommendations(
        self,
        categories: Optional[list[str]] = None,
        max_effort: Optional[str] = None,
        limit: int = 5,
    ) -> list[Recommendation]:
        """Get top recommendations, optionally filtered."""
        recs = ACTIONS
        if categories:
            recs = [r for r in recs if r.category in categories]
        effort_order = {"low": 0, "medium": 1, "high": 2}
        if max_effort:
            recs = [r for r in recs if effort_order[r.effort] <= effort_order[max_effort]]
        return sorted(recs, key=lambda r: r.priority)[:limit]

    def potential_annual_saving(
        self,
        categories: Optional[list[str]] = None,
    ) -> float:
        """Total potential saving from all recommended actions."""
        recs = ACTIONS
        if categories:
            recs = [r for r in recs if r.category in categories]
        return sum(r.potential_saving_kg_annual for r in recs)

    def quick_wins(self, limit: int = 3) -> list[Recommendation]:
        """Low-effort, high-impact recommendations."""
        low_effort = [r for r in ACTIONS if r.effort == "low"]
        return sorted(low_effort, key=lambda r: r.potential_saving_kg_annual, reverse=True)[:limit]
