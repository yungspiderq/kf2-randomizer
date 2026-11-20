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


def WPN(name: str, kind: str, *perks: str, dlc: bool = False) -> Weapon:
    return Weapon(name, kind, tuple(perks), dlc)


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