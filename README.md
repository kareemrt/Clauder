# ⬡ QuantumDrift

### Emergent Particle Life Simulator

> *Give particles simple rules. Watch life appear.*

QuantumDrift is an interactive browser-based simulation of **Particle Life** — a class of emergent complexity where colored "species" of particles follow attraction and repulsion rules toward each other. From these absurdly simple rules, the system spontaneously assembles cells, predator/prey ecosystems, spiral galaxies, coral reefs, and more. No code path explicitly creates any of this. It simply *emerges*.

```
          ·  ✦  ·        ·  ✦         ✦  ·
    ✦  ·      ·    ·  ✦      ·   ·  ✦
  ·    ✦   ●───●    ✦  ·  ●─────●    ·
        ·  │ ◉ │  ·    · │  ◉  │ ·  ✦
  ✦      · ●───●  ✦    · ●─────● ·
    ·  ✦      ·    ✦  ·      ·    ✦  ·
          ✦  ·  ✦        ✦  ·
          
    Species spontaneously organizing into cell-like clusters
```

---

## Features

| Feature | Description |
|---|---|
| **5 Hand-crafted Presets** | Cells, Predator, Coral, Galaxy, Chaos — each tuned to produce distinct emergent behaviors |
| **Infinite Random Universes** | Generate a new random ruleset with one click — every run is unique |
| **Real-time Controls** | Adjust particle count, force range, friction, speed, glow, and trail live |
| **Energy Bursts** | Click anywhere on the canvas to inject kinetic energy — disturb and reshape colonies |
| **Screenshot Export** | Capture any moment as a PNG |
| **Zero Dependencies** | Pure HTML + CSS + vanilla JavaScript — open `index.html` and go |

---

## Presets

### 🟢 Cells
Simulates a simplified cellular biology. Cytoplasm particles cluster around Nucleus particles, while Membrane particles form boundaries. Watch pseudo-organelles assemble and divide.

```
  ██████████████████████████████████████████████████
  █                                                █
  █   ● ● ●    ◆ ◆ ◆ ◆    ● ●      ◆ ◆ ◆         █
  █  ● ◉ ● ●  ◆ ◆ ◆ ◆    ● ◉ ●    ◆ ◆ ◆ ◆        █
  █   ● ● ●    ◆ ◆ ◆ ◆    ● ●      ◆ ◆ ◆         █
  █       ■ ■ ■    ▲ ▲ ▲ ▲    ■ ■ ■               █
  █      ■ ■ ■      ▲ ▲ ▲      ■ ■ ■              █
  █                                                █
  ████████████████ CELLS PRESET ████████████████████
  
  ● Cytoplasm  ◆ Nucleus  ■ Membrane  ▲ Mitochondria
```

### 🔴 Predator
A three-way rock-paper-scissors cycle. Prey is eaten by Predator, which is eaten by Apex. Watch populations oscillate in waves — classic Lotka-Volterra dynamics visualized.

```
  ┌─────────────────────────────────────────────┐
  │  Population over time:                      │
  │                                             │
  │  Prey  ╭╮  ╭╮  ╭╮  ╭╮  ╭╮                 │
  │       ╯  ╰╯  ╰╯  ╰╯  ╰╯  ╰─              │
  │  Pred     ╭╮  ╭╮  ╭╮  ╭╮                  │
  │          ╯  ╰╯  ╰╯  ╰╯  ╰─               │
  │  Apex       ╭╮  ╭╮  ╭╮                    │
  │            ╯  ╰╯  ╰╯  ╰─                 │
  │         time ──────────────────────────>  │
  └─────────────────────────────────────────────┘
```

### 🟠 Coral
Five species with layered symbiosis. Coral grows, Algae feeds it, Polyps attach, Plankton drifts between colonies — structures branching outward like actual coral reefs.

### 🌌 Galaxy
Particles orbit each other in stable configurations — Dark matter tugs at Stars, Gas clouds spiral around Plasma cores. Distinctive spiral arm patterns emerge after ~10 seconds.

```
          . * .  *   .
       *    ╭────╮   *    .
     .    ╭─┤ ●● ├─╮   .
       * ╭┤ │    │ ├╮ *
        ─┤ │ ●● │ ├─
       * ╰┤ │    │ ├╯ .
     .    ╰─┤ ●● ├─╯   *
       .    ╰────╯  *    .
          * .  *  .
          
        Spiral arm formation
```

### 🔮 Chaos
Six species with maximally opposing forces — the most complex ruleset produces turbulent, ever-shifting patterns that never fully stabilize.

---

## Architecture

```
QuantumDrift/
├── index.html          # App shell, canvas, and UI structure
├── style.css           # Visual design — dark theme, glow aesthetics
├── src/
│   ├── presets.js      # Species definitions and interaction matrices
│   ├── simulation.js   # Physics engine — O(N²) force integration
│   ├── renderer.js     # Canvas 2D rendering — trails, glow, particles
│   └── ui.js           # Control wiring, event handling, boot sequence
└── README.md
```

### Data Flow

```
  ┌────────────┐    preset     ┌────────────┐
  │  presets.js│──────────────>│simulation.js│
  └────────────┘               └─────┬──────┘
                                     │ particles[]
                                     ▼
  ┌────────────┐    draw       ┌────────────┐
  │  renderer.js│<─────────────│  RAF loop  │
  └────────────┘               └────────────┘
        ^                            ^
        │                            │
  ┌────────────────────────────────────────┐
  │                 ui.js                  │
  │   sliders · buttons · click events     │
  └────────────────────────────────────────┘
```

---

## How It Works

### The Force Function

Each particle `i` of species `S_i` computes a force from every other particle `j` of species `S_j` within range `R`:

```
  ┌─────────────────────────────────────────────────────┐
  │                                                     │
  │  Force vs Distance                                  │
  │                                                     │
  │  force │        ╭──────╮                            │
  │  (+)   │       ╱        ╲  ← attraction zone        │
  │        │      ╱          ╲                          │
  │  ──────┼─────╱────────────╲────── distance          │
  │        │  ╱↑              ↑╲  R                     │
  │  (-)   │╱ R_min      R/3   ╲                        │
  │        │ ←repulsion→                                │
  │                                                     │
  │  Short-range repulsion prevents total collapse.     │
  │  Mid-range force is preset-matrix defined.          │
  └─────────────────────────────────────────────────────┘
```

The interaction matrix `M[i][j]` encodes the "personality" of each species pair:
- `M[i][j] > 0` → species `i` is **attracted** to species `j`
- `M[i][j] < 0` → species `i` is **repelled** by species `j`

### Emergence

No cell, no predator-prey cycle, no spiral arm is ever explicitly programmed. These patterns self-organize from N²/2 pairwise force computations updated at 60 Hz. This is the core insight of **complex systems theory**: *local rules → global structure*.

---

## Getting Started

```bash
# Clone and open — that's it
git clone https://github.com/kareemrt/clauder.git
cd clauder
open index.html   # macOS
# or: xdg-open index.html  (Linux)
# or: start index.html     (Windows)
```

No build step. No npm install. No server required.

---

## Performance Notes

- The simulation runs an O(N²) force calculation — 1500 particles means ~1.1M pair evaluations per frame
- Runs comfortably at 60fps on modern hardware for N ≤ 1000 with a dedicated GPU
- For slower machines, reduce particle count or increase the trail parameter (reduces per-frame draw calls)
- The renderer uses `globalCompositeOperation: 'lighter'` for bloom — colors add together, brighter where particles cluster

---

## Interaction Matrix Examples

The "Cells" preset's matrix — read as "row species feels toward column species":

```
            Cytoplasm  Nucleus  Membrane  Mitochond
Cytoplasm  [  +0.10,   +0.50,   -0.30,    +0.20 ]
Nucleus    [  +0.60,   +0.05,   -0.10,    +0.40 ]
Membrane   [  -0.20,   -0.10,   +0.30,    +0.10 ]
Mitochond  [  +0.30,   +0.40,   -0.20,    +0.15 ]
```

Nucleus strongly attracts Cytoplasm (+0.60) which clusters around it. Membrane repels everything while maintaining loose cohesion within itself (+0.30). The result: nucleus-centered clusters with membrane boundary particles.

---

## Extending QuantumDrift

Add a new preset in `src/presets.js` by defining a `species` array and `matrix`:

```javascript
myPreset: {
  name: "My Preset",
  description: "...",
  species: [
    { name: "TypeA", color: "#ff4488" },
    { name: "TypeB", color: "#44ff88" },
  ],
  matrix: [
    [ 0.1, -0.8 ],   // TypeA: self-repel, flee TypeB
    [ 0.9,  0.1 ],   // TypeB: hunt TypeA, cluster weakly
  ],
  count: 400,
  range: 90,
  friction: 0.85,
}
```

Then add a button in `index.html` with `data-preset="myPreset"`.

---

## The Science

Particle Life was popularized by [Jeffrey Ventrella](http://www.ventrella.com/) and later by the YouTuber [Brainxyz](https://www.youtube.com/watch?v=p4YirERTVF0). It's closely related to:

- **Cellular Automata** (Conway's Game of Life, Rule 110)
- **Active Matter Physics** (flocking, swarming, motility-induced phase separation)
- **Artificial Life** (Tierra, Avida, Lenia)
- **Complex Systems** (emergence, self-organization, criticality)

The key insight shared across all these systems: **complexity does not require complex rules**. A handful of numbers in a matrix is sufficient to generate behavior indistinguishable from life.

---

*Built by Claude — an AI with a fondness for emergent complexity and the uncomfortable suspicion that the boundary between "simulation" and "reality" is thinner than it appears.*
