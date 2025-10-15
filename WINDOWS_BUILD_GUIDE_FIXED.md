# Windows Build Guide - PyQt6 Fixed

This guide provides instructions for building the ARXML Editor on Windows with proper PyQt6 dependency handling.

## Problem Solved

The original Windows release had PyQt6 dependency issues that caused "no module named PyQt6" errors. This guide provides the solution.

## Prerequisites

1. **Python 3.8+** installed on Windows
2. **Git** (optional, for cloning the repository)
3. **Visual Studio Build Tools** (recommended for better compatibility)

## Quick Fix for Existing Windows Release

If you have the existing Windows release and are getting PyQt6 errors:

1. Download the source code from this repository
2. Follow the build instructions below
3. Use the newly built executable

## Building from Source on Windows

### Method 1: Using the Fixed Build Script (Recommended)

1. **Clone or download the repository**
   ```cmd
   git clone <repository-url>
   cd ARXML_Editor
   ```

2. **Run the fixed build script**
   ```cmd
   build_windows_cross_platform.bat
   ```

   This script will:
   - Install all required dependencies
   - Use PyInstaller with comprehensive PyQt6 collection
   - Create a standalone executable with all dependencies bundled

3. **Find your executable**
   - The built executable will be in `ARXML_Editor_Windows/ARXML_Editor.exe`
   - This is a standalone executable that doesn't require Python or PyQt6 to be installed

### Method 2: Manual Build

1. **Install Python dependencies**
   ```cmd
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. **Build with PyQt6 fixes**
   ```cmd
   pyinstaller --clean --onefile --windowed --name ARXML_Editor ^
       --add-data "schemas;schemas" ^
       --add-data "sample.arxml;." ^
       --hidden-import PyQt6 ^
       --hidden-import PyQt6.QtCore ^
       --hidden-import PyQt6.QtGui ^
       --hidden-import PyQt6.QtWidgets ^
       --hidden-import PyQt6.sip ^
       --collect-all PyQt6 ^
       --collect-all lxml ^
       --collect-all xmlschema ^
       --collect-submodules PyQt6 ^
       --collect-data PyQt6 ^
       --copy-metadata PyQt6 ^
       main.py
   ```

3. **Create distribution folder**
   ```cmd
   mkdir ARXML_Editor_Windows
   copy dist\ARXML_Editor.exe ARXML_Editor_Windows\
   copy sample.arxml ARXML_Editor_Windows\
   xcopy schemas ARXML_Editor_Windows\schemas\ /E /I
   ```

## What's Fixed

### PyQt6 Dependency Issues
- **Problem**: Original build didn't include all PyQt6 platform plugins and libraries
- **Solution**: Uses `--collect-all PyQt6` and `--collect-submodules PyQt6` to include all PyQt6 components

### Platform Plugin Issues
- **Problem**: Missing Qt6 platform plugins for Windows
- **Solution**: Comprehensive collection of PyQt6 data and metadata

### Symbol Resolution Issues
- **Problem**: Undefined Qt symbols in cross-platform builds
- **Solution**: Building on Windows with proper Qt6 libraries

## Build Scripts Included

1. **`build_windows_cross_platform.bat`** - Windows batch script for building
2. **`build_windows_cross_platform.sh`** - Linux/Unix script for cross-compilation
3. **`arxml_editor.spec`** - Updated PyInstaller spec file with PyQt6 fixes

## Testing the Build

After building, test the executable:

1. **Run the executable**
   ```cmd
   ARXML_Editor_Windows\ARXML_Editor.exe
   ```

2. **Check for errors**
   - The application should start without PyQt6 import errors
   - GUI should display properly
   - All functionality should work

## Troubleshooting

### Common Issues

1. **"No module named PyQt6"**
   - Solution: Use the fixed build script with `--collect-all PyQt6`

2. **"Qt platform plugin not found"**
   - Solution: Ensure `--collect-data PyQt6` is included in build command

3. **"Undefined symbol" errors**
   - Solution: Build on Windows instead of cross-compiling from Linux

4. **Build fails with dependency errors**
   - Solution: Use a clean virtual environment and install exact versions

### Build Environment Issues

If you encounter build issues:

1. **Use a clean environment**
   ```cmd
   python -m venv build_env
   build_env\Scripts\activate
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. **Check Python version**
   ```cmd
   python --version
   ```
   Should be 3.8 or higher.

3. **Verify PyQt6 installation**
   ```cmd
   python -c "import PyQt6; print('PyQt6 version:', PyQt6.QtCore.PYQT_VERSION_STR)"
   ```

## Distribution

The built executable is completely standalone and includes:
- All PyQt6 libraries and plugins
- lxml for XML processing
- xmlschema for XSD validation
- All other dependencies

No additional installation is required on the target Windows machine.

## Support

If you encounter issues:
1. Check this guide first
2. Verify you're using the latest version
3. Report issues with build logs and system information