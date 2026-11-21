# 🌱 FoodRescue Connect

> **Turning surplus into sustenance — fighting food waste and hunger simultaneously.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-embedded-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## The Problem

Two crises exist side by side in every American city — and neither needs to be as bad as it is:

```
🍕 40% of all food produced in the US is wasted (~80 million tons/year)
🍽️  1 in 8 Americans face food insecurity (including 1 in 5 children)
💸 $408 billion in food value is discarded annually
🌍 8% of global greenhouse gas emissions come from food decomposing in landfills
```

A restaurant throws away 50 lbs of pasta at closing time. Three miles away, a shelter
runs short of dinner. **They never connect.** FoodRescue Connect fixes that.

---

## The Solution

FoodRescue Connect is a **community food rescue coordination platform** that bridges
the gap between food donors (restaurants, bakeries, grocery stores, events) and
food recipients (food banks, shelters, soup kitchens, community fridges).

```
┌──────────────────────────────────────────────────────────────────┐
│                    FoodRescue Connect Flow                        │
│                                                                  │
│  DONORS                      PLATFORM                RECIPIENTS  │
│                                                                  │
│  Restaurant  ─┐              ┌──────────┐    ┌─→  Food Bank     │
│  Bakery      ─┼──→  Post  ──→│ Listings │───→┤    Shelter       │
│  Grocery     ─┤   Surplus    │ Database │    └─→  Soup Kitchen  │
│  Event       ─┘              └──────────┘        Community Org  │
│                                   │                              │
│                            Impact Tracking                       │
│                       (lbs rescued · meals · CO₂)               │
└──────────────────────────────────────────────────────────────────┘
```

### Core Principles

- **No middleman delays** — donors and recipients connect directly after a claim
- **Zero infrastructure cost** — SQLite, no cloud services required
- **Privacy by default** — contact info only shared after a claim is confirmed
- **Impact accountability** — every rescue is logged and aggregated into real metrics

---

## Features

### For Food Donors
- **Quick posting** — list surplus food in under 2 minutes
- **Flexible units** — pounds, kilograms, items, servings, boxes
- **Category tagging** — prepared meals, baked goods, produce, dairy, and more
- **Expiry alerts** — flag time-sensitive items so they're prioritized
- **Pickup notes** — custom instructions (after-hours, back entrance, vehicle needed)

### For Food Recipients
- **Live browse** — see all available donations with filtering by category
- **One-click claiming** — claim a donation instantly with your contact info
- **Direct connection** — donor contact info revealed immediately after claiming
- **Rescue confirmation** — mark rescues complete to build community impact stats

### For the Community
- **Impact dashboard** — real-time metrics: pounds rescued, meals provided, CO₂ avoided
- **Category breakdown** — visualize which food types are rescued most
- **Rescue history** — log of recent donor-recipient connections
- **Context statistics** — understand the problem your community is solving

---

## Screenshots

### Home Page — Live Impact Counter
```
┌─────────────────────────────────────────────────────────────────┐
│  🌱 FoodRescueConnect          Browse Food  Impact  [Donate Food]│
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Turn Surplus Into          ┌──────────┐  ┌──────────┐         │
│  Sustenance                 │  290 lbs │  │  241     │         │
│                             │  Rescued │  │  Meals   │         │
│  Every day, restaurants     └──────────┘  └──────────┘         │
│  discard food while         ┌──────────┐  ┌──────────┐         │
│  families go hungry.        │  4       │  │ 725kg CO₂│         │
│                             │ Rescues  │  │  Avoided │         │
│  [Post Surplus Food]        └──────────┘  └──────────┘         │
│  [Find Available Food]                                          │
└─────────────────────────────────────────────────────────────────┘
```

### Browse Listings — Filter by Category
```
┌─────────────────────────────────────────────────────────────────┐
│  Filter: [All] [Prepared Meals] [Baked Goods] [Produce] ...     │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────┐  ┌─────────────────────────────┐  │
│  │ [Prepared Meals] ⏰Today│  │ [Baked Goods]   ⏰ Today    │  │
│  │                         │  │                             │  │
│  │ Assorted pasta, salads, │  │ Day-old sourdough loaves,   │  │
│  │ bread rolls             │  │ croissants, muffins         │  │
│  │                         │  │                             │  │
│  │ 🏪 The Golden Spoon    │  │ 🏪 Sunrise Bakery          │  │
│  │ ⚖️  45 lbs              │  │ ⚖️  30 lbs                 │  │
│  │ 📍 123 Main St         │  │ 📍 456 Oak Ave             │  │
│  │              [Claim →] │  │                 [Claim →]  │  │
│  └─────────────────────────┘  └─────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Impact Dashboard
```
┌─────────────────────────────────────────────────────────────────┐
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐   │
│  │  290 lbs  │  │  241      │  │  725 kg   │  │    4      │   │
│  │  Rescued  │  │  Meals    │  │  CO₂ Saved│  │  Partners │   │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘   │
│                                                                  │
│  Food Rescued by Category                                        │
│  Prepared Meals  ████████████████████████  150 lbs (2 rescues)  │
│  Produce         ████████████████          120 lbs (1 rescue)   │
│  Baked Goods     ████████                   20 lbs (1 rescue)   │
│                                                                  │
│  Recent Rescues                                                  │
│  Golden Spoon → City Food Bank      45 lbs   Today             │
│  FreshMart    → Hope Shelter        80 lbs   Today             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Backend** | Python 3.11 + Flask 3 | Lightweight, rapid development, no overhead |
| **Database** | SQLite | Zero-setup, embedded, perfect for community scale |
| **Templates** | Jinja2 | Server-rendered HTML, no JS framework needed |
| **Styling** | Custom CSS (design tokens) | Full control, no CDN dependency, fast load |
| **Typography** | Inter (Google Fonts) | Clean, legible, modern |

**No external API dependencies.** The app runs entirely locally — no cloud services,
no API keys, no sign-up. Deploy it on a $5/month VPS or run it on a Raspberry Pi
at a food pantry.

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/kareemrt/Clauder.git
cd Clauder/foodrescue

# (Recommended) Create a virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app (auto-seeds demo data on first launch)
python app.py
```

The app starts at **http://localhost:5000**. Demo data is seeded automatically on
the first run so you can explore the full experience immediately.

### Project Structure

```
foodrescue/
├── app.py                  # Flask application, routes, DB init
├── requirements.txt        # Python dependencies (flask only)
├── foodrescue.db           # SQLite database (auto-created)
│
├── templates/
│   ├── base.html           # Navbar, flash messages, footer
│   ├── index.html          # Landing page with live stats
│   ├── donate.html         # Post surplus food form
│   ├── listings.html       # Browse available donations
│   ├── claim.html          # Claim a donation
│   └── impact.html         # Impact metrics dashboard
│
└── static/
    ├── css/style.css       # Full design system
    └── js/main.js          # Flash dismiss, bar animations
```

---

## Application Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Landing page with live impact stats and recent listings |
| `/donate` | GET, POST | Form to post surplus food |
| `/listings` | GET | Browse all available donations (filter by category) |
| `/claim/<id>` | GET, POST | Claim a specific donation |
| `/complete/<id>` | POST | Mark a rescue as completed (logs impact) |
| `/impact` | GET | Full impact dashboard with charts and history |
| `/api/stats` | GET | JSON endpoint: pounds, meals, CO₂, active listings |

---

## Database Schema

```sql
-- Core table: one row per donation listing
CREATE TABLE donations (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    donor_name       TEXT NOT NULL,
    donor_type       TEXT NOT NULL,       -- Restaurant, Bakery, Grocery Store...
    food_description TEXT NOT NULL,
    category         TEXT NOT NULL,       -- Prepared Meals, Produce, Baked Goods...
    quantity         REAL NOT NULL,
    unit             TEXT NOT NULL,       -- lbs, kg, items, servings, boxes
    expiry_date      TEXT,
    pickup_address   TEXT NOT NULL,
    contact_info     TEXT NOT NULL,
    notes            TEXT,
    status           TEXT NOT NULL,       -- available | claimed | completed
    created_at       TEXT NOT NULL,
    claimed_at       TEXT,
    completed_at     TEXT,
    recipient_name   TEXT,
    recipient_type   TEXT,
    recipient_contact TEXT
);

-- Impact ledger: each completed rescue logs weight
CREATE TABLE impact_log (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    donation_id  INTEGER NOT NULL REFERENCES donations(id),
    pounds_rescued REAL NOT NULL,
    logged_at    TEXT NOT NULL
);
```

---

## Impact Calculations

FoodRescue Connect derives its impact metrics from peer-reviewed estimates:

```
Meals provided  = pounds_rescued ÷ 1.2 lbs/meal
                  (USDA: average meal is ~1.2 lbs of food)

CO₂ avoided     = pounds_rescued × 2.5 kg CO₂e/lb
                  (EPA: food in landfill emits ~2.5 kg CO₂e per pound)
```

---

## Deployment

### Local / Development
```bash
python app.py          # Debug mode, auto-reloads, localhost:5000
```

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `dev-secret-...` | Flask session secret — **set this in production** |
| `FLASK_ENV` | `development` | Set to `production` for production deploys |

---

## Real-World Impact Potential

If deployed at city scale, coordinating just **10% of restaurant food waste** in a city
of 500,000:

```
Assumed restaurant surplus:  ~20 lbs/restaurant/day × 2,000 restaurants = 40,000 lbs/day
10% captured:                4,000 lbs/day
Annual pounds rescued:       1,460,000 lbs/year
Annual meals provided:       1,216,000 meals/year  (~3,330 meals/day)
Annual CO₂ avoided:          3,650 metric tons/year
```

That's one medium-sized city. At national scale, the impact compounds dramatically.

---

## Roadmap

- [ ] **Geolocation filtering** — show donations within N miles of recipient
- [ ] **Push notifications** — email/SMS alerts for new donations matching preferences
- [ ] **Recurring donors** — set a schedule (e.g., "every Friday at 9pm")
- [ ] **Volunteer coordination** — third-party pickup volunteers for donors without vehicles
- [ ] **API integrations** — connect to POS systems (Square, Toast) for automatic surplus detection
- [ ] **Multi-language support** — accessibility for non-English speaking communities
- [ ] **Tax receipt generation** — automated charitable donation receipts for business donors

---

## Contributing

Contributions are welcome. This project exists to have real community impact — the
bar for a good contribution is "does it make food rescue easier, faster, or more
accessible?"

```bash
git checkout -b feature/your-feature
# make changes
git commit -m "Add: description of your change"
git push origin feature/your-feature
# open a pull request
```

---

## License

MIT License — use this freely, deploy it in your community, fork it, adapt it.
If you deploy it somewhere real, we'd love to hear about it.

---

## Acknowledgements

Built to address a real problem that affects every community.

> *"The world produces enough food to feed everyone. The challenge is distribution,
> not production."* — UN Food and Agriculture Organization

Sources: USDA Economic Research Service, EPA Food Recovery Hierarchy,
Feeding America's Map the Meal Gap, ReFED Food Waste Monitor.
