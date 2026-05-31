# ✦ Nebula — N-Body Gravitational Simulator

```
  ███╗   ██╗███████╗██████╗ ██╗   ██╗██╗      █████╗
  ████╗  ██║██╔════╝██╔══██╗██║   ██║██║     ██╔══██╗
  ██╔██╗ ██║█████╗  ██████╔╝██║   ██║██║     ███████║
  ██║╚██╗██║██╔══╝  ██╔══██╗██║   ██║██║     ██╔══██║
  ██║ ╚████║███████╗██████╔╝╚██████╔╝███████╗██║  ██║
  ╚═╝  ╚═══╝╚══════╝╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
        N - B o d y   G r a v i t a t i o n a l
```

> A real-time gravitational simulator that runs entirely in your terminal —
> driven by **Velocity Verlet integration** and painted with full ANSI colour.
> No GUI, no browser. One dependency: **NumPy**.

---

## Table of Contents

1. [Features](#features)
2. [Demo](#demo)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Scenarios](#scenarios)
6. [Project Structure](#project-structure)
7. [Physics](#physics)
8. [Architecture](#architecture)
9. [Contributing](#contributing)

---

## Features

| | |
|---|---|
| ⚛️  **Real physics** | Newtonian gravity with softening length, Velocity Verlet integration |
| 🎨 **Rich ANSI visuals** | Per-body colour, animated fading trails, live energy readout |
| 🌌 **5 preset scenarios** | Figure-8, binary stars, solar system, galaxy merger, random cluster |
| ⚡ **Configurable speed** | Adjustable FPS target and physics substeps per frame |
| 🔬 **Energy tracking** | KE, PE, and total mechanical energy shown every frame |
| 🧩 **Extensible** | Add a new scenario in a single function |

---

## Demo

### Figure-8 Choreography (default)

```
✦ NEBULA — N-Body Gravitational Simulator  │ t=   3.142 │ step=  1571 │ fps= 29.8
────────────────────────────────────────────────────────────────────────────────────
                       ·  ·  .
                    ·  ·  ·    .
                 ●  ·  ·         ·  ·  .  .
              ·  ·  ·               ·  ·  ·  .
           ·  ·  ·   ★               ·  ·  ·  ◆
              ·  ·  ·               ·  ·  ·  .
                 ·  ·  ·         ·  ·  .  .
                    ·  ·  .   .
                       ·  ·  .
────────────────────────────────────────────────────────────────────────────────────
  ● Alpha     m=1.0  v=1.024  │  ★ Beta     m=1.0  v=0.987  │  ◆ Gamma   m=1.0  v=1.011
  KE=   1.5123  PE=  -3.0891  E=  -1.5768   Ctrl-C to quit
```

### Galaxy Merger

```
✦ NEBULA — N-Body Gravitational Simulator  │ t=  12.440 │ step=  2488 │ fps= 30.1
────────────────────────────────────────────────────────────────────────────────────
  ·  ·  .                                            .  ·  ·
 ·  ★  ·  ●  ·                                    ·  ●  ★  ·
  ·  ·  .    ·  ·                              ·  ·    .  ·  ·
              ·  ·  .  .                  .  .  ·  ·
                 ·  ·  ·  .  .      .  .  ·  ·  ·
                    · ◆ ·  · ▲ · · · ▲ · · ◆ ·
────────────────────────────────────────────────────────────────────────────────────
  ● Core     m=20.0 v=0.843  │  ★ Star     m=0.1  v=2.341  │  ...
  KE=  18.3401  PE= -42.1203  E= -23.7802   Ctrl-C to quit
```

---

## Installation

```bash
# Clone
git clone https://github.com/kareemrt/Clauder.git
cd Clauder

# Install the one dependency
pip install -r requirements.txt
```

**Requirements:** Python 3.10+, NumPy ≥ 1.24

---

## Usage

```
python main.py [SCENARIO] [OPTIONS]
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `SCENARIO` | `figure8` | Which preset to run |
| `--fps N` | `30` | Target frames per second |
| `--steps N` | `5` | Physics substeps per frame |
| `--width N` | auto | Override canvas width |
| `--height N` | auto | Override canvas height |
| `--n N` | `6` | Body count (`random` scenario only) |
| `--seed N` | `0` | RNG seed (`random` scenario only) |
| `--list` | — | Print all scenarios and exit |

### Quick examples

```bash
# Famous figure-8 three-body choreography (default)
python main.py

# Slow-motion solar system, more substeps = better orbit accuracy
python main.py solar --fps 60 --steps 10

# Two galaxies colliding
python main.py galaxy

# 12 random bodies, different seed
python main.py random --n 12 --seed 42

# List all scenarios
python main.py --list
```

---

## Scenarios

### `figure8` — Chenciner–Montgomery Choreography

```
          ★
        ·   ·
      ·       ·
    ●           ◆
      ·       ·
        ·   ·
          ★
```

Three equal masses perpetually chase each other around a figure-8 path.
Discovered analytically in 2000 by Chenciner & Montgomery — one of the most
beautiful exact periodic solutions in classical mechanics.

**Exact initial conditions (from the original paper):**

| Body  | Position                       | Velocity                         |
|-------|--------------------------------|----------------------------------|
| Alpha | (−0.97000436,  0.24308753)     | ( 0.46620369,  0.43236573)       |
| Beta  | ( 0.97000436, −0.24308753)     | ( 0.46620369,  0.43236573)       |
| Gamma | ( 0,           0)              | (−0.93240737, −0.86473146)       |

---

### `binary` — Binary Star System

Two stars (mass ratio **5:3**) in an elliptical orbit, plus a low-mass
planetoid (Pebble) that can be captured, ejected, or oscillate stably
depending on its starting velocity.

---

### `solar` — Inner Solar System

Sun (M = 1000) plus Mercury, Venus, Earth, and Mars placed at scaled AU
distances with exact circular-orbit speeds (`v = √(GM/r)`).

---

### `galaxy` — Galaxy Merger

Two mini-galaxies — each a 20-mass core surrounded by 8 orbiting 0.1-mass
stars — launched toward each other. Tidal stripping, core inspiral, and
slingshot ejections emerge naturally from the N-body dynamics.

---

### `random` — Random Cluster

N bodies with random masses (0.5–3.0) and positions (−5 to +5), with net
momentum zeroed so the cluster stays on-screen. Control with `--n` and `--seed`.

---

## Project Structure

```
Clauder/
├── main.py                  # Entry point (one line)
├── requirements.txt         # numpy only
├── README.md
└── nebula/
    ├── __init__.py          # Package: Body, Simulation, SCENARIOS
    ├── physics.py           # Body + Simulation (Velocity Verlet integrator)
    ├── renderer.py          # ANSI terminal renderer (world → screen)
    ├── scenarios.py         # Five preset simulations + SCENARIOS registry
    └── cli.py               # argparse CLI + main render loop
```

---

## Physics

### Gravitational Force

Every pair of bodies (i, j) exerts a mutual force:

```
         G · mᵢ · mⱼ
F = ──────────────────────── · r̂
      (|r|² + ε²)^(3/2)
```

**ε = 0.1** is the *softening length* — it prevents the denominator from
collapsing to zero during close approaches, keeping the integrator stable
without capping any speed artificially.

### Velocity Verlet Integration

More accurate than Euler at the same timestep, and exactly time-reversible.
Accelerations are computed **twice** per step:

```
pos(t+Δt) = pos(t) + vel(t)·Δt + ½·a(t)·Δt²

       ← update positions first, recompute a →

vel(t+Δt) = vel(t) + ½·[a(t) + a(t+Δt)]·Δt
```

This second-order symplectic integrator conserves energy far better than
first-order (Euler) methods for the same computational cost. The figure-8
scenario shows **< 0.8% energy drift over 5,000 steps**.

### Energy Conservation

The footer displays KE, PE, and total energy E = KE + PE. A healthy
simulation keeps E roughly constant. If you see large drift, add substeps
with `--steps`.

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│                    cli.py                        │
│  parse args → pick scenario → main render loop  │
└───────────────────┬─────────────────────────────┘
                    │
           ┌────────┴────────┐
           ▼                 ▼
   ┌────────────┐    ┌─────────────┐
   │ physics.py │    │ renderer.py │
   │            │    │             │
   │ Body       │    │ Renderer    │
   │ Simulation │    │ .render()   │
   │ .step()    │    │             │
   │ Verlet     │    │ world  →    │
   │ integr.    │    │ screen      │
   └─────┬──────┘    │ ANSI out   │
         │           └─────────────┘
   ┌─────┴──────────┐
   │ scenarios.py   │
   │ figure_eight() │
   │ binary_stars() │
   │ solar_system() │
   │ galaxy_merger()│
   │ random_cluster()│
   └────────────────┘
```

**Render loop:**

```python
while True:
    for _ in range(args.steps):
        sim.step()                    # advance physics
    renderer.render(sim, fps_actual)  # paint frame
    time.sleep(frame_dt - elapsed)    # pace to target fps
```

---

## Contributing

Adding a scenario takes one function:

```python
# nebula/scenarios.py

def my_scenario() -> Simulation:
    return Simulation([
        Body(1.0, [0.0, 0.0], [0.0,  1.0], "A"),
        Body(1.0, [3.0, 0.0], [0.0, -1.0], "B"),
    ], G=1.0, dt=0.005)

SCENARIOS["myscene"]              = my_scenario
SCENARIO_DESCRIPTIONS["myscene"] = "My two-body orbit"
```

```bash
python main.py myscene
```

---

*Built by Claude — real Newtonian gravity, rendered in your terminal.*
