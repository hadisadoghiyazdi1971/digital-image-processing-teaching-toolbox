@echo off
setlocal
cd /d "%~dp0"

echo ================================================================
echo Chapter 3 Toolbox - Python 3.12 launcher
echo ================================================================

py -3.12 -c "import numpy, scipy, skimage, PIL, matplotlib, tkinter" >nul 2>&1
if errorlevel 1 (
  echo [STOP] Python 3.12 or one of the required libraries is not available.
  echo Run CHECK_ENV.cmd first.
  echo See README.md / README_FA.md for installation instructions.
  pause
  exit /b 1
)

py -3.12 app.py
if errorlevel 1 (
  echo.
  echo [ERROR] The toolbox exited with an error.
  pause
  exit /b 2
)
endlocal
