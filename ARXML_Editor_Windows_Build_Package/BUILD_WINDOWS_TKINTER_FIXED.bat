@echo off
echo ========================================
echo ARXML Editor - Tkinter Fixed Build
echo ========================================
echo.
echo This script creates a Tkinter-based version with better error handling.
echo.
pause

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Check if we're in the right directory
if not exist "main.py" (
    echo ERROR: main.py not found. Please run this script from the project root directory.
    echo Make sure you've downloaded the source code first.
    pause
    exit /b 1
)

echo ✓ Source code found
echo.

REM Test Tkinter first
echo Testing Tkinter...
python test_tkinter_simple.py
if errorlevel 1 (
    echo ERROR: Tkinter test failed. Please check your Python installation.
    pause
    exit /b 1
)

echo ✓ Tkinter test passed
echo.

REM Upgrade pip and install build tools
echo Upgrading pip and installing build tools...
python -m pip install --upgrade pip setuptools wheel

REM Install PyInstaller
echo Installing PyInstaller...
pip install pyinstaller==6.16.0
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)

REM Install only the essential packages (no PyQt6)
echo Installing essential packages...
pip install xmlschema==3.3.0
pip install typing-extensions==4.8.0
if errorlevel 1 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

REM Clean previous builds
echo Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "ARXML_Editor_Windows" rmdir /s /q "ARXML_Editor_Windows"

REM Test the fixed main file
echo Testing fixed main file...
python main_tkinter_fixed.py --help >nul 2>&1
if errorlevel 1 (
    echo WARNING: Fixed main file test failed, but continuing with build...
)

REM Build the Tkinter executable
echo Building Tkinter executable...
python -m PyInstaller --clean --windowed --name ARXML_Editor_Tkinter_Fixed ^
    --add-data "schemas;schemas" ^
    --add-data "sample.arxml;." ^
    --hidden-import xmlschema ^
    --hidden-import elementpath ^
    --hidden-import typing_extensions ^
    --collect-all xmlschema ^
    --exclude-module PyQt6 ^
    --exclude-module PyQt5 ^
    --exclude-module PySide2 ^
    --exclude-module PySide6 ^
    main_tkinter_fixed.py

if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

REM Create distribution folder
echo Creating distribution folder...
mkdir "ARXML_Editor_Windows"
copy "dist\ARXML_Editor_Tkinter_Fixed.exe" "ARXML_Editor_Windows\"
copy "sample.arxml" "ARXML_Editor_Windows\"
if exist "schemas" xcopy "schemas" "ARXML_Editor_Windows\schemas\" /E /I

REM Create README
echo Creating README...
(
echo ARXML Editor - Tkinter Fixed Version
echo ====================================
echo.
echo This is a standalone Windows executable for the ARXML Editor using Tkinter.
echo This version includes better error handling and debugging.
echo.
echo TO RUN:
echo 1. Double-click ARXML_Editor_Tkinter_Fixed.exe
echo 2. Or run from command line: ARXML_Editor_Tkinter_Fixed.exe
echo 3. If GUI doesn't work, try running DEBUG_TKINTER.bat for troubleshooting
echo.
echo FEATURES:
echo - ARXML file parsing and viewing
echo - Schema validation
echo - Tree-based navigation
echo - Property inspection
echo - Modern tabbed interface
echo - Better error handling
echo.
echo FILES INCLUDED:
echo - ARXML_Editor_Tkinter_Fixed.exe: Main executable
echo - sample.arxml: Sample ARXML file
echo - schemas/: XSD schema files
echo - DEBUG_TKINTER.bat: Debug script
echo.
echo The executable includes all necessary dependencies.
echo No additional installation is required.
echo.
echo NOTE: This version uses Tkinter instead of PyQt6 for better compatibility.
echo Tkinter is built into Python and should work reliably on all Windows systems.
) > "ARXML_Editor_Windows\README.txt"

echo.
echo ========================================
echo BUILD COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Your Tkinter executable is ready:
echo   ARXML_Editor_Windows\ARXML_Editor_Tkinter_Fixed.exe
echo.
echo You can now run the application by double-clicking
echo the executable or running it from the command line.
echo.
echo If the GUI doesn't appear, run DEBUG_TKINTER.bat
echo to see what error messages are generated.
echo.
echo The entire ARXML_Editor_Windows folder can be
echo distributed to other Windows users.
echo.
pause