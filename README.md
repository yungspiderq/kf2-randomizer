# KF2 Randomizer — Windows Desktop

A self-contained **Killing Floor 2** fan-made randomizer for Windows x64. A real **PySide6 / Qt desktop app**, not a web page, HTML shell or game mod.

## Download and update

**[Latest release](https://github.com/yungspiderq/kf2-randomizer/releases/latest)** → `KF2-Randomizer.exe` under **Assets**.

The button **Проверить обновления** checks official releases for this repository, prompts for confirmation, downloads the verified `.exe`, restarts and preserves settings. SHA-256 validation is mandatory before installation; background automatic install is not performed. Windows SmartScreen may show a prompt because the app is not code-signed.

## Randomizer

- 10 playable KF2 perks, level 5–25 skill-side choices, maps, difficulty, match length and optional challenges.
- **85 curated in-game weapons** in 10 categories, including 12 optionally enabled DLC-labelled entries. Names and assignments are an editable catalog, not a claim of live in-game ownership or inventory.
- **Perk-only weapons** (default) or a global pool, up to 6 unique items, category selector, DLC toggle (off by default), and attempt to avoid weapons used on the previous roll.
- **Reroll weapons** without changing your class, skills, map or difficulty.
- Results in history and on clipboard include chosen weapon names. Compatible with v0.4.0 saved settings/history.
- Clean, restrained dark UI. Thin hand-drawn vector icons in toolbar, perk list and weapon results; no emoji/icon-font dependencies.

**Important:** This is a randomizer of virtual items inside the video game only. It does not change anything in KF2 or grant DLC ownership. Some game content/cross-perk flags may vary by game update; edits are welcome to `weapons_data.py`.

## Build locally

Use Python 3.12 on Windows:

```powershell
python -m pip install -r requirements.txt pyinstaller
python -m PyInstaller --noconfirm --onefile --windowed --clean --name KF2-Randomizer --icon assets/kf2.ico kf2_randomizer.py
```

Or run `START_QT_WINDOWS.bat` to start from Python, `BUILD_QT_EXE_WINDOWS.bat` to produce `dist/KF2-Randomizer.exe`. GitHub Actions automatically creates the Windows build and publishes a GitHub Release when a new `VERSION.txt` is merged to `main`.

Development checks:

```powershell
python -m unittest discover -s tests -v
python tests/qt_smoke.py
```

## Credits

Fan project by [yungspiderq](https://github.com/yungspiderq), not affiliated with Tripwire Interactive. UI cleanup follows the practical principles of [unslop](https://github.com/heydamir/unslop): clear hierarchy, restrained accent color, less visual noise, consistent spacing and purposeful icons. In-game item reference catalog based on the community-maintained [KF2 weapons index](https://killingfloor.fandom.com/wiki/Killing_Floor_2_Weapons).


## Weight-aware in-game inventory randomizer

Choose 15 / 20 capacity points and select **По количеству** (fit as many of the requested items as allowed), **Заполнить до лимита** (maximize weight without exceeding it) or **Случайный весовой бюджет** (pick a random weight target). All modes respect a maximum number of distinct items, the selected category and DLC setting. The requested 20-point option is enforced only for Support/Survivalist; other classes automatically use 15. The user must have the qualifying in-game skill/level unlocked to use 20. Item weights are taken from an older community catalogue; uncertain entries are omitted, not guessed.
