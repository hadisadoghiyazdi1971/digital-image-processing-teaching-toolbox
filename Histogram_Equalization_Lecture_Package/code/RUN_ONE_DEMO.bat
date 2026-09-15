@echo off
setlocal EnableExtensions
cd /d "%~dp0"
if "%~1"=="" (
  echo Usage: RUN_ONE_DEMO.bat demo_02_equalization.py
  pause
  exit /b 1
)
py -3.12 "%~1"
pause
