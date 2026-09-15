@echo off
setlocal
cd /d "%~dp0"
echo Testing the GUI processing core without opening a window...
py -3.12 histogram_gui.py --self-test
if errorlevel 1 (
  echo SELF-TEST FAILED.
  pause
  exit /b 1
)
echo SELF-TEST PASSED.
pause
