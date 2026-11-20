# KF2 Randomizer — Windows Desktop

Standalone Qt application for Windows x64. No browser, HTML, or Python installation required.

## Windows start-up fix (v0.6.1)

If an older one-file version shows `Failed to load Python DLL python312.dll` inside a temporary `_MEI...` folder, **download the portable ZIP** from [GitHub Releases](https://github.com/yungspiderq/kf2-randomizer/releases/latest):

1. Download `KF2-Randomizer-Portable-Windows-x64.zip`.
2. Extract the **whole** `KF2-Randomizer` folder to Documents or another regular folder.
3. Open `KF2-Randomizer.exe` in that folder. **Keep `_internal` alongside it.**

Portable uses a folder-based runtime and does not extract the bundled Python DLL to Windows Temp each time. It is the recommended workaround for this error.

There is also a `KF2-Randomizer.exe` single-file download for systems where the one-file package works. Both editions include the VC++ runtime libraries and are smoke-tested as actual packaged EXEs on a Windows GitHub Actions runner before publication.

If the **portable** edition still fails, check the Windows Security protection history for quarantined DLLs and use the genuine Microsoft Visual C++ Redistributable x64. Keep security protection enabled.

### Updates

The single-file edition can check GitHub Releases and safely download and verify a replacement EXE. The portable edition detects an available update and opens the matching GitHub Release, so the entire portable folder can be replaced. User settings and history remain in their normal profile location.

### Building from source

Python 3.12 and PySide6 are needed for development only:

```powershell
py -3.12 -m pip install -r requirements.txt
py -3.12 -m unittest discover -s tests -v
py -3.12 tests/qt_smoke.py
```

GitHub Actions automatically builds both Windows forms, verifies both EXEs launch with Qt, produces SHA-256 files and publishes a versioned Release.

Previous app functionality and settings remain unchanged.

Independent fan project. Not affiliated with the original game's publisher.
