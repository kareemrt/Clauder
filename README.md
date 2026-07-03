# ASCII Ray Tracer

> A pure-Python 3D renderer that brings physically-based shading, reflections, and animated scenes directly to your terminal — no GPU, no dependencies, no compromise.

```
      ██████╗  █████╗ ██╗   ██╗    ████████╗██████╗  █████╗  ██████╗███████╗██████╗
      ██╔══██╗██╔══██╗╚██╗ ██╔╝       ██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
      ██████╔╝███████║ ╚████╔╝        ██║   ██████╔╝███████║██║     █████╗  ██████╔╝
      ██╔══██╗██╔══██║  ╚██╔╝         ██║   ██╔══██╗██╔══██║██║     ██╔══╝  ██╔══██╗
      ██║  ██║██║  ██║   ██║          ██║   ██║  ██║██║  ██║╚██████╗███████╗██║  ██║
      ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝          ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝
```

---

## What is this?

This project implements a **complete ray tracer from scratch in pure Python** — no C extensions, no OpenGL, no image libraries required. Instead of pixels on a screen, it paints light with ASCII characters and ANSI colour codes, turning your terminal into a 3D viewport.

Every photon is simulated: cast a ray from the camera, find what it hits, compute **Phong shading** (ambient + diffuse + specular), trace **shadow rays** to each light, recurse for **mirror reflections**, and map the final luminance to a character from the density ramp. The result is a fully interactive 3D scene with physically correct lighting and real-time animation.

---

## Gallery

### Classic Scene — orbiting spheres with a checkerboard floor

```
JJJJJJJJUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUJJJJJJJJ
CCCCCCJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJCCCCCC
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
[[[[[[??????????????????????[[[[[[[[[[[[[[[[[[[[[[??????????????????????[[[[[[[[[[[[[[[[[[[[[[??????????????????????[[
??}}}}????}}}}????}}}}????}}}}????}}}}}}????{{{{????{{{{????{{{{????{{{{????{{}}????}}}}????}}}}????}}}}??????}}}}????
????111111????11))))??????))))))??????))))))??????))))??????))))))??????))))))??vvrrffjjuu????))))))??????111111??????
||||||]]]]]]]]\\\\\\]]]]]]]]\\\\\\\\]]]]]]\\\\////]]]]]]]]//////]]]]]]]]\\\\uujj//||||||\\ttxx]]]]]]]]||||||]]]]]]]]
tt[[[[[[[[ffffffff[[[[[[[[[[jjjjjjxxff////ttrrjjjjjjjj[[[[[[[[[[jjjjjjjj[[XXccuuvvuurrrrnnuuuucc]]tttttttttt]]]]]]
rrrrxxxxxx[[[[[[}}}}xxxxnnnnnnrrtt//uu//))))((\\ttnn}}}}}}}}}}nnnnnnnnnn[[nn))//||(([[11jjrrjj[[[[[[[[[[rrrrrrjjjj[
uuuuuuvvvvvv}}}}}}}}}}}}vvvv[[rrffffxxtt////xxxxff__uunnnnnn[[[[[[[[[[[[xxxx[[uu<<11}}nnnnrrjj--))))))))nnnn}}}}[[[[
{{{{{{{{{{{{XXXXXXXXXXYYYY{{{{--??jjjj??--tt______{{{{{{--{{{{{{{{||||vv||uu[[vvttxxnnXXCCYYxxttttjjrr//}}zzzzzzzzcc
YYYY{{{{{{{{{{{{{{{{{{YYYYYYYYYYYY||\\\\//>>!!______--------zzzzzzzz\\jj__>>~~~~//rrxxccXXuuff\\||||(())}}{{{{{{{{{{
UUUUUUUUUUUUUUUU{{{{{{{{{{{{{{{{{{{{--{{{{{{{{{{{{{{{{111111{{{{{{{{[[}}XXXXYYUU//tt\\||tt//||(())11{{__++{{YYYYYYYYYY
CCLLLLLLLLLL11111111111111111111CCCCJJUUUUUUUUUUUUCC111111111111{{{{}}{{YYUUJJYY[[))(({{}}[[]]}}]]--__-->>{{{{{{YYYYYY
1111QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQLL11{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{CCCCCCCCCCCCJJJJJJJJJJJJJJJJJJ{{{{{{{{{{{{{{
```

*Ruby red, silver mirror, and ocean blue spheres orbit a reflective checkerboard floor under two-tone lighting.*

---

### Solar System — the inner planets in motion

```
YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
UUUUUUUUUUUUUUUUUUUUUUUUYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYUUUUUUUUUUUUUUUUUUUUUUU
JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUJJJJJJJJJJJJJJJJJJJJJJ
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQllQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ
OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOllllllllOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZmmmmmmmmmmmmmmmmmmmmmmmmmmllllllllllllllllllllZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
mmmmwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqllllllllqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqwwwwwwwwww
wwwwqqqqqqqqqqqqqqqqqqqqqqqqqqqqppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppqqqqqqqqqqqqqqqqqqqqwwww
qqqqqqqqqqqqppppppppppppppppppppppppppppddddddddddddddddddddddddddddddddddddddddppppppppppppppppppppppppppqqqqqqqqqqqqq
ppppppppppddddddddddddddddddddddddddbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbddddddddddddddddddddpppppppppp
ddddddddbbbbbbbbbbbbbbbbbbbbbbbbbbbbkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkbbbbbbbbbbbbbbbbbbbbbbdddddddddddddddd
bbbbbbbbbbbbbbbbbbkkkkkkkkkkkkkkkkkkkkkkkkkkkkhhhhhhhhhhhhhhhhhhhhhhhhkkkkkkkkkkkkkkkkkkkkkkkkbbbbbbbbbbbbbbbbbbbbbbbb
```

*Mercury, Venus, Earth (with Moon), and Mars orbit a glowing yellow Sun. Eighteen stars dot the background.*

---

### Disco — metallic spheres and spinning coloured lights

```
LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
jjjjjjxxxxxxxxjjjjxxxxxxjjjjjjxxxxjjjjjjxxxxxxjjjjnnnnnnjjjjjjnnnnjjjjjjnnnnnnjjjjnnnnnnjjjjjjnnnnzzjjjjnnnnxxjjjjxx
xxffffffffxxxxxxnnffffffffnnnnnnnnffffxxffuuccCCjjrrffuuvvXXYY[[ffvvjj((\\xxzzvv[[}}xxJJ1111\\uu11<<{{XX//{{{{||ffffuu
xxffffffttttnnnnnnnnnntttttttt11))))(((({{??//ii>>??++++??ii--]]////11++<<??jjjjjj~~<<]]<<))ffffffuunn]]__>>]]__uunnnn
xxxxttttttttttttnnnnnnrrrr////////--iilljj??~~{{\\nn////--;;))uuxxuutt{{[[11\\\\))[[((rrnntt--++__]]//////xxuunnnnnnxx
////rrrrrrrrrrjjjj//\\\\\\\\\\ttttff}}??++1111\\\\||||}}11))//ttrrjj((11]]))||||{{[[]]\\ttxxff11}}]]----\\\\\\////xxxx
rrrrrrrrrrrr\\\\\\\\\\\\\\\\jjjjjj((]]}}}}--++||||}}II++ii\\))jjjjjj{{[[<<>>||||||||++{{))((xxxxtt]]}}>>__<<tt//////xx
\\\\\\\\rrrrrrrrrrrrjjjj||||||||||--????||||xxjjjj||//((11}}--((tt{{}}__||((||jjjjjj||((++____||\\//\\))ffjjnnvvvvuunn
((((((((((ffffffffffffffffffff))))((((||||\\//ffjjvvccccvvvvuunnxxrrjj(((())))))))))))((||xxnnvvXXUUCCQQ00OO00UUXXvvnn
```

*A 5×3 grid of metallic spheres bounces above a mirror floor while three coloured lights sweep in circles.*

---

## Features

| Feature | Details |
|---|---|
| **Phong shading** | Ambient + Lambertian diffuse + Blinn-Phong specular per light |
| **Hard shadows** | Shadow rays cast to each point light before adding diffuse/specular |
| **Mirror reflections** | Configurable recursion depth (default 4 bounces) |
| **Checkerboard planes** | Procedural pattern computed at hit time — no texture memory |
| **ANSI true-colour** | 24-bit RGB foreground codes; gracefully degrades to plain ASCII |
| **3 built-in scenes** | `classic`, `solar`, `disco` — each fully animated |
| **Animation loop** | Smooth orbital/bobbing motion driven by a single time parameter |
| **PNG export** | Optional Pillow backend for high-res image output |
| **Zero required deps** | Only stdlib; Pillow is optional for `--export` |

---

## Architecture

```
ascii-ray-tracer/
│
├── main.py                    ← CLI entry point (argparse)
│
├── raytracer/                 ← Core engine (pure Python, zero deps)
│   ├── __init__.py
│   ├── vector.py              ← Vec3: arithmetic, dot/cross, normalize, reflect
│   ├── ray.py                 ← Ray: origin + unit direction, parametric point
│   ├── objects.py             ← Sphere, Plane, Material, HitRecord
│   ├── light.py               ← PointLight, AmbientLight
│   ├── scene.py               ← Scene (BVH-less list traversal), Camera (pin-hole)
│   ├── renderer.py            ← trace() — Phong, shadow, reflection recursion
│   └── display.py             ← Luminance → ASCII ramp, ANSI colour codes
│
├── scenes/                    ← Pre-built animated scenes
│   ├── classic.py             ← 3 orbiting spheres + checkerboard floor
│   ├── solar.py               ← Inner solar system + starfield
│   └── disco.py               ← Mirror floor + metallic sphere grid
│
└── requirements.txt           ← Pillow (optional, PNG export only)
```

### Data-flow diagram

```
  Camera.get_ray(u, v)
         │
         ▼
  ┌─────────────────────────────────────────────┐
  │  Renderer.trace(ray, scene, depth)          │
  │                                             │
  │  scene.hit(ray) ──► HitRecord?              │
  │       │ no             │ yes                │
  │       ▼                ▼                    │
  │  sky gradient    Phong shading              │
  │                  ┌────────────┐             │
  │                  │ for each   │             │
  │                  │ PointLight │             │
  │                  │  shadow?──►│skip         │
  │                  │  diffuse   │             │
  │                  │  specular  │             │
  │                  └────────────┘             │
  │                  reflectivity > 0?          │
  │                  └──► trace(reflect_ray,    │
  │                            depth+1)         │
  └─────────────────────────────────────────────┘
         │
         ▼
  Vec3(r,g,b) ──gamma──► luminance ──► ramp char + ANSI colour
```

---

## How Ray Tracing Works

Ray tracing simulates the path of light **backwards** — from the camera eye, through each pixel on an imaginary screen, into the scene.

### 1. Camera model (pin-hole)

```
  camera.position
       │
       │  focal_length = 1
       │
  ─────┼───── viewport
       │   ↗ pixel (u, v)
       │  / direction
       │/
       •──────────────────► scene
```

For each pixel `(u, v)` in `[0,1]²`, `Camera.get_ray()` computes:
```
lower_left + horizontal·u + vertical·v − camera_position
```

### 2. Ray–sphere intersection

Expanding `|origin + t·dir − center|² = radius²` gives a quadratic in `t`.
Negative discriminant → miss; smaller positive root → closest hit point.

### 3. Phong illumination model

```
color = ambient
      + Σ_lights [ diffuse · max(0, N·L) + specular · max(0, N·H)^shininess ]
```

Where:
- **N** = surface normal at hit point
- **L** = direction to light (normalised)
- **H** = half-vector `(L + V) / |L + V|`
- Shadow ray confirms light is not occluded before adding diffuse/specular

### 4. Reflection

```
reflect_dir = ray_dir − 2·(ray_dir · N)·N
color = color·(1−reflectivity) + trace(reflect_ray)·reflectivity
```
Capped at `max_depth` bounces to avoid infinite recursion.

### 5. ASCII mapping

Luminance (perceptual: `0.2126R + 0.7152G + 0.0722B`) is mapped to a 70-character density ramp:
```
" .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
```
Each character is printed **twice** (doubled horizontally) to compensate for the 2:1 height-to-width ratio of terminal cells.

---

## Installation

```bash
git clone https://github.com/kareemrt/clauder.git
cd clauder

# No required dependencies — runs on stdlib Python 3.8+
python main.py

# Optional: PNG export
pip install Pillow
```

---

## Usage

```bash
# Single frame — classic scene (default)
python main.py

# Choose a scene
python main.py --scene solar
python main.py --scene disco

# Larger canvas
python main.py --width 120 --height 48

# Increase reflection depth for more accurate mirrors
python main.py --depth 6

# Run the animation loop (Ctrl-C to stop)
python main.py --animate

# Control animation speed and length
python main.py --animate --frames 120 --fps 12

# Render at a specific animation time
python main.py --t 3.14

# Plain ASCII without ANSI colour
python main.py --no-color

# Export a high-res PNG (requires Pillow)
python main.py --export render.png
```

### All options

```
usage: main.py [-h] [--scene {classic,solar,disco}]
               [--width W] [--height H] [--depth D]
               [--animate] [--frames N] [--fps F]
               [--no-color] [--export FILE] [--t T]

  --scene     Which scene to render     (default: classic)
  --width     Output width in chars     (default: 80)
  --height    Output height in lines    (default: 38)
  --depth     Max reflection bounces    (default: 4)
  --animate   Run continuous animation
  --frames    Frames per animation loop (default: 60)
  --fps       Target frame rate         (default: 8)
  --no-color  Disable ANSI colour
  --export    Save frame to PNG file
  --t         Time parameter [0, 2π]   (default: 0)
```

---

## Performance

All rendering is single-threaded pure Python. Approximate times on a modern laptop:

| Resolution | Depth | Scene   | Time/frame |
|-----------|-------|---------|-----------|
| 80 × 38   | 4     | classic | ~2–4 s    |
| 80 × 38   | 4     | solar   | ~3–5 s    |
| 120 × 48  | 4     | disco   | ~8–12 s   |
| 80 × 38   | 6     | classic | ~4–7 s    |

> Tip: Reduce `--depth` to 1–2 for faster previews. The checkerboard and solar scenes look fine at depth 2.

---

## Extending the Tracer

### Add a new material property

Edit `raytracer/objects.py` → `Material` dataclass, then use it in `raytracer/renderer.py` → `trace()`.

### Add a new primitive (e.g. Triangle)

Implement an `intersect(ray, t_min, t_max) → Optional[HitRecord]` method matching the `Sphere` interface, then add instances to `scene.objects`.

### Add a new scene

Create `scenes/my_scene.py`:

```python
from raytracer import Scene, Camera, Sphere, Material, PointLight, Vec3

def build_my_scene(t=0.0, width=80, height=38):
    scene = Scene()
    scene.add(Sphere(Vec3(0, 0, 5), 1.0, Material(color=Vec3(1, 0.5, 0))))
    scene.add_light(PointLight(Vec3(3, 5, 0)))
    aspect = (width * 0.5) / height
    camera = Camera(Vec3(0, 0, -3), Vec3(0, 0, 5), Vec3(0,1,0), 60, aspect)
    return scene, camera
```

Then register it in `scenes/__init__.py` and `main.py`'s `_BUILDERS` dict.

---

## Technical Notes

- **No BVH / acceleration structure** — rays test every object. For `n` objects and `w×h` pixels, cost is `O(n·w·h·depth)`. Good enough for demo scenes; add a BVH for larger worlds.
- **Gamma correction** — output luminance is raised to `1/2.2` before the ASCII ramp mapping, matching sRGB monitor expectations.
- **Shadow acne prevention** — shadow rays start at `point + normal × ε` (`ε = 1e-4`) to avoid self-intersection.
- **Flicker-free animation** — uses ANSI cursor-up sequences (`\033[{n}A\r`) rather than clearing the screen, so each frame overwrites in place.

---

## License

MIT — do whatever you like. Attribution appreciated but not required.

---

*Built entirely in Python by Claude — a demonstration that light itself is just math.*
