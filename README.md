# Attractor

> **Strange Attractor Art Engine** — generate breathtaking imagery from the mathematics of chaos.

```
  ___  _   _  _____  ____    _    ____  _____ ___  ____
 / _ \| | | ||_   _||  _ \  / \  / ___||_   _/ _ \|  _ \
| | | | | | |  | |  | |_) |/ _ \| |      | || | | | |_) |
| |_| | |_| |  | |  |  _ </ ___ \ |___   | || |_| |  _ <
 \___/ \___/   |_|  |_| \_/_/   \_\____|  |_| \___/|_| \_\
```

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![NumPy](https://img.shields.io/badge/NumPy-1.24%2B-orange?logo=numpy)](https://numpy.org)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-blue)](https://matplotlib.org)

---

## What is a Strange Attractor?

A **strange attractor** is a structure in the phase space of a chaotic dynamical system. Feed a set of simple equations a starting point, iterate them millions of times, and the trajectory never repeats — yet it never escapes a bounded region. The result is a shape of infinite complexity: the fingerprint of deterministic chaos.

```
          ┌─────────────────────────────────────────────────────────────┐
          │   Simple rules  →  Infinite complexity  →  Stunning art     │
          │                                                             │
          │   xₙ₊₁ = sin(a·yₙ) + c·cos(a·xₙ)          ╭──────────╮   │
          │   yₙ₊₁ = sin(b·xₙ) + d·cos(b·yₙ)   ──▶    │ 3M iters │   │
          │                                             ╰──────────╯   │
          │                                                  ↓         │
          │                                           [gorgeous art]   │
          └─────────────────────────────────────────────────────────────┘
```

---

## Gallery

### Clifford Attractor — plasma theme

```
                                      +===x=;;;;;+======x=
                   =XXX$$$$$$$X$XXXXXXxxx==+++:;:;;;:::;;xX$&x
         X$$$$$&&&&&$$$$XXXXXXXXXX$$$$$$$$XXxX=======x=xxxXxXXX$&=
     X&##&&&&&&$$XXXXXXXXXXXXXXX$$$$$$$$$$$$$XXXXXXXXxxxx;++;==X$;
  x$$$XX$$$$X$XXXXXXxxxxxx=XXXXXXXXxXXXXX$$X$xxxxXXX$XXXXxxXXX=
 x&$XXXXXxxx=xXXXXXXXxxxxxx$X$XXXxxxxxxxxxxX$XXxxxxxXXXX$$&$Xx+.
  ;xXXXXXXXXXXXxxxxXXXXXXxX$$XXxxxXXxXxxXxXX$$xXXXXXX$&&&&$&&&$$X==:
  XX=====xxx===xXXXXXXX$$$X$X$XXXXxXXXXXXXXX$$XX$$&&&&$$$XXX$$$$&&$XXX=
 =&XXx=x$$Xxx==x========xX$$&&$$XXXXXXXXX$$&$$&&$$x              =$$XXX$X:
                       ;++++X$&$$$$$$$$$$&&&$$x+                   x$XXXX$X
                            :=$&$XxXX$$$$&$x+:                      x$XXxX$$
                               $#XXXXX$$$=+:                        xxXXXxxX$
                                &#$$$$$x+;                         x+:XXXxxx$x
         x$                     $#&X+                          xxx++=X=xXxxxX&
        xXXXXx=.            .=x&&$&=         $$Xxxx====++;;+XXXXxx==xx==XXXXX$
        X=;++====XX$Xxxx==xX$$$$X$$.       :xxXxxx=++;++++++++++++xXx=xxxXxX&=
   XXXxxXx==++:;;+=xXXXXXX$X$XXXX$X           xX$XxxXx==+=++====xx++==xXxXX$$
   x$XxxxXXxxxxxxxxxxxxxXXXXxXXx$$.             +XXx==xxxxx====+++=+=xxxxX&$
    x$X=x=xXxxxxx=xxxXXXXXXXXxX&$                  xXX===xxxx=====xxXxXX$&X
      x$&$XXXXXXXXXXXXXXXXXX$&$x                     =$$$XxxxxXXXXXX$$$&$+
        X##&&$$$$$$$$$$$$$&$X+                         :$&&&$$XXX$$$$$X.
            x$$$$$$$XXXXX=                                 X$$$$$$Xx
```

### Lorenz Attractor — galaxy theme

```
                                                                    .. ......
  .:.....                                                      . .:: :;;::  .:
 :.++==xx==;;:.                                           . ..;:+===x=x==;;  .
 ::+=xxxXXXXXxxx+;:.                                   . ;:==xxXXXXXXxxx=+;  :
 ..=xxX$$$$$$$$$$Xxx=;;.                           ..:+==xXX$$$$$$$$$$x==+; .
  :+=xX$$$&&&&&&&&&&$$XXx+;.                 .. :;+=xX$$$&$&&&&&$$$$X$x==;. .
   .+=xX$$$&&&&&&&&&&&&&$$Xxx=;:        .. :;+=xxX$$&&&&&&$$$$$$&$$$$X==+...
   .:;xxX$$$&&$$$$$$$&&&&&&&$$Xxx=;;::.::+=xxX$$&&&&&$$Xx===xX$$$$$$X==::.
     :+=xX$$$&&$$$&#&&&$&&&&&&&$$$XXxx=xxXX$$&&&&&$$x=;    =x$$&$$XX==;:.
      .+=xX$$$$&$$$&$xX#&$&&&&&&&&&&$$$$$&&&&&&&$Xx;     :=X$$$$$Xxx+; .
        :+xx$$$$&&$$$&&&&$X&&&##&##&&&&##&&&&&$$xx    :+xX$$$$$$Xx=+: .
         .;=xX$$$$&&&&$$$$&&&&&##&###########&&$XXxxxXXX$$&$$$Xx==; ..
           :;xxX$$$$&&&&&&&&&&####&##########&&&&$$$$$&&$$$$Xxx=+: .
            .:+=xXX$$$$&&&&&&&&########&@####&&&&&&&&&$$$$Xx==+:. .
              .:+=xxX$$$&&&&&&&&&######&&#&#&&&&&&&$$$$Xxx==+: .
                 :;+xxxXX$$$$&&&&&&&#&&&&&&&&&&&&$$$Xxx==+;: ..
                  ...;+=xxXX$$$$$$&&$$&&&$$XXXXXXxxxx=+;::...
                      .::++==xxxxXXXXxXXXXXXXXXxx=++:; ...
                          .:::;;++;+== xx===++;;;: ....
```

---

## Features

- **8 Famous Attractors** — discrete iterated maps (Clifford, De Jong, Tinkerbell, Svensson) and continuous ODE flows (Lorenz, Aizawa, Halvorsen, Thomas)
- **10 Color Themes** — plasma, inferno, galaxy, ember, forest, ocean, aurora, gold, neon, twilight
- **High-resolution PNG export** — render up to 4K and beyond
- **ASCII art preview** — ANSI 256-color terminal output for quick inspection
- **Log-density coloring** — dim regions remain visible while bright clusters stay vivid
- **Gamma correction** — tune brightness with a single parameter
- **RK4 integration** — continuous attractors solved with 4th-order Runge-Kutta for accuracy

---

## Architecture

```
attractor/
│
├── __init__.py          Package entry point & version
│
├── attractors.py        Mathematical definitions
│   ├── AttractorDef     Dataclass: name, equations, params, compute fn
│   ├── _clifford()      Discrete: Clifford Pickover map
│   ├── _dejong()        Discrete: Peter de Jong map
│   ├── _tinkerbell()    Discrete: Tinkerbell map
│   ├── _svensson()      Discrete: Johnny Svensson map
│   ├── _lorenz()        Continuous ODE → RK4
│   ├── _aizawa()        Continuous ODE → RK4
│   ├── _halvorsen()     Continuous ODE → RK4
│   ├── _thomas()        Continuous ODE → RK4
│   └── _rk4_integrate() Generic 4th-order Runge-Kutta engine
│
├── renderer.py          Rendering engine
│   ├── _build_density() Point cloud → log-density histogram
│   ├── render_image()   Density → matplotlib → PNG
│   └── render_ascii()   Density → ANSI 256-color terminal art
│
├── themes.py            10 color theme definitions
│   └── THEMES           Dict of (bg_hex, matplotlib_cmap)
│
└── cli.py               Command-line interface
    ├── cmd_list()        List all attractors + themes
    ├── cmd_render()      Render high-res PNG
    ├── cmd_ascii()       Print ASCII preview
    └── cmd_info()        Detailed attractor information
```

### Data Flow

```
  Parameters          Raw Points         Density Grid         Final Image
  ──────────          ──────────         ────────────         ───────────
  {a, b, c, d}  ──▶  (N × 2) f32  ──▶  (H × W) f32   ──▶   (H × W) RGBA
        │              Runge-Kutta        log1p + norm         cmap + gamma
        │              or iteration
        ▼
  AttractorDef
```

---

## Attractor Catalogue

| Name | Type | Equations | Params |
|---|---|---|---|
| **Clifford** | Discrete | xₙ₊₁ = sin(a·yₙ) + c·cos(a·xₙ) | a, b, c, d |
| **De Jong** | Discrete | xₙ₊₁ = sin(a·yₙ) − cos(b·xₙ) | a, b, c, d |
| **Tinkerbell** | Discrete | xₙ₊₁ = x²−y² + a·x + b·y | a, b, c, d |
| **Svensson** | Discrete | xₙ₊₁ = d·sin(ax) − sin(by) | a, b, c, d |
| **Lorenz** | Continuous | dx/dt = σ(y−x) | σ, ρ, β |
| **Aizawa** | Continuous | dx/dt = (z−b)x − dy | a, b, c, d, e, f |
| **Halvorsen** | Continuous | dx/dt = −a·x − 4y − 4z − y² | a |
| **Thomas** | Continuous | dx/dt = sin(y) − b·x | b |

---

## Installation

**Requirements:** Python 3.10+, NumPy, Matplotlib

```bash
git clone https://github.com/kareemrt/clauder.git
cd clauder
pip install -r requirements.txt
pip install -e .
```

---

## Usage

### Render a high-resolution image

```bash
# Clifford attractor, plasma color theme, 1920×1080
attractor render clifford --theme plasma --output clifford.png

# Lorenz butterfly, galaxy theme, 4K resolution
attractor render lorenz --theme galaxy --width 3840 --height 2160 --output lorenz_4k.png

# De Jong with custom iteration count and gamma
attractor render dejong --theme ember --iterations 5000000 --gamma 0.4
```

### ASCII terminal preview

```bash
# Quick preview in the terminal (ANSI colored)
attractor ascii clifford --theme plasma

# Plain ASCII without color
attractor ascii lorenz --nocolor --width 100 --height 30
```

### Discover attractors

```bash
# List all attractors and themes
attractor list

# Detailed info about one attractor
attractor info halvorsen
```

### All options

```
attractor render ATTRACTOR [options]
  --theme   -t   Color theme          [plasma]
  --output  -o   Output file path     [attractor_theme.png]
  --width   -W   Image width px       [1920]
  --height  -H   Image height px      [1080]
  --iterations -n  Point count        [attractor default]
  --gamma   -g   Gamma correction     [0.5]

attractor ascii ATTRACTOR [options]
  --theme   -t   ANSI color theme     [plasma]
  --width   -W   Terminal columns     [110]
  --height  -H   Terminal rows        [36]
  --nocolor      Disable ANSI codes

attractor info  ATTRACTOR    Show math + parameters
attractor list               List everything
```

---

## How It Works

### Discrete Attractors (Iterated Maps)

For a 2D map like Clifford:

```
  Start at (x₀, y₀)
       │
       ▼
  ┌─────────────────────────────────┐
  │  x' = sin(a·y) + c·cos(a·x)    │  ◀── iterate N million times
  │  y' = sin(b·x) + d·cos(b·y)    │
  └─────────────────────────────────┘
       │
       ▼  accumulate all (x,y) points
  Density histogram (log-scaled)
       │
       ▼  apply colormap
  Beautiful image
```

### Continuous Attractors (ODE Systems)

For Lorenz and other ODEs, we use **4th-order Runge-Kutta** (RK4):

```
  k₁ = dt · f(xₙ, yₙ, zₙ)
  k₂ = dt · f(xₙ + k₁/2)
  k₃ = dt · f(xₙ + k₂/2)
  k₄ = dt · f(xₙ + k₃)

  xₙ₊₁ = xₙ + (k₁ + 2k₂ + 2k₃ + k₄) / 6
```

RK4 gives fourth-order accuracy while keeping the attractor's chaotic character intact.

### Density Rendering

Raw points → density grid → log-scale → colormap → PNG

```
  ● ●●●                   0 0 3 0               0.0  0.0  0.8  0.0
  ●  ● ●     bin()        0 1 0 1   log1p()     0.0  0.7  0.0  0.7    cmap()   [image]
  ●●● ●●   ─────────▶     3 0 2 0  ─────────▶  0.8  0.0  0.6  0.0  ─────────▶
   ● ●●●                  1 0 3 0               0.7  0.0  0.8  0.0
```

Log-scaling is the key trick: without it, the densest pixels burn white while sparse regions vanish. With it, every layer of detail is visible simultaneously.

---

## Color Themes

| Theme | Background | Style |
|---|---|---|
| `plasma` | `#0d0221` | Deep purple → yellow |
| `inferno` | `#000000` | Black → orange → white |
| `galaxy` | `#010b1a` | Midnight blue → cyan |
| `ember` | `#0a0200` | Black → deep red → gold |
| `forest` | `#010a01` | Near-black → bright green |
| `ocean` | `#00060f` | Deep navy → electric blue |
| `aurora` | `#020a08` | Dark green → yellow |
| `gold` | `#080400` | Near-black → rich amber |
| `neon` | `#000000` | Magenta → yellow |
| `twilight` | `#08000f` | Twilight purple cycle |

---

## The Mathematics of Chaos

Strange attractors live at the intersection of **order** and **randomness**. Three properties define them:

```
  ┌──────────────────────────────────────────────────────────────┐
  │  1. SENSITIVE DEPENDENCE ON INITIAL CONDITIONS               │
  │     Two nearby starting points diverge exponentially fast.   │
  │     Change x₀ by 0.000001 → completely different trajectory  │
  │                                                              │
  │  2. TOPOLOGICAL MIXING                                       │
  │     Any region of the attractor eventually overlaps          │
  │     any other. No island is ever truly isolated.             │
  │                                                              │
  │  3. DENSE PERIODIC ORBITS                                    │
  │     Embedded within the chaos are infinitely many            │
  │     (unstable) periodic paths — ghosts of order.             │
  └──────────────────────────────────────────────────────────────┘
```

The Lorenz attractor has a **fractal dimension** of approximately 2.06 — it is neither a surface (2D) nor a volume (3D), but something stranger in between.

---

## License

MIT — do whatever you want with it, strange or otherwise.
