"""Curses-based terminal renderer."""

import curses
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .dungeon import Dungeon
    from .entities import Player

# Color pair IDs
_WALL = 1
_FLOOR = 2
_PLAYER = 3
_GREEN = 4
_RED = 5
_WHITE = 6
_MAGENTA = 7
_ITEM = 8
_STAIRS = 9
_GOLD = 10
_HP_HI = 11
_HP_MID = 12
_HP_LO = 13
_TITLE = 14
_HLITE = 15

VIEW_W = 62
VIEW_H = 22
LOG_LINES = 5

_ENEMY_COLOR = {
    "green": _GREEN,
    "red": _RED,
    "white": _WHITE,
    "magenta": _MAGENTA,
}


def _init_colors() -> None:
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(_WALL, curses.COLOR_WHITE, -1)
    curses.init_pair(_FLOOR, curses.COLOR_BLACK, -1)
    curses.init_pair(_PLAYER, curses.COLOR_CYAN, -1)
    curses.init_pair(_GREEN, curses.COLOR_GREEN, -1)
    curses.init_pair(_RED, curses.COLOR_RED, -1)
    curses.init_pair(_WHITE, curses.COLOR_WHITE, -1)
    curses.init_pair(_MAGENTA, curses.COLOR_MAGENTA, -1)
    curses.init_pair(_ITEM, curses.COLOR_YELLOW, -1)
    curses.init_pair(_STAIRS, curses.COLOR_CYAN, -1)
    curses.init_pair(_GOLD, curses.COLOR_YELLOW, -1)
    curses.init_pair(_HP_HI, curses.COLOR_GREEN, -1)
    curses.init_pair(_HP_MID, curses.COLOR_YELLOW, -1)
    curses.init_pair(_HP_LO, curses.COLOR_RED, -1)
    curses.init_pair(_TITLE, curses.COLOR_CYAN, -1)
    curses.init_pair(_HLITE, curses.COLOR_BLACK, curses.COLOR_CYAN)


class Renderer:
    def __init__(self, stdscr: Any):
        self.scr = stdscr
        self.max_y, self.max_x = stdscr.getmaxyx()
        _init_colors()
        curses.curs_set(0)
        self.messages: List[str] = []

    # ------------------------------------------------------------------ #
    # Public interface
    # ------------------------------------------------------------------ #

    def add_message(self, msg: str) -> None:
        self.messages.append(msg)
        if len(self.messages) > 200:
            self.messages = self.messages[-200:]

    def draw_game(self, dungeon: "Dungeon", player: "Player") -> None:
        self.scr.erase()
        self.max_y, self.max_x = self.scr.getmaxyx()

        # Viewport offset — keep player centred
        vx = max(0, min(player.x - VIEW_W // 2, dungeon.width - VIEW_W))
        vy = max(0, min(player.y - VIEW_H // 2, dungeon.height - VIEW_H))

        self._draw_dungeon(dungeon, player, vx, vy)
        self._draw_ui(VIEW_W + 2, dungeon, player)
        self._draw_messages(VIEW_H + 1)
        self._draw_border()
        self.scr.refresh()

    def show_title(self) -> None:
        self.scr.erase()
        self.max_y, self.max_x = self.scr.getmaxyx()
        banner = [
            r" ___  ____  ____  __  __  __  __ _   __   __      ",
            r"  |  |  __ |  __||  \/  || |  | \|  / \  | |      ",
            r"  |  |  _| |  _| | \  / || |  |  .  | |  | |      ",
            r"  |  | |__ | |   | |\/| || |__| |\  | |  | |      ",
            r"  |  |____||_|   |_|  |_||____|_| \_|_|  |_|      ",
            r"                                                    ",
            r"  ___  _   _  ____  ____  ___                      ",
            r" / _ \| | | || ___||  __||  _|                     ",
            r"| |_| | |_| || |_  | |__ | |_                      ",
            r"|  _  ||  _  ||  _| |  __||  _|                    ",
            r"|_| |_||_| |_||____||____||_|                       ",
        ]
        sy = max(0, self.max_y // 2 - len(banner) // 2 - 4)
        for i, line in enumerate(banner):
            sx = max(0, self.max_x // 2 - len(line) // 2)
            self._str(sy + i, sx, line, curses.color_pair(_TITLE) | curses.A_BOLD)

        y = sy + len(banner) + 1
        sub = "Descend into the abyss.  Face the Ancient Dragon.  Survive."
        self._str(y, max(0, self.max_x // 2 - len(sub) // 2), sub)
        y += 2
        prompt = "[ Press ENTER to begin  |  Q to quit ]"
        self._str(
            y,
            max(0, self.max_x // 2 - len(prompt) // 2),
            prompt,
            curses.color_pair(_HLITE),
        )
        self.scr.refresh()

    def show_class_select(self) -> None:
        from .entities import CLASS_STATS, CharClass

        self.scr.erase()
        self.max_y, self.max_x = self.scr.getmaxyx()
        self._str(2, 4, "Choose Your Class", curses.color_pair(_TITLE) | curses.A_BOLD)
        self._str(3, 4, "─" * 40, curses.A_DIM)

        rows = [
            (CharClass.WARRIOR, "1"),
            (CharClass.MAGE, "2"),
            (CharClass.ROGUE, "3"),
        ]
        y = 5
        for cls, key in rows:
            s = CLASS_STATS[cls]
            self._str(y, 4, f"[{key}]  {cls.value}", curses.A_BOLD)
            y += 1
            self._str(y, 9, s["description"], curses.A_DIM)
            y += 1
            self._str(
                y,
                9,
                f"HP:{s['hp']}  ATK:{s['attack']}  DEF:{s['defense']}  "
                f"{s['resource_name']}:{s['resource']}",
            )
            y += 1
            self._str(
                y,
                9,
                f"Special: {s['special_name']} (costs {s['special_cost']} {s['resource_name']})",
                curses.color_pair(_ITEM),
            )
            y += 2
        self.scr.refresh()

    def show_inventory(self, player: "Player") -> Optional[int]:
        self.scr.erase()
        self.max_y, self.max_x = self.scr.getmaxyx()
        self._str(1, 3, "INVENTORY", curses.A_BOLD | curses.color_pair(_TITLE))
        self._str(2, 3, "─" * 35, curses.A_DIM)

        y = 4
        if not player.inventory:
            self._str(y, 3, "Your pack is empty.")
        else:
            for i, item in enumerate(player.inventory):
                self._str(
                    y + i,
                    3,
                    f"[{i+1}] {item.name:<22} {item.description}",
                    curses.color_pair(_ITEM),
                )
        y += max(1, len(player.inventory)) + 1
        self._str(y, 3, f"Gold carried: {player.gold}", curses.color_pair(_GOLD))
        y += 2
        self._str(y, 3, "Press 1-9 to use an item  |  ESC to close.")
        self.scr.refresh()

        while True:
            k = self.scr.getch()
            if k == 27:
                return None
            if ord("1") <= k <= ord("9"):
                idx = k - ord("1")
                if idx < len(player.inventory):
                    return idx

    def show_game_over(self, player: "Player", won: bool) -> None:
        self.scr.erase()
        self.max_y, self.max_x = self.scr.getmaxyx()
        y = max(0, self.max_y // 2 - 6)

        if won:
            headline = "VICTORY!  The Ancient Dragon lies slain!"
            sub = "The dungeon falls silent.  You are legend."
            attr = curses.color_pair(_TITLE) | curses.A_BOLD
        else:
            headline = "YOU HAVE PERISHED..."
            sub = "The dungeon claims another soul."
            attr = curses.color_pair(_RED) | curses.A_BOLD

        self._str(y, max(0, self.max_x // 2 - len(headline) // 2), headline, attr)
        y += 2
        self._str(y, max(0, self.max_x // 2 - len(sub) // 2), sub)
        y += 3

        for line in [
            f"Hero: {player.name}  ({player.char_class.value})",
            f"Floor Reached: {player.dungeon_level}  |  Character Level: {player.level}",
            f"Kills: {player.kills}  |  Gold: {player.gold}",
            f"Final Score: {player.score():,}",
        ]:
            self._str(y, max(0, self.max_x // 2 - len(line) // 2), line)
            y += 1

        y += 2
        p = "[ Press ENTER to see High Scores ]"
        self._str(y, max(0, self.max_x // 2 - len(p) // 2), p, curses.color_pair(_HLITE))
        self.scr.refresh()
        while self.scr.getch() not in (10, 13):
            pass

    def show_highscores(self, scores: List[Dict]) -> None:
        self.scr.erase()
        self.max_y, self.max_x = self.scr.getmaxyx()
        self._str(1, 4, "HALL OF FAME", curses.color_pair(_TITLE) | curses.A_BOLD)
        self._str(2, 4, "─" * 55, curses.A_DIM)

        hdr = f"{'#':<4} {'Name':<12} {'Class':<10} {'Flr':<5} {'Kills':<7} {'Score':>8}"
        self._str(3, 4, hdr, curses.A_BOLD)
        self._str(4, 4, "─" * 55, curses.A_DIM)

        for i, s in enumerate(scores[:10], 1):
            line = (
                f"{i:<4} {s['name'][:11]:<12} {s['class'][:9]:<10} "
                f"{s['floor']:<5} {s['kills']:<7} {s['score']:>8,}"
            )
            attr = curses.color_pair(_GOLD) | curses.A_BOLD if i == 1 else 0
            self._str(4 + i, 4, line, attr)

        y = 16
        p = "[ N — new game  |  Q — quit ]"
        self._str(y, max(0, self.max_x // 2 - len(p) // 2), p, curses.color_pair(_HLITE))
        self.scr.refresh()

    # ------------------------------------------------------------------ #
    # Private drawing helpers
    # ------------------------------------------------------------------ #

    def _draw_dungeon(
        self, dungeon: "Dungeon", player: "Player", vx: int, vy: int
    ) -> None:
        for dy in range(min(VIEW_H, dungeon.height)):
            for dx in range(min(VIEW_W, dungeon.width)):
                mx, my = vx + dx, vy + dy
                if not (0 <= mx < dungeon.width and 0 <= my < dungeon.height):
                    continue
                if not dungeon.revealed[my][mx]:
                    continue

                tile = dungeon.tiles[my][mx]
                vis = dungeon.visible[my][mx]

                if vis:
                    if (mx, my) == (player.x, player.y):
                        self._ch(dy, dx, "@", curses.color_pair(_PLAYER) | curses.A_BOLD)
                    elif (mx, my) in dungeon.enemy_map:
                        e = dungeon.enemy_map[(mx, my)]
                        cp = curses.color_pair(_ENEMY_COLOR.get(e.color, _WHITE))
                        self._ch(dy, dx, e.symbol, cp | curses.A_BOLD)
                    elif (mx, my) in dungeon.item_map:
                        item = dungeon.item_map[(mx, my)]
                        cp = curses.color_pair(_GOLD if item.symbol == "$" else _ITEM)
                        self._ch(dy, dx, item.symbol, cp | curses.A_BOLD)
                    elif tile == "#":
                        self._ch(dy, dx, "#", curses.color_pair(_WALL))
                    elif tile in (">", "<"):
                        self._ch(dy, dx, tile, curses.color_pair(_STAIRS) | curses.A_BOLD)
                    else:
                        self._ch(dy, dx, ".", curses.color_pair(_FLOOR) | curses.A_DIM)
                else:
                    dim = curses.A_DIM
                    if tile == "#":
                        self._ch(dy, dx, "#", dim)
                    elif tile in (">", "<"):
                        self._ch(dy, dx, tile, dim)
                    else:
                        self._ch(dy, dx, ".", dim)

    def _draw_ui(self, x: int, dungeon: "Dungeon", player: "Player") -> None:
        y = 0
        name_line = f" {player.name} "
        self._str(y, x, name_line, curses.color_pair(_TITLE) | curses.A_BOLD)
        y += 1
        self._str(y, x, f" {player.char_class.value}  Lv.{player.level}")
        y += 1
        self._str(y, x, f" Floor: {dungeon.level} / 5")
        y += 2

        # HP bar
        hp_pct = player.hp / player.max_hp
        if hp_pct > 0.55:
            hcp = curses.color_pair(_HP_HI)
        elif hp_pct > 0.25:
            hcp = curses.color_pair(_HP_MID)
        else:
            hcp = curses.color_pair(_HP_LO)
        self._str(y, x, f" HP  {player.hp}/{player.max_hp}", hcp)
        y += 1
        self._str(y, x, " " + _bar(hp_pct, 14), hcp)
        y += 2

        # Resource bar
        rp = player.resource / player.max_resource
        self._str(y, x, f" {player.resource_name}  {player.resource}/{player.max_resource}",
                  curses.color_pair(_TITLE))
        y += 1
        self._str(y, x, " " + _bar(rp, 14), curses.color_pair(_TITLE))
        y += 2

        self._str(y, x, f" ATK {player.total_attack:<4} DEF {player.total_defense}")
        y += 1
        self._str(y, x, f" Gold  {player.gold}")
        y += 1
        self._str(y, x, f" XP    {player.xp}/{player.xp_to_next}")
        y += 1
        self._str(y, x, f" Kills {player.kills}")
        y += 2

        for label in (
            " WASD/Arrows  Move",
            " G            Pick up",
            " C            Special",
            " I            Inventory",
            " .            Wait",
            " Q            Quit",
        ):
            self._str(y, x, label, curses.A_DIM)
            y += 1

    def _draw_messages(self, top_y: int) -> None:
        recent = self.messages[-LOG_LINES:]
        pad = [""] * (LOG_LINES - len(recent)) + recent
        for i, msg in enumerate(pad):
            attr = 0 if i == LOG_LINES - 1 else curses.A_DIM
            self._str(top_y + i, 0, msg[:VIEW_W], attr)

    def _draw_border(self) -> None:
        for row in range(VIEW_H + LOG_LINES + 2):
            self._ch(row, VIEW_W, "|", curses.A_DIM)
        for col in range(min(self.max_x, VIEW_W)):
            self._ch(VIEW_H, col, "-", curses.A_DIM)

    # ------------------------------------------------------------------ #
    # Low-level safe wrappers
    # ------------------------------------------------------------------ #

    def _ch(self, y: int, x: int, ch: str, attr: int = 0) -> None:
        try:
            if 0 <= y < self.max_y and 0 <= x < self.max_x:
                self.scr.addch(y, x, ch, attr)
        except curses.error:
            pass

    def _str(self, y: int, x: int, s: str, attr: int = 0) -> None:
        try:
            if 0 <= y < self.max_y and 0 <= x < self.max_x:
                self.scr.addstr(y, x, s[: self.max_x - x], attr)
        except curses.error:
            pass


def _bar(pct: float, length: int) -> str:
    filled = int(length * max(0.0, min(1.0, pct)))
    return "[" + "#" * filled + "." * (length - filled) + "]"
