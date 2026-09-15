@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================================
echo Histogram Equalization Lecture - OFFLINE Python 3.12 runner
echo ============================================================
echo.
echo This edition does NOT use pip, PyPI, OpenCV, NumPy or Matplotlib.
echo.

echo [1/3] Checking 64-bit Python 3.12...
where py >nul 2>nul
if errorlevel 1 goto :no_python
py -3.12 -c "import sys,struct; assert sys.version_info[:2]==(3,12); assert struct.calcsize('P')*8==64" >nul 2>nul
if errorlevel 1 goto :no_python

echo [2/3] Verifying that no third-party package is required...
py -3.12 -c "import math,random,struct,zlib,pathlib,argparse; print('Standard library OK')"
if errorlevel 1 goto :fail

echo [3/3] Running all demos...
py -3.12 run_all.py %*
if errorlevel 1 goto :fail

echo.
echo ============================================================
echo Finished successfully. Open the outputs folder.
echo ============================================================
pause
exit /b 0

:no_python
echo.
echo ERROR: 64-bit Python 3.12 was not found via the Windows Python Launcher.
echo Install Python 3.12 x64 from python.org and include the Python Launcher.
echo You can inspect detected versions with: py -0p
pause
exit /b 2

:fail
echo.
echo ERROR: execution failed. Review the message above.
pause
exit /b 1
