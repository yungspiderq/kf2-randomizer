@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>&1
if errorlevel 1 (set "PY=python") else (set "PY=py -3.12")
if not exist ".venv\Scripts\python.exe" (
  %PY% -m venv .venv || goto fail
)
".venv\Scripts\python.exe" -m pip install -r requirements.txt "pyinstaller>=6.11,<7" || goto fail
".venv\Scripts\python.exe" -m PyInstaller --onefile --windowed --clean --noconfirm --name "KF2-Randomizer" --icon "assets\kf2.ico" kf2_randomizer.py || goto fail
if not exist "dist\KF2-Randomizer.exe" goto fail
echo Build finished: dist\KF2-Randomizer.exe
pause
exit /b 0
:fail
echo Failed to build Qt desktop EXE. Check Python 3.12 and internet connectivity.
pause
exit /b 1