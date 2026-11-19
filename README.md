# 🥦 FoodSavvy

> **Reduce food waste. Save money. Help the planet.**

FoodSavvy is an open-source, terminal-based food waste reduction tool that helps households track pantry items, receive expiry alerts, discover recipes using ingredients about to go bad, and analyse their waste patterns over time.

---

## The Problem

```
  One-Third of All Food Produced Is Wasted
  ─────────────────────────────────────────
  🌍  1.3 billion tonnes of food wasted per year globally
  💸  $1,500/year avg household food waste cost (US)
  🌡   8–10% of global greenhouse gas emissions
  💧  25% of freshwater usage goes to wasted food
  🌱  Food waste is the #3 contributor to climate change
```

Food waste isn't just a dinner table inconvenience — it's one of the most solvable crises we face. FoodSavvy puts the solution in your hands with a simple, fast CLI you can use every day.

---

## Features

```
┌──────────────────────────────────────────────────────────────────────┐
│  FEATURE                      WHAT IT DOES                           │
├──────────────────────────────────────────────────────────────────────┤
│  🏠 Pantry Tracker            Track items across fridge/freezer/     │
│                               pantry with expiry dates               │
│  🔔 Expiry Alerts             Daily warnings for items expiring       │
│                               within a configurable window           │
│  📖 Recipe Suggestions        Match pantry to 20+ built-in recipes;  │
│                               expiring items get priority scoring    │
│  📊 Waste Analytics           Visualise waste cost, CO₂ impact,      │
│                               monthly trends, and category breakdown │
│  📋 Waste Logging             Record what you threw away and why     │
│  🏃 Single Dashboard          Full status at a glance — alerts,      │
│                               stats, and recipe ideas in one view    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Architecture

```
  foodsavvy/
  ├── cli.py          ← Click CLI commands (add, list, alerts, recipes, stats, dashboard)
  ├── database.py     ← SQLite CRUD — pantry items, waste records, recipes
  ├── models.py       ← PantryItem, WasteRecord, Recipe dataclasses
  ├── recipes.py      ← Ingredient-match engine with expiry-boost scoring
  ├── analytics.py    ← Waste stats, CO₂ estimation, sparklines
  └── ui.py           ← Rich terminal tables, panels, and dashboards

  data/
  └── recipes.json    ← 20 built-in recipes seeded on first run

  tests/
  ├── test_database.py  ← 6 database unit tests
  └── test_recipes.py   ← 6 recipe matching unit tests

  ~/.foodsavvy/
  └── foodsavvy.db    ← SQLite database (created automatically)
```

```
  Data Flow
  ─────────────────────────────────────────────────────────────────
  User input
      │
      ▼
  cli.py  ──────────────────────────────────────────────────────┐
      │                                                          │
      ├── add / list / remove ──► database.py ──► SQLite        │
      │                                               ▲          │
      ├── recipes ──────────────► recipes.py ─────── │          │
      │                               │               │          │
      ├── stats ───────────────► analytics.py         │          │
      │                               │               │          │
      └── dashboard ─────────► ui.py (Rich) ◄─────────┘         │
                                      │                          │
                                      ▼                          │
                              Terminal output ◄──────────────────┘
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/kareemrt/clauder.git
cd clauder/foodsavvy

# Install dependencies
pip install -r requirements.txt

# Install the CLI (optional — for global access)
pip install -e .
```

**Requirements:** Python 3.10+ · `click` · `rich`

---

## Quick Start

```bash
# Add items to your pantry
foodsavvy add "Spinach"    --category produce --quantity 200 --unit g    --days 4  --location fridge
foodsavvy add "Milk"       --category dairy   --quantity 1   --unit litre --days 6  --location fridge
foodsavvy add "Chicken"    --category meat    --quantity 500 --unit g    --days 2  --location fridge
foodsavvy add "Brown Rice" --category grains  --quantity 1   --unit kg   --days 180 --location pantry

# See what needs attention
foodsavvy alerts

# Get recipe ideas for expiring items
foodsavvy recipes

# Check waste analytics
foodsavvy stats

# Full dashboard (alerts + stats + recipes in one view)
foodsavvy dashboard
```

---

## Command Reference

```
  COMMAND                DESCRIPTION
  ─────────────────────────────────────────────────────────────────
  add <name>             Add an item to the pantry
    --category, -c       produce | dairy | meat | grains | …
    --quantity, -q       Amount (default: 1.0)
    --unit, -u           kg | g | pieces | litres | …
    --days, -d           Days until expiry (default: 7)
    --expiry, -e         Exact date YYYY-MM-DD (overrides --days)
    --location, -l       fridge | freezer | pantry
    --notes, -n          Optional notes

  list                   List all pantry items
    --location, -l       Filter by location
    --category, -c       Filter by category
    --expiring, -e       Show only items expiring within 7 days

  remove <id>            Remove an item from pantry
    --waste, -w          Log this removal as food waste
    --cost               Estimated $ value wasted
    --reason, -r         expired | spoiled | overstock | …

  alerts                 Show items expiring soon
    --days, -d           Alert window in days (default: 7)

  recipes                Suggest recipes for pantry items
    --top, -n            Number of suggestions (default: 5)
    --all-items, -a      Use all items, not just expiring ones

  stats                  Show waste analytics dashboard

  log-waste <name>       Manually log a food waste event
    --category, -c
    --quantity, -q
    --unit, -u
    --reason, -r
    --cost               Estimated dollar value

  dashboard              Full view: alerts + stats + recipes
```

---

## Recipe Matching Engine

Recipes are scored by ingredient overlap with the current pantry. Items expiring within **7 days** receive a **1.5× boost** to their contribution — so recipes that use soon-to-expire food surface first.

```
  Match Score Formula
  ───────────────────────────────────────────────────────
  base_score   = matched_ingredients / total_ingredients
  expiry_boost = 1.5 if any matched ingredient expires ≤ 7d
               = 1.2 if any matched ingredient is expired
               = 1.0 otherwise
  final_score  = base_score × expiry_boost
```

20 built-in recipes span breakfast, lunch, dinner, soups, desserts, and more. The database is extensible — add your own via `foodsavvy` (future feature).

---

## Waste Analytics

The `stats` command shows:

```
  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐
  │  Total Wasted      │  │  Annual Projection  │  │  CO₂ Impact       │
  │  $24.75            │  │  $67.50/yr          │  │  61.9 kg CO₂e     │
  └────────────────────┘  └────────────────────┘  └────────────────────┘

  Waste by Category
  ─────────────────────────────
  produce      5 items  $12.00
  dairy        3 items   $7.50
  meat         1 item    $5.25

  Monthly Trend
  ─────────────────────────────────────────────────────────
  2026-11  ████████████  $12.00
  2026-10  █████████     $9.75
  2026-09  ████          $3.00
```

CO₂ estimates use an average of **2.5 kg CO₂e per $1** of food waste (WRAP / FAO methodology).

---

## Running Tests

```bash
cd foodsavvy
python3 -m pytest tests/ -v
```

```
  tests/test_database.py::test_add_and_list_items       PASSED
  tests/test_database.py::test_expiring_items           PASSED
  tests/test_database.py::test_expired_item_status      PASSED
  tests/test_database.py::test_item_status_good         PASSED
  tests/test_database.py::test_waste_record             PASSED
  tests/test_database.py::test_waste_summary_multiple   PASSED
  tests/test_recipes.py::test_exact_match               PASSED
  tests/test_recipes.py::test_partial_match             PASSED
  tests/test_recipes.py::test_no_match_returns_empty    PASSED
  tests/test_recipes.py::test_expiring_boost            PASSED
  tests/test_recipes.py::test_top_n_limit               PASSED
  tests/test_recipes.py::test_matched_ingredients       PASSED

  12 passed in 0.15s
```

---

## Impact Potential

```
  If 1,000 households reduce food waste by 50%:
  ──────────────────────────────────────────────────────────────
  💰  $750,000 saved per year
  🌡   937 tonnes CO₂e avoided
  💧  2.5 million litres of water saved
  🌱  Equivalent to planting ~43,000 trees
```

Scaling to communities, schools, restaurants, or food banks multiplies this impact further.

---

## Roadmap

```
  v1.0  (current)   Core CLI — pantry, alerts, recipes, analytics
  v1.1              Shopping list generation from pantry gaps
  v1.2              Community surplus sharing (notify neighbours)
  v1.3              Barcode scanning for instant item entry
  v2.0              Web dashboard + mobile notifications
  v2.1              Integration with grocery delivery APIs
                    (predict purchases before they spoil)
```

---

## Contributing

1. Fork the repo and create a branch (`git checkout -b feature/my-feature`)
2. Write tests for new logic in `tests/`
3. Run the test suite — all tests must pass
4. Submit a pull request with a clear description of the change

---

## License

MIT © FoodSavvy Contributors

---

*"The most powerful thing you can do about climate change is reduce food waste."*
*— Jonathan Foley, Project Drawdown*
