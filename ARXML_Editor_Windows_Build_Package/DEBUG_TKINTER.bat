@echo off
echo ========================================
echo ARXML Editor - Tkinter Debug
echo ========================================
echo.
echo This script will help debug the Tkinter executable.
echo.

REM Check if the executable exists
if not exist "ARXML_Editor_Windows\ARXML_Editor_Tkinter.exe" (
    echo ERROR: ARXML_Editor_Tkinter.exe not found!
    echo Please run BUILD_WINDOWS_TKINTER.bat first to create the executable.
    pause
    exit /b 1
)

echo ✓ Executable found
echo.

REM Try to run the executable and capture any errors
echo Running ARXML_Editor_Tkinter.exe...
echo.
echo If you see any error messages below, please copy them:
echo ========================================
ARXML_Editor_Windows\ARXML_Editor_Tkinter.exe
echo ========================================
echo.

if errorlevel 1 (
    echo.
    echo ERROR: The executable failed to run (exit code: %errorlevel%)
    echo.
    echo Let's try running it with Python directly to see more details...
    echo.
    python -c "
import sys
import os
sys.path.insert(0, '.')
try:
    from src.ui.tkinter_main_window import main
    print('Tkinter UI import successful')
    main()
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
"
) else (
    echo.
    echo The executable ran but may have closed immediately.
    echo This could mean there was an error that caused it to exit.
)

echo.
echo Debug complete. Please share any error messages you see above.
pause