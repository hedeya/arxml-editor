# ARXML Editor - Windows Build Instructions

This document provides step-by-step instructions for building the ARXML Editor as a Windows executable.

## 🚀 Quick Build (Windows)

### Prerequisites
- **Windows 10/11** (64-bit)
- **Python 3.8+** installed from [python.org](https://python.org)
- **Git** (optional, for cloning the repository)

### Step 1: Install Python Dependencies

Open Command Prompt or PowerShell as Administrator and run:

```cmd
pip install -r requirements_build.txt
```

### Step 2: Build the Executable

Run the build script:

```cmd
build_windows.bat
```

Or manually run PyInstaller:

```cmd
pyinstaller --clean arxml_editor.spec
```

### Step 3: Create Distribution Package

The build script will automatically create a `ARXML_Editor_Windows` folder containing:
- `ARXML_Editor.exe` - The main executable
- `sample.arxml` - Sample file for testing
- `Backup/ECUC/` - Sample ECUC files
- `README_Windows.md` - User documentation

## 🔧 Manual Build Process

If the automated build doesn't work, follow these manual steps:

### 1. Install Dependencies
```cmd
pip install PyQt6==6.6.1
pip install lxml==4.9.3
pip install xmlschema==3.3.0
pip install pyinstaller>=5.13.0
```

### 2. Build with PyInstaller
```cmd
pyinstaller --onefile --windowed --name ARXML_Editor main.py
```

### 3. Include Additional Files
```cmd
pyinstaller --onefile --windowed --name ARXML_Editor --add-data "schemas;schemas" --add-data "sample.arxml;." main.py
```

## 📁 File Structure After Build

```
ARXML_Editor_Windows/
├── ARXML_Editor.exe              # Main executable (~110MB)
├── sample.arxml                  # Sample ARXML file
├── Backup/                       # Sample ECUC files
│   └── ECUC/
│       └── FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml
└── README_Windows.md             # User documentation
```

## 🎯 Distribution

### For Your Friend
1. **Zip the entire `ARXML_Editor_Windows` folder**
2. **Send the zip file** to your friend
3. **Your friend extracts and runs `ARXML_Editor.exe`**

### System Requirements for End Users
- **Windows 10/11** (64-bit)
- **No additional software required**
- **~150MB free disk space**

## 🛠️ Troubleshooting

### Common Build Issues

**"Python not found":**
- Ensure Python is installed and added to PATH
- Try using `python` instead of `python3`

**"PyInstaller not found":**
- Install PyInstaller: `pip install pyinstaller`
- Ensure you're in the correct directory

**"Module not found" errors:**
- Install all dependencies: `pip install -r requirements_build.txt`
- Check that all source files are present

**"Qt library errors":**
- This is a known issue with cross-platform builds
- Build on Windows for best compatibility
- Try different PyQt6 versions if needed

### Build Optimization

**Reduce executable size:**
```cmd
pyinstaller --onefile --windowed --name ARXML_Editor --exclude-module tkinter --exclude-module matplotlib main.py
```

**Include debug information:**
```cmd
pyinstaller --onefile --windowed --name ARXML_Editor --debug all main.py
```

## 📋 Build Verification

After building, test the executable:

1. **Run the executable**: `ARXML_Editor.exe`
2. **Open sample file**: File → Open → `sample.arxml`
3. **Verify tree population**: Check that elements appear in the tree
4. **Test ECUC file**: Open `Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml`
5. **Check validation**: Verify validation panel shows results

## 🎉 Success!

If the build completes successfully and the executable runs without errors, you have a self-contained ARXML Editor that can be distributed to Windows users!

---

**Note**: The Linux build environment may have Qt library compatibility issues. For best results, build directly on Windows.