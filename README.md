# KF2 Randomizer — Windows Desktop

Native desktop randomizer for **Killing Floor 2** with ten classes, class filters, skill side combinations, optional challenges, maps, match difficulties, wave lengths, shuffle-bag anti-repeat mode and saved history. **No browser, HTML, or game injection.**

## Download

**[Latest GitHub Release](https://github.com/yungspiderq/kf2-randomizer/releases/latest)** — download `KF2-Randomizer.exe` under **Assets**. This is a self-contained 64-bit Windows Qt application; Python is not needed to run it.

Open the application and click **Проверить обновления** in the header. If a newer stable GitHub Release exists, confirm to download it. The app verifies SHA-256, exits, replaces itself and relaunches. Automatic checking at launch is enabled by default and can be disabled in the left Settings panel. Updates are opt-in and never install silently. Settings/history remain in your user profile.

The old `KF2-Randomizer-Native.exe` (Win32 build, v0.3.0) is kept in source history for reference, but only the main `KF2-Randomizer.exe` (PySide6) has in-app updates.

## Build from source

- Install Python 3.12 for Windows.
- Run `START_QT_WINDOWS.bat` to launch from source, or `BUILD_QT_EXE_WINDOWS.bat` to build `dist\\KF2-Randomizer.exe`.
- GitHub Actions builds the Windows release automatically on pushes to `main`. A new release is created if its version tag (as stated in `VERSION.txt`) does not already exist.

Development tests: `python -m unittest discover -s tests -v`. The updater code is in `update_service.py` and uses the GitHub REST API; file downloads are limited in size and SHA-256 verified. When the application is launched from Python sources, update downloading works, but auto-replacement of `python.exe` is intentionally disabled.

## Notes

- Windows binaries are unsigned and may prompt SmartScreen; the full source is included here.
- The app provides optional game-only suggestions, not a game mod; it does not modify the game.
- This is a fan project, unaffiliated with Tripwire Interactive.