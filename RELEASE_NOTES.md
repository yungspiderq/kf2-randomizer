# KF2 Randomizer v0.6.1 — Windows startup repair

Fixes the reported `Failed to load Python DLL python312.dll` startup issue by adding a **portable folder-based edition**, explicitly collecting required VC++ runtime DLLs in both editions, and verifying the actual packaged applications start on Windows.

### Recommended download if v0.6.0 failed

**KF2-Randomizer-Portable-Windows-x64.zip**

Extract the entire folder, keeping `_internal`, then open `KF2-Randomizer.exe` inside it. No Python installation, no browser, and no temporary `_MEI` runtime extraction.

### Other download

**KF2-Randomizer.exe** is the revised single-file build for users who prefer a one-file executable. Unlike the portable edition, it extracts to Windows Temp while running, which can be affected by system configuration or security software.

### Additional fixes

- CI now boots both *frozen* Windows EXEs with Qt, not merely the source-code UI.
- The portable edition's update checker directs users to the next portable ZIP instead of overwriting just the executable.
- Existing configuration, saved history, UI and other app features are preserved.
- SHA-256 sidecar files included for both downloads.

If the portable edition also cannot start, check Windows updates, install the official Microsoft Visual C++ Redistributable (x64), and inspect antivirus quarantine history without disabling antivirus protection.
