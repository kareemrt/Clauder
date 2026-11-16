# 🌍 EcoTrack

**Personal Carbon Footprint Tracker — Measure, Understand, and Reduce Your Climate Impact**

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ███████╗ ██████╗ ██████╗ ████████╗██████╗  █████╗  ██████╗██╗ ██╗  ║
║   ██╔════╝██╔════╝██╔═══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝ ║
║   █████╗  ██║     ██║   ██║   ██║   ██████╔╝███████║██║     █████╔╝  ║
║   ██╔══╝  ██║     ██║   ██║   ██║   ██╔══██╗██╔══██║██║     ██╔═██╗  ║
║   ███████╗╚██████╗╚██████╔╝   ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗ ║
║   ╚══════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝║
║                                                               ║
║            Track your impact. Take action. 🌱                ║
╚═══════════════════════════════════════════════════════════════╝
```

[![Tests](https://img.shields.io/badge/tests-37%20passing-brightgreen)](#testing)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Carbon](https://img.shields.io/badge/Paris%20aligned-2.5t%20target-orange)](#why-this-matters)

---

## The Problem

The climate crisis is real, urgent, and driven by everyday choices most people never measure. The average American emits **14.6 tonnes of CO₂e per year** — nearly **6× the Paris Agreement target** of 2.5 tonnes needed to stay under 2°C of warming.

Yet most people have no idea how their daily actions translate into carbon emissions. Without measurement, there's no accountability. Without accountability, there's no change.

```
Current reality vs. what's needed:
                                                           
  🇺🇸 USA (14.6t) ████████████████████████████████████████
  🇨🇳 China (8.2t)  ██████████████████████████
  🇪🇺 EU (7.3t)      ██████████████████████
  🌍 World (4.6t)    █████████████
  🎯 Paris 2°C (2.5t) ███████
  ⭐ Paris 1.5°C (1.6t) ████
```

**EcoTrack bridges this gap.** It gives individuals science-backed, granular measurements of their personal footprint — and actionable, prioritized steps to reduce it.

---

## Why This Matters

> *"The decisions you make at the grocery store, the dealership, and the thermostat collectively matter more than almost any single policy."*
> — Project Drawdown

| Impact Area | Annual Deaths | CO₂ Contribution |
|---|---|---|
| Air pollution from fossil fuels | 8.7 million/year | Direct cause |
| Climate-related disasters | 150,000+/year (rising) | Indirect cause |
| Food system emissions | — | 26% of global GHG |
| Transport emissions | — | 16% of global GHG |

Individual action alone won't solve climate change, but it matters:
1. **Direct impact** — Your choices reduce real emissions
2. **Market signals** — Consumer behavior shifts industry investment
3. **Political legitimacy** — Personal action strengthens advocacy credibility
4. **Community effect** — Visible choices influence others

---

## Features

```
┌─────────────────────────────────────────────────────────────┐
│                    EcoTrack Capabilities                    │
├─────────────────┬───────────────────────────────────────────┤
│  📊 Track        │ Log emissions across 4 categories:        │
│                 │  • 🚗 Transport (car, flight, transit)     │
│                 │  • ⚡ Energy (electricity, gas, oil)       │
│                 │  • 🍽️ Food (items, diet patterns)          │
│                 │  • 🛒 Consumption (purchases, waste)       │
├─────────────────┼───────────────────────────────────────────┤
│  📈 Analyze      │ • Monthly trend tracking                  │
│                 │ • Category breakdowns                      │
│                 │ • Global comparisons                       │
│                 │ • Relatable equivalences                   │
├─────────────────┼───────────────────────────────────────────┤
│  🎯 Goal         │ • Set custom annual CO₂e targets          │
│                 │ • Paris-aligned goal guidance              │
│                 │ • Progress tracking                        │
├─────────────────┼───────────────────────────────────────────┤
│  💡 Recommend    │ • 12 evidence-based actions               │
│                 │ • Prioritized by impact                    │
│                 │ • Filtered by effort level                 │
│                 │ • Potential savings quantified             │
└─────────────────┴───────────────────────────────────────────┘
```

---

## Architecture

```
ecotrack/
│
├── cli.py                 # Click-based CLI entry point
│
├── calculators/           # Emission calculation engines
│   ├── transport.py       #   Car, flight, transit, commute
│   ├── energy.py          #   Electricity, gas, oil, propane
│   ├── food.py            #   Food items, diet patterns
│   └── consumption.py     #   Purchases, waste, digital
│
├── database.py            # SQLite persistence layer
│                          #   EmissionLog DAO
│                          #   GoalManager DAO
│
├── analyzer.py            # Trend & comparison engine
│                          #   FootprintSummary dataclass
│                          #   Global benchmarks
│                          #   Equivalence translations
│
├── advisor.py             # Recommendation engine
│                          #   12 evidence-based actions
│                          #   Effort/impact prioritization
│
└── visualizer.py          # Rich terminal rendering
                           #   Category breakdowns
                           #   Progress bars
                           #   Global comparison tables

tests/
├── test_calculators.py    # 24 unit tests
└── test_analyzer.py       # 13 unit tests
```

**Data Flow:**

```
User Input (CLI)
       │
       ▼
  Calculator     ◄─── Emission factors (EPA, IPCC, Poore & Nemecek 2018)
       │
       ▼
  EmissionLog ──► SQLite (~/.ecotrack/ecotrack.db)
       │
       ▼
   Analyzer ──► FootprintSummary
       │
       ▼
  Visualizer ──► Rich terminal output
```

---

## Installation

**Requirements:** Python 3.10+

```bash
# Clone the repository
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Install dependencies
pip install click rich

# Verify installation
PYTHONPATH=. python3 -m ecotrack.cli --version
```

Or install as a package:

```bash
pip install -e .
ecotrack --version
```

---

## Quick Start

```bash
# Log your morning commute (15 miles each way by car)
ecotrack log transport commute --daily-miles 15 --mode car_gasoline

# Log last month's electricity bill
ecotrack log energy electricity --kwh 750

# Log your diet pattern
ecotrack log food diet --type average

# See your footprint summary
ecotrack summary

# Get personalized recommendations
ecotrack recommend

# Set a Paris-aligned goal
ecotrack goal set 2.5
```

---

## Usage

### Logging Activities

#### 🚗 Transport

```bash
# Single car trip
ecotrack log transport car --miles 50 --fuel gasoline
ecotrack log transport car --miles 50 --fuel electric

# Carpool (emissions divided by passengers)
ecotrack log transport car --miles 25 --fuel gasoline --passengers 3

# Public transit
ecotrack log transport transit --miles 12 --mode subway
ecotrack log transport transit --miles 30 --mode rail_commuter

# Flight (one-way)
ecotrack log transport flight --miles 2500          # NYC → LAX

# Annual commute pattern
ecotrack log transport commute --daily-miles 20 --mode car_gasoline --days 250
```

#### ⚡ Energy

```bash
# Monthly electricity bill
ecotrack log energy electricity --kwh 886

# With renewable grid (much lower emissions)
ecotrack log energy electricity --kwh 886 --grid renewable

# Natural gas (monthly)
ecotrack log energy gas --therms 45

# Heating oil
ecotrack log energy oil --gallons 80
```

#### 🍽️ Food

```bash
# Specific food item
ecotrack log food item beef --kg 0.5
ecotrack log food item chicken --kg 1.0
ecotrack log food item vegetables --kg 2.0

# See all trackable foods
ecotrack foods

# Annual diet pattern
ecotrack log food diet --type average
ecotrack log food diet --type vegan
ecotrack log food diet --type vegetarian
```

Available diet types:
| Type | Description | CO₂e/year |
|---|---|---|
| `meat_heavy` | Meat at most meals | 3,300 kg |
| `average` | Meat ~4× per week | 2,500 kg |
| `low_meat` | Meat ~2× per week | 1,900 kg |
| `pescatarian` | Fish only | 1,500 kg |
| `vegetarian` | No meat | 1,200 kg |
| `vegan` | No animal products | 900 kg |

#### 🛒 Consumption

```bash
# Purchases
ecotrack log consumption purchase smartphone
ecotrack log consumption purchase laptop
ecotrack log consumption purchase jeans --qty 2
```

---

### Viewing Your Footprint

```bash
# Summary of last 30 days
ecotrack summary

# Summary of last 90 days
ecotrack summary --days 90

# Example output:
# ╭────────────────── 🌍 Your Carbon Footprint ──────────────────╮
# │ Annualized footprint: 8.42 tonnes CO₂e/year                  │
# │ vs US average (14.6t): -42.3%  |  Paris 2°C target: 2.5t/yr  │
# ╰──────────────────────────────────────────────────────────────╯
#
# ╭─ Breakdown by Category ──────────────────────────────────────╮
# │ 🚗 transport  │ 320.5 kg │  3.84t  │ 45.1% │ ████████████░░ │
# │ ⚡ energy     │ 215.8 kg │  2.59t  │ 30.4% │ ████████░░░░░░ │
# │ 🍽️ food       │ 125.0 kg │  1.50t  │ 17.6% │ █████░░░░░░░░░ │
# │ 🛒 consumption│  49.2 kg │  0.59t  │  6.9% │ ██░░░░░░░░░░░░ │
# ╰──────────────────────────────────────────────────────────────╯
```

### Trends

```bash
ecotrack trend
# Shows month-over-month change with ↓ improving / ↑ worsening
```

### Global Comparison

```bash
ecotrack compare
# ╭─ 🌐 Global Carbon Footprint Comparison ──────────────────────╮
# │ 🇺🇸 United States      │ 14.6t │ ███████████████████████████ │
# │ 🇨🇳 China               │  8.2t │ ███████████████             │
# │ 🌍 World average        │  4.6t │ ████████                    │
# │ 🎯 Paris 2°C (2030)     │  2.5t │ ████                        │
# │ ⭐ Paris 1.5°C          │  1.6t │ ██                          │
# ╰──────────────────────────────────────────────────────────────╯
```

### Recommendations

```bash
# Top 5 recommendations
ecotrack recommend

# Quick wins only (low effort)
ecotrack recommend --quick

# Budget recommendations (medium effort max)
ecotrack recommend --effort medium --limit 8
```

**Top Actions by Impact:**

| Action | Saves (kg/yr) | Effort | Cost |
|---|---|---|---|
| Switch to electric vehicle | 2,400 | High | 💰 Saves $ |
| Adopt plant-rich diet | 900 | Medium | 💰 Saves $ |
| Switch to renewable electricity | 1,800 | Low | ➖ Neutral |
| Install heat pump | 1,200 | High | 💰 Saves $ |
| Work from home 2 days/week | 600 | Low | 💰 Saves $ |
| Reduce beef by 50% | 460 | Low | 💰 Saves $ |
| Bike/walk for short trips | 350 | Medium | 💰 Saves $ |

### Setting Goals

```bash
# Set a Paris 2°C aligned goal (2.5 tonnes/year)
ecotrack goal set 2.5

# Set a more ambitious goal
ecotrack goal set 1.6   # Paris 1.5°C aligned

# Check current goal
ecotrack goal show
```

### History

```bash
# View last 20 logged activities
ecotrack history

# View more
ecotrack history --limit 50
```

---

## Emission Data Sources

All emission factors are sourced from peer-reviewed and government research:

| Category | Source |
|---|---|
| Transport | US EPA: Greenhouse Gas Emissions from a Typical Passenger Vehicle (2023) |
| Flights | ICAO Carbon Emissions Calculator + UK BEIS 2023 |
| Electricity | EPA eGRID 2022 regional emission factors |
| Natural Gas | EPA: Greenhouse Gases Equivalencies Calculator |
| Food | Poore & Nemecek (2018), *Science*: "Reducing food's environmental impacts through producers and consumers" |
| Diet | Our World in Data: Food and Climate (2023) |
| Waste | EPA Waste Reduction Model (WARM) v15 |
| Products | Carbon Trust lifecycle assessments |

> All factors represent lifecycle (cradle-to-use) emissions in kg CO₂ equivalent (CO₂e), accounting for all greenhouse gases weighted by their global warming potential over 100 years (GWP100).

---

## Testing

```bash
# Run all tests
PYTHONPATH=. python3 -m pytest tests/ -v

# With coverage
PYTHONPATH=. python3 -m pytest tests/ --cov=ecotrack --cov-report=term-missing
```

**Test results:**
```
tests/test_analyzer.py::TestCalculateSummary::test_empty_logs PASSED
tests/test_analyzer.py::TestCalculateSummary::test_annualization PASSED
tests/test_analyzer.py::TestTrendAnalysis::test_improving_trend PASSED
tests/test_calculators.py::TestTransportCalculator::test_car_gasoline PASSED
tests/test_calculators.py::TestTransportCalculator::test_car_electric_lower_than_gas PASSED
tests/test_calculators.py::TestFoodCalculator::test_beef_high_emissions PASSED
...
37 passed in 0.07s ✅
```

---

## Real-World Impact Potential

If 1 million people used EcoTrack and each reduced their footprint by just **2 tonnes/year** through the recommended actions:

```
Population adopting EcoTrack: 1,000,000 people
Average reduction per person:         2.0 t CO₂e/yr
─────────────────────────────────────────────────
Total annual reduction:         2,000,000 t CO₂e/yr
Equivalent to removing:           434,000 cars from the road
Equivalent to planting:        91,827,364 trees
```

At scale, tools like EcoTrack become a force multiplier for climate action — not by replacing systemic change, but by accelerating the personal and cultural shifts that make systemic change politically possible.

---

## Roadmap

- [ ] **Web dashboard** — Browser-based visualization with charts
- [ ] **Import from utility APIs** — Auto-populate energy data from smart meters
- [ ] **Household mode** — Track emissions for a family, divide per capita
- [ ] **Offset marketplace integration** — Verified carbon offset recommendations
- [ ] **Social features** — Compare and compete with friends
- [ ] **iOS/Android app** — Mobile-first entry and notifications
- [ ] **API mode** — Integrate with smart home devices and fitness trackers
- [ ] **Regional electricity factors** — Auto-detect grid region for accuracy

---

## Contributing

Contributions are welcome! Areas where help is especially valuable:

1. **Emission factor updates** — Keep data current with latest research
2. **New activity categories** — Manufacturing, healthcare, digital services
3. **Localization** — Non-US emission factors, currency, units
4. **Visualizations** — Better charts and reporting

```bash
# Development setup
git clone https://github.com/kareemrt/clauder.git
cd clauder
pip install -r requirements-dev.txt
PYTHONPATH=. python3 -m pytest tests/ -v
```

---

## License

MIT License — see [LICENSE](LICENSE). Free to use, modify, and distribute.

---

## Acknowledgments

- **Joseph Poore & Thomas Nemecek** — For the most comprehensive food lifecycle analysis ever published
- **Project Drawdown** — For quantifying the impact of climate solutions
- **Our World in Data** — For making climate data accessible
- **The EPA** — For public emission factor databases

---

*Built with purpose. The science is clear. The need is urgent. The tools are here.*

> "We are the first generation to feel the effect of climate change, and the last generation that can do something about it." — Barack Obama
