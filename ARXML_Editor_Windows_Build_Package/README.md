# ARXML Editor - Windows Build Package

## ⚠️ Important Notice

This package contains the source code and build scripts needed to create a working Windows executable for the ARXML Editor. The previous release contained a Linux binary that won't run on Windows.

## Quick Start

### Option 1: Tkinter Fixed Build (Best for GUI without PyQt6 issues)
1. **Double-click `BUILD_WINDOWS_TKINTER_FIXED.bat`** - Creates Tkinter GUI version with better error handling
2. **Wait for completion** (5-10 minutes)
3. **Find your executable** in `ARXML_Editor_Windows\ARXML_Editor_Tkinter_Fixed.exe`
4. **Double-click to run** - Full GUI with tree navigation, validation, and properties
5. **If GUI doesn't appear** - Run `DEBUG_TKINTER.bat` to see error messages

### Option 2: Tkinter Build (Original)
1. **Double-click `BUILD_WINDOWS_TKINTER.bat`** - Creates Tkinter GUI version
2. **Wait for completion** (5-10 minutes)
3. **Find your executable** in `ARXML_Editor_Windows\ARXML_Editor_Tkinter.exe`
4. **Double-click to run** - Full GUI with tree navigation, validation, and properties

### Option 3: Console Build (Command-line only)
1. **Double-click `BUILD_WINDOWS_CONSOLE.bat`** - Creates console version without GUI
2. **Wait for completion** (5-10 minutes)
3. **Find your executable** in `ARXML_Editor_Windows\ARXML_Editor_Console.exe`
4. **Run from command line**: `ARXML_Editor_Console.exe validate sample.arxml`

### Option 3: PyQt6 Fix Build (Try PyQt6 GUI)
1. **Double-click `BUILD_WINDOWS_PYQT6_FIX.bat`** - Tries to fix PyQt6 installation
2. **Wait for completion** (5-10 minutes)
3. **Find your executable** in `ARXML_Editor_Windows\ARXML_Editor\ARXML_Editor.exe`

### Option 4: Directory Build
1. **Double-click `BUILD_WINDOWS_DIRECTORY.bat`** - Creates directory-based build to avoid DLL issues
2. **Wait for completion** (5-10 minutes)
3. **Find your executable** in `ARXML_Editor_Windows\ARXML_Editor\ARXML_Editor.exe`

### Option 5: Simple PyQt6 Build
1. **Double-click `BUILD_WINDOWS_SIMPLE_PYQT6.bat`** - Simpler PyQt6 handling
2. **Wait for completion** (5-10 minutes)
3. **Find your executable** in `ARXML_Editor_Windows\ARXML_Editor.exe`

### Option 6: No Compilation Build
1. **Double-click `BUILD_WINDOWS_NO_COMPILATION.bat`** - Uses standard library XML parser, no compilation needed
2. **Wait for completion** (5-10 minutes)
3. **Find your executable** in `ARXML_Editor_Windows\ARXML_Editor.exe`

### Option 2: Ultra Simple Build (Alternative)
1. **Double-click `BUILD_WINDOWS_ULTRA_SIMPLE.bat`** - Uses minimal requirements to avoid all compilation
2. **Wait for completion** (5-10 minutes)
3. **Find your executable** in `ARXML_Editor_Windows\ARXML_Editor.exe`

### Option 2: Minimal Build (Alternative)
1. **Double-click `BUILD_WINDOWS_MINIMAL.bat`** - Installs only essential packages one by one
2. **Wait for completion** (5-10 minutes)
3. **Find your executable** in `ARXML_Editor_Windows\ARXML_Editor.exe`

### Option 3: Easy Build
1. **Double-click `BUILD_WINDOWS_EASY.bat`** - Uses pre-compiled packages to avoid compilation issues
2. **Wait for completion** (5-10 minutes)
3. **Find your executable** in `ARXML_Editor_Windows\ARXML_Editor.exe`

### Option 4: Simple Build
1. **Double-click `BUILD_WINDOWS_SIMPLE.bat`** - Installs packages one by one with specific versions
2. **Wait for completion** (5-10 minutes)
3. **Find your executable** in `ARXML_Editor_Windows\ARXML_Editor.exe`

### Option 5: Original Build
1. **Double-click `BUILD_WINDOWS_NOW.bat`** - Original build script (may have compilation issues)
2. **Wait for completion** (5-10 minutes)
3. **Find your executable** in `ARXML_Editor_Windows\ARXML_Editor.exe`

## What's Included

### Build Scripts
- `BUILD_WINDOWS_TKINTER_FIXED.bat` - **Best overall!** Creates Tkinter GUI with better error handling
- `BUILD_WINDOWS_TKINTER.bat` - **Alternative!** Creates Tkinter GUI version (no PyQt6 issues)
- `DEBUG_TKINTER.bat` - **Debug tool!** Helps troubleshoot Tkinter issues
- `BUILD_WINDOWS_CONSOLE.bat` - **Best for PyQt6 DLL issues!** Creates console version without GUI
- `BUILD_WINDOWS_PYQT6_FIX.bat` - **Alternative for PyQt6 issues!** Tries to fix PyQt6 installation
- `BUILD_WINDOWS_DIRECTORY.bat` - Creates directory-based build
- `BUILD_WINDOWS_SIMPLE_PYQT6.bat` - Simpler PyQt6 handling
- `BUILD_WINDOWS_NO_COMPILATION.bat` - Uses standard library XML parser
- `BUILD_WINDOWS_ULTRA_SIMPLE.bat` - Uses minimal requirements only
- `BUILD_WINDOWS_MINIMAL.bat` - Installs only essential packages one by one
- `BUILD_WINDOWS_EASY.bat` - Uses pre-compiled packages to avoid compilation issues
- `BUILD_WINDOWS_SIMPLE.bat` - Installs packages one by one with specific versions
- `BUILD_WINDOWS_NOW.bat` - Original build script (may have compilation issues)
- `build_windows_cross_platform.bat` - Alternative build script
- `build_windows_complete.bat` - Complete build with distribution

### Documentation
- `WINDOWS_USERS_README.md` - Quick explanation and fix
- `WINDOWS_BUILD_INSTRUCTIONS.md` - Detailed build guide
- `README.md` - This file

### Source Code
- `main.py` - Main application entry point
- `src/` - Source code directory (patched for no-compilation build)
- `requirements.txt` - Python dependencies
- `requirements_no_compilation.txt` - **No compilation dependencies** (best for compilation issues)
- `requirements_minimal.txt` - Minimal dependencies
- `requirements_windows.txt` - Windows-specific dependencies
- `requirements_build.txt` - Build dependencies
- `setup.py` - Package setup
- `schemas/` - XSD schema files
- `sample.arxml` - Sample ARXML file

## Requirements

- **Windows 10/11** (64-bit recommended)
- **Python 3.8+** - Download from [python.org](https://python.org)
- **Internet connection** (to download dependencies)

## Build Process

The build process will:
1. Install all required Python packages
2. Install PyInstaller for creating the executable
3. Build a standalone Windows executable with all dependencies
4. Create a distribution folder with the executable and supporting files

## Output

After building, you'll find:
- `ARXML_Editor_Windows\ARXML_Editor.exe` - The working Windows executable
- `ARXML_Editor_Windows\README.txt` - Instructions for the executable
- `ARXML_Editor_Windows\sample.arxml` - Sample file
- `ARXML_Editor_Windows\schemas\` - XSD schema files

## Troubleshooting

If you encounter issues:
1. Check `WINDOWS_BUILD_INSTRUCTIONS.md` for detailed troubleshooting
2. Make sure Python is installed and added to PATH
3. Try running the build script as administrator
4. Check the build output for error messages

## Why This Package?

The previous release contained a Linux binary that was incorrectly labeled as a Windows executable. This package provides everything needed to build a proper Windows PE executable that will actually run on Windows.

## Support

For additional help:
- Check the documentation files included
- Look at the build output for error messages
- Refer to the project repository for issues

## Next Steps

1. Run `BUILD_WINDOWS_NOW.bat`
2. Wait for the build to complete
3. Test the generated executable
4. Distribute the `ARXML_Editor_Windows` folder to other users

The build process is fully automated and handles all the complex PyQt6 dependency issues.