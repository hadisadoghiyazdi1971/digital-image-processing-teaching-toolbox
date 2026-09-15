@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo Histogram Equalization Lecture - OFFLINE GUI
echo ============================================================
echo.
echo This GUI uses only Python 3.12 standard library + Tkinter.
echo No pip, PyPI, OpenCV, NumPy or Matplotlib is used.
echo.

echo [1/3] Checking 64-bit Python 3.12...
where py >nul 2>nul
if errorlevel 1 goto :nopy
py -3.12 -c "import sys,struct; assert sys.version_info[:2]==(3,12); assert struct.calcsize('P')*8==64" >nul 2>nul
if errorlevel 1 goto :nopy

echo [2/3] Checking Tkinter...
py -3.12 -c "import tkinter; print('Tkinter OK - Tk', tkinter.TkVersion)"
if errorlevel 1 goto :notk

echo [3/3] Starting GUI...
py -3.12 histogram_gui.py
if errorlevel 1 goto :failed
exit /b 0

:nopy
echo.
echo ERROR: 64-bit Python 3.12 and the Python Launcher ^(py.exe^) are required.
echo No package installation is attempted by this program.
pause
exit /b 1

:notk
echo.
echo ERROR: Tkinter is not available in this Python 3.12 installation.
echo Install/repair the official Windows Python 3.12 distribution with Tcl/Tk support.
echo This program will NOT use pip or PyPI to install anything.
pause
exit /b 1

:failed
echo.
echo ERROR: GUI execution failed. Review the message above.
pause
exit /b 1
