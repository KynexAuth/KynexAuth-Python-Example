@echo off
title KynexAuth Console .EXE Builder
color 0a
cls
echo ========================================================
echo     BUILDING STANDALONE CONSOLE LOADER .EXE
echo ========================================================
echo.

echo [*] Ensuring PyInstaller is ready...
py -m pip install --upgrade pyinstaller >nul 2>&1

echo [*] Compiling Console Loader to single .EXE...
py -m PyInstaller --console --onefile --clean --name="KynexAuth_Console" main.py

if errorlevel 1 (
    python -m PyInstaller --console --onefile --clean --name="KynexAuth_Console" main.py
)

echo.
echo ========================================================
echo  [+] Build Completed! Check the "dist\" folder!
echo ========================================================
pause
