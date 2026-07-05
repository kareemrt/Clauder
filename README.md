# CosmicCanvas

```
   ██████╗ ██████╗ ███████╗███╗   ███╗██╗ ██████╗
  ██╔════╝██╔═══██╗██╔════╝████╗ ████║██║██╔════╝
  ██║     ██║   ██║███████╗██╔████╔██║██║██║
  ██║     ██║   ██║╚════██║██║╚██╔╝██║██║██║
  ╚██████╗╚██████╔╝███████║██║ ╚═╝ ██║██║╚██████╗
   ╚═════╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝ ╚═════╝
  ██████╗  █████╗ ███╗   ██╗██╗   ██╗ █████╗ ███████╗
  ██╔════╝██╔══██╗████╗  ██║██║   ██║██╔══██╗██╔════╝
  ██║     ███████║██╔██╗ ██║██║   ██║███████║███████╗
  ██║     ██╔══██║██║╚██╗██║╚██╗ ██╔╝██╔══██║╚════██║
  ╚██████╗██║  ██║██║ ╚████║ ╚████╔╝ ██║  ██║███████║
   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝
```

> **Real-time N-body gravitational simulator — because the universe deserves a terminal.**

A Python terminal application that simulates orbital mechanics using the [Leapfrog integrator](https://en.wikipedia.org/wiki/Leapfrog_integration) — the same symplectic scheme used in professional astrophysics codes. Watch the inner solar system, a circumbinary "Tatooine" system, the famous figure-8 three-body choreography, and explosive gravitational chaos, all rendered live in your terminal with colour-coded orbital trails.

---

## Live Preview

```
┌─ Inner Solar System ───────────────────────────────────────────────────┐┌─ Data ─────────────────────┐
│                                                                         ││  BODIES                    │
│                                                                         ││  ─────────────────         │
│                         ·:·····:·                                       ││  ★ Sun                     │
│                     ·:·         ·:·                                     ││    dist:    0.000 AU        │
│                 ·:·   ·····Mercury·  ·:·                                ││    speed:   0.000 AU/yr     │
│              ·:·  ·····      ·    ····  ·:·                             ││  · Mercury                 │
│           ·:·  ·:·                ·  ·:·  ·:·                          ││    dist:    0.387 AU        │
│        ·:·  ·:·  ·Venus○        ★    ·:·    ·:·                        ││    speed:   8.175 AU/yr     │
│      ·:·  ·:·   ··············       ·  ·:·   ·:·                      ││  ○ Venus                   │
│     :·  ·:·  ·                             ·:·  :·                     ││    dist:    0.723 AU        │
│      ·:·  ·:·    ⊕Earth                          ·:·  ·:·              ││    speed:   5.978 AU/yr     │
│        ·:·  ·:·         ·····Mars○·····      ·:·    ·:·                ││  ⊕ Earth                   │
│           ·:·  ·:·   ···              ···    ·:·  ·:·                  ││    dist:    1.000 AU        │
│              ·:·  ·····                    ·····  ·:·                  ││    speed:   6.283 AU/yr     │
│                 ·:·                               ·:·                  ││  ○ Mars                    │
│                     ·:······················:·                         ││    dist:    1.524 AU        │
│                                                                         ││    speed:   5.091 AU/yr     │
│                                                                         ││  ◉ Jupiter                 │
│                                                             ◉ Jupiter  ││    dist:    5.203 AU        │
│                                                                         ││    speed:   2.756 AU/yr     │
│                                                                         ││                            │
│                                                                         ││  SIMULATION                │
│                                                                         ││  ─────────────────         │
│                                                                         ││  Time:     1.250 yr        │
│                                                                         ││           (1y  91.3d)      │
│                                                                         ││  dt:    0.00100 yr         │
│                                                                         ││  subs:        20×          │
│                                                                         ││  ΔE:    0.00003%           │
└─────────────────────────────────────────────────────────────────────────┘└────────────────────────────┘
```

---

## Features

| Feature | Detail |
|---------|--------|
| **Symplectic physics** | Leapfrog (Störmer-Verlet) integration conserves a modified energy exactly — no secular drift |
| **Gravitational softening** | Prevents singularity at close approach, enabling stable long-term simulations |
| **Orbital trails** | Colour-coded fading trails visualise the history of each body's path |
| **4 presets** | Solar system, binary stars, figure-8 choreography, and chaotic cluster |
| **Live energy monitor** | Real-time ΔE display (green < 0.01% → red > 0.5%) validates integration accuracy |
| **Configurable** | Adjust time step, substeps, viewport scale, FPS, and simulated duration |

---

## Presets

### `solar` — Inner Solar System + Jupiter
Six bodies with NASA-accurate masses and Keplerian initial velocities.
Mercury completes an orbit in ~0.24 simulated years; Jupiter in ~11.9.

```
Scale: ±6 AU  |  dt: 0.001 yr  |  Substeps: 20  |  Bodies: 6
```

### `binary` — Binary Star + Tatooine
Two equal half-solar-mass stars orbiting their common centre at ±0.5 AU.
A circumbinary planet at 3 AU experiences a rhythmic double sunrise.

```
Scale: ±4.5 AU  |  dt: 0.001 yr  |  Substeps: 20  |  Bodies: 3
```

### `figure8` — Choreographic Three-Body Orbit
The famous Chenciner-Montgomery solution (2000): three equal masses trace
a single figure-8 path with period ≈10 years — a fragile, mathematically
exquisite choreography.

```
Scale: ±1.8 AU  |  dt: 0.0005 yr  |  Substeps: 10  |  Bodies: 3

          ●━━━━━━━━━━━━━━━━━━━━━●
         ╱         γ             ╲
        ╱   α ●         ● β       ╲
       ╱                           ╲
      β ●       all three bodies    ● α
       ╲        share one orbit    ╱
        ╲                         ╱
         ╲         γ             ╱
          ●━━━━━━━━━━━━━━━━━━━━━●
```

### `chaos` — Seven-Body Gravitational Chaos
Seven bodies equally spaced on a ring with slightly super-circular velocities.
The configuration is unstable: close encounters, gravitational slingshots,
temporary captures, and eventual ejections emerge within a few simulated years.

```
Scale: ±4 AU  |  dt: 0.0005 yr  |  Substeps: 10  |  Bodies: 7

           ● ——— ●
          / ╲   ╱ \
         /   ╲ ╱   \       → close encounter at t≈1.3 yr
        ●   ● ● ●   ●      → first ejection at t≈2.8 yr
         \       /         → chaotic scattering ongoing
          \     /
           ● ——— ●
```

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Install dependencies (Python >= 3.9 required)
pip install -r requirements.txt

# Run the default preset (inner solar system)
python main.py

# Try other presets
python main.py binary
python main.py figure8
python main.py chaos
```

---

## Usage

```
usage: main.py [preset] [options]

positional arguments:
  preset         Scene preset: solar | binary | figure8 | chaos

options:
  --dt FLOAT     Time step in years              (default: preset-dependent)
  --speed INT    Physics substeps per frame      (default: preset-dependent)
  --scale FLOAT  Viewport half-width in AU       (default: preset-dependent)
  --fps FLOAT    Target display frames/sec       (default: 24)
  --years FLOAT  Stop after N simulated years    (default: run forever)
```

### Examples

```bash
# Slow down Mercury with a finer time step
python main.py solar --dt 0.0002

# Watch 10 years of the figure-8 (one complete choreography)
python main.py figure8 --years 10

# Zoom out to see the full solar system
python main.py solar --scale 12

# Run chaos at lower FPS for smoother recording
python main.py chaos --fps 10 --years 5
```

---

## Physics

### Units

CosmicCanvas uses **Gaussian gravitational units** throughout:

| Quantity | Unit | SI Equivalent |
|----------|------|---------------|
| Length   | AU (astronomical unit) | 1.496 × 10¹¹ m |
| Time     | Year                   | 3.156 × 10⁷ s  |
| Mass     | Solar mass (M☉)         | 1.989 × 10³⁰ kg |
| **G**    | AU³ yr⁻² M☉⁻¹           | **4π² ≈ 39.478** |

The value G = 4π² follows exactly from Kepler's third law (a³/T² = 1 for Earth).

### Leapfrog Integration

The leapfrog (Störmer-Verlet) scheme is **symplectic** — it exactly conserves a
modified Hamiltonian, so energy errors oscillate rather than accumulate:

```
┌──────────────────────────────────────────────────────────────────┐
│  1. Kick  ½dt:  v_{n+½} = v_n   + ½ · a(x_n)     · dt          │
│  2. Drift  dt:  x_{n+1} = x_n   + v_{n+½}         · dt          │
│  3. Kick  ½dt:  v_{n+1} = v_{n+½} + ½ · a(x_{n+1}) · dt        │
└──────────────────────────────────────────────────────────────────┘
```

This gives **second-order accuracy** with minimal memory overhead —
ideal for many-orbit simulations where energy conservation matters.

Compare integrator quality over 100 orbits:

```
  Energy error (|ΔE/E₀|)
  1e-0 ─────────────────────────────────────────
  1e-2 ┄┄┄┄┄┄┄┄┄┄┄┄╱ Euler (diverges)
  1e-4 ┄┄┄┄┄┄┄┄┄┄┄┄
  1e-6 ───────────────── Leapfrog (oscillates)  ← CosmicCanvas
  1e-8 ─────────────────────────────────────────
        0    20    40    60    80   100  orbits
```

### Gravitational Softening

To prevent force divergence at close approach, the pairwise distance is
replaced by a softened distance:

```
r_soft = √(r² + ε²)    where ε = 0.005 AU  (~750 000 km)
```

---

## Project Architecture

```
clauder/
│
├── main.py                     Entry point — argument parsing, simulation loop
│
├── cosmic_canvas/
│   ├── __init__.py
│   │
│   ├── bodies.py               CelestialBody dataclass
│   │                           Fields: name, mass, x, y, vx, vy, color, symbol, trail
│   │                           Properties: speed, distance
│   │
│   ├── physics.py              Leapfrog integrator + energy diagnostic
│   │                           G = 4π² AU³ yr⁻² M☉⁻¹
│   │                           Softening ε = 0.005 AU
│   │
│   ├── renderer.py             Rich terminal renderer
│   │                           • _world_to_screen() — AU → (col, row), aspect-corrected
│   │                           • _build_canvas()    — rasterises trails + bodies
│   │                           • _build_info()      — live stats panel
│   │                           • Renderer.render()  — returns Rich Layout
│   │
│   └── presets.py              Scene factories
│                               • solar_system()     — 6 bodies, NASA masses
│                               • binary_star()      — 3 bodies, Tatooine
│                               • figure_eight()     — 3 bodies, choreography
│                               • chaotic_cluster()  — 7 bodies, unstable ring
│
└── requirements.txt            rich >= 13.0.0
```

### Data Flow per Frame

```
  ┌──────────┐        ┌──────────────┐       ┌──────────────┐     ┌───────────┐
  │  bodies  │──N×──▶│ physics.step │──────▶│   renderer   │────▶│ Rich Live │
  │ (state)  │        │  (leapfrog)  │       │  .render()   │     │  display  │
  └──────────┘        └──────────────┘       └──────────────┘     └───────────┘
       ▲                     │                      │
       │                     ▼                      ▼
       │               update x,y,vx,vy      Layout(canvas│info)
       └────────── record_position() ◀──────── Rich Panel + Text
                  (append to trail)
```

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `rich`  | ≥ 13.0  | Terminal colour, panels, live display |

Everything else uses the Python standard library (`math`, `dataclasses`,
`argparse`, `signal`, `time`, `shutil`).

---

## Acknowledgements

- **Chenciner & Montgomery (2000)** — *A remarkable periodic solution of the three-body problem in the case of equal masses*, Annals of Mathematics 152(3)
- **Moore (1993)** — independent discovery of the figure-8 choreography
- **Wisdom & Holman (1991)** — symplectic integrators for solar system dynamics
- NASA Planetary Fact Sheets for planetary masses and orbital parameters

---

*Built with curiosity, caffeine, and an unhealthy love of orbital mechanics.*
