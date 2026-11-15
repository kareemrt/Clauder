# ⚛ Particle Life — Emergent Universe Simulator

> *"Life is not a property of atoms — it emerges from the rules between them."*

A browser-based simulation where simple attraction and repulsion rules between six particle species give rise to complex, life-like emergent behaviors: swarming, hunting, orbiting, clustering. No randomness — just physics creating patterns indistinguishable from living systems.

---

## ✨ Live Demo

Open `index.html` in any modern browser — no install, no build step, no dependencies.

---

## 📸 Screenshots

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║   🔴  🟠  🟡      ·  ·   · ·   ·      ·    ·       ║
║          ·  · ·  · ·      ·  ·· ·   ·   ·  ·       ║
║   🟢  🔵  🟣   · ·  ·· · · ·     ·  ·  ·   ·       ║
║                                                      ║
║   [Cells]    Red clusters form, repelling others     ║
╚══════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════╗
║  ·   ·  · · ·  ·     ·   · ·  ·    ·   ·  · ·      ║
║   · ·     ·   · ·  ·   · ·   ·  ·    ·   ·   ·     ║
║  ·   ·  ·    ·  · ·   ·   ·   · ·  ·   · ·  ·      ║
║                                                      ║
║   [Galaxy]   Cascading attracts form swirling arms   ║
╚══════════════════════════════════════════════════════╝
```

---

## 🧬 How It Works

### The Core Idea

Each particle belongs to one of **6 species** (colors). Every pair of species has a rule — a number from **−1** (strong repulsion) to **+1** (strong attraction). With just these 36 numbers, the simulation produces patterns that look genuinely alive.

### Physics Engine

```
For each particle i:
  for each nearby particle j:
    if dist < minDist:   apply universal repulsion (no overlap)
    elif dist < maxDist: apply rule force × triangular kernel
  velocity += acceleration × dt
  velocity *= (1 - friction)
  position += velocity × dt × 60
  position = position % (canvas size)   // toroidal wrap
```

The **triangular kernel** peaks at the midpoint of the interaction range, then falls to zero — giving a smooth, stable force profile:

```
Force
  │        ▲ peak
  │       / \
  │      /   \
  │_____/     \______
  minDist       maxDist    Distance
```

### Performance: Spatial Hashing

Naively checking all pairs is O(n²) — too slow for 1,000+ particles. The simulation uses a **spatial hash grid**:

1. Divide the canvas into cells of size `maxDist`
2. Each particle inserts itself into its cell
3. Force calculation only checks the **9 neighboring cells** (3×3)
4. Result: O(n · k) where k is average particles per cell (~10–20)

This makes 2,000 particles run smoothly at 60fps on a modern laptop.

---

## 🎮 Controls

### Presets

| Key | Preset | Behavior |
|-----|--------|----------|
| `1` | **Cells** | Each species clusters tightly, repels others — forms colorful cell colonies |
| `2` | **Galaxy** | Cyclic chain of attractions creates rotating galactic arms |
| `3` | **Ecology** | Predator-prey asymmetries — species chase and flee each other |
| `4` | **Predators** | Strict food chain: Red→Orange→Yellow→Green→Blue→Purple→Red |
| `5` | **Harmony** | All species gently attract — one flowing unified dance |
| `6` | **Chaos** | Asymmetric rules create turbulent, explosive patterns |

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Pause / Resume |
| `R` | Randomize rules |
| `S` | Scatter particles |
| `1`–`6` | Switch presets |
| Click canvas | Spawn burst of particles |

### Sliders

- **Particles** (200–2,000): Population size — more = richer patterns, slower simulation
- **Speed** (0.1×–3.0×): Simulation time scale
- **Interaction Radius** (30–150px): How far particles can "sense" each other
- **Friction** (0.01–0.20): Dampening — low friction = chaotic, high friction = sluggish

---

## 🗂 Project Structure

```
Clauder/
├── index.html              # Entry point — full app shell
├── styles/
│   └── main.css            # Dark-mode UI with Catppuccin-inspired palette
├── src/
│   ├── presets.js          # 6 hand-tuned interaction matrices + species colors
│   ├── simulation.js       # Physics engine + spatial hash grid + renderer
│   └── main.js             # UI bindings, animation loop, keyboard shortcuts
└── README.md               # This file
```

---

## 🔬 Interaction Matrix

The panel on the right shows the **6×6 rule matrix** as a color grid:

- 🟢 **Green cell** = species in that row is **attracted** to species in that column
- 🔴 **Red cell** = species in that row is **repelled** by species in that column
- Brightness = strength of the interaction

The matrix is **asymmetric** — Red may be attracted to Blue while Blue flees Red. This asymmetry is what creates chase-and-flee behaviors.

---

## 🧪 Interesting Experiments

1. **Start with Cells, increase Radius to 150** — watch the tight clusters dissolve into looser communities
2. **Galaxy preset + low friction (0.01)** — creates tight, stable vortices
3. **Randomize repeatedly** — each randomization is a unique universe; keep clicking until you find something beautiful
4. **Chaos + 2,000 particles** — the entire canvas becomes a turbulent, roiling sea
5. **Harmony + scatter** — particles slowly drift together and merge into a unified swarm

---

## 🧠 Science Behind It

Particle Life is based on the work of **Jeffrey Ventrella** (Clusters, 1994) and was popularized by **Jeffery's Games** on YouTube. It's related to:

- **Artificial Life** (Langton, 1986) — studying life-like behavior in non-biological systems
- **Flocking algorithms** (Reynolds, 1987) — emergent collective behavior from local rules
- **Cellular automata** (Conway, 1970) — complex global patterns from simple local rules
- **Self-organization** in physics — how order arises without a central controller

The key insight: **you don't need intelligence to get intelligent-looking behavior**. You only need the right rules at the interaction level.

---

## 🛠 Technical Details

| Property | Value |
|----------|-------|
| Language | Vanilla JavaScript (ES2020) |
| Rendering | HTML5 Canvas 2D API |
| Physics | Verlet-inspired integration |
| Spatial index | Custom hash grid |
| Target FPS | 60 |
| Particle count | 200–2,000 |
| Dependencies | **None** |
| Build step | **None** |
| Browser support | Any modern browser (Chrome, Firefox, Safari, Edge) |

---

## 📄 License

MIT — do whatever you want with it.

---

*Built with curiosity by [Claude](https://claude.ai) — because sometimes the most fascinating thing in the universe is what emerges when simple things interact.*
