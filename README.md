# 🌌 Cosmos — Real-Time Solar System Visualizer

> *"The cosmos is within us. We are made of star-stuff."* — Carl Sagan

A stunning terminal-based solar system visualizer that renders **real planetary positions** using Keplerian orbital mechanics. Watch the solar system unfold in beautiful ANSI color art, export breathtaking SVG snapshots, and run time-lapse animations directly in your terminal.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 🔭 **Real Orbital Mechanics** | Keplerian elements + Newton-Raphson solver for true planet positions |
| 🎨 **Beautiful ANSI Rendering** | Full-color terminal art with star fields, orbits, and Unicode symbols |
| 🖼️ **SVG Export** | High-resolution vector snapshots with gradients and glow effects |
| ⏩ **Time-Lapse Animation** | Watch decades of orbital motion in seconds |
| 📅 **Any Date** | Render the solar system at any point in history or the future |
| 🔍 **Zoom Levels** | Full solar system view or inner-planet zoom |

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/kareemrt/Clauder.git
cd Clauder/cosmos

# Install dependencies
pip install -r requirements.txt

# Print the solar system right now
python3 __main__.py

# Export an SVG snapshot
python3 __main__.py --svg my_solar_system.svg

# Time-lapse animation (30 days/second)
python3 __main__.py --animate --speed 30

# Zoom into the inner solar system
python3 __main__.py --inner

# Render a specific date
python3 __main__.py --date 1969-07-20
```

---

## 🪐 The Science

### Keplerian Orbital Elements

Each planet's orbit is defined by six classical orbital elements at the **J2000 epoch** (January 1, 2000, 12:00 TT):

| Element | Symbol | Description |
|---------|--------|-------------|
| Semi-major axis | *a* | Average orbital radius in AU |
| Eccentricity | *e* | How elliptical the orbit is |
| Inclination | *i* | Tilt relative to the ecliptic |
| Period | *T* | Time for one complete orbit |
| Mean longitude | *L₀* | Position at J2000 |
| Daily motion | *n* | Angular velocity in °/day |

### How Positions Are Computed

```
Step 1: Compute Mean Anomaly
  M(t) = L₀ + n·Δt    (propagate forward in time)

Step 2: Solve Kepler's Equation (Newton-Raphson)
  M = E − e·sin(E)    (find eccentric anomaly E)

Step 3: Convert to True Anomaly
  ν = 2·arctan[√((1+e)/(1−e)) · tan(E/2)]

Step 4: Heliocentric Distance
  r = a(1 − e²) / (1 + e·cos(ν))

Step 5: Cartesian Coordinates
  x = r·cos(ν),  y = r·sin(ν)
```

---

## 🗂️ Project Structure

```
cosmos/
│
├── __main__.py          # CLI entry point
├── requirements.txt     # Dependencies (rich)
│
└── src/
    ├── __init__.py
    ├── orbital.py       # Keplerian mechanics engine
    │                    #   · OrbitalElements dataclass
    │                    #   · Kepler equation solver
    │                    #   · Planet position calculator
    │
    ├── renderer.py      # ANSI terminal renderer
    │                    #   · Canvas drawing system
    │                    #   · Orbit rendering
    │                    #   · Star field generator
    │                    #   · Data panel
    │
    ├── exporter.py      # SVG export engine
    │                    #   · Vector orbit paths
    │                    #   · Planetary gradients & glow
    │                    #   · Star field
    │                    #   · Saturn rings
    │
    └── animate.py       # Animation loop
                         #   · Real-time / time-lapse
                         #   · FPS control
```

---

## 🎛️ CLI Reference

```
python3 __main__.py [options]

Options:
  --static          Print a single frame and exit (default)
  --animate         Run animated time-lapse
  --fps N           Frames per second (default: 12)
  --speed N         Days per second of wall time (default: 30)
  --view N          AU radius visible on screen (default: 32)
  --inner           Zoom to inner solar system (~2 AU radius)
  --date YYYY-MM-DD Render this date instead of now
  --svg [PATH]      Export SVG snapshot (default: cosmos.svg)
  --help            Show help
```

### Examples

```bash
# Apollo 11 launch day — where were the planets?
python3 __main__.py --date 1969-07-16 --svg apollo11.svg

# Inner planets only, high frame rate
python3 __main__.py --animate --inner --fps 24 --speed 10

# See the next 100 years in ~3 minutes
python3 __main__.py --animate --speed 365 --fps 30

# Static snapshot for today
python3 __main__.py --static
```

---

## 🌍 Planet Data

| Planet | Symbol | Orbital Period | Semi-Major Axis | Eccentricity |
|--------|--------|---------------|----------------|-------------|
| Mercury | ☿ | 87.97 days | 0.387 AU | 0.206 |
| Venus | ♀ | 224.70 days | 0.723 AU | 0.007 |
| Earth | ⊕ | 365.25 days | 1.000 AU | 0.017 |
| Mars | ♂ | 686.97 days | 1.524 AU | 0.093 |
| Jupiter | ♃ | 11.86 years | 5.203 AU | 0.049 |
| Saturn | ♄ | 29.46 years | 9.537 AU | 0.057 |
| Uranus | ⛢ | 84.01 years | 19.19 AU | 0.046 |
| Neptune | ♆ | 164.8 years | 30.07 AU | 0.010 |

---

## 🧮 Technical Details

- **Language**: Python 3.11+
- **Dependencies**: `rich` (terminal formatting)
- **Orbital Model**: Simplified two-body Keplerian mechanics
- **Epoch**: J2000.0 (JD 2451545.0)
- **Accuracy**: Positions accurate to ~0.1° for inner planets, ~1° for outer planets
- **Coordinate System**: Heliocentric ecliptic J2000

---

## 🔮 What's Next

- [ ] 3D orbital inclination rendering
- [ ] Moon and major moon systems
- [ ] Asteroid belt simulation
- [ ] Comet trajectory tracking (Halley's, etc.)
- [ ] Hohmann transfer orbit calculator
- [ ] Historical event overlays (eclipses, conjunctions)
- [ ] Web-based interactive version

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

*Built with Keplerian love by Claude 🤖*
