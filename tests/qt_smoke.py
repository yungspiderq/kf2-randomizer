"""GUI smoke test for GitHub's Windows runner (no interactive desktop needed)."""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication
from kf2_randomizer import Randomizer, VERSION

app = QApplication([])
win = Randomizer()
assert VERSION == "0.5.0"
assert win.current["perk"]
assert win.current["weapons"]
assert win.weapon_rows_layout.count() >= 1
win.generate()
assert 1 <= len(win.current["weapons"]) <= 3
old_perk = win.current["perk"]
win.reroll_weapons()
assert win.current["perk"] == old_perk
assert "Оружие:" in win.result_text(win.current)
win.reroll_skills()
win.copy_result()
assert "Оружие:" in QApplication.clipboard().text()
win.close()
print("Qt GUI smoke test: passed")