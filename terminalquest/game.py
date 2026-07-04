"""Core game loop and state management."""

import curses
import random
from typing import List, Optional

from .combat import enemy_attack, player_attack, player_special
from .dungeon import Dungeon
from .entities import CharClass, Enemy, Player, spawn_enemies
from .items import Item, ItemType, spawn_items
from .renderer import Renderer
from .scores import load_scores, save_score

_MAX_LEVEL = 5
_FOV_RADIUS = 9
_ENEMIES_PER_LEVEL = [0, 6, 9, 11, 13, 8]  # index = floor number


class Game:
    def __init__(self, stdscr: object):
        self.stdscr = stdscr
        self.renderer = Renderer(stdscr)  # type: ignore[arg-type]
        self.player: Optional[Player] = None
        self.dungeon: Optional[Dungeon] = None
        self.enemies: List[Enemy] = []
        self.items: List[Item] = []
        self.running = False
        self.won = False
        stdscr.timeout(80)  # type: ignore[union-attr]

    # ------------------------------------------------------------------ #
    # Top-level flow
    # ------------------------------------------------------------------ #

    def run(self) -> None:
        while True:
            # Title
            self.renderer.show_title()
            k = self._wait_for_enter_or_quit()
            if k == ord("q"):
                return

            # Class select
            self.renderer.show_class_select()
            cls = self._pick_class()
            if cls is None:
                continue

            # Initialise player with class name as hero name
            self.player = Player(cls.value, cls)
            self._load_floor(1)
            self._game_loop()

            # End screens
            assert self.player is not None
            self.renderer.show_game_over(self.player, self.won)
            save_score(self.player)
            self.renderer.show_highscores(load_scores())

            k = self.stdscr.getch()  # type: ignore[union-attr]
            if k == ord("q"):
                return
            # 'n' or anything else restarts

    # ------------------------------------------------------------------ #
    # Per-floor setup
    # ------------------------------------------------------------------ #

    def _load_floor(self, level: int) -> None:
        assert self.player is not None
        self.dungeon = Dungeon(level=level)
        count = _ENEMIES_PER_LEVEL[min(level, _MAX_LEVEL)]
        self.enemies = spawn_enemies(self.dungeon, level, count)
        self.items = spawn_items(self.dungeon, level)

        px, py = self.dungeon.stairs_up or self.dungeon.rooms[0].center
        self.player.x, self.player.y = px, py
        self.player.dungeon_level = level
        self.dungeon.compute_fov(px, py, _FOV_RADIUS)

        self.renderer.add_message(f"You descend to floor {level}.")
        if level == _MAX_LEVEL:
            self.renderer.add_message("A deep rumble shakes the walls...")

    # ------------------------------------------------------------------ #
    # Main game loop
    # ------------------------------------------------------------------ #

    def _game_loop(self) -> None:
        assert self.player is not None
        assert self.dungeon is not None
        self.running = True
        self.won = False

        while self.running and self.player.is_alive():
            self.renderer.draw_game(self.dungeon, self.player)
            k = self.stdscr.getch()  # type: ignore[union-attr]
            if k == -1:
                continue

            moved = False

            if k in (ord("w"), curses.KEY_UP):
                moved = self._try_move(0, -1)
            elif k in (ord("s"), curses.KEY_DOWN):
                moved = self._try_move(0, 1)
            elif k in (ord("a"), curses.KEY_LEFT):
                moved = self._try_move(-1, 0)
            elif k in (ord("d"), curses.KEY_RIGHT):
                moved = self._try_move(1, 0)
            elif k == ord("g"):
                moved = self._pickup()
            elif k == ord("i"):
                self._open_inventory()
            elif k == ord("c"):
                moved = self._use_special()
            elif k == ord("."):
                # Rest: regenerate resource, enemies act
                self.player.resource = min(
                    self.player.resource + 3, self.player.max_resource
                )
                moved = True
            elif k == ord("q"):
                self.running = False
                return

            if moved:
                self._enemy_turn()
                self.dungeon.compute_fov(self.player.x, self.player.y, _FOV_RADIUS)
                # Passive HP trickle
                if random.random() < 0.12:
                    self.player.hp = min(self.player.hp + 1, self.player.max_hp)

        if not self.player.is_alive():
            self.running = False

    # ------------------------------------------------------------------ #
    # Player actions
    # ------------------------------------------------------------------ #

    def _try_move(self, dx: int, dy: int) -> bool:
        assert self.player is not None
        assert self.dungeon is not None
        nx, ny = self.player.x + dx, self.player.y + dy

        if not self.dungeon.is_walkable(nx, ny):
            return False

        if (nx, ny) in self.dungeon.enemy_map:
            self._attack_enemy(self.dungeon.enemy_map[(nx, ny)], special=False)
            return True

        self.player.x, self.player.y = nx, ny

        tile = self.dungeon.tiles[ny][nx]
        if tile == ">" and self.player.dungeon_level < _MAX_LEVEL:
            self._descend()
        elif tile == ">" and self.player.dungeon_level >= _MAX_LEVEL:
            self.renderer.add_message("There is no deeper floor.")

        return True

    def _attack_enemy(self, enemy: Enemy, special: bool) -> None:
        assert self.player is not None
        assert self.dungeon is not None

        result = (
            player_special(self.player, enemy)
            if special
            else player_attack(self.player, enemy)
        )
        self.renderer.add_message(result.message)

        if result.resource_error:
            return

        if not enemy.is_alive():
            self._kill_enemy(enemy)
            return

        # Enemy retaliates immediately
        r2 = enemy_attack(enemy, self.player)
        self.renderer.add_message(r2.message)
        if not self.player.is_alive():
            self.renderer.add_message("You collapse...")

    def _kill_enemy(self, enemy: Enemy) -> None:
        assert self.player is not None
        assert self.dungeon is not None

        self.player.kills += 1
        self.player.gold += enemy.gold_reward
        pos = (enemy.x, enemy.y)
        self.dungeon.enemy_map.pop(pos, None)
        if enemy in self.enemies:
            self.enemies.remove(enemy)

        xp_msg = self.player.gain_xp(enemy.xp_reward)
        self.renderer.add_message(
            f"{enemy.name} defeated! +{enemy.xp_reward} XP  +{enemy.gold_reward} gold"
        )
        if xp_msg:
            self.renderer.add_message(xp_msg)

        if enemy.etype == "dragon":
            self.won = True
            self.running = False

    def _pickup(self) -> bool:
        assert self.player is not None
        assert self.dungeon is not None

        pos = (self.player.x, self.player.y)
        if pos not in self.dungeon.item_map:
            self.renderer.add_message("Nothing here to pick up.")
            return False

        item = self.dungeon.item_map.pop(pos)
        if item in self.items:
            self.items.remove(item)

        if item.itype == ItemType.GOLD:
            self.player.gold += item.value
            self.renderer.add_message(f"You pocket {item.value} gold.")
        elif item.itype in (ItemType.POTION_HP, ItemType.POTION_MP):
            self.player.inventory.append(item)
            self.renderer.add_message(f"Picked up {item.name}.")
        elif item.itype == ItemType.WEAPON:
            if item.value > self.player.weapon_bonus:
                self.player.weapon_bonus = item.value
                self.renderer.add_message(f"Wielding {item.name}! ATK +{item.value}")
            else:
                self.renderer.add_message(f"{item.name} is weaker than your current weapon.")
        elif item.itype == ItemType.ARMOR:
            if item.value > self.player.armor_bonus:
                self.player.armor_bonus = item.value
                self.renderer.add_message(f"Donning {item.name}! DEF +{item.value}")
            else:
                self.renderer.add_message(f"{item.name} is weaker than your current armor.")

        return True

    def _open_inventory(self) -> None:
        assert self.player is not None
        idx = self.renderer.show_inventory(self.player)
        if idx is not None and idx < len(self.player.inventory):
            self._use_item(idx)
        assert self.dungeon is not None
        self.renderer.draw_game(self.dungeon, self.player)

    def _use_item(self, idx: int) -> None:
        assert self.player is not None
        item = self.player.inventory[idx]

        if item.itype == ItemType.POTION_HP:
            healed = min(item.value, self.player.max_hp - self.player.hp)
            self.player.hp += healed
            self.player.inventory.pop(idx)
            self.renderer.add_message(f"Used {item.name}. Restored {healed} HP.")
        elif item.itype == ItemType.POTION_MP:
            restored = min(item.value, self.player.max_resource - self.player.resource)
            self.player.resource += restored
            self.player.inventory.pop(idx)
            self.renderer.add_message(
                f"Used {item.name}. Restored {restored} {self.player.resource_name}."
            )

    def _use_special(self) -> bool:
        assert self.player is not None
        assert self.dungeon is not None

        # Target closest visible enemy
        target: Optional[Enemy] = None
        best = float("inf")
        for e in self.enemies:
            if self.dungeon.visible[e.y][e.x]:
                d = abs(e.x - self.player.x) + abs(e.y - self.player.y)
                if d < best:
                    best = d
                    target = e

        if target is None:
            self.renderer.add_message("No visible target for your special ability.")
            return False

        self._attack_enemy(target, special=True)
        return True

    def _descend(self) -> None:
        assert self.player is not None
        next_lvl = self.player.dungeon_level + 1
        self.renderer.add_message(f"You plunge deeper into Floor {next_lvl}...")
        self._load_floor(next_lvl)

    # ------------------------------------------------------------------ #
    # Enemy AI turn
    # ------------------------------------------------------------------ #

    def _enemy_turn(self) -> None:
        assert self.player is not None
        assert self.dungeon is not None

        for enemy in list(self.enemies):
            if not enemy.is_alive():
                continue
            if not self.dungeon.visible[enemy.y][enemy.x]:
                continue  # Only enemies the player can see are "active"

            dx = self.player.x - enemy.x
            dy = self.player.y - enemy.y
            dist = abs(dx) + abs(dy)

            if dist <= 1 or (abs(dx) <= 1 and abs(dy) <= 1):
                # Adjacent — attack
                r = enemy_attack(enemy, self.player)
                self.renderer.add_message(r.message)
                if not self.player.is_alive():
                    return
            else:
                # Step toward player
                step_x = (1 if dx > 0 else -1) if dx else 0
                step_y = (1 if dy > 0 else -1) if dy else 0
                for sdx, sdy in [(step_x, step_y), (step_x, 0), (0, step_y)]:
                    if sdx == 0 and sdy == 0:
                        continue
                    nx, ny = enemy.x + sdx, enemy.y + sdy
                    if (
                        self.dungeon.is_walkable(nx, ny)
                        and (nx, ny) not in self.dungeon.enemy_map
                        and (nx, ny) != (self.player.x, self.player.y)
                    ):
                        old = (enemy.x, enemy.y)
                        del self.dungeon.enemy_map[old]
                        enemy.x, enemy.y = nx, ny
                        self.dungeon.enemy_map[(nx, ny)] = enemy
                        break

    # ------------------------------------------------------------------ #
    # Input helpers
    # ------------------------------------------------------------------ #

    def _wait_for_enter_or_quit(self) -> int:
        while True:
            k = self.stdscr.getch()  # type: ignore[union-attr]
            if k in (10, 13, curses.KEY_ENTER):
                return k
            if k == ord("q"):
                return k

    def _pick_class(self) -> Optional[CharClass]:
        while True:
            k = self.stdscr.getch()  # type: ignore[union-attr]
            if k == ord("1"):
                return CharClass.WARRIOR
            if k == ord("2"):
                return CharClass.MAGE
            if k == ord("3"):
                return CharClass.ROGUE
            if k == ord("q"):
                return None
