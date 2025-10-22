@echo off
echo ========================================
echo ARXML Editor - Directory Build
echo ========================================
echo.
echo This script creates a directory-based build to avoid PyQt6 DLL issues.
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

REM Install packages that don't require compilation
echo Installing packages without compilation...
pip install -r requirements_no_compilation.txt
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

REM Build the executable as a directory (not onefile)
echo Building Windows executable...
python -m PyInstaller --clean --windowed --name ARXML_Editor ^
    --add-data "schemas;schemas" ^
    --add-data "sample.arxml;." ^
    --hidden-import PyQt6 ^
    --hidden-import PyQt6.QtCore ^
    --hidden-import PyQt6.QtGui ^
    --hidden-import PyQt6.QtWidgets ^
    --hidden-import PyQt6.sip ^
    --hidden-import xmlschema ^
    --hidden-import elementpath ^
    --hidden-import typing_extensions ^
    --collect-all PyQt6 ^
    --collect-all xmlschema ^
    --collect-submodules PyQt6 ^
    --collect-data PyQt6 ^
    --copy-metadata PyQt6 ^
    main.py

if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

REM Create distribution folder
echo Creating distribution folder...
mkdir "ARXML_Editor_Windows"
xcopy "dist\ARXML_Editor" "ARXML_Editor_Windows\" /E /I
copy "sample.arxml" "ARXML_Editor_Windows\"
if exist "schemas" xcopy "schemas" "ARXML_Editor_Windows\schemas\" /E /I

REM Create README
echo Creating README...
(
echo ARXML Editor - Windows Distribution
echo ===================================
echo.
echo This is a standalone Windows executable for the ARXML Editor.
echo.
echo TO RUN:
echo 1. Double-click ARXML_Editor.exe in the ARXML_Editor folder
echo 2. Or run from command line: ARXML_Editor\ARXML_Editor.exe
echo.
echo FILES INCLUDED:
echo - ARXML_Editor\ARXML_Editor.exe: Main executable
echo - ARXML_Editor\: All required DLLs and libraries
echo - sample.arxml: Sample ARXML file
echo - schemas/: XSD schema files
echo.
echo The executable includes all necessary dependencies.
echo No additional installation is required.
echo.
echo NOTE: This build uses the standard library XML parser
echo instead of lxml to avoid compilation issues on Windows.
) > "ARXML_Editor_Windows\README.txt"

echo.
echo ========================================
echo BUILD COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Your Windows executable is ready:
echo   ARXML_Editor_Windows\ARXML_Editor\ARXML_Editor.exe
echo.
echo You can now run the application by double-clicking
echo the executable or running it from the command line.
echo.
echo The entire ARXML_Editor_Windows folder can be
echo distributed to other Windows users.
echo.
echo NOTE: This build uses the standard library XML parser
echo instead of lxml to avoid compilation issues on Windows.
echo.
pause