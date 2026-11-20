"""Killing Floor 2 Randomizer — desktop app (PySide6, Python 3.10+).

This tool suggests OPTIONAL in-game challenges; it does not change Killing Floor 2
or automatically equip in-game items. Data is a curated, editable starter catalog.
"""
from __future__ import annotations

import json
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from PySide6.QtCore import Qt, QStandardPaths
from PySide6.QtGui import QColor, QFont, QIcon, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QListWidget, QMainWindow, QMessageBox, QPushButton, QScrollArea,
    QSizePolicy, QSplitter, QVBoxLayout, QWidget,
)

APP_TITLE = "KF2 RANDOMIZER"
VERSION = "0.3.0"
RNG = random.SystemRandom()

# Ten playable character classes. The app randomizes skill-side selections
# rather than suggesting any particular physical or in-game equipment.
PERKS: dict[str, dict[str, str]] = {
    "Берсеркер": {"en": "Berserker", "role": "Защита команды", "mark": "BZ"},
    "Коммандос": {"en": "Commando", "role": "Штурм", "mark": "CM"},
    "Поддержка": {"en": "Support", "role": "Помощь отряду", "mark": "SP"},
    "Полевой медик": {"en": "Field Medic", "role": "Лечение союзников", "mark": "MD"},
    "Подрывник": {"en": "Demolitionist", "role": "Специализация на уроне", "mark": "DM"},
    "Поджигатель": {"en": "Firebug", "role": "Контроль толпы", "mark": "FB"},
    "Стрелок": {"en": "Gunslinger", "role": "Мобильность", "mark": "GS"},
    "Снайпер": {"en": "Sharpshooter", "role": "Точность", "mark": "SS"},
    "Спецназ": {"en": "SWAT", "role": "Контроль толпы", "mark": "SW"},
    "Выживальщик": {"en": "Survivalist", "role": "Универсальный класс", "mark": "SV"},
}

MAPS = [
    "Ashwood Asylum", "Biolapse", "Biotics Lab", "Black Forest", "Burning Paris",
    "Catacombs", "Containment Station", "Desolation", "Dystopia 2029", "Elysium",
    "Evacuation Point", "Farmhouse", "Hellmark Station", "Hostile Grounds",
    "Moonbase", "Monster Ball", "Netherhold", "Nightmare", "Nuked",
    "Outpost", "Prison", "Sanitarium", "Shopping Spree", "Steam Fortress",
    "The Tragic Kingdom", "Volter Manor", "Zed Landing",
]

DIFFICULTIES = ["Normal", "Hard", "Suicidal", "Hell on Earth"]
LENGTHS = [("Короткий — 4 волны", 4), ("Средний — 7 волн", 7), ("Длинный — 10 волн", 10)]

# User-made, game-only challenges; they are not official modifiers.
COMMON_CHALLENGES = [
    ("Лёгкий", "Пройди две волны подряд, не меняя выбранный класс."),
    ("Лёгкий", "Выбери одну карту и попробуй завершить на ней всю игру."),
    ("Лёгкий", "Пройди матч на выбранном классе от начала до финальной волны."),
    ("Лёгкий", "На следующей волне используй случайную ветку доступных навыков."),
    ("Лёгкий", "Сыграй две волны подряд с тем же набором навыков."),
    ("Лёгкий", "Пройди одну волну, не меняя выбранные навыки."),
    ("Средний", "Пройди три волны подряд, не меняя класс."),
    ("Средний", "Сыграй полный матч со случайной веткой навыков."),
    ("Средний", "При следующем выборе карты не повторяй предыдущую."),
    ("Средний", "Пройди матч без смены класса до финала."),
    ("Средний", "Сыграй полную партию, не меняя выбранные навыки."),
    ("Средний", "Пройди четыре последовательные волны с одной веткой навыков."),
    ("Сложный", "Выиграй два матча подряд с одним классом."),
    ("Сложный", "Пройди весь матч с полностью случайной веткой навыков."),
    ("Сложный", "Выиграй две последовательные партии, не меняя класс."),
    ("Сложный", "Заверши матч с классом и навыками из первой генерации."),
]

CLASS_CHALLENGES = {
    "Берсеркер": [("Средний", "Сыграй три волны, сохранив одну выбранную ветку навыков.")],
    "Коммандос": [("Лёгкий", "Используй один и тот же вариант навыков две волны подряд.")],
    "Поддержка": [("Средний", "Сыграй матч командой, не переключаясь на другой класс.")],
    "Полевой медик": [("Лёгкий", "Если играешь в команде, помогай союзникам на каждой волне.")],
    "Подрывник": [("Средний", "Оставь выбранные навыки неизменными до финальной волны.")],
    "Поджигатель": [("Средний", "Весь матч оставайся на одном наборе навыков.")],
    "Стрелок": [("Средний", "Пройди три волны с выбранным сочетанием навыков.")],
    "Снайпер": [("Средний", "Не меняй выбранный класс от первой до финальной волны.")],
    "Спецназ": [("Средний", "Выиграй матч с первой случайной комбинацией навыков.")],
    "Выживальщик": [("Средний", "Пройди матч без смены класса до финала.")],
}

def storage_path() -> Path:
    base = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation)
    folder = Path(base) if base else (Path.home() / ".kf2_randomizer")
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "state.json"


def load_state() -> dict:
    try:
        data = json.loads(storage_path().read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def save_state(state: dict) -> None:
    target = storage_path()
    tmp = target.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(target)


def icon_pixmap() -> QPixmap:
    pm = QPixmap(64, 64)
    pm.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QColor("#E34945"))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(4, 4, 56, 56, 13, 13)
    painter.setBrush(QColor("#101317"))
    painter.drawRoundedRect(8, 8, 48, 48, 10, 10)
    painter.setPen(QPen(QColor("#FFE0D9"), 4))
    painter.drawLine(18, 20, 28, 20)
    painter.drawLine(18, 20, 18, 45)
    painter.drawLine(18, 33, 30, 45)
    painter.drawLine(18, 33, 29, 20)
    painter.drawLine(35, 20, 49, 20)
    painter.drawLine(49, 20, 36, 45)
    painter.drawLine(36, 45, 50, 45)
    painter.end()
    return pm


QSS = """
* { font-family: 'Segoe UI', 'Arial'; color: #EBEDEF; font-size: 13px; }
QMainWindow, #Root { background: #101216; }
QFrame#Panel { background: #181B21; border: 1px solid #2B303A; border-radius: 14px; }
QFrame#Card { background: #20242C; border: 1px solid #303641; border-radius: 12px; }
QFrame#Hero { background: #211A1B; border: 1px solid #6B3432; border-radius: 16px; }
QLabel#Brand { color: #FFFFFF; font-size: 23px; font-weight: 900; letter-spacing: 2px; }
QLabel#Kicker { color: #EF736A; font-size: 11px; font-weight: 700; letter-spacing: 1px; }
QLabel#Title { color: #FFFFFF; font-size: 17px; font-weight: 800; }
QLabel#Section { color: #F1F2F3; font-size: 12px; font-weight: 800; }
QLabel#Muted { color: #99A1AF; }
QLabel#Value { color: #FFF9F4; font-size: 18px; font-weight: 750; }
QLabel#HeroValue { color: #FFFFFF; font-size: 33px; font-weight: 900; }
QLabel#Badge { background: #44211F; color: #FFB3A8; border: 1px solid #80443E;
                 border-radius: 8px; padding: 7px 10px; font-weight: 800; }
QPushButton { background: #272C34; border: 1px solid #3A414D; border-radius: 9px;
              padding: 10px 14px; font-weight: 650; }
QPushButton:hover { background: #353C48; border-color: #6B7381; }
QPushButton:pressed { background: #424957; }
QPushButton#Primary { background: #DB4842; border: 1px solid #F46B61; color: white;
                      font-weight: 850; font-size: 14px; }
QPushButton#Primary:hover { background: #F0574E; }
QPushButton#Primary:pressed { background: #C43B37; }
QPushButton#Quiet { background: transparent; border-color: #353A43; color: #AFB6C2; }
QPushButton#Quiet:hover { background: #292E38; color: white; }
QPushButton:disabled { color: #5F646F; background: #1D2025; border-color: #272B32; }
QComboBox { background: #242932; border: 1px solid #414855; border-radius: 8px;
            padding: 9px 10px; min-height: 18px; }
QComboBox:hover { border-color: #E17870; }
QComboBox::drop-down { border: 0px; width: 23px; }
QComboBox QAbstractItemView { background: #242932; border: 1px solid #474F5C;
                              selection-background-color: #96403C; }
QCheckBox { spacing: 9px; padding: 3px 1px; }
QCheckBox::indicator { width: 17px; height: 17px; border-radius: 5px;
                       background: #252B35; border: 1px solid #626A77; }
QCheckBox::indicator:checked { background: #D95149; border-color: #D95149; image: none; }
QScrollArea { background: transparent; border: none; }
QScrollArea > QWidget > QWidget { background: transparent; }
QScrollBar:vertical { background: transparent; width: 9px; margin: 3px; }
QScrollBar::handle:vertical { background: #414955; border-radius: 4px; min-height: 35px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QListWidget { border: 0px; background: #181B21; outline: none; }
QListWidget::item { padding: 10px; border-bottom: 1px solid #2A2E36; }
QListWidget::item:selected { background: #3D292A; border-radius: 8px; }
QSplitter::handle { background: transparent; width: 5px; }
"""


def label(text: str = "", kind: str = "", wrap: bool = False) -> QLabel:
    out = QLabel(text)
    if kind:
        out.setObjectName(kind)
    out.setWordWrap(wrap)
    return out


def button(text: str, kind: str = "") -> QPushButton:
    b = QPushButton(text)
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    if kind:
        b.setObjectName(kind)
    return b


def panel(title: str | None = None) -> tuple[QFrame, QVBoxLayout]:
    frame = QFrame()
    frame.setObjectName("Panel")
    lay = QVBoxLayout(frame)
    lay.setContentsMargins(16, 16, 16, 16)
    lay.setSpacing(10)
    if title:
        lay.addWidget(label(title.upper(), "Section"))
    return frame, lay


def build_card(name: str) -> tuple[QFrame, QLabel]:
    card = QFrame()
    card.setObjectName("Card")
    vl = QVBoxLayout(card)
    vl.setContentsMargins(17, 15, 17, 15)
    vl.setSpacing(8)
    vl.addWidget(label(name.upper(), "Kicker"))
    value = label("—", "Value", True)
    value.setMinimumHeight(46)
    value.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    vl.addWidget(value)
    return card, value


class Randomizer(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"Killing Floor 2 Randomizer — {VERSION}")
        self.setWindowIcon(QIcon(icon_pixmap()))
        self.resize(1330, 855)
        self.setMinimumSize(1000, 700)
        self.prefs = load_state()
        self.history: list[dict] = [x for x in self.prefs.get("history", []) if isinstance(x, dict)][:80]
        self.bag: list[str] = [x for x in self.prefs.get("bag", []) if x in PERKS]
        self.current: dict = self.history[0].copy() if self.history else {}
        self.perk_checks: dict[str, QCheckBox] = {}
        self.build_ui()
        self.refresh_history()
        if self.current:
            self.show_result(self.current)
        else:
            self.generate()

    def build_ui(self) -> None:
        root = QWidget()
        root.setObjectName("Root")
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(24, 20, 24, 18)
        outer.setSpacing(16)

        header = QHBoxLayout()
        brand = QVBoxLayout()
        brand.setSpacing(2)
        brand.addWidget(label("HORZINE // RANDOM SYSTEM", "Kicker"))
        brand.addWidget(label("KILLING FLOOR 2  /  RANDOMIZER", "Brand"))
        header.addLayout(brand)
        header.addStretch(1)
        htag = label(f"DESKTOP  ·  v{VERSION}", "Muted")
        header.addWidget(htag, 0, Qt.AlignmentFlag.AlignVCenter)
        outer.addLayout(header)

        split = QSplitter(Qt.Orientation.Horizontal)
        split.setChildrenCollapsible(False)
        split.setHandleWidth(14)
        outer.addWidget(split, 1)
        sidebar = QScrollArea()
        sidebar.setWidgetResizable(True)
        sidebar.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        sidecontent = QWidget()
        sidelay = QVBoxLayout(sidecontent)
        sidelay.setContentsMargins(0, 0, 0, 0)
        sidelay.setSpacing(12)
        sidebar.setWidget(sidecontent)
        split.addWidget(sidebar)

        prefs_panel, pp = panel("Фильтр классов")
        pp.addWidget(label("Отметь классы, которые могут выпадать.", "Muted", True))
        for perk, data in PERKS.items():
            cb = QCheckBox(f"{perk}   /   {data['en']}")
            cb.setChecked(perk in self.prefs.get("selected_perks", list(PERKS)))
            self.perk_checks[perk] = cb
            cb.toggled.connect(self.persist)
            pp.addWidget(cb)
        select_buttons = QHBoxLayout()
        all_btn = button("Все", "Quiet")
        all_btn.clicked.connect(lambda: self.set_all_perks(True))
        none_btn = button("Снять все", "Quiet")
        none_btn.clicked.connect(lambda: self.set_all_perks(False))
        select_buttons.addWidget(all_btn)
        select_buttons.addWidget(none_btn)
        pp.addLayout(select_buttons)
        sidelay.addWidget(prefs_panel)

        settings_panel, sp = panel("Настройки генерации")
        self.skill_check = QCheckBox("Генерировать ветку навыков (5–25)")
        self.skill_check.setChecked(bool(self.prefs.get("skills_on", True)))
        self.skill_check.toggled.connect(self.persist)
        sp.addWidget(self.skill_check)
        self.map_check = QCheckBox("Случайная карта")
        self.map_check.setChecked(bool(self.prefs.get("map", True)))
        self.map_check.toggled.connect(self.persist)
        sp.addWidget(self.map_check)
        self.smart_check = QCheckBox("Без повторов классов до полного цикла")
        self.smart_check.setChecked(bool(self.prefs.get("smart", True)))
        self.smart_check.toggled.connect(self.persist)
        sp.addWidget(self.smart_check)
        self.solo_check = QCheckBox("Играю в одиночку")
        self.solo_check.setChecked(bool(self.prefs.get("solo", False)))
        self.solo_check.toggled.connect(self.persist)
        sp.addWidget(self.solo_check)

        sp.addWidget(label("СЛОЖНОСТЬ МАТЧА", "Kicker"))
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Случайная"] + DIFFICULTIES)
        self.difficulty_combo.setCurrentText(self.prefs.get("difficulty", "Случайная"))
        self.difficulty_combo.currentTextChanged.connect(self.persist)
        sp.addWidget(self.difficulty_combo)

        sp.addWidget(label("ПРОДОЛЖИТЕЛЬНОСТЬ", "Kicker"))
        self.length_combo = QComboBox()
        self.length_combo.addItems(["Случайная"] + [name for name, _ in LENGTHS])
        self.length_combo.setCurrentText(self.prefs.get("length", "Случайная"))
        self.length_combo.currentTextChanged.connect(self.persist)
        sp.addWidget(self.length_combo)

        sp.addWidget(label("ИСПЫТАНИЕ", "Kicker"))
        self.challenge_combo = QComboBox()
        self.challenge_combo.addItems(["Без испытания", "Случайное", "Лёгкий", "Средний", "Сложный"])
        self.challenge_combo.setCurrentText(self.prefs.get("challenge", "Случайное"))
        self.challenge_combo.currentTextChanged.connect(self.persist)
        sp.addWidget(self.challenge_combo)
        sidelay.addWidget(settings_panel)
        sidelay.addStretch(1)
        split.setStretchFactor(0, 0)

        main = QWidget()
        mainlay = QVBoxLayout(main)
        mainlay.setContentsMargins(0, 0, 0, 0)
        mainlay.setSpacing(13)
        split.addWidget(main)
        split.setStretchFactor(1, 1)
        split.setSizes([345, 950])

        hero = QFrame()
        hero.setObjectName("Hero")
        herolay = QVBoxLayout(hero)
        herolay.setContentsMargins(24, 22, 24, 22)
        herolay.setSpacing(7)
        first = QHBoxLayout()
        first.addWidget(label("ТВОЙ СЛЕДУЮЩИЙ КЛАСС", "Kicker"))
        first.addStretch(1)
        self.mark = label("--", "Badge")
        first.addWidget(self.mark)
        herolay.addLayout(first)
        self.perk_name = label("—", "HeroValue", True)
        herolay.addWidget(self.perk_name)
        self.perk_meta = label("Нажми «Сгенерировать»", "Muted", True)
        herolay.addWidget(self.perk_meta)
        mainlay.addWidget(hero)

        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(12)
        self.skills_card, self.skills_value = build_card("Ветка навыков")
        self.map_card, self.map_value = build_card("Карта")
        self.diff_card, self.diff_value = build_card("Сложность")
        self.length_card, self.length_value = build_card("Длина матча")
        grid.addWidget(self.skills_card, 0, 0)
        grid.addWidget(self.map_card, 0, 1)
        grid.addWidget(self.diff_card, 1, 0)
        grid.addWidget(self.length_card, 1, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        mainlay.addLayout(grid)

        chal, cl = panel("Дополнительное испытание")
        self.challenge_value = label("—", "Value", True)
        self.challenge_value.setMinimumHeight(42)
        cl.addWidget(self.challenge_value)
        self.challenge_level = label("Пользовательский челлендж, не официальный режим игры", "Muted", True)
        cl.addWidget(self.challenge_level)
        mainlay.addWidget(chal)

        actions = QHBoxLayout()
        self.generate_btn = button("СГЕНЕРИРОВАТЬ   /   Ctrl+R", "Primary")
        self.generate_btn.clicked.connect(self.generate)
        self.generate_btn.setMinimumHeight(49)
        actions.addWidget(self.generate_btn, 4)
        reroll = button("Только навыки")
        reroll.clicked.connect(self.reroll_skills)
        actions.addWidget(reroll, 2)
        copy_btn = button("Копировать")
        copy_btn.clicked.connect(self.copy_result)
        actions.addWidget(copy_btn, 2)
        mainlay.addLayout(actions)

        hist, hl = panel("История · двойной клик откроет результат")
        top = QHBoxLayout()
        self.count_label = label("", "Muted")
        top.addWidget(self.count_label)
        top.addStretch(1)
        clear_btn = button("Очистить историю", "Quiet")
        clear_btn.clicked.connect(self.clear_history)
        top.addWidget(clear_btn)
        hl.addLayout(top)
        self.history_list = QListWidget()
        self.history_list.setMinimumHeight(130)
        self.history_list.itemDoubleClicked.connect(self.restore_history)
        hl.addWidget(self.history_list, 1)
        mainlay.addWidget(hist, 1)

        footer = label("Случайный набор для игры вручную. Не изменяет файлы, серверы и инвентарь KF2.", "Muted", True)
        mainlay.addWidget(footer)

    def set_all_perks(self, enabled: bool) -> None:
        for cb in self.perk_checks.values():
            cb.setChecked(enabled)
        self.persist()

    def selected_perks(self) -> list[str]:
        return [p for p, cb in self.perk_checks.items() if cb.isChecked()]

    def persist(self, *_args: object) -> None:
        self.prefs.update({
            "selected_perks": self.selected_perks(),
            "skills_on": self.skill_check.isChecked(),
            "map": self.map_check.isChecked(),
            "smart": self.smart_check.isChecked(),
            "solo": self.solo_check.isChecked(),
            "difficulty": self.difficulty_combo.currentText(),
            "length": self.length_combo.currentText(),
            "challenge": self.challenge_combo.currentText(),
            "bag": self.bag,
            "history": self.history[:80],
        })
        try:
            save_state(self.prefs)
        except OSError as exc:
            self.statusBar().showMessage(f"Не удалось сохранить настройки: {exc}", 6000)

    def pick_perk(self, available: list[str]) -> str:
        if not self.smart_check.isChecked():
            return RNG.choice(available)
        # Shuffle-bag mode: every enabled class appears once per round.
        self.bag = [p for p in self.bag if p in available]
        if not self.bag:
            self.bag = available.copy()
            RNG.shuffle(self.bag)
            if self.history and len(self.bag) > 1 and self.bag[-1] == self.history[0].get("perk"):
                self.bag[0], self.bag[-1] = self.bag[-1], self.bag[0]
        return self.bag.pop()

    def pick_skills(self, old: str = "") -> str:
        if not self.skill_check.isChecked():
            return "Свободный выбор"
        # Character skill tiers unlock at levels 5, 10, 15, 20 and 25.
        for _ in range(10):
            result = "    ".join(f"{level}: {RNG.choice(('Л', 'П'))}" for level in (5, 10, 15, 20, 25))
            if result != old:
                return result
        return result

    def pick_challenge(self, perk: str) -> tuple[str, str]:
        wanted = self.challenge_combo.currentText()
        if wanted == "Без испытания":
            return "Без дополнительного испытания", ""
        all_challenges = list(COMMON_CHALLENGES) + CLASS_CHALLENGES.get(perk, [])
        if self.solo_check.isChecked():
            all_challenges = [(lvl, ch) for lvl, ch in all_challenges if "союзник" not in ch.lower() and "команд" not in ch.lower()]
        if wanted != "Случайное":
            all_challenges = [(lvl, ch) for lvl, ch in all_challenges if lvl == wanted]
        if not all_challenges:
            return "Нет подходящих испытаний", ""
        return RNG.choice(all_challenges)

    def generate(self) -> None:
        perks = self.selected_perks()
        if not perks:
            QMessageBox.warning(self, "Нет доступных классов", "Отметь хотя бы один класс в левой панели.")
            return
        perk = self.pick_perk(perks)
        diff = self.difficulty_combo.currentText()
        if diff == "Случайная":
            diff = RNG.choice(DIFFICULTIES)
        length = self.length_combo.currentText()
        if length == "Случайная":
            length = RNG.choice([x[0] for x in LENGTHS])
        lvl, ch = self.pick_challenge(perk)
        result = {
            "when": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "perk": perk,
            "skills": self.pick_skills(),
            "map": RNG.choice(MAPS) if self.map_check.isChecked() else "Свободный выбор",
            "difficulty": diff,
            "length": length,
            "challenge": ch,
            "level": lvl,
        }
        self.accept_result(result)

    def accept_result(self, result: dict) -> None:
        self.current = result.copy()
        self.history.insert(0, result.copy())
        self.history = self.history[:80]
        self.show_result(result)
        self.refresh_history()
        self.persist()

    def reroll_skills(self) -> None:
        if not self.current:
            return
        result = self.current.copy()
        result["skills"] = self.pick_skills(str(result.get("skills", "")))
        result["when"] = datetime.now().strftime("%d.%m.%Y %H:%M")
        self.accept_result(result)

    def show_result(self, result: dict) -> None:
        perk = result.get("perk", "")
        data = PERKS.get(perk, {})
        self.perk_name.setText(perk or "—")
        self.perk_meta.setText(f"{data.get('en', '')}   /   {data.get('role', '')}")
        self.mark.setText(data.get("mark", "--"))
        self.skills_value.setText(result.get("skills", "—"))
        self.map_value.setText(result.get("map", "—"))
        self.diff_value.setText(result.get("difficulty", "—"))
        self.length_value.setText(result.get("length", "—"))
        self.challenge_value.setText(result.get("challenge", "—"))
        lvl = result.get("level", "")
        self.challenge_level.setText(
            ("Сложность испытания: " + lvl + "  ·  Пользовательский челлендж")
            if lvl else "Без дополнительного условия"
        )

    def result_text(self, data: dict) -> str:
        return ("KILLING FLOOR 2 — RANDOMIZER\n"
                f"Класс: {data.get('perk', '—')}\n"
                f"Навыки: {data.get('skills', '—')}\n"
                f"Карта: {data.get('map', '—')}\n"
                f"Сложность: {data.get('difficulty', '—')}\n"
                f"Длина: {data.get('length', '—')}\n"
                f"Испытание: {data.get('challenge', '—')}\n")

    def copy_result(self) -> None:
        if self.current:
            QApplication.clipboard().setText(self.result_text(self.current))
            self.statusBar().showMessage("Результат скопирован в буфер обмена", 3500)

    def refresh_history(self) -> None:
        self.history_list.clear()
        for item in self.history:
            self.history_list.addItem(
                f"{item.get('when', '')}    •    {item.get('perk', '?')}    /    "
                f"{item.get('map', '?')}    /    {item.get('difficulty', '?')}"
            )
        self.count_label.setText(f"Сохранено: {len(self.history)} / 80")

    def restore_history(self, item) -> None:
        index = self.history_list.row(item)
        if 0 <= index < len(self.history):
            self.current = self.history[index].copy()
            self.show_result(self.current)
            self.statusBar().showMessage("Результат восстановлен из истории", 2500)

    def clear_history(self) -> None:
        if not self.history:
            return
        reply = QMessageBox.question(self, "Очистить историю", "Удалить сохранённые результаты?")
        if reply == QMessageBox.StandardButton.Yes:
            self.history.clear()
            self.refresh_history()
            self.persist()

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_R and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.generate()
            event.accept()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event) -> None:
        self.persist()
        super().closeEvent(event)


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("KF2 Randomizer")
    app.setOrganizationName("YungSpiderQ")
    app.setStyle("Fusion")
    app.setStyleSheet(QSS)
    win = Randomizer()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()