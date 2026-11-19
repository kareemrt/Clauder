"""SQLite database operations for FoodSavvy."""
import sqlite3
from contextlib import contextmanager
from datetime import date, datetime
from pathlib import Path
from typing import Optional

from .models import PantryItem, WasteRecord, Recipe


DB_PATH = Path.home() / ".foodsavvy" / "foodsavvy.db"


def get_db_path() -> Path:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return DB_PATH


@contextmanager
def get_connection(db_path: Optional[Path] = None):
    path = db_path or get_db_path()
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def initialize_db(db_path: Optional[Path] = None):
    with get_connection(db_path) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS pantry_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity REAL NOT NULL,
                unit TEXT NOT NULL,
                expiry_date TEXT NOT NULL,
                location TEXT NOT NULL DEFAULT 'pantry',
                notes TEXT DEFAULT '',
                added_date TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS waste_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity REAL NOT NULL,
                unit TEXT NOT NULL,
                reason TEXT NOT NULL,
                estimated_cost REAL NOT NULL,
                waste_date TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                instructions TEXT NOT NULL,
                prep_time INTEGER NOT NULL,
                servings INTEGER NOT NULL,
                tags TEXT NOT NULL DEFAULT '[]'
            );
        """)


# --- Pantry CRUD ---

def add_pantry_item(item: PantryItem, db_path: Optional[Path] = None) -> int:
    with get_connection(db_path) as conn:
        cur = conn.execute(
            """INSERT INTO pantry_items
               (name, category, quantity, unit, expiry_date, location, notes, added_date)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (item.name, item.category, item.quantity, item.unit,
             item.expiry_date.isoformat(), item.location, item.notes,
             item.added_date.isoformat()),
        )
        return cur.lastrowid


def get_all_pantry_items(db_path: Optional[Path] = None) -> list[PantryItem]:
    with get_connection(db_path) as conn:
        rows = conn.execute("SELECT * FROM pantry_items ORDER BY expiry_date").fetchall()
    return [_row_to_pantry_item(r) for r in rows]


def get_expiring_items(days: int = 7, db_path: Optional[Path] = None) -> list[PantryItem]:
    cutoff = date.today().isoformat()
    future = (date.today().replace(day=date.today().day)).isoformat()
    with get_connection(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM pantry_items WHERE expiry_date <= date('now', ? || ' days') ORDER BY expiry_date",
            (f"+{days}",),
        ).fetchall()
    return [_row_to_pantry_item(r) for r in rows]


def delete_pantry_item(item_id: int, db_path: Optional[Path] = None):
    with get_connection(db_path) as conn:
        conn.execute("DELETE FROM pantry_items WHERE id = ?", (item_id,))


def update_pantry_quantity(item_id: int, quantity: float, db_path: Optional[Path] = None):
    with get_connection(db_path) as conn:
        conn.execute("UPDATE pantry_items SET quantity = ? WHERE id = ?", (quantity, item_id))


def _row_to_pantry_item(row: sqlite3.Row) -> PantryItem:
    return PantryItem(
        id=row["id"],
        name=row["name"],
        category=row["category"],
        quantity=row["quantity"],
        unit=row["unit"],
        expiry_date=date.fromisoformat(row["expiry_date"]),
        location=row["location"],
        notes=row["notes"],
        added_date=date.fromisoformat(row["added_date"]),
    )


# --- Waste Records ---

def add_waste_record(record: WasteRecord, db_path: Optional[Path] = None) -> int:
    with get_connection(db_path) as conn:
        cur = conn.execute(
            """INSERT INTO waste_records
               (item_name, category, quantity, unit, reason, estimated_cost, waste_date)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (record.item_name, record.category, record.quantity, record.unit,
             record.reason, record.estimated_cost, record.waste_date.isoformat()),
        )
        return cur.lastrowid


def get_waste_records(db_path: Optional[Path] = None) -> list[WasteRecord]:
    with get_connection(db_path) as conn:
        rows = conn.execute("SELECT * FROM waste_records ORDER BY waste_date DESC").fetchall()
    return [_row_to_waste(r) for r in rows]


def get_waste_summary(db_path: Optional[Path] = None) -> dict:
    with get_connection(db_path) as conn:
        total_cost = conn.execute(
            "SELECT COALESCE(SUM(estimated_cost), 0) FROM waste_records"
        ).fetchone()[0]
        by_category = conn.execute(
            "SELECT category, COUNT(*) as count, SUM(estimated_cost) as cost FROM waste_records GROUP BY category"
        ).fetchall()
        by_reason = conn.execute(
            "SELECT reason, COUNT(*) as count FROM waste_records GROUP BY reason"
        ).fetchall()
        monthly = conn.execute(
            """SELECT strftime('%Y-%m', waste_date) as month,
               COUNT(*) as count, SUM(estimated_cost) as cost
               FROM waste_records GROUP BY month ORDER BY month DESC LIMIT 6"""
        ).fetchall()
    return {
        "total_cost": total_cost,
        "by_category": [dict(r) for r in by_category],
        "by_reason": [dict(r) for r in by_reason],
        "monthly": [dict(r) for r in monthly],
    }


def _row_to_waste(row: sqlite3.Row) -> WasteRecord:
    return WasteRecord(
        id=row["id"],
        item_name=row["item_name"],
        category=row["category"],
        quantity=row["quantity"],
        unit=row["unit"],
        reason=row["reason"],
        estimated_cost=row["estimated_cost"],
        waste_date=date.fromisoformat(row["waste_date"]),
    )


# --- Recipes ---

def add_recipe(recipe: Recipe, db_path: Optional[Path] = None) -> int:
    import json
    with get_connection(db_path) as conn:
        cur = conn.execute(
            """INSERT INTO recipes (name, ingredients, instructions, prep_time, servings, tags)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (recipe.name, json.dumps(recipe.ingredients), recipe.instructions,
             recipe.prep_time, recipe.servings, json.dumps(recipe.tags)),
        )
        return cur.lastrowid


def get_all_recipes(db_path: Optional[Path] = None) -> list[Recipe]:
    import json
    with get_connection(db_path) as conn:
        rows = conn.execute("SELECT * FROM recipes").fetchall()
    return [
        Recipe(
            id=r["id"], name=r["name"],
            ingredients=json.loads(r["ingredients"]),
            instructions=r["instructions"],
            prep_time=r["prep_time"], servings=r["servings"],
            tags=json.loads(r["tags"]),
        )
        for r in rows
    ]
