# KF2 Randomizer v0.4.0 — In-app updates

**Windows desktop app, no HTML and no browser.** Download `KF2-Randomizer.exe` below and run it.

- New **Проверить обновления** button in the top-right area of the Qt application.
- Optional automatic update check on launch (can be turned off in Settings).
- Downloads a newer stable version from **this repository's GitHub Releases**.
- Verifies the executable against its published **SHA-256** before installation.
- On a Windows `.exe` launch, closes the program, replaces the old executable, and restarts it. Your settings and history stay in your user profile.
- Download progress and cancellation, friendly offline/error handling.
- Automatic Windows `.exe` building and GitHub Release publishing when a new version is merged to `main`.

**Note:** Automatic self-installation is supported by the PySide6 `KF2-Randomizer.exe`. The older lightweight `KF2-Randomizer-Native.exe` from v0.3.0 does not implement self-updates; use this new desktop EXE instead.

The release binaries are unsigned; Windows SmartScreen might ask for confirmation. This is a third-party fan utility, not affiliated with Tripwire Interactive.