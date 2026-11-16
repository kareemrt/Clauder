"""
SQLite database management for EcoTrack.
Stores emission logs, goals, and user profiles.
"""

import sqlite3
import json
from datetime import datetime, date
from pathlib import Path
from typing import Optional


DEFAULT_DB_PATH = Path.home() / ".ecotrack" / "ecotrack.db"


def get_connection(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Get a database connection, creating the DB if needed."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    _init_schema(conn)
    return conn


def _init_schema(conn: sqlite3.Connection) -> None:
    """Create tables if they don't exist."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS profiles (
            id          INTEGER PRIMARY KEY,
            name        TEXT NOT NULL DEFAULT 'default',
            created_at  TEXT NOT NULL,
            metadata    TEXT DEFAULT '{}'
        );

        CREATE TABLE IF NOT EXISTS emission_logs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id  INTEGER NOT NULL DEFAULT 1,
            logged_at   TEXT NOT NULL,
            category    TEXT NOT NULL,
            subcategory TEXT NOT NULL,
            amount      REAL NOT NULL,
            unit        TEXT NOT NULL,
            kg_co2e     REAL NOT NULL,
            description TEXT,
            notes       TEXT,
            FOREIGN KEY (profile_id) REFERENCES profiles(id)
        );

        CREATE TABLE IF NOT EXISTS goals (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id  INTEGER NOT NULL DEFAULT 1,
            created_at  TEXT NOT NULL,
            target_kg_co2e_annual REAL NOT NULL,
            deadline    TEXT,
            notes       TEXT,
            FOREIGN KEY (profile_id) REFERENCES profiles(id)
        );

        CREATE INDEX IF NOT EXISTS idx_logs_profile_date
            ON emission_logs (profile_id, logged_at);

        CREATE INDEX IF NOT EXISTS idx_logs_category
            ON emission_logs (category);
    """)

    # Create default profile if none exists
    cur = conn.execute("SELECT COUNT(*) FROM profiles")
    if cur.fetchone()[0] == 0:
        conn.execute(
            "INSERT INTO profiles (name, created_at, metadata) VALUES (?, ?, ?)",
            ("default", datetime.utcnow().isoformat(), "{}"),
        )
    conn.commit()


class EmissionLog:
    """Data access object for emission log entries."""

    def __init__(self, conn: sqlite3.Connection, profile_id: int = 1):
        self.conn = conn
        self.profile_id = profile_id

    def add(
        self,
        category: str,
        subcategory: str,
        amount: float,
        unit: str,
        kg_co2e: float,
        description: str = "",
        notes: str = "",
        logged_at: Optional[str] = None,
    ) -> int:
        """Insert a new emission log entry. Returns the row id."""
        ts = logged_at or datetime.utcnow().isoformat()
        cur = self.conn.execute(
            """
            INSERT INTO emission_logs
                (profile_id, logged_at, category, subcategory, amount, unit, kg_co2e, description, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (self.profile_id, ts, category, subcategory, amount, unit, kg_co2e, description, notes),
        )
        self.conn.commit()
        return cur.lastrowid

    def get_all(self, limit: int = 100) -> list[sqlite3.Row]:
        """Get recent log entries."""
        return self.conn.execute(
            """
            SELECT * FROM emission_logs
            WHERE profile_id = ?
            ORDER BY logged_at DESC
            LIMIT ?
            """,
            (self.profile_id, limit),
        ).fetchall()

    def get_by_period(
        self,
        start: date,
        end: Optional[date] = None,
    ) -> list[sqlite3.Row]:
        """Get logs within a date range."""
        end = end or date.today()
        return self.conn.execute(
            """
            SELECT * FROM emission_logs
            WHERE profile_id = ?
              AND date(logged_at) BETWEEN ? AND ?
            ORDER BY logged_at DESC
            """,
            (self.profile_id, start.isoformat(), end.isoformat()),
        ).fetchall()

    def get_summary_by_category(
        self, start: Optional[date] = None, end: Optional[date] = None
    ) -> list[sqlite3.Row]:
        """Get total emissions grouped by category for a period."""
        clauses = ["profile_id = ?"]
        params: list = [self.profile_id]
        if start:
            clauses.append("date(logged_at) >= ?")
            params.append(start.isoformat())
        if end:
            clauses.append("date(logged_at) <= ?")
            params.append(end.isoformat())
        where = " AND ".join(clauses)
        return self.conn.execute(
            f"""
            SELECT
                category,
                SUM(kg_co2e) AS total_kg_co2e,
                COUNT(*)     AS entry_count
            FROM emission_logs
            WHERE {where}
            GROUP BY category
            ORDER BY total_kg_co2e DESC
            """,
            params,
        ).fetchall()

    def monthly_totals(self, months: int = 12) -> list[sqlite3.Row]:
        """Get monthly emission totals for the past N months."""
        return self.conn.execute(
            """
            SELECT
                strftime('%Y-%m', logged_at) AS month,
                SUM(kg_co2e)                 AS total_kg_co2e,
                COUNT(*)                     AS entry_count
            FROM emission_logs
            WHERE profile_id = ?
              AND logged_at >= date('now', ? || ' months')
            GROUP BY month
            ORDER BY month ASC
            """,
            (self.profile_id, f"-{months}"),
        ).fetchall()

    def delete(self, entry_id: int) -> bool:
        """Delete an entry by ID."""
        cur = self.conn.execute(
            "DELETE FROM emission_logs WHERE id = ? AND profile_id = ?",
            (entry_id, self.profile_id),
        )
        self.conn.commit()
        return cur.rowcount > 0


class GoalManager:
    """Manage CO2 reduction goals."""

    def __init__(self, conn: sqlite3.Connection, profile_id: int = 1):
        self.conn = conn
        self.profile_id = profile_id

    def set_goal(self, target_annual_kg: float, deadline: Optional[str] = None, notes: str = "") -> int:
        """Set or update the annual emission goal."""
        cur = self.conn.execute(
            """
            INSERT INTO goals (profile_id, created_at, target_kg_co2e_annual, deadline, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (self.profile_id, datetime.utcnow().isoformat(), target_annual_kg, deadline, notes),
        )
        self.conn.commit()
        return cur.lastrowid

    def get_current_goal(self) -> Optional[sqlite3.Row]:
        """Get the most recent goal."""
        return self.conn.execute(
            """
            SELECT * FROM goals
            WHERE profile_id = ?
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (self.profile_id,),
        ).fetchone()
