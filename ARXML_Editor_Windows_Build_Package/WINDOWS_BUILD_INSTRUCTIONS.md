# Windows Build Instructions for ARXML Editor

## ⚠️ Important Notice

The current release contains a Linux binary that was incorrectly labeled as a Windows executable. This is why you're getting the "This app can't run on your PC" error. To get a working Windows executable, you need to build it yourself on Windows.

## Why This Happened

The previous build was created using cross-compilation from Linux, which produces a Linux ELF binary that cannot run on Windows. A proper Windows PE executable must be built on Windows.

## Quick Fix - Build on Windows

### Prerequisites

1. **Windows 10/11** (64-bit recommended)
2. **Python 3.8 or higher** - Download from [python.org](https://python.org)
3. **Git** - Download from [git-scm.com](https://git-scm.com)

### Step 1: Download the Source Code

```cmd
git clone https://github.com/hedeya/arxml-editor.git
cd arxml-editor
```

### Step 2: Run the Windows Build Script

```cmd
build_windows_cross_platform.bat
```

This script will:
- Install all required dependencies
- Build a proper Windows PE executable
- Create a distribution folder with all necessary files

### Step 3: Find Your Executable

After the build completes, you'll find:
- `ARXML_Editor_Windows/ARXML_Editor.exe` - The working Windows executable
- `ARXML_Editor_Windows/README.txt` - Instructions
- `ARXML_Editor_Windows/sample.arxml` - Sample file
- `ARXML_Editor_Windows/schemas/` - XSD schema files

## Alternative Build Methods

### Method 1: Complete Build (Recommended)
```cmd
build_windows_complete.bat
```

### Method 2: Manual Build
```cmd
# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build the executable
pyinstaller --clean --onefile --windowed --name ARXML_Editor ^
    --add-data "schemas;schemas" ^
    --add-data "sample.arxml;." ^
    --hidden-import PyQt6 ^
    --hidden-import PyQt6.QtCore ^
    --hidden-import PyQt6.QtGui ^
    --hidden-import PyQt6.QtWidgets ^
    --collect-all PyQt6 ^
    --collect-all lxml ^
    --collect-all xmlschema ^
    main.py
```

## Troubleshooting

### Common Issues

1. **"Python is not installed"**
   - Install Python from [python.org](https://python.org)
   - Make sure to check "Add Python to PATH" during installation

2. **"PyInstaller not found"**
   - The build script will install it automatically
   - Or run: `pip install pyinstaller`

3. **"No module named PyQt6"**
   - The build script installs PyQt6 automatically
   - Or run: `pip install PyQt6==6.6.1`

4. **Build fails with import errors**
   - Make sure you're using Python 3.8 or higher
   - Try running: `pip install --upgrade pip`

### Build Requirements

- **Python**: 3.8 or higher
- **PyInstaller**: 6.16.0 or higher
- **PyQt6**: 6.6.1
- **lxml**: 4.9.3
- **xmlschema**: 3.3.0

## What You'll Get

After a successful build, you'll have:
- A standalone Windows executable (~134MB)
- All dependencies bundled (no additional installation required)
- Sample ARXML files and schemas
- Complete documentation

## File Structure

```
ARXML_Editor_Windows/
├── ARXML_Editor.exe          # Main executable
├── README.txt                # Instructions
├── sample.arxml              # Sample file
└── schemas/                  # XSD schema files
    ├── autosar_4-6-0.xsd
    └── autosar_4-7-0.xsd
```

## Support

If you encounter issues:
1. Check this guide first
2. Look at the build output for error messages
3. Make sure you're using the correct Python version
4. Try the alternative build methods

For additional help, please refer to the project repository or create an issue.

## Next Steps

1. Download the source code
2. Follow the build instructions above
3. Run the generated `ARXML_Editor.exe`
4. Test with your ARXML files

The build process typically takes 5-10 minutes depending on your system.