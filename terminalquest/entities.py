"""Player and enemy entity definitions."""

import random
from enum import Enum
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

if TYPE_CHECKING:
    from .dungeon import Dungeon


class CharClass(Enum):
    WARRIOR = "Warrior"
    MAGE = "Mage"
    ROGUE = "Rogue"


CLASS_STATS: Dict = {
    CharClass.WARRIOR: {
        "hp": 110,
        "attack": 15,
        "defense": 9,
        "resource": 90,
        "resource_name": "Stamina",
        "special_cost": 28,
        "special_name": "Power Strike",
        "description": "Unyielding tank. High HP & defense, strong melee.",
    },
    CharClass.MAGE: {
        "hp": 60,
        "attack": 24,
        "defense": 3,
        "resource": 80,
        "resource_name": "Mana",
        "special_cost": 35,
        "special_name": "Arcane Blast",
        "description": "Fragile but devastating. Highest magic damage output.",
    },
    CharClass.ROGUE: {
        "hp": 78,
        "attack": 13,
        "defense": 5,
        "resource": 65,
        "resource_name": "Energy",
        "special_cost": 20,
        "special_name": "Shadow Strike",
        "description": "Swift and lethal. 25% critical chance, cheapest special.",
    },
}


class Player:
    def __init__(self, name: str, char_class: CharClass):
        self.name = name
        self.char_class = char_class
        s = CLASS_STATS[char_class]

        self.symbol = "@"
        self.hp = s["hp"]
        self.max_hp = s["hp"]
        self.attack = s["attack"]
        self.defense = s["defense"]
        self.resource = s["resource"]
        self.max_resource = s["resource"]
        self.resource_name = s["resource_name"]
        self.special_cost = s["special_cost"]
        self.special_name = s["special_name"]

        self.weapon_bonus = 0
        self.armor_bonus = 0
        self.inventory: List = []

        self.gold = 0
        self.kills = 0
        self.xp = 0
        self.level = 1
        self.xp_to_next = 50
        self.dungeon_level = 1

        self.x = 0
        self.y = 0

    @property
    def total_attack(self) -> int:
        return self.attack + self.weapon_bonus

    @property
    def total_defense(self) -> int:
        return self.defense + self.armor_bonus

    def is_alive(self) -> bool:
        return self.hp > 0

    def gain_xp(self, amount: int) -> str:
        self.xp += amount
        if self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(self.xp_to_next * 1.6)
            self.max_hp += 12
            self.hp = min(self.hp + 25, self.max_hp)
            self.attack += 2
            self.defense += 1
            return f"Level up! You are now level {self.level}!"
        return ""

    def score(self) -> int:
        return self.dungeon_level * 500 + self.kills * 20 + self.gold + self.level * 100


# ------------------------------------------------------------------ #
# Enemies
# ------------------------------------------------------------------ #

ENEMY_TYPES: Dict = {
    "goblin": {
        "name": "Goblin",
        "symbol": "g",
        "hp": 16,
        "attack": 5,
        "defense": 1,
        "xp": 10,
        "gold": (1, 6),
        "color": "green",
        "min_level": 1,
    },
    "orc": {
        "name": "Orc",
        "symbol": "O",
        "hp": 30,
        "attack": 10,
        "defense": 3,
        "xp": 22,
        "gold": (4, 12),
        "color": "green",
        "min_level": 2,
    },
    "skeleton": {
        "name": "Skeleton",
        "symbol": "s",
        "hp": 24,
        "attack": 12,
        "defense": 5,
        "xp": 28,
        "gold": (3, 9),
        "color": "white",
        "min_level": 2,
    },
    "dark_mage": {
        "name": "Dark Mage",
        "symbol": "M",
        "hp": 22,
        "attack": 18,
        "defense": 2,
        "xp": 38,
        "gold": (6, 16),
        "color": "magenta",
        "min_level": 3,
    },
    "troll": {
        "name": "Troll",
        "symbol": "T",
        "hp": 50,
        "attack": 14,
        "defense": 8,
        "xp": 55,
        "gold": (9, 22),
        "color": "green",
        "min_level": 3,
    },
    "demon": {
        "name": "Demon",
        "symbol": "D",
        "hp": 65,
        "attack": 20,
        "defense": 11,
        "xp": 85,
        "gold": (12, 28),
        "color": "red",
        "min_level": 4,
    },
    "dragon": {
        "name": "Ancient Dragon",
        "symbol": "X",
        "hp": 130,
        "attack": 28,
        "defense": 16,
        "xp": 600,
        "gold": (60, 120),
        "color": "red",
        "min_level": 5,
    },
}


class Enemy:
    def __init__(self, etype: str, x: int = 0, y: int = 0):
        data = ENEMY_TYPES[etype]
        self.etype = etype
        self.name = data["name"]
        self.symbol = data["symbol"]
        self.hp = data["hp"]
        self.max_hp = data["hp"]
        self.attack = data["attack"]
        self.defense = data["defense"]
        self.xp_reward = data["xp"]
        self.gold_reward = random.randint(*data["gold"])
        self.color = data.get("color", "white")
        self.x = x
        self.y = y

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        actual = max(1, amount - self.defense)
        self.hp -= actual
        return actual


def get_enemy_pool(level: int) -> List[str]:
    return [
        k for k, v in ENEMY_TYPES.items()
        if v["min_level"] <= level and k != "dragon"
    ]


def spawn_enemies(dungeon: "Dungeon", level: int, max_count: int) -> List[Enemy]:
    pool = get_enemy_pool(level)
    enemies: List[Enemy] = []
    occupied: set = set()

    # Boss on floor 5 in the last room
    if level == 5 and dungeon.rooms:
        pos = dungeon.get_random_floor_pos(dungeon.rooms[-1], exclude=occupied)
        if pos:
            ex, ey = pos
            e = Enemy("dragon", ex, ey)
            enemies.append(e)
            dungeon.enemy_map[(ex, ey)] = e
            occupied.add(pos)

    for room in dungeon.rooms[1:]:
        n = random.randint(0, 1 + level // 2)
        for _ in range(n):
            if len(enemies) >= max_count:
                break
            etype = random.choice(pool)
            pos = dungeon.get_random_floor_pos(room, exclude=occupied)
            if pos:
                ex, ey = pos
                e = Enemy(etype, ex, ey)
                enemies.append(e)
                dungeon.enemy_map[(ex, ey)] = e
                occupied.add(pos)

    return enemies
