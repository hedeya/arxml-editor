@echo off
echo ARXML Editor - Launcher
echo =======================
echo.

REM Check if executable exists
if exist "dist\ARXML_Editor.exe" (
    echo Starting ARXML Editor...
    start "" "dist\ARXML_Editor.exe"
) else (
    echo Executable not found. Please build first.
    echo Run: build_windows_complete.bat
    pause
)
