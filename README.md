# KF2 Randomizer — Windows desktop (v0.3.0)

A standalone randomizer for **Killing Floor 2**. No browser, no embedded HTML, and no game injection.

## Download and run

- **`KF2-Randomizer-Native.exe`** — a ready-made native Win32 x64 application. No Python, installers, external runtimes or browser required. Start it directly on Windows 10/11.
- **`KF2-Randomizer.exe`** — the more elaborate PySide6/Qt desktop version; automatically compiled on Windows using GitHub Actions. Download from the release assets after the CI build completes.

**Features**: 10 perk classes with independent toggles; shuffle-bag mode (no repeats until all enabled classes have appeared); 27 starter maps; 4 difficulties; 4/7/10 Survival wave formats; 5 perk skill choices; custom optional class-specific challenges; filters for solo mode; copying result; history of up to 80 generations and persistent settings.

Native Win32 settings and history are stored in `%APPDATA%\KF2 Randomizer\settings.ini`. The Qt app stores its own settings in the platform's normal user configuration folder. Each is fully offline and non-invasive: it only suggests in-game challenges; it never changes the game or equips items.

## Publish on GitHub

Run `PUBLISH_TO_GITHUB.bat` on Windows while signed in to GitHub. The script creates **`yungspiderq/kf2-randomizer`** (public), pushes source and the ready Win32 exe, then publishes `v0.3.0` with the ready exe attached. If the repository already exists, the script only updates it when this is the correctly linked local checkout.

It requires Git for Windows and GitHub CLI (`gh`), automatically attempting to install `gh` through `winget` if missing. It does not modify other repositories. The included GitHub Actions workflow compiles the PySide6 version using Windows and attaches the compiled `KF2-Randomizer.exe` to the same release.

## Build the Qt version manually

On Windows with Python 3.12, run `BUILD_QT_EXE_WINDOWS.bat`. The resulting file is `dist\KF2-Randomizer.exe`. Alternatively, `START_QT_WINDOWS.bat` launches the Qt source after installing dependencies.

## Build the lightweight native EXE from source

`src/kf2_win32.c` implements the entire native app using only Windows API functions. `tools/build_native.py` cross-compiles it with `clang` and `lld-link` (Windows x64 target) without the Windows SDK. The Win32 program imports only system DLLs (`kernel32`, `user32`, `gdi32`). It does not use HTML/WebView, Electron, Python or Qt.

## Caveats

- Windows executables have **not** been live-tested on a Windows machine in this environment. The native EXE is statically checked as a valid PE32+ x64 Windows GUI binary, but UI behavior on Windows should still be tested.
- Programs are not code-signed; SmartScreen warnings may appear.
- This is a curated starter set of maps and user-made challenges, not a full official catalog.
- This is a fan utility unaffiliated with Tripwire Interactive.