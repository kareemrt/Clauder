# 🌱 FoodSave — AI-Powered Food Waste Reduction Assistant

> **Fighting food waste one fridge at a time.**  
> An AI assistant that helps households track their food inventory, avoid waste, and understand their environmental and financial impact — powered by Claude.

---

## The Problem

Food waste is one of the most urgent and overlooked drivers of the climate crisis.

```
┌─────────────────────────────────────────────────────────────────┐
│                   The Scale of Food Waste                       │
│                                                                 │
│  🌍  1/3 of all food produced globally is wasted every year    │
│  🌡️  8–10% of global greenhouse gas emissions come from waste  │
│  💸  $1,500 average cost of food waste per US household/year   │
│  🍽️  828 million people go to bed hungry every night           │
│  🚗  Wasting 1 kg of beef = driving ~130 km in a car           │
└─────────────────────────────────────────────────────────────────┘
```

The maddening truth: **most household food waste is preventable**. We forget what's in our fridge, misjudge how much we need, and don't know how to use up ingredients before they expire. FoodSave fixes this.

---

## What FoodSave Does

FoodSave is an interactive CLI tool that sits at the intersection of **behaviour change**, **AI coaching**, and **impact tracking**.

```
┌──────────────────────────────────────────────────────────────────┐
│                    FoodSave Feature Map                          │
│                                                                  │
│   📦 Inventory      →   Track what you have & when it expires   │
│   ⏰  Alerts        →   Get warned before food goes bad         │
│   🗑️  Waste log     →   Record waste with CO₂ + cost impact     │
│   ✅  Saved log     →   Celebrate every item you successfully use│
│   📊  Dashboard     →   See your cumulative environmental impact │
│   🤖  AI Recipes    →   Claude suggests meals for expiring food  │
│   💡  AI Tips       →   Storage advice to extend shelf life      │
│   📋  AI Plan       →   Personalised monthly reduction roadmap   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Architecture

```
foodsave/
├── main.py                  # CLI entry point
├── pyproject.toml           # Package configuration
├── requirements.txt
│
├── foodsave/
│   ├── __init__.py
│   ├── models.py            # FoodItem, WasteRecord, ImpactStats
│   ├── database.py          # SQLite persistence layer
│   ├── impact.py            # CO₂ + financial impact calculations
│   ├── ai_advisor.py        # Claude integration (recipes, tips, plans)
│   └── cli.py               # Rich terminal UI
│
├── data/
│   └── emission_factors.json  # CO₂e per kg by food category
│
└── tests/
    ├── test_database.py
    └── test_impact.py
```

### Data Flow

```
  User Input
      │
      ▼
  ┌────────┐    add/remove    ┌──────────┐
  │  CLI   │◄───────────────► │ Database │ (SQLite)
  │        │                  │          │
  │        │   CO₂ / cost     ├──────────┤
  │        │◄───────────────  │  Impact  │
  │        │                  │  Engine  │
  │        │   AI advice      ├──────────┤
  │        │◄───────────────  │  Claude  │ (Anthropic API)
  └────────┘                  └──────────┘
```

---

## Quick Start

### 1. Clone & install

```bash
git clone https://github.com/kareemrt/clauder.git
cd clauder
pip install -r requirements.txt
```

### 2. (Optional) Enable AI features

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

> AI recipe suggestions, storage tips, and reduction plans require an Anthropic API key.  
> All inventory, waste tracking, and impact dashboard features work without one.

### 3. Run

```bash
python main.py
```

---

## Usage

When you launch FoodSave you get an interactive terminal session:

```
╭──────────────────────────────────────────────╮
│  🌱 FoodSave  AI-powered food waste reduction │
│  Reduce waste · Save money · Protect the planet│
╰──────────────────────────────────────────────╯

⏰  2 item(s) expiring within 3 days:
  • Spinach — expires 2024-11-18 (2d)
  • Chicken thighs — expires 2024-11-19 (3d)

Command:
```

### Available Commands

| Command     | Description                                          |
|-------------|------------------------------------------------------|
| `inventory` | View all items sorted by expiry date                |
| `add`       | Add a new food item with expiry date                |
| `waste`     | Log an item as wasted (records CO₂ + cost)          |
| `used`      | Mark an item as successfully used (records savings) |
| `alerts`    | Show expired and soon-to-expire items               |
| `impact`    | View your cumulative environmental impact dashboard |
| `suggest`   | 🤖 AI recipe suggestions for expiring items         |
| `tips`      | 🤖 AI storage tips for a specific item              |
| `plan`      | 🤖 AI personalised monthly waste-reduction roadmap  |
| `help`      | Show command list                                   |
| `quit`      | Exit                                                |

---

## Impact Dashboard

After a few weeks of use, your impact dashboard shows:

```
╭─────────────── ✅ Saved ─────────────────╮  ╭────────────── ❌ Wasted ─────────────────╮
│ Items used:        47                    │  │ Items wasted:      8                     │
│ Food saved:        12.30 kg              │  │ Food wasted:       1.80 kg               │
│ CO₂ avoided:       28.450 kg             │  │ CO₂ emitted:       4.210 kg              │
│ Money saved:       $87.50                │  │ Money wasted:      $12.40                │
╰──────────────────────────────────────────╯  ╰──────────────────────────────────────────╯

Overall waste rate: 14.6%  |  Reduction rate: 85.4%
```

### Real-World Impact Equivalents

```
  28.5 kg CO₂ avoided  =  ~136 km not driven by car
                        =  ~3,560 smartphone charges avoided
                        =  3 trees growing for a year

  $87.50 saved / month =  $1,050 / year back in your pocket
```

---

## AI Features (Claude-Powered)

### Recipe Suggestions

FoodSave scans your inventory for items expiring within 5 days and asks Claude to suggest practical recipes:

```
🤖 AI Recipe Suggestions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Spinach & Chicken Stir-Fry  (20 min)
   Uses: spinach (expires in 2d), chicken thighs (3d), garlic
   Steps:
   1. Dice chicken and marinate with soy sauce for 5 min
   2. Sauté garlic in oil until fragrant
   3. Add chicken, cook until golden
   4. Toss in spinach, cook 2 min until wilted
   5. Season with sesame oil and serve over rice

2. Creamy Spinach Pasta  (15 min)
   Uses: spinach (expires in 2d), cream (1d)
   ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Storage Tips

Get item-specific advice to extend shelf life:

```
💡 Storage Tips: Spinach
━━━━━━━━━━━━━━━━━━━━━━━
1. Remove any damp paper towel from the bag and replace with
   a dry one to absorb moisture — this adds 3–5 extra days.
2. Store in the crisper drawer at 35–40°F (1–4°C), not the
   door where temperatures fluctuate.
3. If leaves start to wilt, revive them in ice water for
   10 minutes before using.
━━━━━━━━━━━━━━━━━━━━━━━
```

### Personalised Reduction Plan

After building a waste history, get a data-driven monthly action plan:

```
📋 Your Personalised Waste-Reduction Plan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Based on your data, vegetables account for 60% of your waste,
mostly due to over-buying. Here's your 5-step plan for November:

1. Shop twice a week instead of once — buy only 3–4 days of
   fresh produce at a time to match how quickly you consume it.
2. Designate Wednesdays as "use-it-up" nights — cook a meal
   that clears whatever is expiring that week.
3. Store leafy greens in an airtight container with a paper
   towel; they'll last twice as long.
...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Emission Factors

FoodSave uses peer-reviewed lifecycle assessment (LCA) data for CO₂e estimates:

| Category     | kg CO₂e per kg |
|--------------|---------------|
| Beef         | 27.0          |
| Lamb         | 39.2          |
| Butter       | 23.8          |
| Cheese       | 13.5          |
| Pork         | 12.1          |
| Chicken      | 6.9           |
| Eggs         | 4.5           |
| Tofu         | 3.0           |
| Dairy (milk) | 3.2           |
| Grains       | 2.7           |
| Vegetables   | 2.0           |
| Legumes      | 0.9           |

> Sources: Poore & Nemecek (2018), *Science* — "Reducing food's environmental impacts through producers and consumers." Data adjusted for transport and retail waste.

---

## Development

### Running Tests

```bash
pytest tests/ -v
```

All 12 tests cover:
- Weight/unit conversions
- CO₂ emission calculations
- Financial value estimation
- Database CRUD operations
- Expiry filtering logic

### Project Structure Principles

- **No external API calls required** for core functionality — works offline
- **Portable SQLite** database — data lives in a single file, easy to back up
- **Graceful degradation** — AI features show a friendly message if the API key is missing
- **Rich terminal UI** falls back to plain text if the `rich` package isn't available

---

## Roadmap

```
Phase 1 (current)  ✅  CLI inventory + waste tracking + AI advice
Phase 2            🔲  Shared household mode (multi-user SQLite)
Phase 3            🔲  Weekly email digest of waste stats
Phase 4            🔲  Barcode scanning via phone camera (mobile companion)
Phase 5            🔲  Community food-sharing network (donate surplus locally)
Phase 6            🔲  Supermarket integration — import receipts automatically
```

---

## Contributing

Contributions welcome! Areas where help is most needed:

- **Additional emission factor data** — regional variations and new food categories  
- **Barcode database** — mapping UPCs to food categories and typical expiry windows  
- **Translations** — making FoodSave accessible globally  
- **Recipe database** — offline recipe suggestions for areas without API access  

Please open an issue to discuss before submitting a large PR.

---

## License

MIT © FoodSave Contributors

---

## Why This Matters

> *"The single most impactful thing an individual can do for the climate isn't driving an EV or installing solar panels — it's reducing food waste."*  
> — Project Drawdown, 2020

If every household using FoodSave reduced waste by just 50%, the collective impact would be:

```
  10,000 households × 37 kg/year saved × 2.5 kg CO₂e/kg
  = 925 tonnes CO₂e avoided per year
  = equivalent to taking ~200 cars off the road
```

Food waste is a problem everyone can act on, today, with zero cost. FoodSave makes that action visible, measurable, and guided by AI.

**Start saving food. Start saving money. Start saving the planet.**

---

*Built with [Claude](https://www.anthropic.com/claude) · [Report an issue](https://github.com/kareemrt/clauder/issues)*
