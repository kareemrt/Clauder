"""
EcoTrack CLI — Personal Carbon Footprint Tracker

Usage:
    ecotrack log transport car --miles 25 --fuel gasoline
    ecotrack log energy electricity --kwh 500
    ecotrack log food beef --kg 0.5
    ecotrack summary
    ecotrack trend
    ecotrack compare
    ecotrack recommend
    ecotrack goal set 2500
    ecotrack history
"""

import click
from datetime import date, timedelta
from pathlib import Path

from .database import get_connection, EmissionLog, GoalManager
from .calculators import (
    TransportCalculator,
    EnergyCalculator,
    FoodCalculator,
    ConsumptionCalculator,
)
from .calculators.food import DietType, DIET_DESCRIPTIONS
from .calculators.consumption import ShoppingHabit
from .analyzer import calculate_summary, trend_analysis, equivalences, GLOBAL_AVERAGES
from .advisor import Advisor
from . import visualizer as viz


DB_PATH = Path.home() / ".ecotrack" / "ecotrack.db"


def _get_db():
    return get_connection(DB_PATH)


@click.group()
@click.version_option("1.0.0", prog_name="EcoTrack")
def cli():
    """
    \b
    ╔═══════════════════════════════════════╗
    ║   🌿 EcoTrack — Carbon Footprint CLI  ║
    ║   Track your impact. Take action.     ║
    ╚═══════════════════════════════════════╝

    Measure your personal carbon footprint across
    transport, energy, food, and consumption.
    """


# ─── LOG ──────────────────────────────────────────────────────────────────────

@cli.group()
def log():
    """Log an emission-producing activity."""


@log.group()
def transport():
    """Log transportation emissions."""


@transport.command("car")
@click.option("--miles", required=True, type=float, help="Distance in miles")
@click.option("--fuel", default="gasoline",
              type=click.Choice(["gasoline", "diesel", "hybrid", "electric"]),
              help="Fuel/power type")
@click.option("--passengers", default=1, type=int, help="Number of passengers sharing the ride")
@click.option("--notes", default="", help="Optional notes")
def log_car(miles, fuel, passengers, notes):
    """Log a car trip."""
    entry = TransportCalculator().car_trip(miles, fuel, passengers)
    _save_transport(entry, "car", notes)
    _echo_saved(entry.kg_co2e, entry.description)


@transport.command("transit")
@click.option("--miles", required=True, type=float)
@click.option("--mode", default="bus",
              type=click.Choice(["bus", "subway", "rail_commuter", "rail_intercity"]))
@click.option("--notes", default="")
def log_transit(miles, mode, notes):
    """Log a public transit trip."""
    entry = TransportCalculator().public_transit(miles, mode)
    _save_transport(entry, mode, notes)
    _echo_saved(entry.kg_co2e, entry.description)


@transport.command("flight")
@click.option("--miles", required=True, type=float, help="One-way distance in miles")
@click.option("--notes", default="")
def log_flight(miles, notes):
    """Log a flight (one way)."""
    entry = TransportCalculator().flight(miles)
    _save_transport(entry, "flight", notes)
    _echo_saved(entry.kg_co2e, entry.description)


@transport.command("commute")
@click.option("--daily-miles", required=True, type=float, help="One-way commute distance (miles)")
@click.option("--mode", default="car_gasoline",
              type=click.Choice(["car_gasoline", "car_diesel", "car_hybrid", "car_electric",
                                 "bus", "subway", "rail_commuter"]))
@click.option("--days", default=250, type=int, help="Work days per year")
@click.option("--passengers", default=1, type=int)
@click.option("--notes", default="")
def log_commute(daily_miles, mode, days, passengers, notes):
    """Log an annual commute pattern."""
    entry = TransportCalculator().commute_annual(daily_miles, days, mode, passengers)
    _save_transport(entry, f"commute_{mode}", notes)
    _echo_saved(entry.kg_co2e, entry.description)


@log.group()
def energy():
    """Log home energy emissions."""


@energy.command("electricity")
@click.option("--kwh", required=True, type=float, help="kWh consumed")
@click.option("--grid", default="us_avg",
              type=click.Choice(["us_avg", "coal_heavy", "mixed", "renewable"]))
@click.option("--notes", default="")
def log_electricity(kwh, grid, notes):
    """Log electricity consumption."""
    entry = EnergyCalculator().electricity(kwh, grid)
    _save_energy(entry, notes)
    _echo_saved(entry.kg_co2e, entry.description)


@energy.command("gas")
@click.option("--therms", required=True, type=float, help="Therms of natural gas")
@click.option("--notes", default="")
def log_gas(therms, notes):
    """Log natural gas consumption."""
    entry = EnergyCalculator().natural_gas(therms)
    _save_energy(entry, notes)
    _echo_saved(entry.kg_co2e, entry.description)


@energy.command("oil")
@click.option("--gallons", required=True, type=float, help="Gallons of heating oil")
@click.option("--notes", default="")
def log_oil(gallons, notes):
    """Log heating oil consumption."""
    entry = EnergyCalculator().heating_oil(gallons)
    _save_energy(entry, notes)
    _echo_saved(entry.kg_co2e, entry.description)


@log.group()
def food():
    """Log food-related emissions."""


@food.command("item")
@click.argument("food_name", type=str)
@click.option("--kg", required=True, type=float, help="Amount consumed in kg")
@click.option("--notes", default="")
def log_food_item(food_name, kg, notes):
    """Log consumption of a specific food item (beef, chicken, etc.)."""
    try:
        entry = FoodCalculator().food_item(food_name, kg)
    except ValueError as e:
        raise click.ClickException(str(e))
    conn = _get_db()
    EmissionLog(conn).add(
        category="food",
        subcategory=food_name,
        amount=kg,
        unit="kg",
        kg_co2e=entry.kg_co2e,
        description=entry.description,
        notes=notes,
    )
    _echo_saved(entry.kg_co2e, entry.description)


@food.command("diet")
@click.option("--type", "diet_type",
              type=click.Choice([d.value for d in DietType]),
              required=True,
              help="Your general diet pattern")
@click.option("--notes", default="")
def log_diet(diet_type, notes):
    """Log your annual diet pattern (sets a yearly baseline)."""
    calc = FoodCalculator()
    dt = DietType(diet_type)
    annual_kg = calc.diet_annual(dt)
    desc = f"Diet pattern: {DIET_DESCRIPTIONS[dt]}"
    conn = _get_db()
    EmissionLog(conn).add(
        category="food",
        subcategory=f"diet_{diet_type}",
        amount=1,
        unit="year",
        kg_co2e=annual_kg,
        description=desc,
        notes=notes,
    )
    _echo_saved(annual_kg, desc)


@log.group()
def consumption():
    """Log consumption and lifestyle emissions."""


@consumption.command("purchase")
@click.argument("item")
@click.option("--qty", default=1, type=int)
@click.option("--notes", default="")
def log_purchase(item, qty, notes):
    """Log the purchase of an item (smartphone, jeans, etc.)."""
    try:
        entry = ConsumptionCalculator().purchase(item, qty)
    except ValueError as e:
        raise click.ClickException(str(e))
    conn = _get_db()
    EmissionLog(conn).add(
        category="consumption",
        subcategory=item,
        amount=qty,
        unit="items",
        kg_co2e=entry.kg_co2e,
        description=entry.description,
        notes=notes,
    )
    _echo_saved(entry.kg_co2e, entry.description)


# ─── SUMMARY ──────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--days", default=30, type=int, help="Days to include in summary")
def summary(days):
    """Show your carbon footprint summary."""
    conn = _get_db()
    log_dao = EmissionLog(conn)
    start = date.today() - timedelta(days=days)
    logs = log_dao.get_by_period(start)
    s = calculate_summary(logs, start=start, end=date.today())

    goal_row = GoalManager(conn).get_current_goal()
    goal_kg = goal_row["target_kg_co2e_annual"] if goal_row else None

    viz.print_summary(s, goal_kg)


@cli.command()
def trend():
    """Show month-over-month emission trends."""
    conn = _get_db()
    monthly = EmissionLog(conn).monthly_totals(months=12)
    if not monthly:
        click.echo("No data yet. Log some activities first.")
        return
    t = trend_analysis(monthly)
    viz.print_trend(t)


@cli.command()
def compare():
    """Compare your footprint to global averages."""
    viz.print_comparison_table()


# ─── RECOMMEND ────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--effort", default=None, type=click.Choice(["low", "medium", "high"]),
              help="Max effort level")
@click.option("--limit", default=5, type=int, help="Number of recommendations")
@click.option("--quick", is_flag=True, help="Show only quick wins (low effort)")
def recommend(effort, limit, quick):
    """Get personalized carbon reduction recommendations."""
    advisor = Advisor()
    recs = advisor.quick_wins(limit) if quick else advisor.top_recommendations(max_effort=effort, limit=limit)

    click.echo("\n")
    try:
        from rich.console import Console
        from rich.table import Table
        from rich import box

        console = Console()
        table = Table(
            title="🌱 Top Recommendations to Reduce Your Footprint",
            box=box.ROUNDED,
            show_lines=True,
        )
        table.add_column("#", justify="center", width=3)
        table.add_column("Category", style="bold")
        table.add_column("Action")
        table.add_column("Potential Saving", justify="right", style="green")
        table.add_column("Effort", justify="center")
        table.add_column("Cost", justify="center")

        effort_colors = {"low": "green", "medium": "yellow", "high": "red"}
        cost_labels = {"saves_money": "💰 Saves $", "neutral": "➖ Neutral", "costs_more": "💸 Costs more"}

        for i, r in enumerate(recs, 1):
            ec = effort_colors.get(r.effort, "white")
            table.add_row(
                str(i),
                f"{r.category}",
                r.action,
                f"{r.potential_saving_kg_annual:,.0f} kg/yr",
                f"[{ec}]{r.effort}[/{ec}]",
                cost_labels.get(r.cost_impact, r.cost_impact),
            )
        console.print(table)

        click.echo("\nDetails:\n")
        for i, r in enumerate(recs, 1):
            click.echo(f"  [{i}] {r.action}")
            click.echo(f"      {r.description}\n")

    except ImportError:
        for i, r in enumerate(recs, 1):
            click.echo(f"{i}. [{r.category}] {r.action}")
            click.echo(f"   Saves: ~{r.potential_saving_kg_annual:,} kg CO2e/yr | Effort: {r.effort}")
            click.echo(f"   {r.description}\n")


# ─── GOAL ─────────────────────────────────────────────────────────────────────

@cli.group()
def goal():
    """Manage your carbon reduction goal."""


@goal.command("set")
@click.argument("target_tonnes", type=float)
@click.option("--deadline", default=None, help="Target date (YYYY-MM-DD)")
@click.option("--notes", default="")
def goal_set(target_tonnes, deadline, notes):
    """Set an annual CO2e target in tonnes (e.g. 2.5 for Paris-aligned)."""
    target_kg = target_tonnes * 1000
    conn = _get_db()
    GoalManager(conn).set_goal(target_kg, deadline, notes)
    click.echo(f"✅ Goal set: {target_tonnes:.1f} tonnes CO₂e/year")
    if target_kg <= GLOBAL_AVERAGES["paris_target_1_5c"]:
        click.echo("   ⭐ That's Paris 1.5°C aligned! Ambitious and impactful.")
    elif target_kg <= GLOBAL_AVERAGES["paris_target_2030"]:
        click.echo("   🎯 That's Paris 2°C aligned. Well done.")
    else:
        click.echo(f"   💡 Tip: The Paris 2°C target is 2.5 tonnes/year.")


@goal.command("show")
def goal_show():
    """Show your current goal."""
    conn = _get_db()
    g = GoalManager(conn).get_current_goal()
    if not g:
        click.echo("No goal set yet. Use `ecotrack goal set <tonnes>` to set one.")
        return
    click.echo(f"Current goal: {g['target_kg_co2e_annual']/1000:.1f} tonnes CO₂e/year")
    if g["deadline"]:
        click.echo(f"Deadline: {g['deadline']}")


# ─── HISTORY ──────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--limit", default=20, type=int)
def history(limit):
    """Show recent logged activities."""
    conn = _get_db()
    rows = EmissionLog(conn).get_all(limit)
    if not rows:
        click.echo("No entries yet. Use `ecotrack log` to get started.")
        return
    try:
        from rich.console import Console
        from rich.table import Table
        from rich import box

        console = Console()
        table = Table(title=f"Last {len(rows)} Activities", box=box.SIMPLE)
        table.add_column("Date", style="dim")
        table.add_column("Category")
        table.add_column("Description")
        table.add_column("kg CO₂e", justify="right", style="yellow")
        for row in rows:
            table.add_row(
                row["logged_at"][:10],
                row["category"],
                row["description"] or row["subcategory"],
                f"{row['kg_co2e']:.2f}",
            )
        console.print(table)
    except ImportError:
        for row in rows:
            click.echo(f"{row['logged_at'][:10]}  {row['category']:12s}  {row['kg_co2e']:7.2f} kg  {row['description']}")


@cli.command("foods")
def list_foods():
    """List all trackable food items and their emission factors."""
    items = FoodCalculator.list_foods()
    click.echo("\nFood emission factors (kg CO₂e per kg of food):\n")
    for name, factor in items:
        bar = "█" * int(factor / 2)
        click.echo(f"  {name:20s} {factor:6.1f}  {bar}")
    click.echo("\n(Source: Poore & Nemecek, 2018, Science)")


# ─── HELPERS ──────────────────────────────────────────────────────────────────

def _save_transport(entry, subcategory: str, notes: str) -> None:
    conn = _get_db()
    EmissionLog(conn).add(
        category="transport",
        subcategory=subcategory,
        amount=entry.distance_miles,
        unit="miles",
        kg_co2e=entry.kg_co2e,
        description=entry.description,
        notes=notes,
    )


def _save_energy(entry, notes: str) -> None:
    conn = _get_db()
    EmissionLog(conn).add(
        category="energy",
        subcategory=entry.source,
        amount=entry.amount,
        unit=entry.unit,
        kg_co2e=entry.kg_co2e,
        description=entry.description,
        notes=notes,
    )


def _echo_saved(kg: float, description: str) -> None:
    click.echo(f"✅  Logged: {description}")
    click.echo(f"    → {kg:.3f} kg CO₂e emitted")


if __name__ == "__main__":
    cli()
