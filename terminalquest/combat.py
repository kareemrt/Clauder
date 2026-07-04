"""Turn-based combat resolution."""

import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .entities import Enemy, Player


@dataclass
class CombatResult:
    damage: int
    message: str
    is_critical: bool = False
    is_special: bool = False
    resource_error: bool = False


def player_attack(player: "Player", enemy: "Enemy") -> CombatResult:
    from .entities import CharClass

    base = max(1, player.total_attack - enemy.defense + random.randint(-3, 6))
    is_crit = player.char_class == CharClass.ROGUE and random.random() < 0.25
    dmg = base * 2 if is_crit else base
    enemy.hp -= dmg

    if is_crit:
        msg = f"CRITICAL HIT! You strike {enemy.name} for {dmg} damage!"
    else:
        msg = f"You hit {enemy.name} for {dmg} damage."

    return CombatResult(damage=dmg, message=msg, is_critical=is_crit)


def player_special(player: "Player", enemy: "Enemy") -> CombatResult:
    from .entities import CharClass

    if player.resource < player.special_cost:
        return CombatResult(
            0,
            f"Not enough {player.resource_name}! ({player.resource}/{player.special_cost})",
            resource_error=True,
        )

    player.resource -= player.special_cost

    if player.char_class == CharClass.WARRIOR:
        dmg = max(5, int(player.total_attack * 2.5) + random.randint(0, 12))
        enemy.hp -= dmg
        msg = f"POWER STRIKE! You crush {enemy.name} for {dmg} damage!"

    elif player.char_class == CharClass.MAGE:
        dmg = max(10, int(player.total_attack * 2.2) + random.randint(8, 22))
        enemy.hp -= dmg
        msg = f"ARCANE BLAST! {dmg} magic damage sears {enemy.name}!"

    else:  # Rogue
        dmg = max(8, int(player.total_attack * 3.0) + random.randint(-2, 10))
        enemy.hp -= dmg
        msg = f"SHADOW STRIKE from the dark! {dmg} damage to {enemy.name}!"

    return CombatResult(damage=dmg, message=msg, is_special=True)


def enemy_attack(enemy: "Enemy", player: "Player") -> CombatResult:
    base = max(1, enemy.attack - player.total_defense + random.randint(-3, 5))
    is_fierce = random.random() < 0.15
    dmg = int(base * 1.6) if is_fierce else base
    player.hp -= dmg

    if is_fierce:
        msg = f"{enemy.name} attacks FIERCELY! You take {dmg} damage!"
    else:
        msg = f"{enemy.name} hits you for {dmg} damage."

    return CombatResult(damage=dmg, message=msg)
