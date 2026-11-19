"""Tests for recipe matching engine."""
import pytest
import tempfile
from datetime import date, timedelta
from pathlib import Path

from foodsavvy.database import initialize_db, add_recipe
from foodsavvy.models import PantryItem, Recipe
from foodsavvy.recipes import suggest_recipes


@pytest.fixture
def db(tmp_path):
    db_path = tmp_path / "test.db"
    initialize_db(db_path)
    # Seed a few test recipes
    recipes = [
        Recipe("Banana Pancakes", ["banana", "oats", "egg", "milk"], "Cook...", 15, 2),
        Recipe("Veggie Stir-Fry", ["carrot", "broccoli", "pepper", "garlic"], "Fry...", 20, 2),
        Recipe("Tomato Soup", ["tomato", "onion", "garlic", "broth"], "Boil...", 30, 4),
    ]
    for r in recipes:
        add_recipe(r, db_path)
    return db_path


def make_item(name, days=5):
    return PantryItem(name, "produce", 1.0, "unit", date.today() + timedelta(days=days))


def test_exact_match(db):
    items = [make_item("banana"), make_item("oats"), make_item("egg"), make_item("milk")]
    suggestions = suggest_recipes(items, top_n=3, db_path=db)
    assert len(suggestions) > 0
    best = suggestions[0]
    assert best[0].name == "Banana Pancakes"
    assert best[1] > 0.9  # near-perfect match


def test_partial_match(db):
    items = [make_item("tomato"), make_item("onion")]
    suggestions = suggest_recipes(items, top_n=5, db_path=db)
    assert any(r.name == "Tomato Soup" for r, _, _ in suggestions)


def test_no_match_returns_empty(db):
    items = [make_item("durian"), make_item("jackfruit")]
    suggestions = suggest_recipes(items, top_n=5, db_path=db)
    assert len(suggestions) == 0


def test_expiring_boost(db):
    # banana expiring today should boost banana pancakes
    expiring = [make_item("banana", days=1), make_item("oats", days=1)]
    normal = [make_item("banana", days=20), make_item("oats", days=20)]

    s_expiring = suggest_recipes(expiring, top_n=3, prioritize_expiring=True, db_path=db)
    s_normal = suggest_recipes(normal, top_n=3, prioritize_expiring=False, db_path=db)

    # Expiring items should have equal or higher score due to boost
    if s_expiring and s_normal:
        assert s_expiring[0][1] >= s_normal[0][1]


def test_top_n_limit(db):
    items = [make_item("banana"), make_item("carrot"), make_item("tomato"), make_item("garlic")]
    suggestions = suggest_recipes(items, top_n=2, db_path=db)
    assert len(suggestions) <= 2


def test_matched_ingredients_returned(db):
    items = [make_item("banana"), make_item("oats"), make_item("egg")]
    suggestions = suggest_recipes(items, top_n=1, db_path=db)
    assert len(suggestions) == 1
    _, score, matched = suggestions[0]
    assert len(matched) > 0
    assert any("banana" in m.lower() for m in matched)
