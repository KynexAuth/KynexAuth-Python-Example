@echo off
title KynexAuth Python Web Server
cls
echo ===================================================
echo        KynexAuth Python Flask Web Server
echo ===================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Python is not found in your PATH!
    pause
    exit /b 1
)

echo [*] Installing/Verifying requirements...
pip install -r requirements.txt --quiet

echo [*] Starting Flask Web Server at http://localhost:5000 ...
echo [*] Opening browser...
start http://localhost:5000
echo.
echo [✓] Web Server is RUNNING. Press Ctrl+C to stop.
echo ===================================================
echo.

python app.py
pause
