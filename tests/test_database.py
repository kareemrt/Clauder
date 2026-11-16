"""Tests for database layer."""

import os
import tempfile
import pytest
from datetime import date, timedelta

from foodsave.database import Database
from foodsave.models import FoodItem, WasteRecord


@pytest.fixture
def db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        path = f.name
    db = Database(path)
    yield db
    os.unlink(path)


def _make_item(name="Apple", days_until_expiry=5):
    return FoodItem(
        name=name,
        quantity=1.0,
        unit="kg",
        category="fruits",
        purchase_date=date.today(),
        expiry_date=date.today() + timedelta(days=days_until_expiry),
    )


def test_add_and_get(db):
    item = db.add_item(_make_item())
    assert item.item_id is not None
    items = db.get_all_items()
    assert len(items) == 1
    assert items[0].name == "Apple"


def test_remove_item(db):
    item = db.add_item(_make_item())
    assert db.remove_item(item.item_id)
    assert db.get_all_items() == []


def test_expiring_items(db):
    db.add_item(_make_item("Banana", days_until_expiry=2))
    db.add_item(_make_item("Cherry", days_until_expiry=10))
    expiring = db.get_expiring_items(days=3)
    assert len(expiring) == 1
    assert expiring[0].name == "Banana"


def test_log_waste_and_impact(db):
    record = WasteRecord(
        item_name="Beef", quantity=0.5, unit="kg", category="beef",
        waste_date=date.today(), reason="expired",
        kg_co2_wasted=13.5, usd_wasted=5.0,
    )
    db.log_waste(record)
    totals = db.get_impact_totals()
    assert totals["wasted_count"] == 1
    assert totals["co2_wasted"] == pytest.approx(13.5)


def test_impact_empty(db):
    totals = db.get_impact_totals()
    assert totals["wasted_count"] == 0
    assert totals["saved_count"] == 0
