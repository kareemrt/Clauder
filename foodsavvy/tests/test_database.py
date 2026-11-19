"""Tests for database operations."""
import pytest
import tempfile
from datetime import date, timedelta
from pathlib import Path

from foodsavvy.database import initialize_db, add_pantry_item, get_all_pantry_items, get_expiring_items, add_waste_record, get_waste_summary
from foodsavvy.models import PantryItem, WasteRecord


@pytest.fixture
def db(tmp_path):
    db_path = tmp_path / "test.db"
    initialize_db(db_path)
    return db_path


def make_item(name="Apple", days_until_expiry=5):
    return PantryItem(
        name=name,
        category="produce",
        quantity=2.0,
        unit="pieces",
        expiry_date=date.today() + timedelta(days=days_until_expiry),
        location="fridge",
    )


def test_add_and_list_items(db):
    item = make_item("Milk", days_until_expiry=3)
    item_id = add_pantry_item(item, db)
    assert item_id > 0

    items = get_all_pantry_items(db)
    assert len(items) == 1
    assert items[0].name == "Milk"
    assert items[0].location == "fridge"


def test_expiring_items(db):
    add_pantry_item(make_item("Soon", days_until_expiry=3), db)
    add_pantry_item(make_item("Later", days_until_expiry=30), db)

    expiring = get_expiring_items(days=7, db_path=db)
    assert len(expiring) == 1
    assert expiring[0].name == "Soon"


def test_expired_item_status(db):
    item = make_item("Old Cheese", days_until_expiry=-3)
    add_pantry_item(item, db)
    items = get_all_pantry_items(db)
    assert items[0].status == "expired"
    assert items[0].days_until_expiry < 0


def test_item_status_good(db):
    item = make_item("Fresh Bread", days_until_expiry=14)
    add_pantry_item(item, db)
    items = get_all_pantry_items(db)
    assert items[0].status == "good"


def test_waste_record(db):
    record = WasteRecord(
        item_name="Broccoli",
        category="produce",
        quantity=1.0,
        unit="head",
        reason="expired",
        estimated_cost=2.50,
    )
    record_id = add_waste_record(record, db)
    assert record_id > 0

    summary = get_waste_summary(db)
    assert summary["total_cost"] == pytest.approx(2.50)
    assert len(summary["by_category"]) == 1
    assert summary["by_category"][0]["category"] == "produce"


def test_waste_summary_multiple(db):
    for name, cat, cost in [("Milk", "dairy", 3.0), ("Tomato", "produce", 1.5), ("Chicken", "meat", 8.0)]:
        add_waste_record(WasteRecord(name, cat, 1, "unit", "expired", cost), db)

    summary = get_waste_summary(db)
    assert summary["total_cost"] == pytest.approx(12.5)
    assert len(summary["by_category"]) == 3
