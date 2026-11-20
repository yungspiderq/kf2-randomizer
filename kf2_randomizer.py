"""Killing Floor 2 Randomizer — desktop app (PySide6, Python 3.10+).

This tool suggests OPTIONAL in-game challenges; it does not change Killing Floor 2
or automatically equip in-game items. Data is a curated, editable starter catalog.
"""
from __future__ import annotations

import json
import random
import sys
import threading
from datetime import datetime
from pathlib import Path
from typing import Any

from update_service import Release, fetch_latest, download_update, launch_replace_and_restart
from weapons_data import CATEGORIES, WEAPONS, WEAPON_BY_ID, available_weapons, choose_loadout, weapon_labels
from ui_icons import icon as glyph

from PySide6.QtCore import Qt, QStandardPaths, QThread, Signal, QTimer, QUrl
from PySide6.QtGui import QColor, QFont, QIcon, QPainter, QPen, QPixmap, QDesktopServices
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QListWidget, QMainWindow, QMessageBox, QPushButton, QProgressDialog, QScrollArea,
    QSizePolicy, QSplitter, QVBoxLayout, QWidget,
)

APP_TITLE = "KF2 RANDOMIZER"
VERSION = "0.5.0"
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

PERK_ICONS = {
    "Берсеркер": "melee", "Коммандос": "assault", "Поддержка": "shotgun",
    "Полевой медик": "medical", "Подрывник": "explosive", "Поджигатель": "flame",
    "Стрелок": "handgun", "Снайпер": "precision", "Спецназ": "smg",
    "Выживальщик": "special",
}

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
* { font-family: 'Segoe UI', 'Arial'; color: #E5E9EF; font-size: 13px; }
QMainWindow, #Root { background: #111419; }
QFrame#Panel { background: #1B2026; border: 1px solid #303640; border-radius: 9px; }
QFrame#Card { background: #1A1F25; border: 1px solid #303640; border-radius: 8px; }
QFrame#Hero { background: #1C2026; border: 1px solid #35383E; border-left: 3px solid #C95A50; border-radius: 9px; }
QFrame#WeaponRow { background: #191E23; border: 1px solid #303640; border-radius: 7px; }
QLabel#Brand { color: #F3F5F8; font-size: 23px; font-weight: 700; }
QLabel#Kicker { color: #C1C8D1; font-size: 11px; font-weight: 600; }
QLabel#Title { color: #F3F5F8; font-size: 17px; font-weight: 700; }
QLabel#Section { color: #F3F5F8; font-size: 13px; font-weight: 650; }
QLabel#Muted { color: #9EA8B5; }
QLabel#Value { color: #F0F2F5; font-size: 16px; font-weight: 600; }
QLabel#HeroValue { color: #FFFFFF; font-size: 30px; font-weight: 700; }
QLabel#Badge { background: #382624; color: #E9B0A9; border: 1px solid #60423E;
                 border-radius: 5px; padding: 5px 8px; font-weight: 700; }
QLabel#WeaponTitle { color: #F3F5F8; font-size: 14px; font-weight: 650; }
QLabel#WeaponInfo { color: #AAB4BE; font-size: 11px; }
QLabel#DlcBadge { color: #D4C09D; font-size: 10px; background: #302C26;
                  border: 1px solid #554B3E; border-radius: 4px; padding: 3px 6px; }
QPushButton { background: #262C34; border: 1px solid #3B434D; border-radius: 7px;
              padding: 9px 12px; font-weight: 600; }
QPushButton:hover { background: #333B45; border-color: #626B77; }
QPushButton:pressed { background: #404850; }
QPushButton#Primary { background: #C85750; border: 1px solid #CB615A; color: white;
                      font-weight: 700; }
QPushButton#Primary:hover { background: #DC655D; }
QPushButton#Primary:pressed { background: #A4443F; }
QPushButton#Quiet { background: transparent; border-color: #38414C; color: #CED5DE; }
QPushButton#Quiet:hover { background: #282F38; color: white; }
QPushButton:disabled { color: #667180; background: #20252B; border-color: #303640; }
QComboBox { background: #242B33; border: 1px solid #414B55; border-radius: 7px;
            padding: 8px 10px; min-height: 18px; }
QComboBox:hover { border-color: #B26962; }
QComboBox::drop-down { border: 0px; width: 22px; }
QComboBox QAbstractItemView { background: #242B33; border: 1px solid #414B55;
                              selection-background-color: #68423F; }
QCheckBox { spacing: 8px; padding: 3px 1px; }
QCheckBox::indicator { width: 16px; height: 16px; border-radius: 4px;
                       background: #252B33; border: 1px solid #687380; }
QCheckBox::indicator:checked { background: #C85750; border-color: #C85750; image: none; }
QScrollArea { background: transparent; border: none; }
QScrollArea > QWidget > QWidget { background: transparent; }
QScrollBar:vertical { background: transparent; width: 9px; margin: 3px; }
QScrollBar::handle:vertical { background: #454D58; border-radius: 4px; min-height: 35px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QListWidget { border: 0px; background: #1B2026; outline: none; }
QListWidget::item { padding: 10px; border-bottom: 1px solid #303640; }
QListWidget::item:selected { background: #3D3030; border-radius: 6px; }
QSplitter::handle { background: transparent; width: 7px; }
"""


def label(text: str = "", kind: str = "", wrap: bool = False) -> QLabel:
    out = QLabel(text)
    if kind:
        out.setObjectName(kind)
    out.setWordWrap(wrap)
    return out


def button(text: str, kind: str = "", icon_name: str = "") -> QPushButton:
    b = QPushButton(text)
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    if icon_name:
        b.setIcon(glyph(icon_name, "#FFFFFF" if kind == "Primary" else "#D5DCE5"))
    if kind:
        b.setObjectName(kind)
    return b


def panel(title: str | None = None, icon_name: str = "") -> tuple[QFrame, QVBoxLayout]:
    frame = QFrame()
    frame.setObjectName("Panel")
    lay = QVBoxLayout(frame)
    lay.setContentsMargins(16, 16, 16, 16)
    lay.setSpacing(10)
    if title:
        heading = QHBoxLayout()
        heading.setSpacing(8)
        if icon_name:
            emblem = QLabel()
            emblem.setPixmap(glyph(icon_name, "#A9B3BF").pixmap(18, 18))
            heading.addWidget(emblem)
        heading.addWidget(label(title, "Section"), 1)
        lay.addLayout(heading)
    return frame, lay


def build_card(name: str) -> tuple[QFrame, QLabel]:
    card = QFrame()
    card.setObjectName("Card")
    vl = QVBoxLayout(card)
    vl.setContentsMargins(17, 15, 17, 15)
    vl.setSpacing(8)
    vl.addWidget(label(name, "Kicker"))
    value = label("—", "Value", True)
    value.setMinimumHeight(46)
    value.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    vl.addWidget(value)
    return card, value


class UpdateWorker(QThread):
    checked = Signal(object)
    downloaded = Signal(str)
    progress = Signal(int)
    failed = Signal(str)

    def __init__(self, mode: str, release: Release | None = None) -> None:
        super().__init__()
        self.mode = mode
        self.release = release
        self.stop_event = threading.Event()

    def cancel(self) -> None:
        self.stop_event.set()

    def run(self) -> None:
        try:
            if self.mode == "check":
                self.checked.emit(fetch_latest(VERSION))
            elif self.mode == "download" and self.release is not None:
                path = download_update(
                    self.release,
                    lambda done, total: self.progress.emit(int(done * 100 / total)),
                    self.stop_event.is_set,
                )
                self.downloaded.emit(str(path))
        except Exception as exc:
            self.failed.emit(str(exc))


class Randomizer(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"Killing Floor 2 Randomizer — {VERSION}")
        self.setWindowIcon(QIcon(icon_pixmap()))
        self.resize(1320, 900)
        self.setMinimumSize(1024, 690)
        self.prefs = load_state()
        self.history: list[dict] = [x for x in self.prefs.get("history", []) if isinstance(x, dict)][:80]
        self.bag: list[str] = [x for x in self.prefs.get("bag", []) if x in PERKS]
        self.current: dict = self.history[0].copy() if self.history else {}
        self.perk_checks: dict[str, QCheckBox] = {}
        self._update_workers: set[UpdateWorker] = set()
        self._checking_silently = False
        self._downloading_update = False
        self._progress_dialog: QProgressDialog | None = None
        self.build_ui()
        self.refresh_history()
        if self.current:
            self.show_result(self.current)
        else:
            self.generate()
        if self.auto_updates_check.isChecked():
            QTimer.singleShot(1800, lambda: self.check_updates(silent=True))

    def build_ui(self) -> None:
        root = QWidget()
        root.setObjectName("Root")
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(20, 18, 20, 15)
        outer.setSpacing(12)

        header = QHBoxLayout()
        brand = QVBoxLayout()
        brand.setSpacing(2)
        brand.addWidget(label("Killing Floor 2 · утилита для матчей", "Muted"))
        brand.addWidget(label("Randomizer", "Brand"))
        header.addLayout(brand)
        header.addStretch(1)
        self.update_button = button("Проверить обновления", "Quiet", "update")
        self.update_button.clicked.connect(self.check_updates)
        header.addWidget(self.update_button, 0, Qt.AlignmentFlag.AlignVCenter)
        htag = label(f"v{VERSION}", "Muted")
        header.addWidget(htag, 0, Qt.AlignmentFlag.AlignVCenter)
        outer.addLayout(header)

        split = QSplitter(Qt.Orientation.Horizontal)
        split.setChildrenCollapsible(False)
        split.setHandleWidth(10)
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

        prefs_panel, pp = panel("Классы", "class")
        pp.addWidget(label("Отметь классы, которые могут выпадать.", "Muted", True))
        for perk, data in PERKS.items():
            perkrow = QHBoxLayout()
            perkrow.setSpacing(8)
            emblem = QLabel()
            emblem.setPixmap(glyph(PERK_ICONS[perk], "#B9C2CD", 17).pixmap(17, 17))
            emblem.setFixedWidth(19)
            perkrow.addWidget(emblem)
            cb = QCheckBox(perk)
            cb.setToolTip(data["en"] + " · " + data["role"])
            cb.setChecked(perk in self.prefs.get("selected_perks", list(PERKS)))
            self.perk_checks[perk] = cb
            cb.toggled.connect(self.persist)
            perkrow.addWidget(cb, 1)
            pp.addLayout(perkrow)
        select_buttons = QHBoxLayout()
        all_btn = button("Все", "Quiet")
        all_btn.clicked.connect(lambda: self.set_all_perks(True))
        none_btn = button("Снять все", "Quiet")
        none_btn.clicked.connect(lambda: self.set_all_perks(False))
        select_buttons.addWidget(all_btn)
        select_buttons.addWidget(none_btn)
        pp.addLayout(select_buttons)
        sidelay.addWidget(prefs_panel)

        settings_panel, sp = panel("Матч и испытания", "settings")
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
        self.auto_updates_check = QCheckBox("Проверять обновления при запуске")
        self.auto_updates_check.setChecked(bool(self.prefs.get("auto_updates", True)))
        self.auto_updates_check.toggled.connect(self.persist)
        sp.addWidget(self.auto_updates_check)

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

        weapon_panel, wp = panel("Оружие", "weapon")
        self.weapon_check = QCheckBox("Добавлять случайное оружие")
        self.weapon_check.setChecked(bool(self.prefs.get("weapons_on", True)))
        self.weapon_check.toggled.connect(self.persist)
        wp.addWidget(self.weapon_check)

        wp.addWidget(label("РЕЖИМ", "Kicker"))
        self.weapon_mode_combo = QComboBox()
        self.weapon_mode_combo.addItems(["По классу", "Любое оружие"])
        self.weapon_mode_combo.setCurrentText(self.prefs.get("weapon_mode", "По классу"))
        self.weapon_mode_combo.currentTextChanged.connect(self.persist)
        wp.addWidget(self.weapon_mode_combo)

        wp.addWidget(label("КОЛИЧЕСТВО", "Kicker"))
        self.weapon_count_combo = QComboBox()
        self.weapon_count_combo.addItems(["1", "2", "3"])
        self.weapon_count_combo.setCurrentText(str(self.prefs.get("weapon_count", "2")))
        self.weapon_count_combo.currentTextChanged.connect(self.persist)
        wp.addWidget(self.weapon_count_combo)

        wp.addWidget(label("КАТЕГОРИЯ", "Kicker"))
        self.weapon_kind_combo = QComboBox()
        self.weapon_kind_combo.addItem("Все категории", None)
        for kind, title in CATEGORIES.items():
            self.weapon_kind_combo.addItem(title, kind)
        stored_kind = self.prefs.get("weapon_kind")
        kind_index = self.weapon_kind_combo.findData(stored_kind)
        self.weapon_kind_combo.setCurrentIndex(max(kind_index, 0))
        self.weapon_kind_combo.currentIndexChanged.connect(self.persist)
        wp.addWidget(self.weapon_kind_combo)

        self.weapon_dlc_check = QCheckBox("Включить DLC-оружие")
        self.weapon_dlc_check.setChecked(bool(self.prefs.get("weapon_dlc", False)))
        self.weapon_dlc_check.toggled.connect(self.persist)
        wp.addWidget(self.weapon_dlc_check)
        self.weapon_avoid_check = QCheckBox("Стараться не повторять оружие")
        self.weapon_avoid_check.setChecked(bool(self.prefs.get("weapon_avoid", True)))
        self.weapon_avoid_check.toggled.connect(self.persist)
        wp.addWidget(self.weapon_avoid_check)
        wp.addWidget(label(
            "При фильтре по классу неподходящие классы временно пропускаются. "
            "DLC по умолчанию выключены.", "Muted", True))
        sidelay.addWidget(weapon_panel)
        sidelay.addStretch(1)
        split.setStretchFactor(0, 0)

        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True)
        main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        main = QWidget()
        mainlay = QVBoxLayout(main)
        mainlay.setContentsMargins(3, 1, 5, 3)
        mainlay.setSpacing(12)
        main_scroll.setWidget(main)
        split.addWidget(main_scroll)
        split.setStretchFactor(1, 1)
        split.setSizes([335, 970])

        hero = QFrame()
        hero.setObjectName("Hero")
        herolay = QVBoxLayout(hero)
        herolay.setContentsMargins(24, 22, 24, 22)
        herolay.setSpacing(7)
        first = QHBoxLayout()
        self.perk_icon = QLabel()
        self.perk_icon.setPixmap(glyph("class", "#E1A69E", 22).pixmap(22, 22))
        first.addWidget(self.perk_icon)
        first.addWidget(label("Случайный класс", "Kicker"))
        first.addStretch(1)
        self.mark = label("--", "Badge")
        first.addWidget(self.mark)
        herolay.addLayout(first)
        self.perk_name = label("—", "HeroValue", True)
        herolay.addWidget(self.perk_name)
        self.perk_meta = label("Нажми «Сгенерировать»", "Muted", True)
        herolay.addWidget(self.perk_meta)
        mainlay.addWidget(hero)

        weapons_frame, wl = panel("Набор оружия", "weapon")
        weapons_header = QHBoxLayout()
        weapons_header.setSpacing(8)
        self.weapon_summary = label("Оружие выбирается из игрового каталога", "Muted", True)
        weapons_header.addWidget(self.weapon_summary, 1)
        self.reroll_weapon_btn = button("Другое оружие", "Quiet", "reroll")
        self.reroll_weapon_btn.clicked.connect(self.reroll_weapons)
        weapons_header.addWidget(self.reroll_weapon_btn)
        wl.addLayout(weapons_header)
        self.weapon_rows_layout = QVBoxLayout()
        self.weapon_rows_layout.setSpacing(7)
        wl.addLayout(self.weapon_rows_layout)
        mainlay.addWidget(weapons_frame)

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

        chal, cl = panel("Дополнительное испытание", "check")
        self.challenge_value = label("—", "Value", True)
        self.challenge_value.setMinimumHeight(42)
        cl.addWidget(self.challenge_value)
        self.challenge_level = label("Пользовательский челлендж, не официальный режим игры", "Muted", True)
        cl.addWidget(self.challenge_level)
        mainlay.addWidget(chal)

        actions = QHBoxLayout()
        self.generate_btn = button("Сгенерировать", "Primary", "random")
        self.generate_btn.setToolTip("Случайный матч · Ctrl+R")
        self.generate_btn.clicked.connect(self.generate)
        self.generate_btn.setMinimumHeight(49)
        actions.addWidget(self.generate_btn, 4)
        reroll = button("Навыки", "", "reroll")
        reroll.clicked.connect(self.reroll_skills)
        actions.addWidget(reroll, 2)
        copy_btn = button("Копировать", "", "copy")
        copy_btn.clicked.connect(self.copy_result)
        actions.addWidget(copy_btn, 2)
        mainlay.addLayout(actions)

        hist, hl = panel("История", "history")
        top = QHBoxLayout()
        self.count_label = label("", "Muted")
        top.addWidget(self.count_label)
        top.addWidget(label("· двойной клик — открыть", "Muted"))
        top.addStretch(1)
        clear_btn = button("Очистить", "Quiet", "trash")
        clear_btn.clicked.connect(self.clear_history)
        top.addWidget(clear_btn)
        hl.addLayout(top)
        self.history_list = QListWidget()
        self.history_list.setMinimumHeight(145)
        self.history_list.setMaximumHeight(200)
        self.history_list.itemDoubleClicked.connect(self.restore_history)
        hl.addWidget(self.history_list, 1)
        mainlay.addWidget(hist)

        footer = label("Планировщик для матчей KF2. Ничего не меняет в самой игре.", "Muted", True)
        mainlay.addWidget(footer)

    def _spawn_update_worker(self, worker: UpdateWorker) -> None:
        self._update_workers.add(worker)
        worker.finished.connect(lambda: self._update_workers.discard(worker))
        worker.finished.connect(worker.deleteLater)
        worker.failed.connect(self._update_failed)
        worker.start()

    def check_updates(self, *_unused: object, silent: bool = False) -> None:
        if any(w.isRunning() for w in self._update_workers):
            return
        self._checking_silently = silent
        self.update_button.setEnabled(False)
        self.update_button.setText("Проверка...")
        worker = UpdateWorker("check")
        worker.checked.connect(self._updates_checked)
        worker.finished.connect(self._check_finished)
        self._spawn_update_worker(worker)

    def _check_finished(self) -> None:
        self.update_button.setEnabled(True)
        self.update_button.setText("Проверить обновления")

    def _updates_checked(self, release: Release | None) -> None:
        if release is None:
            self.statusBar().showMessage(f"Установлена актуальная версия {VERSION}", 5000)
            if not self._checking_silently:
                QMessageBox.information(self, "Обновления", f"Установлена актуальная версия v{VERSION}.")
            return
        details = ("\n\nЧто нового:\n" + release.notes) if release.notes else ""
        answer = QMessageBox.question(
            self, "Доступно обновление",
            f"Доступна версия v{release.version}.\nТекущая версия: v{VERSION}."
            f"{details}\n\nСкачать обновление и перезапустить программу?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )
        if answer == QMessageBox.StandardButton.Yes:
            QTimer.singleShot(100, lambda: self._download_release(release))

    def _download_release(self, release: Release) -> None:
        if any(w.isRunning() for w in self._update_workers):
            QTimer.singleShot(300, lambda: self._download_release(release))
            return
        self._downloading_update = True
        dialog = QProgressDialog("Загрузка обновления из GitHub Releases...", "Отмена", 0, 100, self)
        dialog.setWindowTitle(f"Обновление до v{release.version}")
        dialog.setAutoClose(False)
        dialog.setAutoReset(False)
        dialog.setMinimumDuration(0)
        dialog.setWindowModality(Qt.WindowModality.NonModal)
        dialog.setValue(0)
        self._progress_dialog = dialog
        worker = UpdateWorker("download", release)
        worker.progress.connect(dialog.setValue)
        worker.downloaded.connect(self._update_downloaded)
        dialog.canceled.connect(worker.cancel)
        self._spawn_update_worker(worker)
        dialog.show()

    def _update_downloaded(self, filename: str) -> None:
        self._downloading_update = False
        if self._progress_dialog is not None:
            self._progress_dialog.close()
            self._progress_dialog = None
        path = Path(filename)
        try:
            launch_replace_and_restart(path)
        except Exception as exc:
            QMessageBox.information(
                self, "Обновление загружено",
                f"Файл обновления проверен и сохранён:\n{path}\n\n"
                f"Для автоматической установки запусти собранный KF2-Randomizer.exe.\n{exc}",
            )
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(path.parent)))
            return
        self.persist()
        QTimer.singleShot(250, QApplication.quit)

    def _update_failed(self, message: str) -> None:
        was_downloading = self._downloading_update
        self._downloading_update = False
        if self._progress_dialog is not None:
            self._progress_dialog.close()
            self._progress_dialog = None
        self.statusBar().showMessage("Обновление: " + message, 9000)
        if message == "Загрузка отменена":
            return
        if was_downloading or not self._checking_silently:
            QMessageBox.warning(self, "Ошибка обновления", message)

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
            "auto_updates": self.auto_updates_check.isChecked(),
            "difficulty": self.difficulty_combo.currentText(),
            "length": self.length_combo.currentText(),
            "challenge": self.challenge_combo.currentText(),
            "weapons_on": self.weapon_check.isChecked(),
            "weapon_mode": self.weapon_mode_combo.currentText(),
            "weapon_count": self.weapon_count_combo.currentText(),
            "weapon_kind": self.weapon_kind_combo.currentData(),
            "weapon_dlc": self.weapon_dlc_check.isChecked(),
            "weapon_avoid": self.weapon_avoid_check.isChecked(),
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

    def weapon_pool(self, perk: str) -> list:
        return available_weapons(
            perk,
            any_class=self.weapon_mode_combo.currentText() == "Любое оружие",
            include_dlc=self.weapon_dlc_check.isChecked(),
            kind=self.weapon_kind_combo.currentData(),
        )

    def pick_weapon_ids(self, perk: str, old_ids: list[str] | None = None) -> list[str]:
        if not self.weapon_check.isChecked():
            return []
        count = int(self.weapon_count_combo.currentText())
        recent = old_ids or []
        if self.weapon_avoid_check.isChecked() and not recent:
            recent = self.current.get("weapons", []) if self.current else []
        selected = choose_loadout(
            self.weapon_pool(perk), count,
            recent=recent if self.weapon_avoid_check.isChecked() else (),
            rng=RNG,
        )
        return [w.id for w in selected]

    def reroll_weapons(self) -> None:
        if not self.current:
            return
        if not self.weapon_check.isChecked():
            QMessageBox.information(self, "Оружие выключено", "Включи случайное оружие в левой панели.")
            return
        perk = self.current.get("perk", "")
        if not self.weapon_pool(perk):
            QMessageBox.warning(self, "Нет оружия", "Для этого класса и фильтра нет доступных предметов. Измени настройки оружия.")
            return
        result = self.current.copy()
        result["weapons"] = self.pick_weapon_ids(perk, list(result.get("weapons", [])))
        result["when"] = datetime.now().strftime("%d.%m.%Y %H:%M")
        self.accept_result(result)

    def update_weapon_rows(self, ids: list[str]) -> None:
        while self.weapon_rows_layout.count():
            child = self.weapon_rows_layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
        weapons = [WEAPON_BY_ID[x] for x in ids if x in WEAPON_BY_ID]
        self.reroll_weapon_btn.setEnabled(bool(weapons))
        if not weapons:
            self.weapon_summary.setText("Случайное оружие выключено или не найдено")
            self.weapon_rows_layout.addWidget(label(
                "Включи оружие в настройках или поменяй категорию.", "Muted", True))
            return
        self.weapon_summary.setText(f"Выбрано: {len(weapons)} · {len(WEAPONS)} позиций в каталоге")
        for number, weapon in enumerate(weapons, 1):
            row = QFrame()
            row.setObjectName("WeaponRow")
            rowlayout = QHBoxLayout(row)
            rowlayout.setContentsMargins(13, 10, 13, 10)
            rowlayout.setSpacing(12)
            emblem = QLabel()
            emblem.setPixmap(glyph(weapon.kind, "#D9A19A", 22).pixmap(22, 22))
            emblem.setFixedWidth(24)
            rowlayout.addWidget(emblem)
            info = QVBoxLayout()
            info.setSpacing(3)
            info.addWidget(label(weapon.name, "WeaponTitle", True))
            info.addWidget(label(f"Слот {number:02d}  ·  {CATEGORIES[weapon.kind]}", "WeaponInfo"))
            rowlayout.addLayout(info, 1)
            if weapon.dlc:
                rowlayout.addWidget(label("DLC", "DlcBadge"))
            self.weapon_rows_layout.addWidget(row)

    def generate(self) -> None:
        perks = self.selected_perks()
        if not perks:
            QMessageBox.warning(self, "Нет доступных классов", "Отметь хотя бы один класс в левой панели.")
            return
        if self.weapon_check.isChecked():
            eligible = [p for p in perks if self.weapon_pool(p)]
            if not eligible:
                QMessageBox.warning(
                    self, "Нет подходящего оружия",
                    "Выбранная категория не содержит доступных предметов для разрешённых классов. "
                    "Включи другие категории, DLC или режим «Любое оружие»."
                )
                return
            perks = eligible
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
            "weapons": self.pick_weapon_ids(perk),
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
        self.perk_icon.setPixmap(glyph(PERK_ICONS.get(perk, "class"), "#E1A69E", 22).pixmap(22, 22))
        self.update_weapon_rows(result.get("weapons", []))
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
                f"Оружие: {', '.join(weapon_labels(data.get('weapons', []))) or 'Не выбрано'}\n"
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