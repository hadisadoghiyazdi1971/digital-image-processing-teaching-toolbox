@echo off
cd /d "%~dp0"
call SETUP_ENV.bat || goto :err
.venv\Scripts\python.exe app.py
goto :eof
:err
echo Setup failed.
pause
exit /b 1
