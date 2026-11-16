"""SQLite persistence layer for FoodSave."""

import sqlite3
import uuid
from datetime import date
from pathlib import Path
from typing import List, Optional

from .models import FoodItem, WasteRecord


class Database:
    def __init__(self, db_path: str = "foodsave.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with self._conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS inventory (
                    item_id     TEXT PRIMARY KEY,
                    name        TEXT NOT NULL,
                    quantity    REAL NOT NULL,
                    unit        TEXT NOT NULL,
                    category    TEXT NOT NULL,
                    purchase_date TEXT NOT NULL,
                    expiry_date TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS waste_log (
                    record_id   TEXT PRIMARY KEY,
                    item_name   TEXT NOT NULL,
                    quantity    REAL NOT NULL,
                    unit        TEXT NOT NULL,
                    category    TEXT NOT NULL,
                    waste_date  TEXT NOT NULL,
                    reason      TEXT NOT NULL,
                    kg_co2_wasted REAL NOT NULL,
                    usd_wasted  REAL NOT NULL
                );

                CREATE TABLE IF NOT EXISTS saved_log (
                    record_id   TEXT PRIMARY KEY,
                    item_name   TEXT NOT NULL,
                    quantity    REAL NOT NULL,
                    unit        TEXT NOT NULL,
                    category    TEXT NOT NULL,
                    saved_date  TEXT NOT NULL,
                    kg_co2_avoided REAL NOT NULL,
                    usd_saved   REAL NOT NULL
                );
            """)

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def add_item(self, item: FoodItem) -> FoodItem:
        item.item_id = item.item_id or str(uuid.uuid4())[:8]
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO inventory VALUES (?,?,?,?,?,?,?)",
                (
                    item.item_id, item.name, item.quantity, item.unit,
                    item.category, item.purchase_date.isoformat(),
                    item.expiry_date.isoformat(),
                ),
            )
        return item

    def get_all_items(self) -> List[FoodItem]:
        with self._conn() as conn:
            rows = conn.execute("SELECT * FROM inventory ORDER BY expiry_date").fetchall()
        return [self._row_to_item(r) for r in rows]

    def get_expiring_items(self, days: int = 3) -> List[FoodItem]:
        cutoff = date.today().isoformat()
        limit = date.fromordinal(date.today().toordinal() + days).isoformat()
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM inventory WHERE expiry_date BETWEEN ? AND ? ORDER BY expiry_date",
                (cutoff, limit),
            ).fetchall()
        return [self._row_to_item(r) for r in rows]

    def remove_item(self, item_id: str) -> bool:
        with self._conn() as conn:
            cursor = conn.execute("DELETE FROM inventory WHERE item_id=?", (item_id,))
        return cursor.rowcount > 0

    def log_waste(self, record: WasteRecord) -> WasteRecord:
        record.record_id = record.record_id or str(uuid.uuid4())[:8]
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO waste_log VALUES (?,?,?,?,?,?,?,?,?)",
                (
                    record.record_id, record.item_name, record.quantity,
                    record.unit, record.category, record.waste_date.isoformat(),
                    record.reason, record.kg_co2_wasted, record.usd_wasted,
                ),
            )
        return record

    def log_saved(self, item: FoodItem, kg_co2_avoided: float, usd_saved: float):
        record_id = str(uuid.uuid4())[:8]
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO saved_log VALUES (?,?,?,?,?,?,?,?)",
                (
                    record_id, item.name, item.quantity, item.unit,
                    item.category, date.today().isoformat(),
                    kg_co2_avoided, usd_saved,
                ),
            )

    def get_waste_records(self, since: Optional[date] = None) -> List[WasteRecord]:
        with self._conn() as conn:
            if since:
                rows = conn.execute(
                    "SELECT * FROM waste_log WHERE waste_date >= ? ORDER BY waste_date DESC",
                    (since.isoformat(),),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM waste_log ORDER BY waste_date DESC"
                ).fetchall()
        return [self._row_to_waste(r) for r in rows]

    def get_impact_totals(self) -> dict:
        with self._conn() as conn:
            w = conn.execute(
                "SELECT COUNT(*), SUM(quantity), SUM(kg_co2_wasted), SUM(usd_wasted) FROM waste_log"
            ).fetchone()
            s = conn.execute(
                "SELECT COUNT(*), SUM(quantity), SUM(kg_co2_avoided), SUM(usd_saved) FROM saved_log"
            ).fetchone()
        return {
            "wasted_count": w[0] or 0,
            "wasted_kg": w[1] or 0.0,
            "co2_wasted": w[2] or 0.0,
            "money_wasted": w[3] or 0.0,
            "saved_count": s[0] or 0,
            "saved_kg": s[1] or 0.0,
            "co2_saved": s[2] or 0.0,
            "money_saved": s[3] or 0.0,
        }

    @staticmethod
    def _row_to_item(row) -> FoodItem:
        return FoodItem(
            item_id=row[0], name=row[1], quantity=row[2], unit=row[3],
            category=row[4], purchase_date=date.fromisoformat(row[5]),
            expiry_date=date.fromisoformat(row[6]),
        )

    @staticmethod
    def _row_to_waste(row) -> WasteRecord:
        return WasteRecord(
            record_id=row[0], item_name=row[1], quantity=row[2], unit=row[3],
            category=row[4], waste_date=date.fromisoformat(row[5]),
            reason=row[6], kg_co2_wasted=row[7], usd_wasted=row[8],
        )
