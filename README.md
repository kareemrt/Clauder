# TerraGen 🌍

```
 ████████╗███████╗██████╗ ██████╗  █████╗  ██████╗ ███████╗███╗   ██╗
    ██╔══╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔════╝████╗  ██║
    ██║   █████╗  ██████╔╝██████╔╝███████║██║  ███╗█████╗  ██╔██╗ ██║
    ██║   ██╔══╝  ██╔══██╗██╔══██╗██╔══██║██║   ██║██╔══╝  ██║╚██╗██║
    ██║   ███████╗██║  ██║██║  ██║██║  ██║╚██████╔╝███████╗██║ ╚████║
    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝
```

> **Procedural ASCII World Map Generator** — Conjure entire worlds from your terminal, complete with terrain, biomes, rivers, and ancient cities.

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Powered by Rich](https://img.shields.io/badge/rendered%20with-Rich-orange?style=flat-square)](https://github.com/Textualize/rich)
[![Noise: fBm](https://img.shields.io/badge/terrain-fractal%20brownian%20motion-purple?style=flat-square)]()

---

## ✨ Features

| Feature | Description |
|---|---|
| 🏔️ **Fractal Terrain** | Multi-octave fBm noise with continent mask blending for realistic landmasses |
| 🌊 **Dynamic Oceans** | Three ocean depth zones — deep sea, open ocean, shallow coastal waters |
| 🌿 **17 Biomes** | Rainforest to tundra, deserts to boreal forests — governed by a temperature × moisture climate model |
| 🌡️ **Climate Simulation** | Latitude-based temperature gradients, equatorial heat, and altitude cooling |
| 🏞️ **Rivers** | Waterways traced downhill from mountain sources, naturally meeting the sea |
| 🏙️ **Settlements** | Towns and capitals placed at strategic coastal or riverside locations |
| 🎨 **Rich Colors** | Full 256-color terminal rendering via the `rich` library |
| 🔁 **Reproducible** | Pin any world with a `--seed` value; every seed produces the same world every time |
| 📄 **HTML Export** | Save any world as a standalone, full-color HTML file |

---

## 🗺️ Preview

The map below is a monochrome representation — in your terminal, every character blazes with colour:

```
╭────────────────────────  Galemor  (seed: 42)  ──────────────────────────╮
│ ≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≈≈≈≈≈≈≈≈≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋       │
│ ≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≈≈≈≈≈≈≈≈≈≈≈≈≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋     │
│ ≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≈≈≈≈≈~~░░░░~~~≈≈≈≈≈≈≈≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋     │
│ ≈≈≋≋≋≋≋≋≋≋≋≋≋≋≈≈≈≈≈≈░♧♧♧♧♧♧··········░░~≀≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≋≋≋≋≋≋≋≋     │
│ ≈≈≈≈≈≈≈≈≈≈≈≈≈≈~░♠♦♦♦♦♦♧♧♧♧··▲▲····▲▲···★······⁚⁚⁚⁚·····⁚⁚⁚░~~≈≈≈≈     │
│ ≈≈≈≈≈≈≈≈≈≈≈≈≈~░░♠♠♠♠♦♦♦♦♧♧··▲▲▲▲▲▲▲▲▲≀▲▲▲···············⁚⁚⁚⁚⁚⁚░≈≈     │
│ ≋≈≈≈≈≈≈≈≈≈≈≈≈≈~░♠♠♠♠♠♦♦♦♦♧···▲▲▲▲▲▲▲≀▲▲▲▲▲▲▲▲············⁚⁚⁚⁚⁚⁚⁚~≈   │
│ ≋≋≋≈≈≈≈≈≈≈≈≈≈≈≈~♠♠♠♠♠♦♦♦♦♦·····▲▲▲▲≀▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲·∴∴∴∴⁚⁚⁚⁚⁚⁚░≈≈    │
│ ≋≋≋≋≋≈≈≈≈≈≈≈≈≈≈≈~♠♠♠♦♦♦♦♦♦★♧▲▲▲▲▲▲▲▲▲△△△△△△△△△△△△△△△△△△△△△△▲▲▲▲▲    │
│ ≋≋≋≋≋≋≈≈≈≈≈≈≈≈≈≈≈~♠♦♦♦♦♦≀♦♧♧♣♣≀♣▲▲▲▲▲▲▲▲△△△△△△△△△△△△△△△△△△△△△△△△▲   │
│ ≋≋≋≋≋≋≋≋≋≋≈≈≈≈≈≈≈~░♦♦♦≀♦♦♧♧♧♣★♣♣▲▲▲▲▲▲▲▲△△△△△△△△△△△△△△△△△△△△△△△△△△  │
╰──────────────────────────────────────────────────────────────────────────╯

  ≋ Deep Ocean   ≈ Ocean   ~ Shallow   ░ Beach   · Grassland   ♣ Forest
  ♧ Deciduous   ♠ Rainforest   ♦ Tropical   ⁚ Savanna   ∴ Desert   ∵ Shrub
  ▴ Boreal   ▫ Tundra   ❄ Snow   ▲ Mountain   △ Snowy Peak   ≀ River   ★ City
```

> **Full colour** — deep navy oceans, emerald forests, gold deserts, slate mountains — renders live in any 256-colour terminal.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- A 256-colour terminal (iTerm2, Windows Terminal, most Linux terminals)

### Installation

```bash
# Clone the repository
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Install dependencies
pip install -r requirements.txt
```

### Generate Your First World

```bash
python main.py
```

That's it. A new world is born.

---

## 🎮 Usage

```
Usage: python main.py [OPTIONS]

  Procedural ASCII World Map Generator.

Options:
  -W, --width INTEGER     Map width in characters.  [default: 140]
  -H, --height INTEGER    Map height in characters. [default: 45]
  -s, --seed INTEGER      Seed for reproducible worlds.
  --no-legend             Omit the biome legend.
  --no-stats              Omit world statistics.
  --no-cities             Omit the settlements table.
  --export-html PATH      Also export map to a standalone HTML file.
  -h, --help              Show this message and exit.
```

### Examples

```bash
# A random world (different every time)
python main.py

# Pin a world by seed — same seed = same world
python main.py --seed 42

# Large epic map
python main.py -W 200 -H 70

# Minimal — map only, no tables
python main.py --no-legend --no-stats --no-cities

# Export to shareable HTML (preserves all terminal colours)
python main.py --seed 7 --export-html world.html

# Tiny quick preview
python main.py -W 80 -H 25
```

---

## 🧬 How It Works

TerraGen uses a layered procedural generation pipeline:

```
┌─────────────────────────────────────────────────────────────────┐
│                    GENERATION PIPELINE                          │
│                                                                 │
│  1. HEIGHTMAP                                                   │
│     ┌──────────────┐    ┌────────────────┐                     │
│     │  fBm Noise   │ +  │ Continent Mask │ ──▶ Heightmap       │
│     │  (7 octaves) │    │ (Gaussian blobs│                     │
│     └──────────────┘    │  + fBm warp)   │                     │
│                         └────────────────┘                     │
│                                                                 │
│  2. CLIMATE                                                     │
│     ┌──────────────┐    ┌────────────────┐                     │
│     │ Latitude cos │ +  │  fBm Noise     │ ──▶ Temperature     │
│     │  gradient    │    │  (variation)   │      - altitude adj │
│     └──────────────┘    └────────────────┘                     │
│     ┌──────────────┐                                           │
│     │  fBm Noise   │ ──────────────────────▶ Moisture map      │
│     └──────────────┘                                           │
│                                                                 │
│  3. BIOME ASSIGNMENT                                            │
│     height × temperature × moisture ──▶ one of 17 biomes       │
│                                                                 │
│  4. RIVERS                                                      │
│     Mountain sources ──▶ greedy downhill trace ──▶ sea          │
│                                                                 │
│  5. SETTLEMENTS                                                 │
│     Score land cells (coastal/riverside bonus) ──▶ place cities │
│                                                                 │
│  6. RENDER                                                      │
│     Rich terminal output  /  HTML export                        │
└─────────────────────────────────────────────────────────────────┘
```

### Fractal Brownian Motion Noise

Terrain height is computed by summing multiple octaves of smooth value noise,
each at double the frequency and half the amplitude of the previous:

```
H(x,y) = Σ  amplitude_i × ValueNoise(x·freq_i, y·freq_i)
         i=0..N

where  amplitude_i = persistence^i
       freq_i      = lacunarity^i
```

This produces the characteristic *self-similar* roughness seen in real mountain
ranges — smooth broad shapes at low frequency, sharp rocky detail at high
frequency.

### Climate Model

```
                    Poles                Equator               Poles
Temperature:  ❄ Cold ◄──────────── 🌡 Hot ──────────────▶ ❄ Cold
              (cos latitude gradient + noise + altitude penalty)

Moisture:     fBm noise field (independent of temperature)
```

Biomes are assigned from a temperature-by-moisture lookup:

```
              DRY       SEMI-DRY   MODERATE    WET        VERY WET
  HOT       Desert     Savanna    Trop.Forest  Trop.Frs   Rainforest
  WARM      Desert     Grassland  Decid.Frs    Forest     Forest
  COOL      Shrubland  Forest     Forest       Boreal     Boreal
  COLD      Tundra     Tundra     Boreal       Boreal     Boreal
  POLAR     Snow       Snow       Tundra       Tundra     Tundra

  (elevation overrides: coastline → Beach → Mountain → Snowy Peak)
```

---

## 🌿 Biome Reference

| Symbol | Biome | Conditions |
|:------:|-------|-----------|
| `≋` | **Deep Ocean** | height < 24% |
| `≈` | **Ocean** | height 24–40% |
| `~` | **Shallow Water** | height 40–42.5% |
| `░` | **Beach** | height 42.5–44% |
| `∴` | **Desert** | hot & dry |
| `⁚` | **Savanna** | hot & semi-dry |
| `·` | **Grassland** | warm & moderate |
| `♦` | **Tropical Forest** | hot & wet |
| `♠` | **Rainforest** | hot & very wet |
| `∵` | **Shrubland** | cool & dry |
| `♣` | **Forest** | warm & wet |
| `♧` | **Deciduous Forest** | warm-cool & wet |
| `▴` | **Boreal Forest** | cold & moderate–wet |
| `▫` | **Tundra** | cold |
| `❄` | **Snow** | polar |
| `▲` | **Mountain** | height > 72% |
| `△` | **Snowy Peak** | height > 86% |
| `≀` | **River** | overlay — traces downhill from mountains |
| `★` | **Settlement** | overlay — towns and one capital |

---

## 📁 Project Structure

```
clauder/
├── main.py                  ← CLI entry point (Click)
├── requirements.txt
├── README.md
└── terragen/
    ├── __init__.py
    ├── noise.py             ← fBm + value noise + continent mask
    ├── biomes.py            ← Biome enum, display data, climate→biome logic
    ├── names.py             ← Phonetic name generator (worlds & cities)
    ├── world.py             ← World class: generate, rivers, city placement
    └── renderer.py          ← Rich terminal renderer (map + legend + stats)
```

---

## 🛠️ Dependencies

| Package | Purpose |
|---------|---------|
| [`rich`](https://github.com/Textualize/rich) | Coloured terminal output, panels, tables |
| [`click`](https://click.palletsprojects.com) | CLI argument parsing |
| [`numpy`](https://numpy.org) | Vectorised noise generation |

---

## 💡 Tips & Tricks

```bash
# Find a world you love?  Note the seed in the output header.
python main.py --seed 31415

# Very wide terminals give the best experience
python main.py -W 220 -H 65

# Share a world with a colleague
python main.py --seed 8675309 --export-html shared_world.html
# → open shared_world.html in any browser

# Screensaver one-liner
while true; do python main.py --no-legend --no-stats --no-cities; sleep 5; done
```

---

## 📜 License

MIT — do whatever you like with it.

---

*Built with fractal math, ancient cartography, and a lot of enthusiasm.*
