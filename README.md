# TerminalQuest

```
  ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗
     ██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║
     ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║
     ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║
     ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗
     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝

              ██████╗ ██╗   ██╗███████╗███████╗████████╗
             ██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
             ██║   ██║██║   ██║█████╗  ███████╗   ██║
             ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║
             ╚██████╔╝╚██████╔╝███████╗███████║   ██║
              ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝
```

> **Descend into the abyss. Face the Ancient Dragon. Survive.**

A fully-featured **ASCII roguelike dungeon crawler** built in pure Python — no external dependencies, just your terminal and your wits.

---

## Features

- **Procedural dungeon generation** — unique layouts every run via room-and-corridor BSP placement
- **Bresenham raycasting FOV** — true line-of-sight fog of war (see walls block vision)
- **3 distinct character classes** — Warrior, Mage, and Rogue with asymmetric stats & specials
- **Turn-based tactical combat** — attack, special ability, items, or flee
- **Full item system** — weapons, armour, health/resource potions, and gold treasure
- **7 enemy types** — scaling difficulty from floor 1 Goblins to the Floor 5 Ancient Dragon boss
- **Character progression** — level up mid-dungeon, gaining HP, attack, and defense
- **Persistent high scores** — JSON leaderboard saved to `~/.terminalquest_scores.json`
- **Zero dependencies** — pure Python 3.7+ stdlib (`curses`, `json`, `math`, `random`)

---

## Screenshot

```
##########   ##############               |  Warrior  Lv.3
#........#   #............#               |  Floor: 2 / 5
#...<....#   #..g.........#               |
#........#   #............#               |  HP  78/110
#........+####+...........#               |  [########......] 
##########   #......!.....#               |
             #...........##               |  Stamina  62/90
     ########+#####       #               |  [########......]
     #.........X...#######               |
     #....@........)......#               |  ATK 19   DEF 12
     #.......#......#......               |  Gold  37
     #.......#......#......               |  XP    28/50
     #########......#......               |  Kills 4
              ##########                  |
                                          |  WASD/Arrows  Move
- - - - - - - - - - - - - - - - - - - -  |  G            Pick up
[Floor 2] You hit the Orc for 11 damage. |  C            Special
The Orc hits you for 7 damage.           |  I            Inventory
You pocket 8 gold.                       |  .            Wait
```

*Legend: `@` player · `g` goblin · `O` orc · `s` skeleton · `M` dark mage · `T` troll · `D` demon · `X` dragon*  
*`#` wall · `.` floor · `+` door · `>` stairs down · `<` stairs up · `!` item · `)` weapon · `]` armour · `$` gold*

---

## Character Classes

| Class | HP | ATK | DEF | Resource | Special | Playstyle |
|---|---|---|---|---|---|---|
| **Warrior** | 110 | 15 | 9 | Stamina 90 | Power Strike (2.5× dmg) | Tank — soak hits, brute-force fights |
| **Mage** | 60 | 24 | 3 | Mana 80 | Arcane Blast (2.2× + bonus) | Glass cannon — burst enemies before they reach you |
| **Rogue** | 78 | 13 | 5 | Energy 65 | Shadow Strike (3× dmg) | Skirmisher — 25% crit on every swing, cheapest special |

> **Tip:** Rogues scale best with weapon pickups; Mages should hoard potions for the Dragon fight.

---

## Bestiary

```
Floor 1 ─── g Goblin      HP:16   ATK:5   DEF:1   XP:10
Floor 2 ─── O Orc         HP:30   ATK:10  DEF:3   XP:22
            s Skeleton    HP:24   ATK:12  DEF:5   XP:28
Floor 3 ─── M Dark Mage   HP:22   ATK:18  DEF:2   XP:38
            T Troll       HP:50   ATK:14  DEF:8   XP:55
Floor 4 ─── D Demon       HP:65   ATK:20  DEF:11  XP:85
Floor 5 ─── X Ancient Dragon  HP:130  ATK:28  DEF:16  XP:600  ★ BOSS
```

---

## Dungeon Layout

Each floor is generated fresh using a room-placement algorithm:

```
Step 1 — Place rooms randomly           Step 2 — Connect with L-corridors
  ┌──────┐                                ┌──────┐
  │      │                                │      │
  │  R1  │   ┌────┐                       │  R1  ├─────┐
  │      │   │ R2 │          ──►          │      │  R2 │
  └──────┘   │    │                       └──────┘     │
             └────┘                              ┌─────┘
       ┌───────────┐                             │  ┌───────────┐
       │    R3     │                             └──┤    R3     │
       └───────────┘                               └───────────┘

Step 3 — Fog of war (Bresenham raycasting)
  ░░░░░░░░░░░░░░░
  ░░#############░░          Key:  ░ unexplored
  ░░#...........#░░                # dim-revealed wall
    #.....@.....#                  . dim-revealed floor
    #...........#                  @ player (full bright)
  ░░#############░░                8-radius sight cone
  ░░░░░░░░░░░░░░░
```

---

## Installation

**Requirements:** Python 3.7+ (stdlib only)

```bash
# Clone the repo
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Run directly
python run.py

# Or as a module
python -m terminalquest.main
```

> Windows users: `curses` is included in the standard CPython distribution.  
> For best results use a terminal with at least **85 × 28** characters and UTF-8 support.

---

## Controls

| Key | Action |
|---|---|
| `W` / `↑` | Move north |
| `S` / `↓` | Move south |
| `A` / `←` | Move west |
| `D` / `→` | Move east |
| `G` | Pick up item / gold on current tile |
| `C` | Use special ability (targets nearest visible enemy) |
| `I` | Open inventory — press `1-9` to use a consumable |
| `.` | Wait one turn (regenerates 3 resource) |
| `Q` | Quit to title |
| `Enter` | Confirm on menus |
| `Esc` | Close inventory without using an item |

### Combat
Moving into an enemy tile attacks them. Each attack round:
1. Your strike resolves (with crit chance if Rogue)
2. Enemy immediately retaliates if still alive

---

## Scoring

```
Score = (floor × 500) + (kills × 20) + gold_collected + (level × 100)
```

Top 20 scores are saved to `~/.terminalquest_scores.json` and displayed in the Hall of Fame after each run.

---

## Gameplay Tips

- **Conserve your special** — resource does not refill automatically; wait (`.`) or drink potions.
- **Fog of war protects you** — enemies only activate when you can see them. Use doorways as choke points.
- **Upgrade early** — weapons and armour found on later floors are strictly better; always equip the best one.
- **Mage strategy** — open every fight with Arcane Blast, then finish with normal attacks. Never stand adjacent to a Troll.
- **Dragon fight (Floor 5)** — the boss spawns in the *last* room. Arrive with full HP and at least one Greater Potion.

---

## Architecture

```
clauder/
├── run.py                    # Repo-root launcher
├── README.md
└── terminalquest/
    ├── __init__.py
    ├── main.py               # Entry point, curses.wrapper()
    ├── game.py               # Game loop, player actions, enemy AI
    ├── dungeon.py            # Procedural generation + Bresenham FOV
    ├── entities.py           # Player / Enemy classes, spawn logic
    ├── items.py              # Item definitions, dungeon spawning
    ├── combat.py             # Damage formulas, special abilities
    ├── renderer.py           # Curses rendering engine
    └── scores.py             # JSON high-score persistence
```

### Data flow

```
main.py
  └── Game (game.py)
        ├── Dungeon (dungeon.py)   ← BSP generation + FOV
        ├── Player  (entities.py)  ← stats, inventory, XP
        ├── Enemy[] (entities.py)  ← AI movement, combat
        ├── Item[]  (items.py)     ← pickups, effects
        ├── combat.py              ← pure damage functions
        ├── Renderer (renderer.py) ← curses draw calls
        └── scores.py              ← save/load JSON
```

---

## License

MIT — do whatever you like with it.

---

*Built by Claude (claude-sonnet-4-6) as an autonomous creative coding project — July 2026.*
