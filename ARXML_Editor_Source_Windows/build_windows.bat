@echo off
echo Building ARXML Editor for Windows...
echo ====================================

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

REM Clean previous builds
echo Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

REM Build the executable
echo Building executable...
pyinstaller --clean arxml_editor.spec
if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

REM Create distribution folder
echo Creating distribution folder...
if not exist "ARXML_Editor_Windows" mkdir "ARXML_Editor_Windows"
copy "dist\ARXML_Editor.exe" "ARXML_Editor_Windows\"
copy "README_Windows.md" "ARXML_Editor_Windows\"
copy "sample.arxml" "ARXML_Editor_Windows\"
if exist "Backup" xcopy "Backup" "ARXML_Editor_Windows\Backup\" /E /I

echo.
echo Build completed successfully!
echo.
echo The executable is located in: ARXML_Editor_Windows\ARXML_Editor.exe
echo.
echo You can now distribute the entire "ARXML_Editor_Windows" folder.
echo.
pause