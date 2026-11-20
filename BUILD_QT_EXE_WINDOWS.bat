@echo off
setlocal
cd /d "%~dp0"
py -3.12 -m pip install -r requirements.txt "pyinstaller>=6.20,<7"
if errorlevel 1 exit /b 1
py -3.12 -m PyInstaller --noconfirm --clean --onedir --windowed --name KF2-Randomizer --icon assets\kf2.ico kf2_randomizer.py
if errorlevel 1 exit /b 1
echo Portable: dist\KF2-Randomizer\KF2-Randomizer.exe
pause
