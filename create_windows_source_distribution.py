#!/usr/bin/env python3
"""
Create Windows Source Distribution Package
Creates a ZIP file with all source code and build files for Windows development
"""

import os
import zipfile
import shutil
from pathlib import Path

def create_windows_source_distribution():
    """Create a Windows-compatible source distribution package"""
    
    print("Creating ARXML Editor Windows Source Distribution")
    print("=" * 50)
    
    # Create distribution directory
    dist_dir = "ARXML_Editor_Source_Windows"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)
    
    # Files and directories to include
    files_to_copy = [
        # Source code
        "src/",
        "main.py",
        
        # Build files
        "build_windows.bat",
        "build_windows_complete.bat", 
        "build_windows.sh",
        "arxml_editor.spec",
        "setup.py",
        
        # Requirements
        "requirements.txt",
        "requirements_build.txt",
        
        # Documentation
        "README.md",
        "README_Windows.md",
        "WINDOWS_BUILD_GUIDE.md",
        "BUILD_INSTRUCTIONS.md",
        "DISTRIBUTION_READY.md",
        "LICENSE",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        
        # Schemas
        "schemas/",
        
        # Sample files
        "sample.arxml",
        
        # Tests
        "Tests/",
        
        # Git files
        ".gitignore",
    ]
    
    # Copy files and directories
    for item in files_to_copy:
        src_path = Path(item)
        if src_path.exists():
            dst_path = Path(dist_dir) / item
            if src_path.is_dir():
                print(f"✓ Copied directory: {item}")
                shutil.copytree(src_path, dst_path)
            else:
                print(f"✓ Copied file: {item}")
                shutil.copy2(src_path, dst_path)
        else:
            print(f"⚠ Skipped (not found): {item}")
    
    # Create Windows-specific files
    create_windows_readme(dist_dir)
    create_windows_build_script(dist_dir)
    
    # Create ZIP file
    zip_filename = "ARXML_Editor_Source_Windows.zip"
    print(f"\nCreating zip file: {zip_filename}")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, dist_dir)
                zipf.write(file_path, arc_path)
    
    print(f"✓ Created: {zip_filename}")
    
    # Display contents
    print(f"\nDistribution Package Contents:")
    print(f"Directory: {dist_dir}")
    print(f"Zip file: {zip_filename}")
    print(f"\nFiles included:")
    for root, dirs, files in os.walk(dist_dir):
        level = root.replace(dist_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")
    
    print(f"\n🎉 Windows Source Distribution created successfully!")
    print(f"📦 Send '{zip_filename}' to Windows developers")
    print(f"📁 Or send the entire '{dist_dir}' folder")
    
    return zip_filename

def create_windows_readme(dist_dir):
    """Create Windows-specific README"""
    readme_content = """# ARXML Editor - Windows Source Distribution

## Quick Start

1. **Extract this ZIP file** to your desired location
2. **Open Command Prompt** in the extracted folder
3. **Run the build script:**
   ```batch
   build_windows_complete.bat
   ```
4. **Run the application:**
   ```batch
   ARXML_Editor.exe
   ```

## Prerequisites

- **Python 3.8 or higher** - Download from [python.org](https://python.org)
- **Git** (optional, for version control) - Download from [git-scm.com](https://git-scm.com)

## Build Options

### Quick Build
```batch
build_windows.bat
```

### Complete Build (Recommended)
```batch
build_windows_complete.bat
```

### Manual Build
```batch
pip install -r requirements.txt
pip install -r requirements_build.txt
pyinstaller arxml_editor.spec
```

## What's Included

- **Source Code** - Complete Python source code
- **Build Scripts** - Windows batch files for building
- **Documentation** - Comprehensive guides and instructions
- **Schemas** - AUTOSAR XSD schema files
- **Tests** - Test suite for validation
- **Sample Files** - Example ARXML files

## File Structure

```
ARXML_Editor_Source_Windows/
├── src/                          # Source code
├── build_windows.bat             # Quick build script
├── build_windows_complete.bat    # Complete build script
├── arxml_editor.spec             # PyInstaller spec
├── requirements.txt              # Runtime dependencies
├── requirements_build.txt        # Build dependencies
├── schemas/                      # AUTOSAR schemas
├── Tests/                        # Test files
├── README_Windows.md             # Windows documentation
├── WINDOWS_BUILD_GUIDE.md        # Detailed build guide
└── sample.arxml                  # Sample file
```

## Support

- Check `WINDOWS_BUILD_GUIDE.md` for detailed instructions
- Check `BUILD_INSTRUCTIONS.md` for general build info
- Check `README.md` for general project information

## License

See LICENSE file for details.

---
**Ready to build on Windows!** 🪟✨
"""
    
    readme_path = Path(dist_dir) / "README_Windows_Source.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"✓ Created: README_Windows_Source.md")

def create_windows_build_script(dist_dir):
    """Create a simple Windows build script"""
    build_script = """@echo off
echo ARXML Editor - Windows Build Script
echo ===================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found. Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install runtime dependencies
    pause
    exit /b 1
)

pip install -r requirements_build.txt
if errorlevel 1 (
    echo ERROR: Failed to install build dependencies
    pause
    exit /b 1
)

echo Building executable...
pyinstaller arxml_editor.spec
if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo Executable created: dist\\ARXML_Editor.exe
echo.
echo To run the application:
echo   dist\\ARXML_Editor.exe
echo.
pause
"""
    
    script_path = Path(dist_dir) / "build.bat"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(build_script)
    print(f"✓ Created: build.bat")

if __name__ == "__main__":
    create_windows_source_distribution()