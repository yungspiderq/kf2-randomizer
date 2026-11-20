"""GUI smoke test for GitHub's Windows runner (no interactive desktop needed)."""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication
from kf2_randomizer import Randomizer, VERSION
from weapons_data import WEAPON_BY_ID, sum_weight

app = QApplication([])
win = Randomizer()
assert VERSION == "0.6.0"
assert win.current["perk"]
assert win.current["weapons"]
assert win.weapon_rows_layout.count() >= 1
for mode in ("fixed", "fill", "surprise"):
    win.weapon_weight_mode_combo.setCurrentIndex(win.weapon_weight_mode_combo.findData(mode))
    win.generate()
    chosen = [WEAPON_BY_ID[x] for x in win.current["weapons"]]
    assert 1 <= len(chosen) <= 6
    assert sum_weight(chosen) <= win.current["weight_cap"]
    assert len(chosen) == len({x.id for x in chosen})
old_perk = win.current["perk"]
win.reroll_weapons()
assert win.current["perk"] == old_perk
assert "Вес:" in win.result_text(win.current)
win.reroll_skills()
win.copy_result()
assert "Оружие:" in QApplication.clipboard().text()
win.close()
print("Qt GUI smoke test: passed")