"""Recipe matching and suggestion engine."""
import json
from pathlib import Path
from typing import Optional

from .models import Recipe, PantryItem
from .database import get_all_recipes, add_recipe, initialize_db


DATA_DIR = Path(__file__).parent.parent / "data"


def load_seed_recipes(db_path: Optional[Path] = None):
    """Load built-in recipe database if recipes table is empty."""
    existing = get_all_recipes(db_path)
    if existing:
        return
    recipes_file = DATA_DIR / "recipes.json"
    if not recipes_file.exists():
        return
    with open(recipes_file) as f:
        raw = json.load(f)
    for r in raw:
        recipe = Recipe(
            name=r["name"],
            ingredients=r["ingredients"],
            instructions=r["instructions"],
            prep_time=r["prep_time"],
            servings=r["servings"],
            tags=r.get("tags", []),
        )
        add_recipe(recipe, db_path)


def suggest_recipes(
    pantry_items: list[PantryItem],
    top_n: int = 5,
    prioritize_expiring: bool = True,
    db_path: Optional[Path] = None,
) -> list[tuple[Recipe, float, list[str]]]:
    """Return (recipe, match_score, matched_ingredient_list) sorted by relevance.

    When prioritize_expiring=True, items expiring within 7 days get a 1.5x weight boost.
    """
    all_recipes = get_all_recipes(db_path)
    if not all_recipes:
        return []

    item_names = [item.name for item in pantry_items]

    if prioritize_expiring:
        expiring = {item.name for item in pantry_items if 0 <= item.days_until_expiry <= 7}
        expired = {item.name for item in pantry_items if item.days_until_expiry < 0}
    else:
        expiring = set()
        expired = set()

    results = []
    for recipe in all_recipes:
        base_score = recipe.matches(item_names)
        if base_score == 0:
            continue

        # Boost score for recipes using expiring items
        boost = 1.0
        matched = []
        for ing in recipe.ingredients:
            for name in item_names:
                if ing.lower() in name.lower() or name.lower() in ing.lower():
                    matched.append(name)
                    if name in expiring:
                        boost = max(boost, 1.5)
                    elif name in expired:
                        boost = max(boost, 1.2)

        results.append((recipe, base_score * boost, list(set(matched))))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_n]
