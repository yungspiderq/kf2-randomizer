@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>&1
if errorlevel 1 (set "PY=python") else (set "PY=py -3.12")
if not exist ".venv\Scripts\python.exe" (
  %PY% -m venv .venv || goto fail
)
".venv\Scripts\python.exe" -m pip install -r requirements.txt || goto fail
".venv\Scripts\python.exe" kf2_randomizer.py
exit /b %errorlevel%
:fail
echo PySide6/Python install failed.
pause
exit /b 1