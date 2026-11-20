"""Regression tests for the virtual in-game carry-capacity rules."""
import random
import unittest
from weapons_data import (
    Weapon, WEAPONS, available_weapons, effective_weight_capacity,
    sum_weight, weighted_loadout,
)


def sample_weapons():
    return [Weapon('Sample A', 'assault', ('Коммандос',), weight=3),
            Weapon('Sample B', 'assault', ('Коммандос',), weight=5),
            Weapon('Sample C', 'assault', ('Коммандос',), weight=7),
            Weapon('Sample D', 'assault', ('Коммандос',), weight=9),
            Weapon('Unknown', 'assault', ('Коммандос',), weight=None),
            Weapon('Excess', 'assault', ('Коммандос',), weight=25)]


class WeightInventoryTests(unittest.TestCase):
    def test_weighted_catalog_has_no_phantom_values(self):
        self.assertEqual(len(WEAPONS), 85)
        self.assertGreaterEqual(sum(w.weight is not None for w in WEAPONS), 75)
        self.assertTrue(all(w.weight is None or w.weight >= 0 for w in WEAPONS))

    def test_default_limit_and_eligible_bonus(self):
        self.assertEqual(effective_weight_capacity('Снайпер', 20), 15)
        self.assertEqual(effective_weight_capacity('Берсеркер', 15), 15)
        self.assertEqual(effective_weight_capacity('Поддержка', 20), 20)
        self.assertEqual(effective_weight_capacity('Выживальщик', 20), 20)
        self.assertEqual(effective_weight_capacity('Выживальщик', 15), 15)

    def test_weight_modes_never_exceed_limit_or_repeat(self):
        all_items = sample_weapons()
        for mode in ('fixed', 'fill', 'surprise'):
            for max_weight in (5, 10, 15, 20):
                for seed in range(100):
                    chosen = weighted_loadout(all_items, max_weight, 4,
                                              mode, rng=random.Random(seed))
                    self.assertLessEqual(sum_weight(chosen), max_weight)
                    self.assertLessEqual(len(chosen), 4)
                    self.assertEqual(len({w.id for w in chosen}), len(chosen))
                    self.assertTrue(all(w.weight and w.weight <= max_weight for w in chosen))

    def test_fixed_prefers_requested_count(self):
        chosen = weighted_loadout(sample_weapons(), 15, 3, 'fixed', rng=random.Random(2))
        self.assertEqual(len(chosen), 3)
        self.assertLessEqual(sum_weight(chosen), 15)

    def test_fill_maximizes_available_capacity(self):
        chosen = weighted_loadout(sample_weapons(), 15, 3, 'fill', rng=random.Random(4))
        self.assertEqual(sum_weight(chosen), 15)

    def test_surprise_not_always_same_amount(self):
        results = {sum_weight(weighted_loadout(sample_weapons(), 15, 3, 'surprise',
                                               rng=random.Random(seed))) for seed in range(100)}
        self.assertGreater(len(results), 1)

    def test_unknown_and_overweight_never_selected(self):
        selected = weighted_loadout(sample_weapons()[-2:], 15, 4, 'fill', rng=random.Random(2))
        self.assertEqual(selected, [])

    def test_one_item_capacity(self):
        chosen = weighted_loadout(sample_weapons(), 7, 1, 'fill', rng=random.Random(1))
        self.assertEqual(len(chosen), 1)
        self.assertEqual(sum_weight(chosen), 7)

    def test_empty_invalid_mode_and_filters(self):
        self.assertEqual(weighted_loadout([], 15, 3), [])
        self.assertEqual(weighted_loadout(sample_weapons(), 0, 3), [])
        self.assertEqual(weighted_loadout(sample_weapons(), 15, 0), [])
        with self.assertRaises(ValueError):
            weighted_loadout(sample_weapons(), 15, 3, 'invalid')
        for perk in ('Коммандос', 'Выживальщик', 'Поддержка'):
            pool = available_weapons(perk)
            result = weighted_loadout(pool, 15, 6, 'fill', rng=random.Random(8))
            self.assertLessEqual(sum_weight(result), 15)


if __name__ == '__main__':
    unittest.main()