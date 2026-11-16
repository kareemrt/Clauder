"""
Terminal visualizations using ASCII charts and Rich formatting.
"""

from __future__ import annotations

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import BarColumn, Progress, TextColumn
    from rich import box
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from .analyzer import GLOBAL_AVERAGES, equivalences, FootprintSummary

console = Console() if HAS_RICH else None

CATEGORY_ICONS = {
    "transport": "🚗",
    "energy": "⚡",
    "food": "🍽️",
    "consumption": "🛒",
    "services": "🏢",
}

TREND_ICONS = {
    "improving": "📉 Improving",
    "worsening": "📈 Worsening",
    "stable": "➡️  Stable",
    "insufficient_data": "❓ Not enough data",
}


def _bar(value: float, max_val: float, width: int = 30, fill: str = "█", empty: str = "░") -> str:
    filled = int(round(value / max_val * width)) if max_val > 0 else 0
    filled = max(0, min(filled, width))
    return fill * filled + empty * (width - filled)


def print_summary(summary: FootprintSummary, goal_kg: float | None = None) -> None:
    """Print a rich footprint summary to the terminal."""
    if not HAS_RICH:
        _plain_summary(summary, goal_kg)
        return

    total_t = summary.annualized_kg_co2e / 1000
    us_avg_t = GLOBAL_AVERAGES["usa"] / 1000
    paris_t = GLOBAL_AVERAGES["paris_target_2030"] / 1000

    # Header panel
    pct_vs_us = summary.vs_average("usa")
    sign = "+" if pct_vs_us > 0 else ""
    color = "red" if pct_vs_us > 0 else "green"
    console.print(Panel(
        f"[bold]Annualized footprint:[/bold] [yellow]{total_t:.2f} tonnes CO₂e/year[/yellow]\n"
        f"vs US average ({us_avg_t:.1f}t): [{color}]{sign}{pct_vs_us:.1f}%[/{color}]  |  "
        f"Paris 2°C target: {paris_t:.1f}t/yr",
        title="[bold cyan]🌍 Your Carbon Footprint[/bold cyan]",
        border_style="cyan",
    ))

    if not summary.by_category:
        console.print("[dim]No entries logged yet. Use `ecotrack log` to add activities.[/dim]")
        return

    # Category breakdown table
    table = Table(title="Breakdown by Category", box=box.ROUNDED, show_lines=True)
    table.add_column("Category", style="bold")
    table.add_column("kg CO₂e", justify="right", style="yellow")
    table.add_column("Annualized (t)", justify="right")
    table.add_column("Share", justify="right")
    table.add_column("", no_header=True, min_width=32)

    max_val = max(summary.by_category.values()) if summary.by_category else 1
    for cat, kg in summary.by_category.items():
        pct = kg / summary.total_kg_co2e * 100 if summary.total_kg_co2e else 0
        annual_t = kg / summary.period_days * 365 / 1000
        icon = CATEGORY_ICONS.get(cat, "📊")
        bar = _bar(kg, max_val)
        table.add_row(
            f"{icon} {cat}",
            f"{kg:.1f}",
            f"{annual_t:.2f}",
            f"{pct:.1f}%",
            f"[cyan]{bar}[/cyan]",
        )
    console.print(table)

    # Goal progress
    if goal_kg:
        progress_pct = min(summary.annualized_kg_co2e / goal_kg * 100, 150)
        bar = _bar(progress_pct, 100, width=40, fill="█" if progress_pct <= 100 else "▓")
        color = "green" if progress_pct <= 100 else "red"
        console.print(
            f"\n[bold]Goal progress:[/bold] [{color}]{bar}[/{color}] "
            f"[{color}]{progress_pct:.1f}%[/{color}] of {goal_kg/1000:.1f}t target\n"
        )

    # Equivalences
    eq = equivalences(summary.total_kg_co2e)
    console.print(Panel(
        f"  🚗  {eq['miles_driven']:,.0f} miles driven\n"
        f"  🌳  {eq['trees_year']:.1f} trees needed to absorb this for a year\n"
        f"  🥩  {eq['beef_kg']:.1f} kg of beef\n"
        f"  ✈️   {eq['flights_nyc_la']:.2f} NYC→LAX flights",
        title="[bold]What this equals...[/bold]",
        border_style="dim",
    ))


def print_trend(trend: dict) -> None:
    """Print trend analysis."""
    if not HAS_RICH:
        print(f"Trend: {trend['trend']} ({trend['change_pct']:+.1f}%)")
        return

    icon = TREND_ICONS.get(trend["trend"], "❓")
    color = "green" if trend["trend"] == "improving" else ("red" if trend["trend"] == "worsening" else "yellow")
    console.print(
        f"\n[bold]Month-over-month trend:[/bold] [{color}]{icon} ({trend['change_pct']:+.1f}%)[/{color}]"
    )
    if trend.get("best_month"):
        console.print(f"  Best month: [green]{trend['best_month']}[/green]  |  "
                      f"Worst month: [red]{trend['worst_month']}[/red]")


def print_comparison_table() -> None:
    """Print a global comparison table."""
    if not HAS_RICH:
        for name, kg in GLOBAL_AVERAGES.items():
            print(f"  {name}: {kg/1000:.1f}t/year")
        return

    table = Table(title="🌐 Global Carbon Footprint Comparison", box=box.ROUNDED)
    table.add_column("Region / Target", style="bold")
    table.add_column("t CO₂e / year", justify="right", style="yellow")
    table.add_column("", min_width=35)

    max_val = max(GLOBAL_AVERAGES.values())
    labels = {
        "world": "🌍 World average",
        "usa": "🇺🇸 United States",
        "eu": "🇪🇺 European Union",
        "china": "🇨🇳 China",
        "india": "🇮🇳 India",
        "paris_target_2030": "🎯 Paris 2°C target (2030)",
        "paris_target_1_5c": "⭐ Paris 1.5°C target",
    }
    for key, label in labels.items():
        kg = GLOBAL_AVERAGES[key]
        bar = _bar(kg, max_val, width=35)
        color = "green" if "target" in key else "cyan"
        table.add_row(label, f"{kg/1000:.1f}", f"[{color}]{bar}[/{color}]")

    console.print(table)


def _plain_summary(summary: FootprintSummary, goal_kg: float | None = None) -> None:
    """Fallback plain-text summary."""
    print(f"\n=== Your Carbon Footprint ===")
    print(f"Annualized: {summary.annualized_kg_co2e/1000:.2f} tonnes CO2e/year")
    print(f"vs US avg: {summary.vs_average('usa'):+.1f}%")
    print("\nBy category:")
    for cat, kg in summary.by_category.items():
        print(f"  {cat}: {kg:.1f} kg")
    if goal_kg:
        print(f"\nGoal: {goal_kg/1000:.1f}t/yr | Current: {summary.annualized_kg_co2e/1000:.1f}t/yr")
