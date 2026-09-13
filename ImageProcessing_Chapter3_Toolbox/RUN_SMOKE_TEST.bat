@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe call SETUP_ENV.bat || goto :err
.venv\Scripts\python.exe tests\smoke_test.py
pause
goto :eof
:err
pause
exit /b 1
