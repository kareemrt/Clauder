# 🌉 FoodBridge

> **Turning surplus into sustenance** — a real-time platform connecting food donors with people in need.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey.svg)](https://flask.palletsprojects.com)
[![Impact](https://img.shields.io/badge/Impact-Food%20Waste%20%26%20Food%20Insecurity-orange.svg)](#the-problem)

---

## The Problem

Two crises exist side by side — and FoodBridge directly bridges them:

| Crisis | Scale |
|--------|-------|
| 🗑️ **Food Waste** | ~40% of the US food supply goes to waste (~80M tons/year) |
| 🍽️ **Food Insecurity** | 44 million Americans — including 1 in 5 children — face hunger |
| 🌍 **Climate Impact** | Food waste drives 8–10% of global greenhouse gas emissions |

Restaurants, grocery stores, hotels, farms, and catering companies regularly discard good, safe food because redistribution is logistically hard. **FoodBridge makes it easy.**

---

## Solution

```
┌─────────────────────────────────────────────────────────────────┐
│                        FOODBRIDGE FLOW                          │
│                                                                 │
│  ┌──────────────┐    POST listing     ┌──────────────────────┐  │
│  │   DONORS     │ ──────────────────► │   FoodBridge DB      │  │
│  │              │                     │                      │  │
│  │ • Restaurants│    instant publish  │ • Available listings │  │
│  │ • Grocers    │                     │ • Expiry tracking    │  │
│  │ • Hotels     │ ◄────────────────── │ • Impact metrics     │  │
│  │ • Farms      │   confirmed pickup  │                      │  │
│  └──────────────┘                     └──────────┬───────────┘  │
│                                                  │               │
│                                           CLAIM listing          │
│                                                  │               │
│  ┌──────────────┐                     ┌──────────▼───────────┐  │
│  │  RECIPIENTS  │ ◄────────────────── │  REAL-TIME BROWSER   │  │
│  │              │   browse & reserve  │                      │  │
│  │ • Food banks │                     │ • Filter by category │  │
│  │ • Shelters   │                     │ • Filter by city     │  │
│  │ • Families   │                     │ • Urgency indicators │  │
│  │ • Community  │                     │ • Impact dashboard   │  │
│  └──────────────┘                     └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Features

### 🍱 For Food Donors
- **Quick listing form** — post surplus food in under 2 minutes
- **Live impact preview** — see estimated meals and CO₂ saved before you post
- **Flexible units** — portions, lbs, kg, loaves, trays, gallons, and more
- **Food safety tips** built into the donation flow

### 🔍 For Food Recipients
- **Real-time browsing** — filter by food category and city
- **Urgency indicators** — color-coded expiry warnings (expires today / within 3 days)
- **One-click reservation** — claim food instantly with pickup time selection
- **No account required** — zero friction for people in need

### 📊 Impact Dashboard
- Running totals: meals provided, kg rescued, kg CO₂ prevented
- Monthly trend chart (last 6 months)
- Breakdown by food category
- Contextual comparisons (tree equivalents, food insecurity facts)

### 🧮 Science-Backed Impact Math
```python
# CO₂ impact (EPA average)
CO2_per_kg_food = 2.5 kg CO₂e

# Meals estimate
kg_per_meal = 0.4 kg

impact = {
    "kg_rescued": quantity × unit_weight,
    "meals":      kg_rescued / 0.4,
    "co2_saved":  kg_rescued × 2.5,
    "trees":      co2_saved / 21  # avg tree absorbs 21 kg CO₂/yr
}
```

---

## Project Structure

```
foodbridge/
├── app.py                  # Flask app — routes, DB, impact math
├── wsgi.py                 # WSGI entry point for production
├── requirements.txt        # Python dependencies
├── data/                   # SQLite database (auto-created)
│   └── foodbridge.db
├── templates/
│   ├── base.html           # Nav, footer, shared layout
│   ├── index.html          # Landing page with live stats
│   ├── donate.html         # Donor listing form
│   ├── find.html           # Recipient browse + claim modal
│   └── impact.html         # Charts and impact dashboard
└── static/
    ├── css/style.css       # Design system + responsive layout
    └── js/main.js          # Shared card rendering helpers
```

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/kareemrt/clauder.git
cd clauder/foodbridge

# 2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python wsgi.py

# 5. Open http://localhost:5000
```

The database is created automatically on first run. Demo data seeds on first page load.

---

## API Reference

All endpoints return JSON.

### Listings

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/listings` | List food listings |
| `POST` | `/api/listings` | Create a new listing |
| `POST` | `/api/listings/:id/claim` | Claim / reserve a listing |

**GET `/api/listings`** — query params: `status` (available\|claimed), `category`, `city`

```json
[
  {
    "id": 1,
    "donor_name": "Green Leaf Bistro",
    "donor_type": "restaurant",
    "food_name": "Mixed Vegetable Stir-Fry",
    "food_category": "prepared",
    "quantity": 20,
    "unit": "portions",
    "expiry_date": "2024-11-19",
    "neighborhood": "Downtown",
    "city": "San Francisco",
    "notes": "Freshly made, mild seasoning.",
    "status": "available",
    "created_at": "2024-11-18T12:00:00"
  }
]
```

**POST `/api/listings`** — required fields: `donor_name`, `donor_type`, `food_name`, `food_category`, `quantity`, `unit`, `expiry_date` (YYYY-MM-DD), `neighborhood`, `city`

**POST `/api/listings/:id/claim`** — required fields: `recipient_name`, `recipient_type`, `contact`, `pickup_time`

### Stats

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/stats` | Aggregate impact statistics |
| `POST` | `/api/seed` | Seed demo data (idempotent) |

**GET `/api/stats`**

```json
{
  "totals": {
    "listings": 18,
    "claimed": 10,
    "available": 8,
    "kg_rescued": 175.3,
    "meals": 434,
    "co2_saved_kg": 438.2,
    "trees_equivalent": 20.9
  },
  "monthly_trend": [
    { "month": "Jun 2024", "meals": 0 },
    { "month": "Jul 2024", "meals": 75 },
    ...
  ],
  "by_category": [
    { "category": "prepared", "count": 7, "meals": 310 },
    ...
  ]
}
```

---

## Database Schema

```sql
listings (
  id              INTEGER PRIMARY KEY,
  donor_name      TEXT,
  donor_type      TEXT,     -- restaurant | grocery | bakery | hotel | ...
  food_name       TEXT,
  food_category   TEXT,     -- prepared | produce | bakery | dairy | ...
  quantity        INTEGER,
  unit            TEXT,     -- portions | lbs | kg | loaves | ...
  expiry_date     TEXT,     -- YYYY-MM-DD
  neighborhood    TEXT,
  city            TEXT,
  lat             REAL,     -- optional, for future map integration
  lng             REAL,
  notes           TEXT,
  status          TEXT,     -- available | claimed
  created_at      TEXT,
  claimed_at      TEXT,
  recipient_name  TEXT
)

claims (
  id              INTEGER PRIMARY KEY,
  listing_id      INTEGER,
  recipient_name  TEXT,
  recipient_type  TEXT,     -- food_bank | shelter | community_org | individual
  contact         TEXT,
  pickup_time     TEXT,
  claimed_at      TEXT
)

impact_log (
  id              INTEGER PRIMARY KEY,
  listing_id      INTEGER,
  food_weight_kg  REAL,
  meals_equivalent INTEGER,
  co2_saved_kg    REAL,
  logged_at       TEXT
)
```

---

## Deployment

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY foodbridge/ .
RUN pip install -r requirements.txt gunicorn
ENV FLASK_ENV=production
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app"]
```

### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE` | `data/foodbridge.db` | SQLite database path |
| `FLASK_ENV` | `development` | `production` to disable debug mode |

---

## Roadmap

- [ ] **Geolocation filtering** — radius-based search using lat/lng
- [ ] **Push notifications** — alert nearby recipients when high-volume food is listed
- [ ] **Donor dashboard** — history, impact certificate, recurring donor profiles
- [ ] **Food safety checklist** — mandatory pre-submit food safety confirmation
- [ ] **SMS integration** — Twilio-powered pickup reminders
- [ ] **Multilingual UI** — Spanish, Chinese, Vietnamese for broader access
- [ ] **API rate limiting** — protect the seed/listing endpoints
- [ ] **Admin moderation panel** — flag inappropriate or unsafe listings
- [ ] **Weekly digest email** — impact summary for active donors

---

## Real-World Context

> *"The most sustainable meal is the one that was already made."*

**Why food rescue beats food production every time:**

A single restaurant meal represents not just the food itself, but also:
- 🌊 ~100 gallons of embedded water
- ⚡ Energy for farming, transport, refrigeration, cooking
- 👩‍🌾 Agricultural labor across the supply chain
- 🚛 Fuel for the full distribution journey

When that meal is rescued instead of discarded, **all of that investment is saved** — multiplied across every listing on FoodBridge.

---

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a pull request

Please run the app locally and verify all pages load before submitting a PR.

---

## License

MIT License — free to use, modify, and distribute. See [LICENSE](LICENSE) for details.

---

<div align="center">

**Built to fight food waste and food insecurity.**

*1 in 8 Americans are food insecure. 40% of US food goes to waste. Those two facts should not coexist.*

[Donate Food](https://github.com/kareemrt/clauder) · [Find Food](https://github.com/kareemrt/clauder) · [View Impact](https://github.com/kareemrt/clauder)

</div>
