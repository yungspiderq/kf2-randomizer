# KF2 Randomizer v0.3.0 — desktop Windows edition

This release has **two real Windows desktop applications**, with **no HTML/browser launcher**:

- **KF2-Randomizer-Native.exe** — portable, dependency-free Windows x64 application, built directly against Win32 APIs. Included immediately in this release.
- **KF2-Randomizer.exe** — PySide6/Qt Windows desktop GUI, assembled by GitHub Actions and added to the release when the workflow completes successfully.

Both allow class selection, map/difficulty/length randomization, optional skill choices and challenges. They don't alter the game, access user accounts, or require an online connection. Native edition saves settings and up to 80 history entries in `%APPDATA%\KF2 Randomizer\settings.ini`.

**Windows SmartScreen:** the programs are not code-signed. Windows may show a security warning. Review the source code and releases before running.