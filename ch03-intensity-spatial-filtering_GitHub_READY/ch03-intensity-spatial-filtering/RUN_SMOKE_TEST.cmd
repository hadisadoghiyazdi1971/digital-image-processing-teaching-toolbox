@echo off
setlocal
cd /d "%~dp0"
py -3.12 tests\smoke_test.py
pause
