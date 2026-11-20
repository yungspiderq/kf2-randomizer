import random
import unittest

from weapons_data import (CATEGORIES, WEAPONS, WEAPON_BY_ID, available_weapons,
                          choose_loadout)


PERKS = (
    "Берсеркер", "Коммандос", "Поддержка", "Полевой медик", "Подрывник",
    "Поджигатель", "Стрелок", "Снайпер", "Спецназ", "Выживальщик",
)


class WeaponsCatalogTests(unittest.TestCase):
    def test_catalog_consistency(self):
        self.assertGreaterEqual(len(WEAPONS), 70)
        self.assertEqual(len(WEAPONS), len(WEAPON_BY_ID), "Weapon IDs must be unique")
        for weapon in WEAPONS:
            self.assertIn(weapon.kind, CATEGORIES)
            self.assertTrue(weapon.perks)
            for perk in weapon.perks:
                self.assertIn(perk, PERKS)

    def test_perk_filter_default_excludes_dlc(self):
        for perk in PERKS:
            pool = available_weapons(perk)
            self.assertGreaterEqual(len(pool), 5, perk)
            self.assertTrue(all(not w.dlc for w in pool))
            if perk != "Выживальщик":
                self.assertTrue(all(perk in w.perks for w in pool))

    def test_survivalist_sees_everything(self):
        self.assertEqual(len(available_weapons("Выживальщик", include_dlc=True)), len(WEAPONS))

    def test_category_filter_and_any_class(self):
        rows = available_weapons("Берсеркер", kind="medic", any_class=True)
        self.assertTrue(rows)
        self.assertTrue(all(w.kind == "medic" for w in rows))

    def test_dlc_toggle(self):
        without = available_weapons("Берсеркер")
        with_dlc = available_weapons("Берсеркер", include_dlc=True)
        self.assertGreater(len(with_dlc), len(without))

    def test_no_repeating_items_within_one_roll(self):
        pool = available_weapons("Выживальщик")
        for seed in range(100):
            selected = choose_loadout(pool, 3, rng=random.Random(seed))
            self.assertEqual(len(selected), 3)
            self.assertEqual(len(set(w.id for w in selected)), 3)

    def test_previous_ones_avoided_when_possible(self):
        pool = available_weapons("Коммандос")
        old = [pool[0].id, pool[1].id]
        for seed in range(25):
            selected = choose_loadout(pool, 2, recent=old, rng=random.Random(seed))
            self.assertFalse(any(w.id in old for w in selected))

    def test_narrow_pool_is_not_padded_with_duplicates(self):
        pool = available_weapons("Берсеркер", kind="medic")
        selected = choose_loadout(pool, 3, rng=random.Random(9))
        self.assertLessEqual(len(selected), 3)
        self.assertEqual(len(set(w.id for w in selected)), len(selected))

    def test_empty_input(self):
        self.assertEqual(choose_loadout([], 3), [])
        self.assertEqual(choose_loadout(available_weapons("Коммандос"), 0), [])


if __name__ == "__main__":
    unittest.main()