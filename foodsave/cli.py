"""Rich CLI interface for FoodSave."""

import sys
from datetime import date, timedelta
from typing import Optional

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich import box
    from rich.text import Text
    from rich.columns import Columns
    _HAS_RICH = True
except ImportError:
    _HAS_RICH = False

from .database import Database
from .models import FoodItem, WasteRecord
from .impact import calculate_co2_impact, estimate_usd_value, co2_to_human_equivalent
from . import ai_advisor

console = Console() if _HAS_RICH else None

CATEGORIES = [
    "beef", "lamb", "pork", "chicken", "fish", "dairy", "eggs",
    "vegetables", "fruits", "grains", "legumes", "bread", "cheese",
    "butter", "tofu", "nuts", "other",
]

UNITS = ["kg", "g", "lb", "oz", "l", "ml", "unit", "item", "slice", "can", "bag", "bunch", "loaf", "bottle", "pack", "box", "cup"]

WASTE_REASONS = [
    "expired", "forgotten", "overcooked", "over-bought",
    "did not like", "mouldy", "other",
]


def _print(msg: str, style: str = ""):
    if _HAS_RICH:
        console.print(msg, style=style)
    else:
        print(msg)


def _ask(prompt: str, choices=None, default=None) -> str:
    if _HAS_RICH:
        return Prompt.ask(prompt, choices=choices, default=default)
    return input(f"{prompt}: ").strip() or (default or "")


def _confirm(prompt: str) -> bool:
    if _HAS_RICH:
        return Confirm.ask(prompt)
    return input(f"{prompt} [y/N]: ").strip().lower() == "y"


def show_banner():
    if _HAS_RICH:
        console.print(Panel.fit(
            "[bold green]🌱 FoodSave[/bold green]  [dim]AI-powered food waste reduction[/dim]\n"
            "[dim]Reduce waste · Save money · Protect the planet[/dim]",
            border_style="green",
        ))
    else:
        print("=" * 50)
        print("  FoodSave — AI-powered food waste reduction")
        print("=" * 50)


def show_inventory(db: Database):
    items = db.get_all_items()
    if not items:
        _print("[yellow]Your inventory is empty. Add items with 'add'.[/yellow]")
        return

    if _HAS_RICH:
        table = Table(title="🏠 Your Food Inventory", box=box.ROUNDED)
        table.add_column("ID", style="dim", width=8)
        table.add_column("Name", style="bold")
        table.add_column("Qty / Unit")
        table.add_column("Category")
        table.add_column("Expiry", style="cyan")
        table.add_column("Days Left", justify="center")

        for item in items:
            days = item.days_until_expiry()
            if item.is_expired():
                day_str = Text(f"EXPIRED ({days}d)", style="red bold")
            elif item.is_expiring_soon():
                day_str = Text(f"{days}d ⚠", style="yellow bold")
            else:
                day_str = Text(str(days) + "d", style="green")
            table.add_row(
                item.item_id or "-",
                item.name,
                f"{item.quantity} {item.unit}",
                item.category,
                item.expiry_date.isoformat(),
                day_str,
            )
        console.print(table)
    else:
        for item in items:
            days = item.days_until_expiry()
            status = "EXPIRED" if item.is_expired() else f"{days}d left"
            print(f"[{item.item_id}] {item.name} — {item.quantity} {item.unit} — expires {item.expiry_date} ({status})")


def add_item(db: Database):
    _print("\n[bold]Add a food item to your inventory[/bold]")
    name = _ask("Item name")
    if not name:
        return

    try:
        quantity = float(_ask("Quantity", default="1"))
    except ValueError:
        quantity = 1.0

    unit = _ask("Unit", choices=UNITS, default="unit")
    category = _ask("Category", choices=CATEGORIES, default="other")

    purchase_date = date.today()
    exp_str = _ask("Expiry date (YYYY-MM-DD)", default=(date.today() + timedelta(days=7)).isoformat())
    try:
        expiry_date = date.fromisoformat(exp_str)
    except ValueError:
        _print("[red]Invalid date format. Using 7 days from today.[/red]")
        expiry_date = date.today() + timedelta(days=7)

    item = FoodItem(
        name=name, quantity=quantity, unit=unit, category=category,
        purchase_date=purchase_date, expiry_date=expiry_date,
    )
    item = db.add_item(item)
    _print(f"[green]✓ Added '{name}' (ID: {item.item_id}) — expires {expiry_date}[/green]")


def log_waste(db: Database):
    items = db.get_all_items()
    if not items:
        _print("[yellow]Inventory is empty.[/yellow]")
        return

    show_inventory(db)
    item_id = _ask("\nEnter Item ID to mark as wasted (or leave blank to enter manually)")

    item = next((i for i in items if i.item_id == item_id), None)

    if item:
        name, quantity, unit, category = item.name, item.quantity, item.unit, item.category
    else:
        name = _ask("Item name")
        quantity = float(_ask("Quantity wasted", default="1"))
        unit = _ask("Unit", choices=UNITS, default="unit")
        category = _ask("Category", choices=CATEGORIES, default="other")

    reason = _ask("Reason for waste", choices=WASTE_REASONS, default="expired")

    co2 = calculate_co2_impact(quantity, unit, category)
    usd = estimate_usd_value(quantity, unit, category)

    record = WasteRecord(
        item_name=name, quantity=quantity, unit=unit, category=category,
        waste_date=date.today(), reason=reason,
        kg_co2_wasted=co2, usd_wasted=usd,
    )
    db.log_waste(record)

    if item:
        db.remove_item(item.item_id)

    equiv = co2_to_human_equivalent(co2)
    _print(f"\n[red]Waste logged: {name}[/red]")
    _print(f"  CO₂ emitted:  {co2:.3f} kg  ({equiv})")
    _print(f"  Money wasted: ${usd:.2f}")


def mark_saved(db: Database):
    items = db.get_all_items()
    if not items:
        _print("[yellow]Inventory is empty.[/yellow]")
        return

    show_inventory(db)
    item_id = _ask("\nEnter Item ID you successfully used")
    item = next((i for i in items if i.item_id == item_id), None)

    if not item:
        _print("[red]Item not found.[/red]")
        return

    co2 = calculate_co2_impact(item.quantity, item.unit, item.category)
    usd = estimate_usd_value(item.quantity, item.unit, item.category)
    db.log_saved(item, co2, usd)
    db.remove_item(item.item_id)

    equiv = co2_to_human_equivalent(co2)
    _print(f"\n[green]Great job using '{item.name}'![/green]")
    _print(f"  CO₂ avoided:  {co2:.3f} kg  ({equiv})")
    _print(f"  Money saved:  ${usd:.2f}")


def show_alerts(db: Database):
    expiring = db.get_expiring_items(days=3)
    expired = [i for i in db.get_all_items() if i.is_expired()]

    if not expiring and not expired:
        _print("[green]✓ No items expiring soon.[/green]")
        return

    if expired:
        _print(f"\n[red bold]⚠  {len(expired)} item(s) EXPIRED:[/red bold]")
        for item in expired:
            _print(f"  • {item.name} ({item.quantity} {item.unit}) — expired {item.expiry_date}")

    if expiring:
        _print(f"\n[yellow bold]⏰  {len(expiring)} item(s) expiring within 3 days:[/yellow bold]")
        for item in expiring:
            _print(f"  • {item.name} — expires {item.expiry_date} ({item.days_until_expiry()}d)")


def show_impact(db: Database):
    totals = db.get_impact_totals()

    if _HAS_RICH:
        saved_panel = Panel(
            f"[green]Items used:        {totals['saved_count']}[/green]\n"
            f"[green]Food saved:        {totals['saved_kg']:.2f} kg[/green]\n"
            f"[green]CO₂ avoided:       {totals['co2_saved']:.3f} kg[/green]\n"
            f"[green]Money saved:       ${totals['money_saved']:.2f}[/green]",
            title="[bold green]✅ Saved[/bold green]", border_style="green",
        )
        wasted_panel = Panel(
            f"[red]Items wasted:      {totals['wasted_count']}[/red]\n"
            f"[red]Food wasted:       {totals['wasted_kg']:.2f} kg[/red]\n"
            f"[red]CO₂ emitted:       {totals['co2_wasted']:.3f} kg[/red]\n"
            f"[red]Money wasted:      ${totals['money_wasted']:.2f}[/red]",
            title="[bold red]❌ Wasted[/bold red]", border_style="red",
        )
        console.print(Columns([saved_panel, wasted_panel]))

        total_co2 = totals["co2_saved"] + totals["co2_wasted"]
        if total_co2 > 0:
            pct = (totals["co2_saved"] / total_co2) * 100
            console.print(f"\n[bold]Overall waste rate:[/bold] {100-pct:.1f}%  |  "
                          f"[bold]Reduction rate:[/bold] {pct:.1f}%")
    else:
        print(f"Saved — {totals['saved_count']} items, ${totals['money_saved']:.2f}, {totals['co2_saved']:.3f} kg CO2 avoided")
        print(f"Wasted — {totals['wasted_count']} items, ${totals['money_wasted']:.2f}, {totals['co2_wasted']:.3f} kg CO2 emitted")


def ai_suggest(db: Database):
    items = db.get_all_items()
    if not items:
        _print("[yellow]Add items to your inventory first.[/yellow]")
        return
    prefs = _ask("Any dietary preferences or restrictions? (press Enter to skip)", default="")
    _print("\n[dim]Asking Claude for recipe suggestions...[/dim]")
    try:
        result = ai_advisor.suggest_recipes(items, preferences=prefs or None)
        if _HAS_RICH:
            console.print(Panel(result, title="[bold green]🤖 AI Recipe Suggestions[/bold green]", border_style="green"))
        else:
            print("\n--- AI Recipe Suggestions ---")
            print(result)
    except (EnvironmentError, ImportError) as e:
        _print(f"[yellow]{e}[/yellow]")


def ai_storage_tips(db: Database):
    items = db.get_all_items()
    if not items:
        _print("[yellow]Add items first.[/yellow]")
        return
    show_inventory(db)
    item_id = _ask("Enter Item ID for storage tips")
    item = next((i for i in items if i.item_id == item_id), None)
    if not item:
        _print("[red]Item not found.[/red]")
        return
    _print(f"\n[dim]Getting storage tips for {item.name}...[/dim]")
    try:
        result = ai_advisor.get_storage_tips(item)
        if _HAS_RICH:
            console.print(Panel(result, title=f"[bold cyan]💡 Storage Tips: {item.name}[/bold cyan]", border_style="cyan"))
        else:
            print(result)
    except (EnvironmentError, ImportError) as e:
        _print(f"[yellow]{e}[/yellow]")


def ai_reduction_plan(db: Database):
    totals = db.get_impact_totals()
    records = db.get_waste_records()
    if not records:
        _print("[yellow]No waste history yet — start logging to unlock your plan.[/yellow]")
        return

    top_categories = {}
    for r in records:
        top_categories[r.category] = top_categories.get(r.category, 0) + r.quantity
    top = sorted(top_categories.items(), key=lambda x: x[1], reverse=True)[:3]
    top_str = ", ".join(f"{c} ({q:.1f} units)" for c, q in top)

    summary = (
        f"Total items wasted: {totals['wasted_count']}\n"
        f"Total money wasted: ${totals['money_wasted']:.2f}\n"
        f"Total CO2 emitted from waste: {totals['co2_wasted']:.3f} kg\n"
        f"Top wasted categories: {top_str}\n"
        f"Most common reasons: {', '.join(set(r.reason for r in records[:10]))}"
    )

    _print("\n[dim]Generating your personalised waste-reduction plan...[/dim]")
    try:
        result = ai_advisor.get_reduction_plan(summary)
        if _HAS_RICH:
            console.print(Panel(result, title="[bold magenta]📋 Your Personalised Waste-Reduction Plan[/bold magenta]", border_style="magenta"))
        else:
            print(result)
    except (EnvironmentError, ImportError) as e:
        _print(f"[yellow]{e}[/yellow]")


COMMANDS = {
    "inventory": ("Show your food inventory", show_inventory),
    "add": ("Add a food item", add_item),
    "waste": ("Log food as wasted", log_waste),
    "used": ("Mark food as used/saved", mark_saved),
    "alerts": ("Show expiry alerts", show_alerts),
    "impact": ("Show your impact dashboard", show_impact),
    "suggest": ("AI recipe suggestions", ai_suggest),
    "tips": ("AI storage tips for an item", ai_storage_tips),
    "plan": ("AI personalised reduction plan", ai_reduction_plan),
    "help": ("Show this help", None),
    "quit": ("Exit FoodSave", None),
}


def show_help():
    if _HAS_RICH:
        table = Table(title="FoodSave Commands", box=box.SIMPLE)
        table.add_column("Command", style="bold cyan")
        table.add_column("Description")
        for cmd, (desc, _) in COMMANDS.items():
            table.add_row(cmd, desc)
        console.print(table)
    else:
        for cmd, (desc, _) in COMMANDS.items():
            print(f"  {cmd:<12} {desc}")


def run_cli(db_path: str = "foodsave.db"):
    db = Database(db_path)
    show_banner()
    show_alerts(db)

    while True:
        try:
            cmd = _ask("\n[bold cyan]Command[/bold cyan]", default="help").strip().lower()
        except (KeyboardInterrupt, EOFError):
            _print("\n[dim]Goodbye! Keep fighting food waste. 🌱[/dim]")
            break

        if cmd in ("quit", "exit", "q"):
            _print("[dim]Goodbye! Keep fighting food waste. 🌱[/dim]")
            break
        elif cmd == "help":
            show_help()
        elif cmd in COMMANDS and COMMANDS[cmd][1]:
            COMMANDS[cmd][1](db)
        else:
            _print(f"[red]Unknown command '{cmd}'. Type 'help' for options.[/red]")
