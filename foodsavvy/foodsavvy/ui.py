"""Rich terminal UI helpers."""
from datetime import date
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.columns import Columns
from rich.progress import Progress, BarColumn, TextColumn
from rich.align import Align

from .models import PantryItem, WasteRecord, Recipe

console = Console()

STATUS_STYLES = {
    "good": "green",
    "warning": "yellow",
    "critical": "bold red",
    "expires_today": "bold magenta",
    "expired": "red strike",
}

STATUS_ICONS = {
    "good": "✓",
    "warning": "⚠",
    "critical": "⚡",
    "expires_today": "🔔",
    "expired": "✗",
}

LOCATION_ICONS = {
    "fridge": "❄",
    "freezer": "🧊",
    "pantry": "🏠",
}


def print_banner():
    banner = Text()
    banner.append("  ╔═══════════════════════════════╗\n", style="bold green")
    banner.append("  ║   🥦  ", style="bold green")
    banner.append("FoodSavvy", style="bold white")
    banner.append("  🍎  v1.0   ║\n", style="bold green")
    banner.append("  ║  Reduce waste. Save money.   ║\n", style="green")
    banner.append("  ╚═══════════════════════════════╝\n", style="bold green")
    console.print(banner)


def print_pantry_table(items: list[PantryItem], title: str = "Pantry Inventory"):
    table = Table(
        title=title,
        box=box.ROUNDED,
        border_style="cyan",
        header_style="bold cyan",
        show_lines=False,
    )
    table.add_column("#", style="dim", width=4)
    table.add_column("Item", min_width=18)
    table.add_column("Qty", justify="right", width=8)
    table.add_column("Location", width=10)
    table.add_column("Expires", width=12)
    table.add_column("Status", width=14)

    for item in items:
        style = STATUS_STYLES.get(item.status, "white")
        icon = STATUS_ICONS.get(item.status, "")
        loc_icon = LOCATION_ICONS.get(item.location, "")
        days = item.days_until_expiry
        days_str = (
            f"{abs(days)}d ago" if days < 0
            else "today" if days == 0
            else f"in {days}d"
        )
        table.add_row(
            str(item.id),
            item.name,
            f"{item.quantity} {item.unit}",
            f"{loc_icon} {item.location}",
            item.expiry_date.strftime("%Y-%m-%d"),
            Text(f"{icon} {days_str}", style=style),
        )
    console.print(table)


def print_recipe_suggestions(suggestions: list[tuple]):
    if not suggestions:
        console.print("[yellow]No matching recipes found for current pantry.[/yellow]")
        return

    console.print("\n[bold cyan]📖 Recipe Suggestions[/bold cyan]\n")
    for i, (recipe, score, matched) in enumerate(suggestions, 1):
        pct = int(score * 100)
        bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
        matched_str = ", ".join(matched) if matched else "none"
        console.print(
            Panel(
                f"[bold white]{recipe.name}[/bold white]\n"
                f"[green]Match: [{bar}] {min(pct, 100)}%[/green]  "
                f"[dim]⏱ {recipe.prep_time} min  👤 {recipe.servings} servings[/dim]\n"
                f"[cyan]Using:[/cyan] {matched_str}\n"
                f"[dim]{', '.join(recipe.tags)}[/dim]",
                border_style="green" if pct >= 60 else "yellow",
                title=f"[dim]#{i}[/dim]",
                title_align="left",
            )
        )


def print_analytics_dashboard(stats: dict):
    console.print("\n[bold cyan]📊 Waste Analytics Dashboard[/bold cyan]\n")

    # Summary cards
    cards = [
        Panel(
            Align(
                f"[bold red]${stats['total_waste_cost']:.2f}[/bold red]\n[dim]Total Wasted[/dim]",
                align="center"
            ),
            border_style="red", width=22
        ),
        Panel(
            Align(
                f"[bold yellow]${stats['annual_projection']:.2f}[/bold yellow]\n[dim]Annual Projection[/dim]",
                align="center"
            ),
            border_style="yellow", width=22
        ),
        Panel(
            Align(
                f"[bold orange1]{stats['co2_saved_kg']:.1f} kg[/bold orange1]\n[dim]CO₂ Impact[/dim]",
                align="center"
            ),
            border_style="orange1", width=22
        ),
        Panel(
            Align(
                f"[bold green]{stats['total_pantry_items']}[/bold green]\n[dim]Pantry Items[/dim]",
                align="center"
            ),
            border_style="green", width=22
        ),
    ]
    console.print(Columns(cards, padding=(0, 1)))

    # At-risk items
    console.print(
        f"\n[bold yellow]⚠  {stats['items_at_risk']} items expiring in 7 days[/bold yellow]  "
        f"[bold red]✗  {stats['items_expired']} items already expired[/bold red]"
    )

    # Category breakdown
    if stats["by_category"]:
        console.print("\n[bold]Waste by Category:[/bold]")
        cat_table = Table(box=box.SIMPLE, show_header=True, header_style="bold dim")
        cat_table.add_column("Category")
        cat_table.add_column("Items", justify="right")
        cat_table.add_column("Cost", justify="right")
        for row in sorted(stats["by_category"], key=lambda x: x["cost"] or 0, reverse=True):
            cat_table.add_row(
                row["category"],
                str(row["count"]),
                f"${row['cost'] or 0:.2f}",
            )
        console.print(cat_table)

    # Monthly trend
    if stats["monthly_trend"]:
        console.print("\n[bold]Monthly Waste Trend:[/bold]")
        for m in reversed(stats["monthly_trend"]):
            cost = m["cost"] or 0
            bar_len = min(int(cost / 5), 40)
            bar = "█" * bar_len
            console.print(f"  [dim]{m['month']}[/dim]  [yellow]{bar}[/yellow]  [dim]${cost:.2f}[/dim]")


def print_alert_panel(expiring: list[PantryItem]):
    if not expiring:
        console.print(Panel("[green]✓ No items expiring soon. Pantry is healthy![/green]",
                            title="Expiry Alerts", border_style="green"))
        return

    lines = []
    for item in sorted(expiring, key=lambda x: x.days_until_expiry):
        style = STATUS_STYLES.get(item.status, "white")
        icon = STATUS_ICONS.get(item.status, "")
        days = item.days_until_expiry
        label = "today!" if days == 0 else f"in {days}d" if days > 0 else f"{abs(days)}d ago"
        lines.append(f"[{style}]{icon} {item.name} ({item.quantity} {item.unit}) — expires {label}[/{style}]")

    console.print(Panel(
        "\n".join(lines),
        title=f"[bold yellow]⚠  {len(expiring)} Items Need Attention[/bold yellow]",
        border_style="yellow",
    ))
