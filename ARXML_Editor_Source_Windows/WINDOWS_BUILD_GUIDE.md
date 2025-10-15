# Windows Build Guide for ARXML Editor

This guide explains how to build the ARXML Editor on Windows from source.

## Prerequisites

### 1. Python Installation
- Download and install Python 3.8 or higher from [python.org](https://python.org)
- Make sure to check "Add Python to PATH" during installation
- Verify installation: `python --version`

### 2. Git Installation
- Download and install Git from [git-scm.com](https://git-scm.com)
- Verify installation: `git --version`

## Building from Source

### Method 1: Quick Build (Recommended)
```batch
# Clone the repository
git clone https://github.com/hedeya/arxml-editor.git
cd arxml-editor

# Run the Windows build script
build_windows.bat
```

### Method 2: Complete Build
```batch
# Clone the repository
git clone https://github.com/hedeya/arxml-editor.git
cd arxml-editor

# Run the complete build script
build_windows_complete.bat
```

### Method 3: Manual Build
```batch
# Clone the repository
git clone https://github.com/hedeya/arxml-editor.git
cd arxml-editor

# Install dependencies
pip install -r requirements.txt
pip install -r requirements_build.txt

# Build the executable
pyinstaller arxml_editor.spec

# The executable will be in dist/ARXML_Editor.exe
```

## Build Scripts Explained

### `build_windows.bat`
- Quick build script
- Installs PyInstaller if needed
- Builds the executable
- Creates a simple distribution

### `build_windows_complete.bat`
- Complete build script
- Installs all dependencies
- Builds the executable
- Creates a full distribution with schemas and documentation
- Creates a ZIP file for distribution

### `build_windows.sh`
- Linux/Unix build script
- Can be run in WSL or Git Bash on Windows

## Output Files

After building, you'll find:
- `dist/ARXML_Editor.exe` - The main executable
- `ARXML_Editor_Windows/` - Complete distribution directory
- `ARXML_Editor_Windows.zip` - Distribution ZIP file (if using complete build)

## Troubleshooting

### Common Issues

1. **Python not found**
   - Make sure Python is installed and added to PATH
   - Try running `python` in Command Prompt

2. **PyInstaller not found**
   - The build script will install it automatically
   - Or install manually: `pip install pyinstaller`

3. **Missing dependencies**
   - Run: `pip install -r requirements.txt`
   - Run: `pip install -r requirements_build.txt`

4. **Build fails**
   - Check Python version (3.8+ required)
   - Update pip: `python -m pip install --upgrade pip`
   - Clear build cache: `rmdir /s build dist`

### Build Requirements

- Python 3.8 or higher
- PyInstaller 5.0 or higher
- All dependencies from `requirements.txt`
- All build dependencies from `requirements_build.txt`

## Distribution

The complete build creates a distribution-ready package:
- `ARXML_Editor.exe` - Standalone executable
- `schemas/` - AUTOSAR XSD schemas
- `README_Windows.md` - User documentation
- `run_editor.bat` - Launcher script
- `sample.arxml` - Sample file

## Support

If you encounter issues:
1. Check this guide first
2. Check the main README.md
3. Check BUILD_INSTRUCTIONS.md
4. Open an issue on GitHub

## File Structure

```
arxml-editor/
├── build_windows.bat          # Quick build script
├── build_windows_complete.bat # Complete build script
├── build_windows.sh           # Linux/Unix build script
├── arxml_editor.spec          # PyInstaller spec file
├── requirements.txt           # Runtime dependencies
├── requirements_build.txt     # Build dependencies
├── setup.py                   # Python setup file
├── src/                       # Source code
├── schemas/                   # AUTOSAR schemas
└── Tests/                     # Test files
```