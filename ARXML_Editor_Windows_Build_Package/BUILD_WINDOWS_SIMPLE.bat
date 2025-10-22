@echo off
echo ========================================
echo ARXML Editor - Simple Windows Build
echo ========================================
echo.
echo This script uses a more conservative approach
echo to avoid compilation issues.
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

REM Install packages one by one with specific versions
echo Installing PyQt6...
pip install PyQt6==6.6.1
if errorlevel 1 (
    echo ERROR: Failed to install PyQt6
    pause
    exit /b 1
)

echo Installing lxml...
pip install lxml==4.9.3
if errorlevel 1 (
    echo ERROR: Failed to install lxml
    pause
    exit /b 1
)

echo Installing xmlschema...
pip install xmlschema==3.3.0
if errorlevel 1 (
    echo ERROR: Failed to install xmlschema
    pause
    exit /b 1
)

echo Installing other dependencies...
pip install lxml-stubs==0.4.0
pip install typing-extensions==4.8.0

REM Clean previous builds
echo Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "ARXML_Editor_Windows" rmdir /s /q "ARXML_Editor_Windows"

REM Build the executable with minimal dependencies
echo Building Windows executable...
pyinstaller --clean --onefile --windowed --name ARXML_Editor ^
    --add-data "schemas;schemas" ^
    --add-data "sample.arxml;." ^
    --hidden-import PyQt6 ^
    --hidden-import PyQt6.QtCore ^
    --hidden-import PyQt6.QtGui ^
    --hidden-import PyQt6.QtWidgets ^
    --hidden-import PyQt6.sip ^
    --hidden-import PyQt6.QtCore.Qt ^
    --hidden-import PyQt6.QtGui.QFont ^
    --hidden-import PyQt6.QtGui.QIcon ^
    --hidden-import PyQt6.QtGui.QKeySequence ^
    --hidden-import PyQt6.QtGui.QAction ^
    --hidden-import PyQt6.QtGui.QPen ^
    --hidden-import PyQt6.QtGui.QBrush ^
    --hidden-import PyQt6.QtGui.QColor ^
    --hidden-import PyQt6.QtGui.QPainter ^
    --hidden-import PyQt6.QtCore.pyqtSignal ^
    --hidden-import PyQt6.QtCore.QRectF ^
    --hidden-import PyQt6.QtCore.QPointF ^
    --collect-all PyQt6 ^
    --collect-all lxml ^
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
copy "dist\ARXML_Editor.exe" "ARXML_Editor_Windows\"
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
echo 1. Double-click ARXML_Editor.exe
echo 2. Or run from command line: ARXML_Editor.exe
echo.
echo FILES INCLUDED:
echo - ARXML_Editor.exe: Main executable
echo - sample.arxml: Sample ARXML file
echo - schemas/: XSD schema files
echo.
echo The executable includes all necessary dependencies.
echo No additional installation is required.
) > "ARXML_Editor_Windows\README.txt"

echo.
echo ========================================
echo BUILD COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Your Windows executable is ready:
echo   ARXML_Editor_Windows\ARXML_Editor.exe
echo.
echo You can now run the application by double-clicking
echo the executable or running it from the command line.
echo.
echo The entire ARXML_Editor_Windows folder can be
echo distributed to other Windows users.
echo.
pause