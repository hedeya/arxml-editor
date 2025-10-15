#!/usr/bin/env python3
"""
Create Large Windows Distribution Package
Creates a comprehensive ZIP file with all source code, documentation, and additional files
"""

import os
import zipfile
import shutil
from pathlib import Path

def create_large_windows_distribution():
    """Create a large Windows distribution package"""
    
    print("Creating Large ARXML Editor Windows Distribution")
    print("=" * 55)
    
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
    total_size = 0
    for item in files_to_copy:
        src_path = Path(item)
        if src_path.exists():
            dst_path = Path(dist_dir) / item
            if src_path.is_dir():
                print(f"✓ Copied directory: {item}")
                shutil.copytree(src_path, dst_path)
                # Calculate directory size
                dir_size = sum(f.stat().st_size for f in dst_path.rglob('*') if f.is_file())
                total_size += dir_size
                print(f"  Size: {dir_size:,} bytes")
            else:
                print(f"✓ Copied file: {item}")
                shutil.copy2(src_path, dst_path)
                file_size = dst_path.stat().st_size
                total_size += file_size
                print(f"  Size: {file_size:,} bytes")
        else:
            print(f"⚠ Skipped (not found): {item}")
    
    print(f"\nTotal size of source directory: {total_size:,} bytes ({total_size/1024/1024:.1f} MB)")
    
    # Create additional Windows-specific files
    create_windows_readme(dist_dir)
    create_windows_build_script(dist_dir)
    create_windows_launcher(dist_dir)
    create_windows_installer(dist_dir)
    create_sample_arxml_files(dist_dir)
    create_additional_documentation(dist_dir)
    create_large_sample_files(dist_dir)
    
    # Create ZIP file
    zip_filename = "ARXML_Editor_Source_Windows.zip"
    print(f"\nCreating zip file: {zip_filename}")
    
    zip_size = 0
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, dist_dir)
                zipf.write(file_path, arc_path)
                zip_size += os.path.getsize(file_path)
    
    actual_zip_size = os.path.getsize(zip_filename)
    print(f"✓ Created: {zip_filename}")
    print(f"  Source size: {zip_size:,} bytes ({zip_size/1024/1024:.1f} MB)")
    print(f"  ZIP size: {actual_zip_size:,} bytes ({actual_zip_size/1024/1024:.1f} MB)")
    print(f"  Compression ratio: {actual_zip_size/zip_size*100:.1f}%")
    
    # Verify ZIP contents
    print(f"\nVerifying ZIP contents...")
    with zipfile.ZipFile(zip_filename, 'r') as zipf:
        file_list = zipf.namelist()
        print(f"  Total files in ZIP: {len(file_list)}")
        
        src_files = [f for f in file_list if f.startswith('src/')]
        print(f"  Source files: {len(src_files)}")
        
        test_files = [f for f in file_list if f.startswith('Tests/')]
        print(f"  Test files: {len(test_files)}")
        
        py_files = [f for f in file_list if f.endswith('.py')]
        print(f"  Python files: {len(py_files)}")
        
        bat_files = [f for f in file_list if f.endswith('.bat')]
        print(f"  Batch files: {len(bat_files)}")
        
        arxml_files = [f for f in file_list if f.endswith('.arxml')]
        print(f"  ARXML files: {len(arxml_files)}")
    
    print(f"\n🎉 Large Windows Distribution created successfully!")
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

- **Complete Source Code** - All Python source files (src/ directory)
- **Build Scripts** - Windows batch files for building
- **Documentation** - Comprehensive guides and instructions
- **Schemas** - AUTOSAR XSD schema files
- **Tests** - Complete test suite (37 test files)
- **Sample Files** - Example ARXML files
- **Launcher Scripts** - Easy-to-use launcher scripts

## File Structure

```
ARXML_Editor_Source_Windows/
├── src/                          # Source code (36 files)
│   ├── core/                     # Core modules
│   └── ui/                       # UI modules
├── build_windows.bat             # Quick build script
├── build_windows_complete.bat    # Complete build script
├── build.bat                     # Simple build script
├── install.bat                   # Installation script
├── run_editor.bat                # Launcher script
├── arxml_editor.spec             # PyInstaller spec
├── requirements.txt              # Runtime dependencies
├── requirements_build.txt        # Build dependencies
├── schemas/                      # AUTOSAR schemas (2 files)
├── Tests/                        # Test files (37 files)
├── samples/                      # Sample ARXML files
├── docs/                         # Additional documentation
├── README_Windows_Source.md      # This file
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

def create_windows_launcher(dist_dir):
    """Create Windows launcher script"""
    launcher_script = """@echo off
echo ARXML Editor - Launcher
echo =======================
echo.

REM Check if executable exists
if exist "dist\\ARXML_Editor.exe" (
    echo Starting ARXML Editor...
    start "" "dist\\ARXML_Editor.exe"
) else (
    echo Executable not found. Please build first.
    echo Run: build_windows_complete.bat
    pause
)
"""
    
    launcher_path = Path(dist_dir) / "run_editor.bat"
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(launcher_script)
    print(f"✓ Created: run_editor.bat")

def create_windows_installer(dist_dir):
    """Create Windows installer script"""
    installer_script = """@echo off
echo ARXML Editor - Windows Installer
echo =================================
echo.

echo Installing Python dependencies...
pip install -r requirements.txt
pip install -r requirements_build.txt

echo.
echo Installation completed!
echo.
echo To build the application, run:
echo   build_windows_complete.bat
echo.
echo To run the application, run:
echo   run_editor.bat
echo.
pause
"""
    
    installer_path = Path(dist_dir) / "install.bat"
    with open(installer_path, 'w', encoding='utf-8') as f:
        f.write(installer_script)
    print(f"✓ Created: install.bat")

def create_sample_arxml_files(dist_dir):
    """Create additional sample ARXML files"""
    samples_dir = Path(dist_dir) / "samples"
    samples_dir.mkdir(exist_ok=True)
    
    # Create multiple sample ARXML files
    sample_files = [
        ("complex_sample.arxml", """<?xml version="1.0" encoding="UTF-8"?>
<AUTOSAR xmlns="http://autosar.org/schema/r4.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://autosar.org/schema/r4.0 AUTOSAR_4-6-0.xsd">
  <AR-PACKAGES>
    <AR-PACKAGE>
      <SHORT-NAME>ComplexSample</SHORT-NAME>
      <ELEMENTS>
        <ECUC-MODULE-CONFIGURATION-VALUES>
          <SHORT-NAME>EcuC</SHORT-NAME>
          <DEFINITION-REF DEST="ECUC-MODULE-DEF">/AUTOSAR/EcuC</DEFINITION-REF>
          <CONTAINERS>
            <ECUC-CONTAINER-VALUE>
              <SHORT-NAME>EcuCConfiguration</SHORT-NAME>
              <DEFINITION-REF DEST="ECUC-PARAM-CONF-CONTAINER-DEF">/AUTOSAR/EcuC/EcuCConfiguration</DEFINITION-REF>
              <PARAMETER-VALUES>
                <ECUC-NUMERICAL-PARAM-VALUE>
                  <DEFINITION-REF DEST="ECUC-INTEGER-PARAM-DEF">/AUTOSAR/EcuC/EcuCConfiguration/EcuCNumberOfConfigurations</DEFINITION-REF>
                  <VALUE>1</VALUE>
                </ECUC-NUMERICAL-PARAM-VALUE>
                <ECUC-TEXT-PARAM-VALUE>
                  <DEFINITION-REF DEST="ECUC-TEXT-PARAM-DEF">/AUTOSAR/EcuC/EcuCConfiguration/EcuCConfigurationComment</DEFINITION-REF>
                  <VALUE>Complex Sample Configuration</VALUE>
                </ECUC-TEXT-PARAM-VALUE>
              </PARAMETER-VALUES>
              <SUB-CONTAINERS>
                <ECUC-CONTAINER-VALUE>
                  <SHORT-NAME>EcuCConfiguration_1</SHORT-NAME>
                  <DEFINITION-REF DEST="ECUC-PARAM-CONF-CONTAINER-DEF">/AUTOSAR/EcuC/EcuCConfiguration/EcuCConfiguration</DEFINITION-REF>
                  <PARAMETER-VALUES>
                    <ECUC-TEXT-PARAM-VALUE>
                      <DEFINITION-REF DEST="ECUC-TEXT-PARAM-DEF">/AUTOSAR/EcuC/EcuCConfiguration/EcuCConfiguration/EcuCConfigurationName</DEFINITION-REF>
                      <VALUE>MainConfiguration</VALUE>
                    </ECUC-TEXT-PARAM-VALUE>
                  </PARAMETER-VALUES>
                </ECUC-CONTAINER-VALUE>
              </SUB-CONTAINERS>
            </ECUC-CONTAINER-VALUE>
          </CONTAINERS>
        </ECUC-MODULE-CONFIGURATION-VALUES>
      </ELEMENTS>
    </AR-PACKAGE>
  </AR-PACKAGES>
</AUTOSAR>"""),
        
        ("simple_sample.arxml", """<?xml version="1.0" encoding="UTF-8"?>
<AUTOSAR xmlns="http://autosar.org/schema/r4.0">
  <AR-PACKAGES>
    <AR-PACKAGE>
      <SHORT-NAME>SimpleSample</SHORT-NAME>
      <ELEMENTS>
        <ECUC-MODULE-CONFIGURATION-VALUES>
          <SHORT-NAME>EcuC</SHORT-NAME>
          <DEFINITION-REF DEST="ECUC-MODULE-DEF">/AUTOSAR/EcuC</DEFINITION-REF>
        </ECUC-MODULE-CONFIGURATION-VALUES>
      </ELEMENTS>
    </AR-PACKAGE>
  </AR-PACKAGES>
</AUTOSAR>"""),
        
        ("test_sample.arxml", """<?xml version="1.0" encoding="UTF-8"?>
<AUTOSAR xmlns="http://autosar.org/schema/r4.0">
  <AR-PACKAGES>
    <AR-PACKAGE>
      <SHORT-NAME>TestSample</SHORT-NAME>
      <ELEMENTS>
        <ECUC-MODULE-CONFIGURATION-VALUES>
          <SHORT-NAME>EcuC</SHORT-NAME>
          <DEFINITION-REF DEST="ECUC-MODULE-DEF">/AUTOSAR/EcuC</DEFINITION-REF>
          <CONTAINERS>
            <ECUC-CONTAINER-VALUE>
              <SHORT-NAME>EcuCConfiguration</SHORT-NAME>
              <DEFINITION-REF DEST="ECUC-PARAM-CONF-CONTAINER-DEF">/AUTOSAR/EcuC/EcuCConfiguration</DEFINITION-REF>
              <PARAMETER-VALUES>
                <ECUC-TEXT-PARAM-VALUE>
                  <DEFINITION-REF DEST="ECUC-TEXT-PARAM-DEF">/AUTOSAR/EcuC/EcuCConfiguration/EcuCConfigurationComment</DEFINITION-REF>
                  <VALUE>Test Configuration for ARXML Editor</VALUE>
                </ECUC-TEXT-PARAM-VALUE>
              </PARAMETER-VALUES>
            </ECUC-CONTAINER-VALUE>
          </CONTAINERS>
        </ECUC-MODULE-CONFIGURATION-VALUES>
      </ELEMENTS>
    </AR-PACKAGE>
  </AR-PACKAGES>
</AUTOSAR>""")
    ]
    
    for filename, content in sample_files:
        sample_path = samples_dir / filename
        with open(sample_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"✓ Created: samples/ ({len(sample_files)} sample files)")

def create_additional_documentation(dist_dir):
    """Create additional documentation files"""
    docs_dir = Path(dist_dir) / "docs"
    docs_dir.mkdir(exist_ok=True)
    
    # Create API documentation
    api_doc = """# ARXML Editor API Documentation

## Core Modules

### Application Module
The main application controller that orchestrates the entire ARXML editor.

### ARXML Document Model
Handles the in-memory representation of ARXML documents and manages modifications.

### ARXML Parser
Parses ARXML files into the internal document model.

### Schema Service
Manages AUTOSAR schema detection and validation.

### Validation Service
Provides validation functionality for ARXML documents.

## UI Modules

### Main Window
The main application window that coordinates all UI components.

### Tree Navigator
Displays the hierarchical structure of ARXML documents.

### Property Editor
Allows editing of selected element properties.

### Validation List
Shows validation errors and warnings.

### Diagram View
Displays visual representation of ARXML structure.

## Usage Examples

### Loading an ARXML File
```python
from src.core.application import Application

app = Application()
document = app.load_document("path/to/file.arxml")
```

### Validating a Document
```python
validation_service = ValidationService()
errors = validation_service.validate_document(document)
```

### Saving a Document
```python
document.save_as("path/to/output.arxml")
```
"""
    
    api_doc_path = docs_dir / "API_DOCUMENTATION.md"
    with open(api_doc_path, 'w', encoding='utf-8') as f:
        f.write(api_doc)
    
    # Create user guide
    user_guide = """# ARXML Editor User Guide

## Getting Started

1. **Installation**: Follow the Windows build guide to install dependencies
2. **Building**: Run the build script to create the executable
3. **Running**: Launch the application using the provided scripts

## Basic Usage

### Opening Files
- Use File > Open to load ARXML files
- The tree view will populate with the document structure
- Select elements to view their properties

### Editing Properties
- Click on any element in the tree
- Edit properties in the Properties panel
- Changes are automatically saved to the data model

### Saving Changes
- Use File > Save As to save modifications
- The application preserves the original structure

## Advanced Features

### Schema Validation
- Automatic schema detection from ARXML files
- Real-time validation feedback
- Error highlighting in the validation panel

### Drag and Drop
- Reorder elements by dragging in the tree
- Visual feedback shows drop location
- Maintains document structure integrity

### Search and Navigation
- Use Ctrl+F to search for elements
- Navigate through large documents efficiently
- Bookmark important sections

## Troubleshooting

### Common Issues
1. **File won't open**: Check file format and schema compatibility
2. **Properties not showing**: Ensure element is selected in tree
3. **Changes not saving**: Verify write permissions to output location

### Getting Help
- Check the validation panel for error messages
- Review the console output for detailed information
- Consult the API documentation for advanced usage
"""
    
    user_guide_path = docs_dir / "USER_GUIDE.md"
    with open(user_guide_path, 'w', encoding='utf-8') as f:
        f.write(user_guide)
    
    print(f"✓ Created: docs/ (2 documentation files)")

def create_large_sample_files(dist_dir):
    """Create larger sample files to increase distribution size"""
    large_samples_dir = Path(dist_dir) / "large_samples"
    large_samples_dir.mkdir(exist_ok=True)
    
    # Create a large sample ARXML file
    large_arxml = """<?xml version="1.0" encoding="UTF-8"?>
<AUTOSAR xmlns="http://autosar.org/schema/r4.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://autosar.org/schema/r4.0 AUTOSAR_4-6-0.xsd">
  <AR-PACKAGES>
    <AR-PACKAGE>
      <SHORT-NAME>LargeSample</SHORT-NAME>
      <ELEMENTS>"""
    
    # Add many containers to make the file larger
    for i in range(50):
        large_arxml += f"""
        <ECUC-MODULE-CONFIGURATION-VALUES>
          <SHORT-NAME>EcuC_{i}</SHORT-NAME>
          <DEFINITION-REF DEST="ECUC-MODULE-DEF">/AUTOSAR/EcuC</DEFINITION-REF>
          <CONTAINERS>
            <ECUC-CONTAINER-VALUE>
              <SHORT-NAME>EcuCConfiguration_{i}</SHORT-NAME>
              <DEFINITION-REF DEST="ECUC-PARAM-CONF-CONTAINER-DEF">/AUTOSAR/EcuC/EcuCConfiguration</DEFINITION-REF>
              <PARAMETER-VALUES>
                <ECUC-TEXT-PARAM-VALUE>
                  <DEFINITION-REF DEST="ECUC-TEXT-PARAM-DEF">/AUTOSAR/EcuC/EcuCConfiguration/EcuCConfigurationComment</DEFINITION-REF>
                  <VALUE>Large Sample Configuration {i} - This is a comprehensive test configuration for the ARXML Editor application. It includes multiple parameters and containers to test the full functionality of the editor.</VALUE>
                </ECUC-TEXT-PARAM-VALUE>
                <ECUC-NUMERICAL-PARAM-VALUE>
                  <DEFINITION-REF DEST="ECUC-INTEGER-PARAM-DEF">/AUTOSAR/EcuC/EcuCConfiguration/EcuCNumberOfConfigurations</DEFINITION-REF>
                  <VALUE>{i + 1}</VALUE>
                </ECUC-NUMERICAL-PARAM-VALUE>
              </PARAMETER-VALUES>
              <SUB-CONTAINERS>
                <ECUC-CONTAINER-VALUE>
                  <SHORT-NAME>EcuCConfiguration_{i}_1</SHORT-NAME>
                  <DEFINITION-REF DEST="ECUC-PARAM-CONF-CONTAINER-DEF">/AUTOSAR/EcuC/EcuCConfiguration/EcuCConfiguration</DEFINITION-REF>
                  <PARAMETER-VALUES>
                    <ECUC-TEXT-PARAM-VALUE>
                      <DEFINITION-REF DEST="ECUC-TEXT-PARAM-DEF">/AUTOSAR/EcuC/EcuCConfiguration/EcuCConfiguration/EcuCConfigurationName</DEFINITION-REF>
                      <VALUE>MainConfiguration_{i}</VALUE>
                    </ECUC-TEXT-PARAM-VALUE>
                    <ECUC-TEXT-PARAM-VALUE>
                      <DEFINITION-REF DEST="ECUC-TEXT-PARAM-DEF">/AUTOSAR/EcuC/EcuCConfiguration/EcuCConfiguration/EcuCConfigurationDescription</DEFINITION-REF>
                      <VALUE>This is a detailed description for configuration {i}. It provides comprehensive information about the configuration parameters and their intended use in the AUTOSAR system.</VALUE>
                    </ECUC-TEXT-PARAM-VALUE>
                  </PARAMETER-VALUES>
                </ECUC-CONTAINER-VALUE>
              </SUB-CONTAINERS>
            </ECUC-CONTAINER-VALUE>
          </CONTAINERS>
        </ECUC-MODULE-CONFIGURATION-VALUES>"""
    
    large_arxml += """
      </ELEMENTS>
    </AR-PACKAGE>
  </AR-PACKAGES>
</AUTOSAR>"""
    
    large_sample_path = large_samples_dir / "large_sample.arxml"
    with open(large_sample_path, 'w', encoding='utf-8') as f:
        f.write(large_arxml)
    
    print(f"✓ Created: large_samples/ (1 large sample file)")

if __name__ == "__main__":
    create_large_windows_distribution()