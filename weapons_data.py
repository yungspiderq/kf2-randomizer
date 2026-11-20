"""Curated *in-game* KF2 trader weapons for a fan-made randomizer.

No real-world weapon advice. Ownership is not inferred; paid items are excluded by
 default. Cross-perk assignments are intentionally conservative. The game may
 rebalance its catalogue independently of this app.
"""
from __future__ import annotations

from dataclasses import dataclass
import random
import re
from typing import Iterable


@dataclass(frozen=True, slots=True)
class Weapon:
    name: str
    kind: str
    perks: tuple[str, ...]
    dlc: bool = False
    weight: int | None = None  # game carry slots; None if unverified

    @property
    def id(self) -> str:
        return re.sub(r"[^a-z0-9]+", "-", self.name.lower()).strip("-")


CATEGORIES: dict[str, str] = {
    "melee": "Ближний бой",
    "assault": "Штурмовое",
    "shotgun": "Дробовики",
    "medic": "Медицинское",
    "explosive": "Взрывное",
    "flame": "Огненное",
    "handgun": "Пистолеты",
    "precision": "Точное",
    "smg": "Пистолеты-пулемёты",
    "special": "Специальное",
}

# Russian perk keys match the application's visible perk list.
B = "Берсеркер"
C = "Коммандос"
S = "Поддержка"
M = "Полевой медик"
D = "Подрывник"
F = "Поджигатель"
G = "Стрелок"
P = "Снайпер"
W = "Спецназ"
V = "Выживальщик"



# Base (un-upgraded) in-game carry weights. Older/community data can differ
# from the latest game patch; unknowns remain None and do not enter strict modes.
# References: https://steamcommunity.com/sharedfiles/filedetails/?id=894320418
#             https://w.atwiki.jp/killingfloor2a/pages/33.html
WEIGHT_BY_NAME: dict[str, int] = {
    '.50 Desert Eagle': 2,
    '.500 Magnum Revolver': 3,
    '1858 Revolvers': 2,
    '9mm Pistol': 0,
    'AA-12 Auto Shotgun': 10,
    'AF2011-A1': 3,
    'AK-12': 6,
    'AR-15 Varmint Rifle': 4,
    'Battleaxe': 10,
    'Blunderbuss': 7,
    'Bone Crusher': 8,
    'C4 Explosives': 3,
    "Caulk n' Burn": 5,
    'Compound Bow': 8,
    'Crossbow': 6,
    'Crovel Survival Tool': 4,
    'Doomstick': 10,
    'Double-Barrel Boomstick': 5,
    'Eviscerator': 9,
    'FN FAL ACOG': 8,
    'Fire Axe': 5,
    'Flamethrower': 7,
    'Frost Fang': 7,
    'Glock 18C': 4,
    'HMTech-101 Pistol': 1,
    'HMTech-201 SMG': 3,
    'HMTech-301 Shotgun': 6,
    'HMTech-401 Assault Rifle': 7,
    'HMTech-501 Grenade Rifle': 8,
    'HRG Buckshot': 2,
    'HRG Incision': 8,
    'HRG Nailgun': 5,
    'HRG Scorcher': 4,
    'HRG Vampire': 8,
    'HRG Winterbite': 2,
    'HX25 Grenade Pistol': 4,
    'HZ12 Multi-Action': 5,
    'Healthrower': 7,
    'Helios Rifle': 8,
    'Hemoclobber': 4,
    'Hemogoblin': 8,
    'Husk Cannon': 8,
    'Ion Thruster': 8,
    'Kaboomstick': 6,
    'Katana': 4,
    'Kriss SMG': 6,
    'M14 EBR': 7,
    'M16 M203 Assault Rifle': 6,
    'M1911 Pistol': 2,
    'M32 Grenade Launcher': 9,
    'M4 Combat Shotgun': 6,
    'M79 Grenade Launcher': 6,
    'M99 AMR': 12,
    'MAC-10': 4,
    'MP5RAS': 4,
    'MP7 SMG': 4,
    'Microwave Gun': 9,
    'Mine Reconstructor': 8,
    'Minigun': 10,
    'Mosin Nagant': 7,
    'P90 SMG': 5,
    'Pulverizer': 6,
    'RPG-7': 9,
    'Rail Gun': 9,
    'SA80 L85A2': 5,
    'SCAR-H Assault Rifle': 6,
    'SG 500 Pump-Action': 5,
    'SPX 464 Centerfire': 5,
    'Seal Squeal': 7,
    'Seeker Six': 8,
    'Static Strikers': 7,
    'Stoner 63A LMG': 9,
    'Tommy Gun': 6,
    'UMP-45 SMG': 5,
    'VLAD-1000 Nailgun': 5,
    'Winchester 1894': 4,
    'Zweihander': 7,
}

def WPN(name: str, kind: str, *perks: str, dlc: bool = False) -> Weapon:
    return Weapon(name, kind, tuple(perks), dlc, WEIGHT_BY_NAME.get(name))


WEAPONS: tuple[Weapon, ...] = (
    # Berserker
    WPN("Crovel Survival Tool", "melee", B),
    WPN("Katana", "melee", B),
    WPN("Fire Axe", "melee", B),
    WPN("Pulverizer", "melee", B, D),
    WPN("Eviscerator", "melee", B),
    WPN("Zweihander", "melee", B, dlc=True),
    WPN("Bone Crusher", "melee", B),
    WPN("Battleaxe", "melee", B),
    WPN("Static Strikers", "melee", B),
    WPN("Hemoclobber", "melee", B, M),
    WPN("Ion Thruster", "melee", B, dlc=True),
    # Commando
    WPN("AR-15 Varmint Rifle", "assault", C),
    WPN("SA80 L85A2", "assault", C),
    WPN("AK-12", "assault", C),
    WPN("SCAR-H Assault Rifle", "assault", C),
    WPN("HMTech-401 Assault Rifle", "medic", M, C),
    WPN("M16 M203 Assault Rifle", "assault", C, D),
    WPN("FN FAL ACOG", "precision", C, P),
    WPN("Stoner 63A LMG", "assault", C),
    WPN("Minigun", "assault", C, dlc=True),
    WPN("501 Grenade Rifle", "assault", C),
    # Support
    WPN("SG 500 Pump-Action", "shotgun", S),
    WPN("Double-Barrel Boomstick", "shotgun", S),
    WPN("HZ12 Multi-Action", "shotgun", S),
    WPN("M4 Combat Shotgun", "shotgun", S),
    WPN("AA-12 Auto Shotgun", "shotgun", S),
    WPN("Doomstick", "shotgun", S),
    WPN("VLAD-1000 Nailgun", "shotgun", S, B),
    WPN("HMTech-301 Shotgun", "medic", S, M),
    WPN("HRG Buckshot", "shotgun", S, G),
    WPN("Frost Fang", "shotgun", S, B, dlc=True),
    # Field Medic
    WPN("HMTech-101 Pistol", "medic", M, G),
    WPN("HMTech-201 SMG", "medic", M, W),
    WPN("HMTech-501 Grenade Rifle", "medic", M, D),
    WPN("Healthrower", "medic", M),
    WPN("Hemogoblin", "medic", M),
    WPN("HRG Incision", "medic", M),
    WPN("HRG Vampire", "medic", M),
    WPN("Mine Reconstructor", "medic", M, dlc=True),
    # Demolitionist
    WPN("HX25 Grenade Pistol", "explosive", D),
    WPN("C4 Explosives", "explosive", D),
    WPN("M79 Grenade Launcher", "explosive", D),
    WPN("Seeker Six", "explosive", D),
    WPN("RPG-7", "explosive", D),
    WPN("M32 Grenade Launcher", "explosive", D),
    WPN("Kaboomstick", "explosive", D, S),
    WPN("HRG Bombardier", "explosive", D),
    WPN("Seal Squeal", "explosive", D, dlc=True),
    WPN("Blunderbuss", "explosive", D, S, dlc=True),
    # Firebug
    WPN("Caulk n' Burn", "flame", F),
    WPN("Flamethrower", "flame", F),
    WPN("Trench Gun", "flame", F, S),
    WPN("MAC-10", "smg", F, W),
    WPN("Microwave Gun", "flame", F),
    WPN("Dual Spitfires", "handgun", F, G),
    WPN("Husk Cannon", "flame", F),
    WPN("HRG Dragonsblaze", "flame", F),
    WPN("HRG Scorcher", "flame", F),
    WPN("Helios Rifle", "flame", F),
    # Gunslinger
    WPN("1858 Revolvers", "handgun", G),
    WPN("9mm Pistol", "handgun", G),
    WPN("M1911 Pistol", "handgun", G),
    WPN(".50 Desert Eagle", "handgun", G),
    WPN(".500 Magnum Revolver", "handgun", G),
    WPN("AF2011-A1", "handgun", G),
    WPN("SPX 464 Centerfire", "precision", G, P),
    WPN("HRG Winterbite", "handgun", G),
    WPN("Rhino Revolver", "handgun", G, dlc=True),
    WPN("Glock 18C", "handgun", G, dlc=True),
    # Sharpshooter
    WPN("Winchester 1894", "precision", P),
    WPN("Crossbow", "precision", P),
    WPN("M14 EBR", "precision", P),
    WPN("Rail Gun", "precision", P),
    WPN("M99 AMR", "precision", P),
    WPN("Mosin Nagant", "precision", P, dlc=True),
    WPN("Compound Bow", "precision", P, dlc=True),
    # SWAT
    WPN("MP7 SMG", "smg", W),
    WPN("MP5RAS", "smg", W),
    WPN("P90 SMG", "smg", W),
    WPN("Kriss SMG", "smg", W),
    WPN("UMP-45 SMG", "smg", W),
    WPN("Tommy Gun", "smg", W, C),
    WPN("HRG Nailgun", "smg", W),
    WPN("HRG Stunner", "smg", W),
    WPN("G36C Assault Rifle", "smg", W, dlc=True),
)
WEAPON_BY_ID = {w.id: w for w in WEAPONS}


def available_weapons(perk: str, *, any_class: bool = False,
                      include_dlc: bool = False, kind: str | None = None) -> list[Weapon]:
    return [
        w for w in WEAPONS
        if (any_class or perk == V or perk in w.perks)
        and (include_dlc or not w.dlc)
        and (kind is None or w.kind == kind)
    ]


def choose_loadout(pool: Iterable[Weapon], count: int, *, recent: Iterable[str] = (),
                   rng: random.Random | None = None) -> list[Weapon]:
    """Pick unique in-game items, avoid previous items when feasible.

    If the category filter yields too few items, return the available subset;
    never duplicate a name to fill extra slots.
    """
    rnd = rng if rng is not None else random.SystemRandom()
    by_id = {w.id: w for w in pool}
    candidates = list(by_id.values())
    if not candidates or count <= 0:
        return []
    count = min(count, len(candidates))
    recent_ids = set(recent)
    fresh = [w for w in candidates if w.id not in recent_ids]
    rnd.shuffle(fresh)
    if len(fresh) >= count:
        return fresh[:count]
    used = {w.id for w in fresh}
    remaining = [w for w in candidates if w.id not in used]
    rnd.shuffle(remaining)
    return (fresh + remaining)[:count]


def weapon_labels(ids: Iterable[str]) -> list[str]:
    return [WEAPON_BY_ID[x].name for x in ids if x in WEAPON_BY_ID]


def effective_weight_capacity(perk: str, requested: int) -> int:
    """Limit game capacity by class. A 20-unit bonus is never universal.

    Users choosing 20 for a qualifying class are responsible for having the
    level/skill unlocked in KF2; this tool does not inspect game character data.
    """
    return 20 if perk in {S, V} and requested >= 20 else 15


def sum_weight(weapons: Iterable[Weapon]) -> int:
    """Total of verified in-game carry weights. Callers must check unknowns."""
    return sum(w.weight or 0 for w in weapons)


def weighted_loadout(
    pool: Iterable[Weapon], maximum_weight: int, maximum_items: int,
    mode: str = "fixed", *, recent: Iterable[str] = (),
    rng: random.Random | None = None,
) -> list[Weapon]:
    """Randomized capacity-limited subset of known-weight *game items*.

    Modes:
      fixed: prefer the requested item count while respecting total weight
      fill: maximize used weight with up to maximum_items
      surprise: select an achievable random target weight, not an item count

    No duplicate items, no overweight outcomes, and None weights excluded.
    Dynamic programming stores one randomized representative per (item count, weight)
    state; this is bounded by max_items*capacity, not 2**len(pool).
    """
    if mode not in {"fixed", "fill", "surprise"}:
        raise ValueError(f"Unknown game inventory mode: {mode}")
    if maximum_weight < 1 or maximum_items < 1:
        return []
    rnd = rng if rng is not None else random.SystemRandom()
    seen: set[str] = set()
    candidates = []
    for item in pool:
        if (item.id not in seen and item.weight is not None
                and 0 < item.weight <= maximum_weight):
            candidates.append(item)
            seen.add(item.id)
    if not candidates:
        return []
    rnd.shuffle(candidates)
    maximum_items = min(maximum_items, len(candidates))
    recent_ids = set(recent)
    # Each (number, weight) holds one randomized path; random replacement
    # gives different results between rolls instead of a hardcoded template.
    dp: dict[tuple[int, int], tuple[int, ...]] = {(0, 0): ()}
    for idx, item in enumerate(candidates):
        next_states = dict(dp)
        for (number, weight), picked in dp.items():
            new_n = number + 1
            new_w = weight + item.weight
            if new_n > maximum_items or new_w > maximum_weight:
                continue
            key = (new_n, new_w)
            if key not in next_states or rnd.random() < 0.40:
                next_states[key] = (*picked, idx)
        dp = next_states
    states = [(count, kg, ids) for (count, kg), ids in dp.items() if count >= 1]
    if not states:
        return []
    if mode == "surprise":
        floor = max(1, maximum_weight // 2)
        goal = rnd.randint(floor, maximum_weight)
        # no crossing the randomly chosen target if possible
        below = [state for state in states if state[1] <= goal]
        possible = below or states
        best_distance = min(abs(goal - state[1]) for state in possible)
        top = [state for state in possible if abs(goal - state[1]) == best_distance]
    elif mode == "fill":
        best_kg = max(state[1] for state in states)
        top = [state for state in states if state[1] == best_kg]
    else:
        best_n = max(state[0] for state in states)
        top = [state for state in states if state[0] == best_n]
    # Prefer avoiding recently rolled items if an equivalent state exists.
    fewest_repeats = min(sum(candidates[i].id in recent_ids for i in ids) for _, _, ids in top)
    top = [s for s in top if sum(candidates[i].id in recent_ids for i in s[2]) == fewest_repeats]
    _, _, ids = rnd.choice(top)
    result = [candidates[i] for i in ids]
    rnd.shuffle(result)
    return result