@echo off
echo ========================================
echo ARXML Editor - Console Build
echo ========================================
echo.
echo This script creates a console-based version that avoids PyQt6 DLL issues.
echo The application will run in the command line instead of a GUI.
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

REM Create a console version of main.py
echo Creating console version...
(
echo import sys
echo import os
echo from src.core.services.arxml_parser import ARXMLParser
echo from src.core.services.schema_service import SchemaService
echo from src.core.services.validation_service import ValidationService
echo.
echo def main(^):
echo     print("ARXML Editor - Console Version")
echo     print("=============================")
echo     print("This is a console-based version of the ARXML Editor.")
echo     print("GUI functionality is not available in this build.")
echo     print()
echo     print("Available commands:")
echo     print("  python main.py validate ^<file.arxml^> - Validate an ARXML file")
echo     print("  python main.py parse ^<file.arxml^> - Parse an ARXML file")
echo     print()
echo     if len(sys.argv^) ^> 1:
echo         command = sys.argv[1]
echo         if command == "validate" and len(sys.argv^) ^> 2:
echo             file_path = sys.argv[2]
echo             if os.path.exists(file_path^):
echo                 print(f"Validating: {file_path}")
echo                 try:
echo                     parser = ARXMLParser(^)
echo                     schema_service = SchemaService(^)
echo                     validation_service = ValidationService(^)
echo                     
echo                     # Parse the file
echo                     root = parser.parse_arxml_file(file_path^)
echo                     if root is None:
echo                         print("ERROR: Failed to parse ARXML file")
echo                         return
echo                     
echo                     # Validate against schema
echo                     schema_version = schema_service.detect_schema_version(file_path^)
echo                     if schema_version:
echo                         print(f"Detected schema version: {schema_version}")
echo                         is_valid, errors = schema_service.validate_arxml_file(file_path^)
echo                         if is_valid:
echo                             print("✓ ARXML file is valid")
echo                         else:
echo                             print("✗ ARXML file has validation errors:")
echo                             for error in errors:
echo                                 print(f"  - {error}")
echo                     else:
echo                         print("WARNING: Could not detect schema version")
echo                         print("File parsed successfully but validation skipped")
echo                     
echo                 except Exception as e:
echo                     print(f"ERROR: {e}")
echo             else:
echo                 print(f"ERROR: File not found: {file_path}")
echo         elif command == "parse" and len(sys.argv^) ^> 2:
echo             file_path = sys.argv[2]
echo             if os.path.exists(file_path^):
echo                 print(f"Parsing: {file_path}")
echo                 try:
echo                     parser = ARXMLParser(^)
echo                     root = parser.parse_arxml_file(file_path^)
echo                     if root is not None:
echo                         print("✓ ARXML file parsed successfully")
echo                         
echo                         # Extract basic information
echo                         sw_components = parser.extract_sw_component_types(root^)
echo                         compositions = parser.extract_compositions(root^)
echo                         port_interfaces = parser.extract_port_interfaces(root^)
echo                         
echo                         print(f"Found {len(sw_components^)} software components")
echo                         print(f"Found {len(compositions^)} compositions")
echo                         print(f"Found {len(port_interfaces^)} port interfaces")
echo                     else:
echo                         print("ERROR: Failed to parse ARXML file")
echo                 except Exception as e:
echo                     print(f"ERROR: {e}")
echo             else:
echo                 print(f"ERROR: File not found: {file_path}")
echo         else:
echo             print("Invalid command. Use 'validate' or 'parse' with a file path.")
echo     else:
echo         print("No command specified. Use 'validate' or 'parse' with a file path.")
echo.
echo if __name__ == "__main__":
echo     main(^)
) > main_console.py

REM Build the console executable
echo Building console executable...
python -m PyInstaller --clean --onefile --console --name ARXML_Editor_Console ^
    --add-data "schemas;schemas" ^
    --add-data "sample.arxml;." ^
    --hidden-import xmlschema ^
    --hidden-import elementpath ^
    --hidden-import typing_extensions ^
    --collect-all xmlschema ^
    main_console.py

if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

REM Create distribution folder
echo Creating distribution folder...
mkdir "ARXML_Editor_Windows"
copy "dist\ARXML_Editor_Console.exe" "ARXML_Editor_Windows\"
copy "sample.arxml" "ARXML_Editor_Windows\"
if exist "schemas" xcopy "schemas" "ARXML_Editor_Windows\schemas\" /E /I

REM Create README
echo Creating README...
(
echo ARXML Editor - Console Version
echo ==============================
echo.
echo This is a console-based version of the ARXML Editor that avoids PyQt6 DLL issues.
echo.
echo TO RUN:
echo 1. Open Command Prompt in this directory
echo 2. Run: ARXML_Editor_Console.exe validate sample.arxml
echo 3. Or: ARXML_Editor_Console.exe parse sample.arxml
echo.
echo COMMANDS:
echo - validate ^<file.arxml^>: Validate an ARXML file against AUTOSAR schemas
echo - parse ^<file.arxml^>: Parse an ARXML file and show basic information
echo.
echo FILES INCLUDED:
echo - ARXML_Editor_Console.exe: Main console executable
echo - sample.arxml: Sample ARXML file
echo - schemas/: XSD schema files
echo.
echo The executable includes all necessary dependencies.
echo No additional installation is required.
echo.
echo NOTE: This is a console version without GUI functionality.
echo For full GUI functionality, you need to resolve PyQt6 DLL issues.
) > "ARXML_Editor_Windows\README.txt"

echo.
echo ========================================
echo BUILD COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Your console executable is ready:
echo   ARXML_Editor_Windows\ARXML_Editor_Console.exe
echo.
echo You can now run the application from the command line:
echo   ARXML_Editor_Console.exe validate sample.arxml
echo   ARXML_Editor_Console.exe parse sample.arxml
echo.
echo The entire ARXML_Editor_Windows folder can be
echo distributed to other Windows users.
echo.
echo NOTE: This is a console version without GUI functionality.
echo For full GUI functionality, you need to resolve PyQt6 DLL issues.
echo.
pause