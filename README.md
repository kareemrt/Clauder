# Cosmosim

```
   ___  ___  ____ __  __  ___  ____  ____  __  __
  / __)(__ \/ ___)(  \/  )/ _ \/ ___)(_  _)(  \/  )
 ( (__  / _/\__ \ )    ( ) (_) )\___ \ _)(_  )    (
  \___)(____)___/(_/\/\_)\___/(____/(____)(_/\/\_)
         R E A L - T I M E   G R A V I T Y
```

> A physics-accurate N-body gravitational simulator that runs entirely in your
> terminal — leapfrog integration, ANSI 256-color rendering, and five dramatic
> astrophysical scenarios.

---

## Live Demo

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
              ✦ COSMOSIM  │  Solar System  │  t =   47.320  │  step     5915
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                                     ·  ·
                                  ·  ·
                        ·  ◉  ·  ★  ·  ●
                          · · ○    ···
                         ·○○       ·· ◦◦
                          ◦         ○○
                    ◉              ●○
                   ○·◦
                   ◦•
                    •·
                       ·  ·             ◎
                                       ○ ○
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ▸ ★ Sol  ● Mercury  ● Venus  ◉ Earth  ● Mars  ◎ Jupiter   E=-148823.4
```

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
       ✦ COSMOSIM  │  Figure-Eight Choreography  │  t =   19.002  │  step   47506
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                        ·  ·  ·  ·  ·  ★  ·  ·  ·  ·
                     ·  ·  ·              ·  ·  ·  ·
                  ·  ·                          ·  ·
                 ★                                ·
                  ·  ·                          ·  ·
                     ·  ·  ·              ·  ·  ·
                        ·  ·  ·  ·  ★  ·  ·  ·  ·
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ▸ ★ Alpha  ★ Beta  ★ Gamma   E=+2.4   [Ctrl+C to quit]
```

---

## Features

| Feature | Details |
|---|---|
| **Physics engine** | Leapfrog (Störmer-Verlet) integration — energy-conserving for orbital mechanics |
| **Scenarios** | Solar system, binary stars, figure-eight choreography, galaxy collision, chaotic cluster |
| **Rendering** | ANSI 256-color, fading orbital trails (`. · • ◦ ○`), auto-fits your terminal size |
| **HUD** | Real-time step counter, simulation time, total energy, center-of-mass tracking |
| **No heavy deps** | Pure Python + `numpy` only |

---

## Scenarios

### 🌟 Solar System (`solar`)
Sun with five planets (Mercury → Jupiter) in stable circular orbits.
Each orbital radius and speed is computed from the circular orbit condition `v = √(GM/r)`.

### ⭐ Binary Stars (`binary`)
Two massive stars (Sirius A & B) orbiting their shared center of mass, with a distant
companion tracing a wide elliptical path. Demonstrates how gravitational wells merge.

### ∞ Figure-Eight Choreography (`figure8`)
The famous **Chenciner-Montgomery** solution (2000): three equal-mass stars perpetually
chasing each other along a stable figure-eight curve. A rare island of order in a
chaotic system.

### 🌌 Galaxy Collision (`galaxy`)
Two mini-galaxies — each with a central black hole and a disk of orbiting stars —
on a collision course. Watch tidal tails form as stellar orbits are disrupted.

### 💥 Chaotic Star Cluster (`cluster`)
Twelve stars of random masses thrown into a dense region. Highly chaotic — bodies
are flung out, binary pairs form, and the cluster slowly evaporates.

---

## Installation

```bash
git clone https://github.com/kareemrt/Clauder
cd Clauder
pip install -r requirements.txt
```

**Requirements:** Python 3.9+, numpy ≥ 1.24, a terminal with ANSI 256-color support
(iTerm2, Windows Terminal, any modern Linux terminal).

---

## Usage

```bash
# Run with default scenario (Solar System)
python run_cosmosim.py

# Pick a specific scenario
python run_cosmosim.py solar
python run_cosmosim.py binary
python run_cosmosim.py figure8
python run_cosmosim.py galaxy
python run_cosmosim.py cluster

# Adjust simulation speed and view
python run_cosmosim.py galaxy --fps 60 --spf 10
python run_cosmosim.py solar  --scale 1.4

# List all scenarios
python run_cosmosim.py --list
```

### CLI Reference

| Flag | Default | Description |
|---|---|---|
| `scenario` | `solar` | Which scenario to run |
| `--fps N` | `30` | Target frames per second |
| `--spf N` | auto | Simulation steps per rendered frame |
| `--scale F` | auto | View zoom factor |
| `--list` | — | Print scenario names and exit |

---

## Architecture

```
cosmosim/
├── __init__.py          package marker
│
├── bodies.py            Body dataclass
│                         name · mass · pos · vel · color · symbol · trail
│
├── physics.py           Simulation class
│                         ┌─ _accelerations()  — O(n²) pairwise gravity
│                         │    F_ij = G·mᵢ·mⱼ·r̂ / (|r|² + ε²)   [softened]
│                         └─ step()            — Leapfrog integration
│                              ½-step vel → full-step pos → recompute F → complete vel
│
├── renderer.py          Renderer class
│                         world → screen projection  (aspect-ratio corrected)
│                         trail fade:  .  ·  •  ◦  ○
│                         ANSI 256-color body + trail compositing
│                         auto-fit to terminal size via shutil.get_terminal_size
│
├── scenarios.py         Scenario factories + SCENARIOS registry
│                         solar · binary · figure8 · galaxy · cluster
│
└── main.py              CLI (argparse) + animation run-loop
                          center-of-mass tracking · FPS throttle
```

### Data flow per frame

```
  SCENARIOS[key]
       │
       ▼
  factory() ──► List[Body]
       │              │
       ▼              ▼
  Simulation        Renderer
   .step() ×N    .render(bodies, …)
       │              │
       │    com/E     │
       └──────────────┘
              │
              ▼
        stdout (ANSI)
```

---

## Physics

### Gravitational force (softened)

To prevent force blow-up when two bodies pass very close, a **softening parameter** ε
is added to the denominator:

```
        G · mᵢ · mⱼ
Fᵢⱼ = ──────────────── · r̂ᵢⱼ
       |rᵢⱼ|² + ε²
```

This keeps the force finite and the integrator stable without meaningfully changing
long-range dynamics (ε = 0.8 in normalized units).

### Leapfrog integration

Simple Euler integration loses energy over time (orbits spiral outward). The
**Störmer-Verlet / leapfrog** scheme interleaves position and velocity updates at
half-integer time steps, giving a **symplectic** (energy-preserving) integrator:

```
v_{n+½} = vₙ + aₙ · (Δt/2)            ← half-step velocity
x_{n+1} = xₙ + v_{n+½} · Δt           ← full-step position
a_{n+1} = F(x_{n+1}) / m               ← new acceleration at new pos
v_{n+1} = v_{n+½} + a_{n+1} · (Δt/2)  ← complete velocity step
```

### Circular orbit condition (G = 1 units)

All scenarios use **normalized units** where `G = 1`. For a planet of mass `m`
orbiting a star of mass `M` at radius `r`, the circular orbit speed satisfies:

```
  centripetal force  =  gravitational force
  m · v² / r         =  G · M · m / r²
         → v         =  √(M / r)
```

---

## Controls

| Input | Action |
|---|---|
| `Ctrl+C` | Stop simulation gracefully |

Resize your terminal at any time — the renderer auto-fits on the next frame.

---

## Contributing

Issues and PRs welcome. For large changes, open an issue first.

---

*Built with ♥ and gravity.*
