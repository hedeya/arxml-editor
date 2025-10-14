@echo off
echo Starting ARXML Editor...
echo.
if exist "ARXML_Editor.exe" (
    ARXML_Editor.exe
) else (
    echo ERROR: ARXML_Editor.exe not found!
    echo Please ensure the executable is in the same directory.
    pause
)
