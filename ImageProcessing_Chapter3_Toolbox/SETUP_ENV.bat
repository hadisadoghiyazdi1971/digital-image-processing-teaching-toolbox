@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  set "PY=py -3"
) else (
  where python >nul 2>nul
  if errorlevel 1 (
    echo Python 3 was not found. Install Python from python.org and try again.
    pause
    exit /b 1
  )
  set "PY=python"
)
if not exist .venv\Scripts\python.exe (
  echo [1/4] Creating virtual environment...
  %PY% -m venv .venv || exit /b 1
) else (
  echo [1/4] Virtual environment already exists.
)
echo [2/4] Installing/updating requirements...
.venv\Scripts\python.exe -m pip install --upgrade pip || exit /b 1
.venv\Scripts\python.exe -m pip install -r requirements.txt || exit /b 1
echo [3/4] Checking Tkinter GUI support...
.venv\Scripts\python.exe -c "import tkinter; print('Tkinter OK')" || (
  echo Tkinter is missing from this Python installation.
  pause
  exit /b 1
)
echo [4/4] Checking scientific packages...
.venv\Scripts\python.exe -c "import numpy, scipy, skimage, PIL, matplotlib; print('Scientific stack OK')" || exit /b 1
echo Setup complete.
exit /b 0
