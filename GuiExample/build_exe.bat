@echo off
title KynexAuth GUI .EXE Builder
color 0b
cls
echo ========================================================
echo       BUILDING STANDALONE GUI LOADER .EXE
echo ========================================================
echo.

echo [*] Ensuring PyInstaller is ready...
py -m pip install --upgrade pyinstaller >nul 2>&1

echo [*] Compiling GUI Loader to single .EXE...
py -m PyInstaller --noconsole --onefile --clean --name="KynexAuth_GUI" main.py

if errorlevel 1 (
    python -m PyInstaller --noconsole --onefile --clean --name="KynexAuth_GUI" main.py
)

echo.
echo ========================================================
echo  [+] Build Completed! Check the "dist\" folder!
echo ========================================================
pause
