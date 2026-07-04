"""Item definitions and dungeon item spawning."""

import random
from enum import Enum
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Tuple

if TYPE_CHECKING:
    from .dungeon import Dungeon


class ItemType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    POTION_HP = "potion_hp"
    POTION_MP = "potion_mp"
    GOLD = "gold"


class Item:
    def __init__(
        self,
        itype: ItemType,
        name: str,
        symbol: str,
        value: int = 0,
        description: str = "",
    ):
        self.itype = itype
        self.name = name
        self.symbol = symbol
        self.value = value
        self.description = description
        self.x = 0
        self.y = 0

    def __str__(self) -> str:
        return self.name


# Each entry is a factory function so values like gold amounts are re-randomized per spawn.
_POOL: Dict[int, List[Callable[[], Item]]] = {
    1: [
        lambda: Item(ItemType.POTION_HP, "Health Potion", "!", 30, "Restores 30 HP"),
        lambda: Item(ItemType.POTION_MP, "Energy Tonic", "!", 20, "Restores 20 resource"),
        lambda: Item(ItemType.WEAPON, "Short Sword", ")", 4, "+4 Attack"),
        lambda: Item(ItemType.ARMOR, "Leather Vest", "]", 3, "+3 Defense"),
        lambda: Item(ItemType.GOLD, "Gold Coins", "$", random.randint(5, 15), "Shiny."),
    ],
    2: [
        lambda: Item(ItemType.POTION_HP, "Health Potion", "!", 30, "Restores 30 HP"),
        lambda: Item(ItemType.POTION_HP, "Greater Potion", "!", 60, "Restores 60 HP"),
        lambda: Item(ItemType.POTION_MP, "Mana Crystal", "!", 40, "Restores 40 resource"),
        lambda: Item(ItemType.WEAPON, "Battle Axe", ")", 7, "+7 Attack"),
        lambda: Item(ItemType.WEAPON, "Steel Blade", ")", 6, "+6 Attack"),
        lambda: Item(ItemType.ARMOR, "Chain Mail", "]", 5, "+5 Defense"),
        lambda: Item(ItemType.GOLD, "Treasure Bag", "$", random.randint(10, 30), "Jingling."),
    ],
    4: [
        lambda: Item(ItemType.POTION_HP, "Elixir of Life", "!", 100, "Restores 100 HP"),
        lambda: Item(ItemType.POTION_MP, "Arcane Flask", "!", 60, "Restores 60 resource"),
        lambda: Item(ItemType.WEAPON, "Enchanted Blade", ")", 12, "+12 Attack"),
        lambda: Item(ItemType.ARMOR, "Dragon Scale", "]", 10, "+10 Defense"),
        lambda: Item(ItemType.GOLD, "Hoard Fragment", "$", random.randint(30, 80), "Legendary wealth."),
    ],
}


def generate_item_for_level(level: int) -> Item:
    pool = list(_POOL[1])
    if level >= 2:
        pool += _POOL[2]
    if level >= 4:
        pool += _POOL[4]
    return random.choice(pool)()


def spawn_items(dungeon: "Dungeon", level: int) -> List[Item]:
    items: List[Item] = []
    occupied: set = {
        p for p in [dungeon.stairs_up, dungeon.stairs_down] if p
    } | set(dungeon.enemy_map.keys())

    for room in dungeon.rooms[1:]:
        if random.random() < 0.65:
            pos = dungeon.get_random_floor_pos(room, exclude=occupied)
            if pos:
                ix, iy = pos
                item = generate_item_for_level(level)
                item.x, item.y = ix, iy
                items.append(item)
                dungeon.item_map[(ix, iy)] = item
                occupied.add(pos)

    return items
