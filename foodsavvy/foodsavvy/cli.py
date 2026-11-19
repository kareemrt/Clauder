"""FoodSavvy CLI - main entry point."""
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.prompt import Prompt, Confirm, FloatPrompt

from .database import (
    initialize_db, add_pantry_item, get_all_pantry_items, get_expiring_items,
    delete_pantry_item, update_pantry_quantity, add_waste_record,
)
from .models import PantryItem, WasteRecord
from .recipes import suggest_recipes, load_seed_recipes
from .analytics import compute_waste_stats
from .ui import (
    console, print_banner, print_pantry_table, print_recipe_suggestions,
    print_analytics_dashboard, print_alert_panel,
)

CATEGORIES = [
    "produce", "dairy", "meat", "seafood", "grains", "legumes",
    "condiments", "beverages", "snacks", "frozen", "other",
]
LOCATIONS = ["pantry", "fridge", "freezer"]
WASTE_REASONS = ["expired", "spoiled", "overstock", "taste", "other"]


def setup(db_path: Optional[Path] = None):
    initialize_db(db_path)
    load_seed_recipes(db_path)


@click.group()
@click.version_option("1.0.0", prog_name="foodsavvy")
def cli():
    """🥦 FoodSavvy — Reduce food waste. Save money. Help the planet."""
    setup()


# ─── PANTRY COMMANDS ───────────────────────────────────────────────────────────

@cli.command("add")
@click.argument("name")
@click.option("--category", "-c", default="other", type=click.Choice(CATEGORIES), show_default=True)
@click.option("--quantity", "-q", default=1.0, type=float, help="Amount")
@click.option("--unit", "-u", default="unit", help="e.g. kg, g, pieces, litres")
@click.option("--days", "-d", default=7, type=int, help="Days until expiry")
@click.option("--expiry", "-e", default=None, help="Exact expiry date YYYY-MM-DD")
@click.option("--location", "-l", default="fridge", type=click.Choice(LOCATIONS), show_default=True)
@click.option("--notes", "-n", default="", help="Optional notes")
def add_item(name, category, quantity, unit, days, expiry, location, notes):
    """Add an item to your pantry."""
    if expiry:
        expiry_date = date.fromisoformat(expiry)
    else:
        expiry_date = date.today() + timedelta(days=days)

    item = PantryItem(
        name=name, category=category, quantity=quantity, unit=unit,
        expiry_date=expiry_date, location=location, notes=notes,
    )
    item_id = add_pantry_item(item)
    console.print(f"[green]✓ Added [bold]{name}[/bold] (ID: {item_id}) — expires {expiry_date}[/green]")


@cli.command("list")
@click.option("--location", "-l", default=None, type=click.Choice(LOCATIONS), help="Filter by location")
@click.option("--category", "-c", default=None, type=click.Choice(CATEGORIES), help="Filter by category")
@click.option("--expiring", "-e", is_flag=True, help="Show only items expiring within 7 days")
def list_items(location, category, expiring):
    """List pantry items."""
    print_banner()
    if expiring:
        items = get_expiring_items(days=7)
        title = "Items Expiring Within 7 Days"
    else:
        items = get_all_pantry_items()
        title = "Pantry Inventory"

    if location:
        items = [i for i in items if i.location == location]
    if category:
        items = [i for i in items if i.category == category]

    if not items:
        console.print("[yellow]No items found.[/yellow]")
        return
    print_pantry_table(items, title=title)


@cli.command("remove")
@click.argument("item_id", type=int)
@click.option("--waste", "-w", is_flag=True, help="Log this removal as food waste")
@click.option("--cost", default=0.0, type=float, help="Estimated cost of wasted item")
@click.option("--reason", "-r", default="other", type=click.Choice(WASTE_REASONS))
def remove_item(item_id, waste, cost, reason):
    """Remove an item from your pantry."""
    items = get_all_pantry_items()
    item = next((i for i in items if i.id == item_id), None)
    if not item:
        console.print(f"[red]Item {item_id} not found.[/red]")
        sys.exit(1)

    if waste:
        record = WasteRecord(
            item_name=item.name, category=item.category,
            quantity=item.quantity, unit=item.unit,
            reason=reason, estimated_cost=cost,
        )
        add_waste_record(record)
        console.print(f"[yellow]📋 Logged waste: {item.name} (${cost:.2f})[/yellow]")

    delete_pantry_item(item_id)
    console.print(f"[green]✓ Removed {item.name} from pantry.[/green]")


@cli.command("alerts")
@click.option("--days", "-d", default=7, type=int, help="Alert window in days")
def alerts(days):
    """Show items expiring soon."""
    print_banner()
    expiring = get_expiring_items(days=days)
    print_alert_panel(expiring)


# ─── RECIPE COMMANDS ───────────────────────────────────────────────────────────

@cli.command("recipes")
@click.option("--top", "-n", default=5, type=int, help="Number of suggestions")
@click.option("--all-items", "-a", is_flag=True, help="Consider all items (not just expiring)")
def show_recipes(top, all_items):
    """Suggest recipes based on your pantry."""
    print_banner()
    items = get_all_pantry_items()
    if not items:
        console.print("[yellow]Pantry is empty. Add some items first with: foodsavvy add[/yellow]")
        return
    suggestions = suggest_recipes(items, top_n=top, prioritize_expiring=not all_items)
    print_recipe_suggestions(suggestions)


# ─── ANALYTICS COMMANDS ────────────────────────────────────────────────────────

@cli.command("stats")
def show_stats():
    """Show waste analytics dashboard."""
    print_banner()
    stats = compute_waste_stats()
    print_analytics_dashboard(stats)


@cli.command("log-waste")
@click.argument("name")
@click.option("--category", "-c", default="other", type=click.Choice(CATEGORIES))
@click.option("--quantity", "-q", default=1.0, type=float)
@click.option("--unit", "-u", default="unit")
@click.option("--reason", "-r", default="expired", type=click.Choice(WASTE_REASONS))
@click.option("--cost", default=0.0, type=float, help="Estimated $ value wasted")
def log_waste(name, category, quantity, unit, reason, cost):
    """Log a food waste event directly."""
    record = WasteRecord(
        item_name=name, category=category, quantity=quantity,
        unit=unit, reason=reason, estimated_cost=cost,
    )
    add_waste_record(record)
    console.print(f"[yellow]📋 Waste logged: {name} ({quantity} {unit}) — {reason} — ${cost:.2f}[/yellow]")


# ─── DASHBOARD ─────────────────────────────────────────────────────────────────

@cli.command("dashboard")
def dashboard():
    """Full dashboard: alerts + stats + recipe suggestions."""
    print_banner()
    items = get_all_pantry_items()
    expiring = [i for i in items if 0 <= i.days_until_expiry <= 7]
    expired = [i for i in items if i.days_until_expiry < 0]

    # Alerts
    print_alert_panel(expiring + expired)

    # Stats
    stats = compute_waste_stats()
    print_analytics_dashboard(stats)

    # Recipes
    console.print("\n[bold cyan]💡 Recipe Suggestions (using items expiring soon):[/bold cyan]")
    suggestions = suggest_recipes(items, top_n=3, prioritize_expiring=True)
    print_recipe_suggestions(suggestions)


def main():
    cli()


if __name__ == "__main__":
    main()
