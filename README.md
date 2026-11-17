# 🌱 FreshSave — AI-Powered Food Waste Reduction

<div align="center">

**Stop throwing money (and the planet) in the trash.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Claude AI](https://img.shields.io/badge/Claude_AI-Anthropic-CC785C?style=flat-square)](https://anthropic.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## The Problem

> **1 in 3 bites of food produced globally never gets eaten.**

Food waste is one of the most solvable crises we face — and it starts at home.

```
🏠 Average U.S. household wastes ~$1,500 worth of food per year
🌍 Food waste generates ~10% of global greenhouse gas emissions  
💧 4× more water is used to grow food that gets thrown out vs. food that's eaten
🗑️  40% of food waste in the U.S. happens at the consumer level
```

FreshSave gives households the tools to actually do something about this — not through guilt, but through *intelligence*. By knowing what's in your pantry and generating recipes around what's about to expire, you rescue food before it hits the bin.

---

## What FreshSave Does

```
┌─────────────────────────────────────────────────────────────┐
│                      FRESHSAVE FLOW                         │
│                                                             │
│  1. ADD ITEMS          2. TRACK EXPIRY       3. GET RECIPES │
│  ┌──────────┐          ┌──────────────┐      ┌───────────┐  │
│  │ Spinach  │  ──────► │ ⚠️  1 day    │ ───► │ 🍳 Claude │  │
│  │ Chicken  │          │ ⚠️  2 days   │      │  suggests │  │
│  │ Yogurt   │          │ ✅  10 days  │      │  recipes  │  │
│  └──────────┘          └──────────────┘      └───────────┘  │
│                                                             │
│  4. MARK OUTCOMES       5. TRACK IMPACT                     │
│  ┌────────────────┐     ┌────────────────────────────────┐  │
│  │ ✓ Used         │ ──► │  💚 $45 saved  🌍 7.5kg CO₂   │  │
│  │ ✗ Wasted       │     │  ♻️  85% rescue rate           │  │
│  └────────────────┘     └────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Core Features

| Feature | Description |
|---|---|
| 🧺 **Smart Pantry Tracker** | Add items with expiry dates; color-coded urgency at a glance |
| ⚠️ **Expiry Alerts** | Automatic warnings for items expiring within 2–3 days |
| 🤖 **Claude AI Recipes** | Select expiring ingredients; Claude generates custom recipes on-the-spot |
| 📊 **Impact Dashboard** | Track money saved, CO₂ prevented, and your food rescue rate |
| 🗂️ **Category Organization** | Vegetables, fruits, meat, dairy, grains, leftovers — filtered views |
| 📱 **Responsive UI** | Works on mobile, tablet, and desktop |
| 🌱 **Demo Mode** | Ships with realistic seed data so you can explore immediately |

---

## Screenshots

### Pantry View

```
┌─────────────────────────────────────────────────────────────────┐
│  🌱 FreshSave     [Pantry] [AI Recipes] [My Impact]   [+ Add]  │
├─────────────────────────────────────────────────────────────────┤
│  ⚠️  2 items need attention: Spinach, Salmon Fillet...          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─ 10 Active ─┐  ┌─ 3 Expiring ─┐  ┌─ 5 Rescued ─┐  ┌─85%─┐ │
│  │     10      │  │      3       │  │      5      │  │ 85% │ │
│  │ Active Items│  │ in 3 Days    │  │   Rescued   │  │Rate │ │
│  └─────────────┘  └──────────────┘  └─────────────┘  └─────┘ │
│                                                                 │
│  ┌── 🥬 Spinach ──────┐  ┌── 🥩 Salmon ───────┐              │
│  │ [Expires today]    │  │ [Expires tomorrow] │              │
│  │ 1 bag              │  │ 1 piece            │              │
│  │ [✓ Used] [✗ Waste] │  │ [✓ Used] [✗ Waste] │              │
│  └────────────────────┘  └────────────────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

### AI Recipe Generator

```
┌─────────────────────────────────────────────────────────────────┐
│  ✨ Powered by Claude AI                                        │
│  Select expiring ingredients and get personalized recipes.      │
│                                                                 │
│  Ingredients: [🟡 Spinach 1d] [🔴 Salmon 1d] [🟡 Yogurt 2d]  │
│               [🟡 Tomatoes 3d] [🟢 Broccoli 4d]               │
│                                                                 │
│           [ 🍳 Generate Recipes ]                               │
├─────────────────────────────────────────────────────────────────┤
│  ✨ 3 Recipes Generated                                         │
│                                                                 │
│  ┌── Herb-Crusted Salmon with Creamed Spinach ────────────────┐ │
│  │  A quick weeknight dinner using everything expiring.  ⏱30m│ │
│  │  ✓ Salmon  ✓ Spinach  ✓ Greek Yogurt                      │ │
│  │  1. Season salmon with herbs and sear 4 min per side       │ │
│  │  2. Wilt spinach in same pan...                            │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- An [Anthropic API key](https://console.anthropic.com) *(optional — app works without it in demo mode)*

### 1. Clone & Install

```bash
git clone https://github.com/kareemrt/clauder.git
cd clauder

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
ANTHROPIC_API_KEY=sk-ant-...   # Get from console.anthropic.com
DATABASE_URL=sqlite:///freshsave.db
```

> **Without an API key**, the app still works — recipe generation falls back to built-in suggestions.

### 3. Run

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) — the app loads with demo pantry data so you can explore immediately.

---

## How It Works

### Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Browser (SPA)                     │
│  HTML + Vanilla JS + CSS  ──► REST API calls        │
└───────────────────────┬─────────────────────────────┘
                        │ HTTP
┌───────────────────────▼─────────────────────────────┐
│                 Flask Application                    │
│                                                     │
│  Routes:  /api/items    /api/recipes   /api/stats   │
│           ↓                ↓                        │
│  SQLAlchemy ORM      Anthropic SDK                  │
└───────────┬──────────────────┬──────────────────────┘
            │                  │
   ┌────────▼──────┐  ┌────────▼────────┐
   │ SQLite DB     │  │  Claude API     │
   │               │  │  claude-opus    │
   │ items         │  │                 │
   │ waste_logs    │  │  Recipe gen     │
   └───────────────┘  └─────────────────┘
```

### Claude AI Integration

When a user selects expiring ingredients and clicks **Generate Recipes**, FreshSave calls the Claude API with a structured prompt:

```
"I have these ingredients expiring soon:
  - Spinach (1 bag, expires 2024-01-16)
  - Salmon Fillet (1 piece, expires 2024-01-17)
  - Greek Yogurt (1 container, expires 2024-01-17)

Please suggest 3 practical recipes that use as many of these 
ingredients as possible. Format as JSON: { recipes: [...] }"
```

Claude returns structured JSON with recipe names, descriptions, steps, and timing — parsed and displayed immediately in the UI.

### Data Model

```sql
-- Pantry items with expiry tracking
items (
  id, name, quantity, unit,
  expiry_date,          -- drives urgency calculation
  category,             -- vegetables/fruits/meat/dairy/grains/leftovers
  status,               -- active | used | wasted
  added_date
)

-- Outcome tracking for impact metrics
waste_logs (
  id, item_id, item_name,
  quantity, unit,
  outcome,              -- used | wasted
  category,
  logged_date
)
```

---

## Impact Calculations

FreshSave estimates real-world impact from your usage patterns:

| Metric | Calculation | Source |
|---|---|---|
| Money Saved | `items_used × $3` avg value per food item | USDA food waste studies |
| CO₂ Prevented | `items_used × 0.5 kg CO₂` | EPA food waste emissions data |
| Rescue Rate | `items_used / (items_used + items_wasted) × 100` | Tracked locally |

---

## Project Structure

```
freshsave/
├── app.py              # Flask application, routes, Claude integration
├── database.py         # SQLAlchemy models, seed data
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── templates/
│   └── index.html      # Single-page application shell
└── static/
    ├── style.css        # Dark theme, responsive layout
    └── app.js           # Frontend logic, API calls, rendering
```

---

## Deployment

### Production with Gunicorn

```bash
gunicorn app:app --workers 4 --bind 0.0.0.0:8000
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

### Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | No | — | Enables real Claude AI recipe generation |
| `DATABASE_URL` | No | `sqlite:///freshsave.db` | Database connection string |
| `FLASK_ENV` | No | `production` | Set to `development` for debug mode |

---

## Why This Approach

**Problem with existing solutions:** Most food tracking apps focus on grocery list management or calorie counting. They don't address the core behavior that causes waste — not knowing what's in your fridge and what to do with it before it expires.

**Our approach:**
1. **Friction reduction** — Adding an item takes 10 seconds. No barcode scanning, no subscriptions.
2. **Actionable AI** — Don't just show a warning. Tell people *what to cook tonight*.
3. **Impact visibility** — People change behavior when they see tangible outcomes. $45 saved and 7.5kg CO₂ prevented is concrete and motivating.
4. **No judgment** — Tracking wasted items is not about shame; it's data to improve over time.

---

## Roadmap

- [ ] **Barcode scanning** — Use camera to scan grocery items automatically
- [ ] **Household sharing** — Multiple users tracking one shared pantry
- [ ] **Weekly digest** — Email/push summary of what needs to be used
- [ ] **Community recipes** — Share Claude-generated recipes with other users
- [ ] **Grocery store integration** — Import purchase receipts automatically
- [ ] **Meal planning** — Plan the week's meals around what's about to expire

---

## Contributing

Contributions are welcome. Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push and open a pull request

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with 💚 to reduce food waste, one meal at a time.**

*If FreshSave saves you even one bag of spinach a week, that's $150/year and 25kg of CO₂.*

</div>
