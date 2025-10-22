@echo off
echo Building ARXML Editor for Windows with PyQt6 fixes...
echo =====================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install required packages
    pause
    exit /b 1
)

REM Install PyQt6 explicitly to ensure all dependencies are available
echo Installing PyQt6 with all dependencies...
pip install PyQt6==6.6.1 --upgrade
if errorlevel 1 (
    echo ERROR: Failed to install PyQt6
    pause
    exit /b 1
)

REM Clean previous builds
echo Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

REM Build the executable with comprehensive PyQt6 support
echo Building executable with comprehensive PyQt6 support...
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
if not exist "ARXML_Editor_Windows" mkdir "ARXML_Editor_Windows"
copy "dist\ARXML_Editor.exe" "ARXML_Editor_Windows\"
copy "sample.arxml" "ARXML_Editor_Windows\"
if exist "schemas" xcopy "schemas" "ARXML_Editor_Windows\schemas\" /E /I

REM Create a comprehensive README for the distribution
echo Creating README for distribution...
(
echo ARXML Editor - Windows Distribution ^(Fixed^)
echo ===========================================
echo.
echo This is a standalone Windows executable for the ARXML Editor with PyQt6 dependencies properly bundled.
echo.
echo CHANGES IN THIS VERSION:
echo - Fixed PyQt6 dependency issues that caused "no module named PyQt6" errors
echo - All PyQt6 libraries and platform plugins are now properly included
echo - Uses PyInstaller's comprehensive collection options for PyQt6
echo - Includes all necessary Qt6 platform plugins for Windows
echo.
echo TO RUN THE APPLICATION:
echo 1. Double-click ARXML_Editor.exe
echo 2. Or run from command line: ARXML_Editor.exe
echo.
echo The application includes all necessary dependencies including PyQt6, lxml, and xmlschema.
echo.
echo FILES INCLUDED:
echo - ARXML_Editor.exe: Main executable ^(standalone, no installation required^)
echo - sample.arxml: Sample ARXML file for testing
echo - schemas/: XSD schema files for validation
echo - README.txt: This file
echo.
echo TECHNICAL DETAILS:
echo - Built with PyInstaller 6.16.0
echo - PyQt6 6.6.1 with all platform plugins
echo - lxml 4.9.3 for XML processing
echo - xmlschema 3.3.0 for XSD validation
echo - All dependencies statically linked
echo.
echo For support or issues, please refer to the project repository.
) > "ARXML_Editor_Windows\README.txt"

echo.
echo Build completed successfully!
echo.
echo The executable is located in: ARXML_Editor_Windows\ARXML_Editor.exe
echo.
echo You can now distribute the entire "ARXML_Editor_Windows" folder.
echo.
pause