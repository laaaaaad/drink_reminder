@echo off
chcp 65001 >nul
echo ========================================
echo        Drink Reminder - Build Tool
echo ========================================
echo.

echo [1/3] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo [2/3] Building executable...
if not exist "dist" mkdir dist

pyinstaller --onefile --windowed --name drink_reminder --add-data ".;." drink_reminder.py
if %errorlevel% neq 0 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo [3/3] Cleaning up...
if exist "build" rmdir /s /q build
if exist "drink_reminder.spec" del drink_reminder.spec

echo.
echo ========================================
echo        Build Complete!
echo ========================================
echo.
echo exe location: dist\drink_reminder.exe
echo.
echo Usage:
echo   1. Double-click drink_reminder.exe to run
echo   2. Program runs in system tray
echo   3. Workday reminders at half past the hour
echo   4. Right-click tray icon to exit or test
echo.
echo For auto-startup:
echo   Put a shortcut in:
echo   C:\Users\%username%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
echo.
pause
