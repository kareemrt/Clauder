# FractalDreams

> *A journey through infinite mathematics — rendered live in your terminal.*

**FractalDreams** is a pure-Python fractal explorer that renders the Mandelbrot set, Julia sets, the Burning Ship, Newton basins, and the Tricorn directly in your terminal using smooth-colored ASCII art and optional Claude AI narration.

---

## Gallery

All renders below are real output from the program — no post-processing.

### The Mandelbrot Set

```
                  ..............................................................
                ..............................'''''''''''''''...................
               ...........................'''''''''``,"```''''''................
              ........................''''''''''''```^,;"^`'''''''..............
            .......................''''''''''''```^I;1r l:^``'''''''............
            ....................'''''''''''``````^^>     >"^`````'''''..........
           ..................'''''''''''```"_I,"X>OZc  c hl:i,^^^,^`'''.........
          ...............'''''''''''''````^"+                    !"`''''........
          ..........'''''''`````````````^"{ k                   -,^``''''.......
         .......''''''''''``:"^"^,,^^^^^"j                         !^''''.......
         ....''''''''''''```^"> >    !,,:                         I,`'''''......
         ...''''''''````^,^",]          i                         [^`'''''......
        ....''```^`^`^^"":<             x                        i^``'''''......
        ....''```^`^`^^"":<             x                        i^``'''''......
         ...''''''''````^,^",]          i                         [^`'''''......
         ....''''''''''''```^"> >    !,,:                         I,`'''''......
         .......''''''''''``:"^"^,,^^^^^"j                         !^''''.......
          ..........'''''''`````````````^"{ k                   -,^``''''.......
          ...............'''''''''''''````^"+                    !"`''''........
           ..................'''''''''''```"_I,"X>OZc  c hl:i,^^^,^`'''.........
            ....................'''''''''''``````^^>     >"^`````'''''..........
            .......................''''''''''''```^I;1r l:^``'''''''............
              ........................''''''''''''```^,;"^`'''''''..............
               ...........................'''''''''``,"```''''''................
                ..............................''''''''''''''''...................
```

The iconic cardioid (period-1 bulb) and its attached period-2 disk dominate the center.
Every point of the set has its own infinite filament structure extending into the plane.

---

### Seahorse Valley — 512× zoom

```
>|Q[J (}drX0&z([-_[+_0|L)x)&w_-<>~(x>oIIIIIIIIIIII>+-?xXtcJ d          *dw0Uvxu/
 [-[}jO     p(} -_%}1tt\XQ(-Lm[(_&MU _<~ -IIIIIIIIll<-{1 J@Oh           ab aY vx
t)fUq        ftb&[[[1cx[ ++__- utav+-z})_ -J|llllllllO \O  O0O     8    qam YUh
_-}t          nX(1c (  pB8d)<>>>>><>>>>>>><< ~\ !lllllj jfQuXuX Om  Z 0p%#Q dpu
>fx_{ d     M   }X -uxf}<Uj_>>>>>>>>>>>>>><<<<<~ur!!!!!~u~?1YLqc uk mcd Yvv   Yj
}uL| |}}zn@ *()jn(f~<>>>>>>>>>>>>>>>>>>><(__/)~~+(i!!!!!!r]1YfU  Zfr M @jrh   r/
__][xx\?-___unn}Cu|<>>>>>>>>>>>iiiiiiii>>-()Qd] }ii!!!!!!ii++rZv|   8 |// dL Y a
f an}u_________-nX>>>>>>>>>>iiiiiiiiiiiiiiiiiiiiiii!!!!!ii+  j+@b]][))  d   U\ 1
 [[[z?z__+++u]?1<<<<><>>>>>>iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii _+  ){av  mQa/rU
))x //U___B+_Yr\  0w//x_|>>>iiiiiiiiiiiiiiiiiiiiiiiiiiiiiii>Qr  jr {10 @#/ ]]]][
 {kf tJ)c[}Bxo M     +_Z_>>>>iiiiiiiiiiiiiiiiiiiiiiiiiii [c  MqLqLQ__10  \?M]]]]
+++_/pr}[cxnw/twxw # Y>>>>>>>iiiiiiiiiiiiiiiiiiiiiiiiiiii>>>><~ +++++++___@([[[[
<  Z} }p[q c|z ))f v| z->>>>>>iiiiiiiiiiiiiiiiiiiiiiiiiii>>L }__++++++++__  f J
>u__pCbtb  B JCj[[[Y___c><<>>>>>>>>>>>>>>>>Bh>>iiiiii>>/fxcU}(___+++_-  _& xd  t
```

Seahorse Valley sits along the boundary of the main cardioid at x ≈ −0.746.
The spiraling tendrils are period-doubling cascades visible at any zoom level.

---

### Julia Set — Douady Rabbit (c = −0.1226 + 0.7449i)

```
                              .......' '....
           .. ''...................''`";   ...
        .....'    '''''" `'....''"      "'.....
      .  '                   ```"       ^ '.......
     .   '    `'`               ,    ^`'''..........
      ...........'`            ",      ^ `'^''.........
           .......'  '''^"'''``"             "^'`   '....
               ............'''                       '.....
                  ..........'^                    `'.........
                    .........'`                    ^'..........
                      .....'                       '''............
                        ....'   `'^"             "``'''"^'''  '.......
                          .........''^'` ^      ,"            `'...........
                             ..........'''`^    ,               `'`    '   .
                               .......' ^       "```                   '  .
                                  .....'"      "''....' "'''''    '.....
                                   ...   ;"`''...................'' ..
                                     ....' '.......
```

The Douady Rabbit is named for Adrien Douady who discovered it. Three interlocked
spiraling lobes emerge because c lies in the period-3 bulb of the Mandelbrot set.

---

### The Burning Ship (full view)

```
                                                   ................
                                              .......................
                                         .............................
                                  ....................''''````''.......
                         .........................'''`^:         '......
                ...........................'''''``")             '.......
   .......................''''''''''''''```^"l                   ........
 .....'''''''''''`^^"":~                                      ''.........
 ..........''`                                               ^''.........
 .............};)                                            "`''.........
    ............`!cC                                         ;`''.........
         ..........I'..'                                      ,`''.........
                ........I^]                                     ^''.........
                    ....`x,~`'h@j                                +`''.........
                     ....^",'I_X`zl !                              "''......
                      ...^,:"`"{,  i[/: /' {                         ^''......
                       ....^,:''lii`"}rI`^`|)'B I                      ;`'....
```

Invented independently by Michael Michelitsch and Otto E. Rössler in 1992.
The fold `z ↦ (|Re z| + i|Im z|)²` breaks the up-down symmetry of the Mandelbrot set,
creating the eerie silhouette of a flaming ship beneath the complex plane.

---

### Newton's Basins of Attraction (f(z) = z³ − 1)

```
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓░░░▓▓░░░░░
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓ ░    ░░░▓▓░░
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓ ▓░░░░░░ ▒▒▓░
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓░░░░░░░░░░░▓
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▒░░░░▓░
░░▓░░░▓▓▒▒▒▒▒▓░░▓▒▒▒▒▒▒▒▒▒▓░░▒▓▓▒▒▒▒▒▒▒▓░░░░░░░▒
         ░▓▓░░░▒      ▒▓▓░░           ▓▓░░░░
         ▓░░▓▓▓▓      ▓░░▓▓          ▒░░░▓▓░
▒▓▒▓▓░░░░░░░░░░▓░░░░░░░░░░░▓░░░░░░░░░░░░░▓▒▒▒▒▓░
░░░░░░░░░░░░░░░░░                    ░░░▓░▒▒▒▒▒▒▓▓▓
░░░░░░░░░░                              ░░ ░ ▒▒▒░░░
```

Each shade represents one of three roots of z³ = 1 (at 1, e^{2πi/3}, e^{4πi/3}).
Where basins meet, the iteration becomes chaotic — the boundary is a fractal of measure zero
and has the property that every basin-boundary point touches all three basins simultaneously.

---

## Features

| Feature | Description |
|---|---|
| **5 Fractal Types** | Mandelbrot, Julia, Burning Ship, Newton, Tricorn |
| **7 Color Palettes** | fire, ocean, galaxy, psychedelic, electric, newton, mono |
| **3 Character Sets** | dense (70-char gradient), simple, unicode blocks |
| **14 Curated Presets** | Famous locations: Seahorse Valley, Douady Rabbit, Starfish… |
| **Smooth Coloring** | Eliminates banding via escape-time potential function |
| **AI Narration** | Claude API generates mathematical + poetic descriptions |
| **Save to File** | Export plain-text renders for sharing |
| **Auto Terminal Size** | Renders adapt to your terminal dimensions |

---

## Architecture

```
fractal-dreams/
│
├── fractal_dreams/
│   ├── __init__.py        ← package metadata
│   │
│   ├── fractals.py        ← core math
│   │   ├── mandelbrot()   ← z² + c iteration
│   │   ├── julia()        ← fixed-c Julia sets
│   │   ├── burning_ship() ← |Re z| + i|Im z| fold
│   │   ├── newton()       ← Newton-Raphson on z³−1
│   │   ├── tricorn()      ← conjugate iteration
│   │   └── compute_frame()← parallel viewport grid
│   │
│   ├── palette.py         ← color mathematics
│   │   ├── fire()         ← black → red → yellow → white
│   │   ├── ocean()        ← midnight → teal → foam
│   │   ├── galaxy()       ← purple → violet → starlight
│   │   ├── psychedelic()  ← HSV hue cycling
│   │   ├── electric()     ← sine-wave cyan on black
│   │   └── newton_palette()← three-basin RGB map
│   │
│   ├── renderer.py        ← ASCII/ANSI engine
│   │   ├── render_frame() ← colored ANSI output
│   │   └── render_frame_plain() ← no-color file output
│   │
│   ├── presets.py         ← curated gallery
│   │   ├── MANDELBROT_PRESETS  (6 locations)
│   │   ├── JULIA_PRESETS       (5 Julia sets)
│   │   └── EXOTIC_PRESETS      (3 exotic types)
│   │
│   ├── narrator.py        ← Claude API integration
│   │   └── narrate()      ← prompt-cached AI narration
│   │
│   └── cli.py             ← command-line interface
│       ├── render         ← render one fractal
│       ├── gallery        ← list presets
│       ├── explore        ← batch render category
│       └── info           ← mathematical background
│
├── main.py                ← entry point
├── requirements.txt
└── pyproject.toml
```

---

## The Mathematics

### Escape-Time Algorithm

Every fractal here is based on iterating a function on the complex plane and asking:
**does the orbit of point z escape to infinity?**

```
Mandelbrot:    f_c(z) = z² + c          (z₀ = 0, c = pixel)
Julia:         f_c(z) = z² + c          (z₀ = pixel, c = fixed parameter)
Burning Ship:  f_c(z) = (|Re z| + i|Im z|)² + c
Tricorn:       f_c(z) = z̄² + c          (z̄ = complex conjugate)
Newton:        z ↦ z − f(z)/f'(z)       (f(z) = z³ − 1)
```

A point escapes if `|z_n| > 2` for some n. The **iteration count** n becomes the color.

### Smooth Coloring

Integer iteration counts create ugly banding. The smooth value removes it:

```
smooth = n + 1 − log₂(log|z_n|)
```

This uses the **potential function** of the Mandelbrot set — the harmonic measure of
the complement — to interpolate continuously between integer escape times.

### The Mandelbrot–Julia Duality

Every parameter c corresponds to exactly one Julia set J(c). The Mandelbrot set M is:

```
M = { c ∈ ℂ : J(c) is connected }
```

If c ∈ M, the Julia set is a connected fractal (like the rabbit). If c ∉ M, it
shatters into a Cantor dust of infinitely many disconnected pieces.

---

## Installation

```bash
git clone https://github.com/kareemrt/clauder.git
cd clauder
pip install -e .
```

**Optional** — for AI narration:

```bash
pip install anthropic
export ANTHROPIC_API_KEY="your-key-here"
```

---

## Usage

### List available presets

```bash
python main.py gallery
```

```
  ── Mandelbrot Set ─────────────────────────────────────
  • Full Mandelbrot                  The classic overview…
  • Seahorse Valley                  Spiraling seahorse-shaped filaments…
  • Elephant Valley                  Repeating elephant-trunk spirals…
  • Starfish                         A five-fold symmetric starfish…
  • Lightning Tendrils               Charged filaments radiating…
  • Miniature Mandelbrot             A perfect mini-copy of the full set…

  ── Julia Sets ─────────────────────────────────────────
  • Douady Rabbit                    Three interlocked spiraling rabbit ears…
  • San Marco Dragon                 A basilica-like structure…
  • Dendrite                         Crystalline dendrite growing…
  • Siegel Disk                      Smooth quasi-periodic rotation disk…
  • Snowflake                        Six-fold symmetric snowflake Julia set…

  ── Exotic Fractals ────────────────────────────────────
  • Burning Ship                     The ghostly burning ship…
  • Newton's Basins                  Three-basin attraction zones…
  • Tricorn                          The Mandelbar set…
```

### Render a named preset

```bash
python main.py render "Seahorse Valley"
python main.py render "Douady Rabbit" --palette psychedelic
python main.py render "Newton's Basins" --charset blocks
```

### Custom viewport

```bash
python main.py render \
  --fractal mandelbrot \
  --xmin -0.7466 --xmax -0.7464 \
  --ymin 0.1012 --ymax 0.1014 \
  --iter 2048 \
  --palette ocean
```

### Render with AI narration (requires `ANTHROPIC_API_KEY`)

```bash
python main.py render "Starfish" --narrate
```

Output:
```
  ✦  You are looking at one of the most astonishing features in the Mandelbrot
     set: a five-fold symmetric miniature at the tip of a thin filament…
```

### Save to file

```bash
python main.py render "Full Mandelbrot" --save mandelbrot.txt
```

### Explore an entire category

```bash
python main.py explore julia --pause
python main.py explore all
```

### Mathematical background

```bash
python main.py info
```

---

## Color Palettes

| Palette | Colors | Best for |
|---|---|---|
| `fire` | Black → red → orange → white | Mandelbrot overview |
| `ocean` | Midnight blue → teal → cyan | Deep zooms |
| `galaxy` | Purple → violet → starlight | Julia sets |
| `psychedelic` | Full HSV hue rotation | Exotic types |
| `electric` | Black → cyan → white | Seahorse Valley |
| `newton` | Three-color basin map | Newton fractals |
| `mono` | Black to white gradient | File export |

---

## Preset Gallery Reference

### Mandelbrot Presets

| Name | Zoom | Iterations | Notable Feature |
|---|---|---|---|
| Full Mandelbrot | 1× | 256 | Complete set overview |
| Seahorse Valley | ~2000× | 1024 | Spiraling seahorse filaments |
| Elephant Valley | ~1500× | 512 | Repeating elephant trunks |
| Starfish | ~50,000× | 2048 | Five-fold symmetry |
| Lightning Tendrils | ~2,000,000× | 4096 | Electric filament structure |
| Miniature Mandelbrot | ~5000× | 512 | Embedded copy of the full set |

### Julia Presets

| Name | c parameter | Character |
|---|---|---|
| Douady Rabbit | −0.1226 + 0.7449i | Three interlocked lobes |
| San Marco Dragon | −0.7269 + 0.1889i | Two-fold basilica |
| Dendrite | 0 + 1i | Crystalline tree |
| Siegel Disk | −0.3905 − 0.5875i | Smooth quasiperiodic disk |
| Snowflake | −1.755 + 0i | Symmetric six-pointed form |

---

## AI Narration with Claude

FractalDreams integrates the **Claude API** to generate mathematical + poetic descriptions
of fractal renders. The system uses **prompt caching** so the system prompt is cached
across narration calls — keeping API costs low when exploring multiple presets.

```python
# narrator.py excerpt — cached system prompt
response = client.messages.create(
    model="claude-opus-4-7",
    system=[{
        "type": "text",
        "text": SYSTEM_PROMPT,
        "cache_control": {"type": "ephemeral"},  # cached across calls
    }],
    messages=[{"role": "user", "content": fractal_context}],
)
```

Each narration blends rigorous mathematics with lyrical wonder:

> *"You are looking at Seahorse Valley, a region along the boundary of the main
> cardioid where period-doubling cascades produce infinite spiraling tendrils.
> Each spiral is a miniature version of the seahorse at the next scale, repeating
> forever — a concrete example of self-similarity in a non-self-similar fractal."*

---

## Requirements

- Python 3.11+
- `anthropic >= 0.40.0` (optional, for AI narration)
- A terminal with ANSI 24-bit color support (most modern terminals)

---

## License

MIT — do whatever you want with it. Just look at fractals.
