@echo off
echo ========================================
echo ARXML Editor - Complete Windows Build
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv build_env
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call build_env\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install PyInstaller
echo Installing PyInstaller...
pip install pyinstaller

REM Install project dependencies
echo Installing project dependencies...
pip install -r requirements.txt

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist ARXML_Editor_Windows rmdir /s /q ARXML_Editor_Windows

REM Create distribution directory
echo Creating distribution directory...
mkdir ARXML_Editor_Windows

REM Build executable
echo Building ARXML Editor executable...
pyinstaller --clean arxml_editor.spec
if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

REM Copy executable to distribution folder
echo Copying executable...
copy "dist\ARXML_Editor.exe" "ARXML_Editor_Windows\ARXML_Editor.exe"

REM Copy additional files
echo Copying additional files...
copy "sample.arxml" "ARXML_Editor_Windows\"
copy "README_Windows.md" "ARXML_Editor_Windows\"
copy "BUILD_INSTRUCTIONS.md" "ARXML_Editor_Windows\"
xcopy "schemas" "ARXML_Editor_Windows\schemas\" /e /i
xcopy "Backup" "ARXML_Editor_Windows\Backup\" /e /i

REM Create run script
echo Creating run script...
echo @echo off > "ARXML_Editor_Windows\run_editor.bat"
echo echo Starting ARXML Editor... >> "ARXML_Editor_Windows\run_editor.bat"
echo ARXML_Editor.exe >> "ARXML_Editor_Windows\run_editor.bat"
echo pause >> "ARXML_Editor_Windows\run_editor.bat"

REM Create zip file
echo Creating zip file...
powershell Compress-Archive -Path "ARXML_Editor_Windows\*" -DestinationPath "ARXML_Editor_Windows.zip" -Force

echo.
echo ========================================
echo BUILD COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Distribution files created:
echo - ARXML_Editor_Windows\ (folder)
echo - ARXML_Editor_Windows.zip (archive)
echo.
echo The executable is ready to run!
echo Double-click ARXML_Editor_Windows\ARXML_Editor.exe
echo.
pause