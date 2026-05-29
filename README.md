# WorldForge

```
╔═══════════════════════════════════════════════════════════════════╗
║                        W O R L D F O R G E                        ║
║              Procedural ASCII World Generator · v1.0              ║
╚═══════════════════════════════════════════════════════════════════╝
```

> **Grow infinite worlds from a single integer.** WorldForge procedurally generates
> full-featured ASCII maps — fractal terrain, biome ecology, river systems, and
> civilisation placement — entirely from mathematical noise. Every seed produces
> a unique, geographically plausible planet.

---

## Features

- **Fractal terrain** via Diamond-Square midpoint displacement
- **Dual-layer moisture** blending fractal noise with coastal-humidity diffusion
- **Whittaker biome classification** — 14 distinct biomes from tundra to jungle
- **Hydrological rivers** that follow steepest-descent gradients from mountains to sea
- **City placement** scored by habitability and river proximity
- **ANSI colour rendering** in terminal; clean plain-text export for files
- **Fully deterministic** — same seed always produces the same world
- **Four map sizes**: 33×33 · 65×65 · 129×129 · 257×257
- Zero external dependencies (pure Python stdlib)

---

## Quick Start

```bash
# Clone and run — no install required
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Default world (seed 42, 65×65, coloured output)
python generate.py

# Custom seed
python generate.py --seed 1337

# Larger world with legend and biome stats
python generate.py --size 129 --legend --stats

# Save to file (plain text, no ANSI)
python generate.py --seed 42 --output my_world.txt

# See all options
python generate.py --help
```

---

## Example Worlds

### Seed 42 · 65×65

```
""""",,.~~...,,.",..,,,,,,,∙∙∙∙;··;∙∙∙∙∙∙∙∙∙;∙∙∙∙∙∙∙∙..~~~~~~~~~~
"""""...~~..,,.".".,,,,,,,,∙∙∙∙;;;∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙,~~~~~~~~~~~
""""".~~~~,,,,,,"..,.,,,,,,∙∙∙∙∙;∙∙∙∙∙.∙∙∙∙∙∙∙∙∙∙∙∙∙..~~~~~~~~~~~
""""""..~~.,,,,....,.,.,..,,∙∙∙∙∙∙∙∙∙..∙.∙∙∙∙∙∙∙∙∙∙,.~~~~~~~~~~~~
"""""",.~...,,,.~.,,,,....,∙∙,,∙∙∙∙,,....∙,∙∙∙∙∙,,,,,~~~~~~~~~~~~
"""""","",,,,.,.~~.,,,,.~~..,,,.,,∙...~..,,,,,,.,,,,.~~~~~~~~~~~~
""""""""""""""".~~,,,,,,~~~~...~.,~..~...,,,,,,.,,,..~~~~~~~~~~~~
"""""""""""""""~~~.,,,,.~~~.~~..~~~~~~~~.~..,,..,.~~~~~.~~.~~~~~~
"""""""""""""".~~~.,,,,~~~~~~~..~~~~~~~~~~~~..~.,~~~~..,,,.~~~~~~
""""""""""""".~~~~.,,,,...,~~...~.~~~~~~~~~~~~~~.~~~~...,,,~~~~~~
"♣♣"""""""""""~.~.,.....~,,.~,,~~..~~~~~~~~~~~~~~~~~.,,.,,,.~~~~~
♣♣♣"""""""""".~.~............,..,,,~~~~~~~~~~~~~~~~~....,.,,.~~~~
♦♣♣""""""""".."....,...",..~,,~,,,,~~~~~~~~~~~~~~~~~~.....~.,~~~~
♦♣♣♣""""""""""""."".≈.,,,,,...,,...~~~~~~~~~~~~~~~~~~~..~...~~~~~
♦♣♦♣"""♣♣""""""""""≈"..,,..,.,...".~~~~~~~~~~~~~~~~~~~.,,~.~..~~~
♦♦♦♣♣""""""""""""""≈",,,.≈..,.....~~~~~~~~~~~~~~~~~~~~..,.~..~~~~
···♦♣♣♣♣♣""★♣""""≈≈",,..≈..,,,~~~~~~~~~~~~~~~~~~~~~~~~~..~~~~~~~~
♦♦♦♦♦♦♣♣♣♣"♣♣♣♣♣≈""★,,,≈,,,,,,.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
▲·♦♦·♦♦♦♣♣♣♣♦♦♦≈♣♣≈",,,≈,,,,,,,...~~~~~~~~~~~~~~~~~~~~~~~~~~~~~≈≈
▲▲··▲♦♦♦♦♦♦♦♦♦≈♣♣≈♣""""≈,,,,..,~.≈~.~~~~~~~~~~~~~~~~~~~~~~~~~~≈≈≈
▲▲▲▲▲▲▲♦♦·▲▲▲≈♦♦♣≈♣♦♣""≈,,,,.~..≈~~,.~~~~~~~~~~~~~~~~~~~~~~~≈≈~≈~
▲▲▲▲▲▲▲♦♦♦····♦♦♦≈♦♦♦"≈",,,,,★..≈..,,,~~~~~~~~~~~~~~~~~~~≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲♦▲▲▲▲··▲≈≈·♦·≈""",,,,"""≈.,,,..~~..~~~~~~~~~~~~≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲♦♦▲▲▲≈≈▲▲▲♦♦♦♦""",,,≈",,,,,..~...~~~~~~~~~~~~≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲·♦▲▲▲▲▲≈▲▲▲▲♦·♦""""≈"≈",,",,,......~~~~~~~~≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲♦♦""≈"""≈",,,,,,.,..~~~~~~~~~≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲♦"≈""""≈,,",,,,...~~~~≈~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲♦♦≈"""""≈,,,,,,"".~~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲♦▲≈♦♦"""≈",,,,,""""~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲♦♦"≈"",,,",""".~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲·≈"""",""""""~~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲·♦≈♦♣""",""""".~~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲≈·♦♦"★"""""..~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲≈·♦♦♦♣"""""".~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲·♦♦♣""♣"""""~~~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲♦▲·♦♦"♣♣♣""""~~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲♦▲▲♦♦♦♦"♦♦♣"""".~~~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲·♦♦♦♦♦♦♦♦♦"""""".~~~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲≈▲▲♦♦♦♦♦♦♦♦"""""""".~~~~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲≈·♦"♦"♦♦♦""""""""""~~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲·≈·"·""♦♦""""",,"".~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲♦·≈"""""""""",,,""~~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲···"≈""""""""",,,,.~~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲·♦♦♦"""≈""""",,,,,,"..~~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲♦♦♦♦♦♦"""≈",,,,,,,,,,..~~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲·♦♦""""",≈",,,,,,,,,,,".~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲♦♦"",""",★,,,,,,,,,,.,.~~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲▲▲▲▲▲♦·♦""","",,,≈,,",,,,,,,,"~~~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲♦▲▲♦·♦♦""",,,,",,,,≈,""",",,,".~~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲▲▲▲▲▲♦·≈·♦""",,,,,,,,,,,,"",""",,,"~~~~≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
▲▲▲▲≈·♦♦♦···≈"""",,,,,,,",,","",,",,★≈≈≈~~~~≈≈≈≈~≈≈~~~~~~~~~~~≈≈≈
▲▲▲▲▲≈··""""≈"",,,,,,,,,,,"""""""",≈,,,..~~~~~~~~~~~~~~~~~~~~~≈≈≈
▲▲▲▲▲♦≈"≈",,≈"",,,,,,,,,,,",""♦·""≈,,,,,"~~~~~~~~~~~~~~~~~~~~~≈~≈
▲▲▲▲▲♦·≈"≈,★≈,,,,,,,,,,,,,,,""""≈≈"",,,,.~~~~~~~~~~~~~~~~~~~~~~~~
▲▲▲♦♦♦♦"",≈,≈,,,,,,,",,,,,"""","""",,,,,~~~~~~~~~~~~~~~~~~~~~~~~~
▲▲·▲♦♦♦",,,,≈,,,,,,,,,,,,,""""""",,,,,,,.~~~~~~~~~~~~~~~~~~~~~~~~
▲·♦♦▲♦♦"",,,,,,,,,,,,,,,",,"""",,,,,,,,,,~~~~~~~~~.~,.~~~~~~~~~~.
♦♦♦♦♦♦♦""",,,,,,,,.,,,,,,,,,,"""",,,,,,.,,~~~~~~~.,,,,,.~~~~~~~~~
♦♦♦"""""""",,,,,,,~.~..,,,,,,,""",,,,,,,.,.~~~~~.,,,,,,,..~~~~~~~
≈"""""""""",,,,,~..~~."..,,,,,,,,",,,,,,...~~....,,,,,,,,..~~~~~~
"≈",","""",,,,..~~~~~~~.~.,,,,,,.,",,,,,","".,,,.,,,,,,,,,,..~~~,
★,≈,,,,,,,,,,,~~~~~~~~~~~.,,,,..~"",,,,,,,,,,,,,,,,,,,,,,.~.~.~.,
,,≈,,,,,,,,,,,.~~~~~~~~~~.,,"..~~.,,",",,...,,,,,,,,,,,.,,~..~.∙∙
,,,≈,,,,,,,,,,.~~~~~~~~~~~~."".~~","","",,,,,,,,,,,,,,,,,,,....~∙
,.≈.,,,,,,,,,.~~~~~~~~~.~~~.,,.~".""",,"..,,,,,,,,,,,,,,,,,...~~.
```

*Savanna + Grassland plains (top-left), Boreal/Temperate Forest belt (centre), massive Mountain range (bottom-left), sprawling Ocean (right). Cities ★ sit along river ≈ corridors.*

---

### Seed 99 · 33×33 (compact)

```
~.".~~~≈≈≈≈~~~~≈≈≈≈~""""""~~.~~≈≈
~~.~~~~≈≈≈≈~~~≈≈≈≈≈~.~~"""~~~~≈≈≈
≈~~~~≈≈≈≈~~~~~≈≈≈≈≈≈~~~""""~≈≈≈≈≈
≈~~~~≈≈≈≈~~~~≈≈≈≈≈≈~~~♠""".~≈≈≈≈≈
≈≈~~~~≈~≈≈~~~≈≈≈≈≈≈≈≈~."♠~.~≈≈≈≈≈
≈~~≈~~~~~~.~≈~~≈~~~≈~~.""~~~~≈≈≈≈
≈≈≈~≈~~"~"""~~~~~~≈~≈~~~~≈≈≈~≈~~♠
≈~~≈~~~,,,,~~~~~~~~~~≈~~~~~~≈~~""
~~~~~,,"▲,,~~~""~~~~~~~"~~≈≈≈~~.♣
~~~~~,,,",,,.,".~~.~~~""".~~~~~~"
≈~~~~",,,,,""",,,.~~..""♦"".~~~,~
≈≈≈≈≈~,.,,,"·",.,,.,,"♣♣♦"""""★.≈
≈~≈≈≈~~,""""▲",,,,",,"▲"▲♦""""",≈
~≈~~≈≈~~.""",,,,,,;",""♦""♦,""♦"≈
~~~~≈~~≈≈~~~.;·"∙,";;·"▲,"♦"""♦♦≈
≈~≈≈≈≈≈≈≈~...,·;,";▲··;▲▲"▲▲▲▲"≈·
≈~≈≈≈~~≈≈≈~"≈≈,,··▲▲·"▲·▲·▲♦▲··▲≈
~≈≈≈~≈~≈~~~".,≈,≈≈·▲··▲▲▲·▲▲▲▲▲▲≈
~≈≈~≈~~≈≈~"".,★≈≈≈▲▲▲▲▲·"▲▲▲▲▲▲▲▲
~~~~~.~~~""~~"""·≈▲▲▲▲·",·▲·▲▲▲▲▲
~~~.,""."~~~""""▲▲·≈≈▲·","····▲▲▲
∙.,,,★,,".~""♣♣""▲≈▲▲▲·"♦·▲·▲▲▲▲▲
∙∙,,,,","~~"""♦""≈""▲··"·≈·▲▲▲▲▲▲
∙~~,,"".~".""♣""≈,""·▲·▲≈·;··▲▲▲▲
∙∙~,,~""~~""""..≈.""""·≈"·▲;·▲▲▲▲
~~~,"~~~~~"""""~..,,"★,≈∙▲▲▲▲·▲▲▲
~.~~~~~~≈~"""""".~~~~,,≈∙·▲▲;;·;·
~~~~~~~≈≈~~.""..~~~~~~≈∙∙;▲····;∙
≈≈~≈≈~~≈≈~~♠♣.~~~~.,~,~~∙;▲▲▲·∙∙∙
≈~≈≈~≈~~~~~~~"~.~~.~~,.∙,;"▲▲·∙∙∙
≈≈≈≈~~~~..".~.~~"~,,",,∙·;··▲▲",~
≈≈≈≈≈≈≈~~."~...~.,,,;,",▲·▲▲▲▲;,~
≈≈≈≈≈≈≈≈~~.~"~~"",.,;"▲··▲▲▲▲·;.~
```

*Compact island world with an ocean-dominated northern hemisphere. Desert ∙ coastlines, Tropical Forest ♠ coves, and a rugged mountain interior.*

---

## Biome Reference

| Symbol | Biome | Conditions |
|--------|-------|-----------|
| `≈` (deep blue) | **Deep Ocean** | Below 65% of sea level |
| `~` (blue) | **Ocean** | Below sea level |
| `~` (cyan) | **Coast** | Just below sea level |
| `.` (yellow) | **Beach** | Just above sea level |
| `∙` (dark yellow) | **Desert** | Hot zone, low moisture |
| `,` (green) | **Savanna** | Hot zone, moderate moisture |
| `"` (bright green) | **Grassland** | Temperate, moderate moisture |
| `;` (green) | **Shrubland** | Temperate, low moisture |
| `♣` (green) | **Temperate Forest** | Temperate, high moisture |
| `♠` (bright green) | **Tropical Forest** | Hot zone, high moisture |
| `♦` (cyan) | **Boreal Forest** | Cool zone, moderate+ moisture |
| `·` (white) | **Tundra** | Cold zone |
| `*` (bright white) | **Snow** | High altitude |
| `▲` (dark gray) | **Mountain** | High elevation |
| `▲` (bright white) | **Peak** | Highest elevation |
| `≈` (bright cyan) | **River** | Flowing downhill to sea |
| `★` (yellow) | **City** | Habitable land near rivers |

---

## How It Works

### 1 · Diamond-Square Terrain

WorldForge builds its heightmap using the **Diamond-Square midpoint displacement** algorithm — a fractal technique that produces natural-looking terrain in O(n²) time.

```
Initialise corners              Diamond step
┌───────────┐                   ┌───────────┐
│A         B│                   │A    d    B│
│           │                   │           │
│     ?     │    ──────────►    │     X     │
│           │                   │           │
│C         D│                   │C    e    D│
└───────────┘                   └───────────┘
                                 X = avg(A,B,C,D) + noise

Square step (edge midpoints)    Recurse with halved step
┌───────────┐                   ┌───────────┐
│A    d    B│                   │A  f  d  g B│
│           │                   │           │
│h    X    i│    ──────────►    │j  X  k  X m│
│           │                   │           │
│C    e    D│                   │C  n  e  p D│
└───────────┘                   └───────────┘
 h,i = avg(adjacent diamonds)    Repeat until 1×1 cells
```

The `roughness` parameter controls how quickly the random displacement decays — lower values produce smoother, rounder landscapes; higher values give jagged, cratered terrain.

### 2 · Moisture Simulation

Moisture combines two sources:

```
Base moisture        Ocean diffusion      Blended result
(Diamond-Square)  +  (iterated blur)  ──► 55% noise + 45% coast
                                           ──► normalise [0, 1]
```

A secondary Diamond-Square pass provides global moisture variation (trade-wind analogue). A separate ocean-proximity layer is computed by flood-blurring a binary "is-ocean" mask outward for 10 iterations, then blended in — coastal regions become reliably humid, inland areas depend on the noise pass.

### 3 · Whittaker Biome Classification

Each land cell is classified using a simplified **Whittaker biome diagram**, mapping temperature (derived from elevation) and moisture to one of 14 biome types.

```
         LOW MOISTURE ◄──────────────────► HIGH MOISTURE
  HOT  │  Desert   │  Savanna  │  Grassland │  Tropical Forest  │
       │           │           │            │                    │
WARM   │ Shrubland │  Grassland│  Temp.     │  Temperate Forest  │
       │           │           │  Forest    │                    │
 COOL  │  Tundra   │  Boreal   │  Boreal    │  Boreal Forest     │
       │           │  (sparse) │  Forest    │                    │
 COLD  │  Tundra   │  Tundra   │  Snow/Ice  │  Snow/Ice          │
```

Elevation overrides temperature: above a mountain threshold cells become `MOUNTAIN`; above a peak threshold they become `PEAK`.

### 4 · River Hydrology

Rivers originate at randomly selected mid-to-high elevation tiles and flow downhill by **greedy steepest descent** across 8-connected neighbours until reaching sea level.

```
  Source ●                        Paths that reach the sea
    │  (elevation 0.75)           in ≥ 6 steps are kept
    ▼
    ●  ← pick lowest neighbour    Rivers carve through
    │    at each step             forests, plains, and
    ▼                             mountain foothills,
    ●  ←──────────────────────    creating natural
    │                             corridors
    ▼
  ~~~  (sea level)
```

### 5 · City Placement

City sites are scored by:
- Being in habitable elevation (not ocean, not peak)
- Random variation to prevent uniform grids
- **+0.55 bonus** for tiles within 3 cells of a river

Candidates are placed in score order, rejecting any that fall within `min_dist` tiles of an already-placed city.

---

## Project Structure

```
clauder/
├── worldforge/
│   ├── __init__.py          Package exports
│   ├── terrain.py           HeightMap — Diamond-Square algorithm
│   ├── moisture.py          MoistureMap — noise + coastal-diffusion blend
│   ├── biomes.py            Biome definitions + Whittaker classification
│   ├── rivers.py            RiverSystem — steepest-descent hydrology
│   ├── cities.py            CitySystem — scored placement near rivers
│   └── renderer.py          ANSI terminal rendering + plain-text export
├── generate.py              CLI entry point
├── demo.py                  Generates example maps (used in this README)
├── examples/
│   ├── world_42.txt         Seed 42, 65×65
│   ├── world_1337.txt       Seed 1337, 65×65
│   ├── world_ocean.txt      Seed 7, 65×65
│   └── world_small.txt      Seed 99, 33×33
└── README.md
```

---

## CLI Reference

```
python generate.py [OPTIONS]

Options:
  --seed INT        World generation seed               [default: 42]
  --size {33,65,129,257}
                    Map edge length (2^k + 1)           [default: 65]
  --rivers INT      Target number of rivers             [default: 12]
  --cities INT      Target number of cities             [default: 8]
  --no-color        Disable ANSI colour output
  --output FILE     Save plain-text map to file
  --legend          Print biome legend after map
  --stats           Print biome coverage percentages
  -h, --help        Show this help message
```

---

## Extending WorldForge

The modular design makes it easy to swap or extend individual systems:

| Module | Swap idea |
|--------|-----------|
| `terrain.py` | Replace Diamond-Square with OpenSimplex/Perlin noise |
| `moisture.py` | Add wind direction / rain-shadow simulation |
| `biomes.py` | Add seasons, soil types, or altitude zones |
| `rivers.py` | Add lakes at local minima; river merging |
| `cities.py` | Add trade-route networks between cities |
| `renderer.py` | Output SVG, PNG, or HTML colour maps |

---

## Requirements

Python 3.11+ · no third-party packages required.

---

## License

MIT — do whatever you like with it. If you generate a world you love, share the seed.
