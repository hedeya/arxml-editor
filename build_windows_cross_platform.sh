#!/bin/bash

echo "Building ARXML Editor for Windows with PyQt6 fixes..."
echo "====================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

# Create a clean virtual environment for building
echo "Creating clean build environment..."
rm -rf build_env_clean
python3 -m venv build_env_clean --upgrade-deps
source build_env_clean/bin/activate

# Install build dependencies
echo "Installing build dependencies..."
pip install --upgrade pip
pip install pyinstaller==6.16.0
pip install PyQt6==6.6.1
pip install lxml==4.9.3
pip install xmlschema==3.3.0
pip install pydantic==2.5.0
pip install typing-extensions==4.8.0

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist build

# Build the executable with comprehensive PyQt6 support
echo "Building executable with comprehensive PyQt6 support..."
pyinstaller --clean --onefile --windowed --name ARXML_Editor \
    --add-data "schemas:schemas" \
    --add-data "sample.arxml:." \
    --hidden-import PyQt6 \
    --hidden-import PyQt6.QtCore \
    --hidden-import PyQt6.QtGui \
    --hidden-import PyQt6.QtWidgets \
    --hidden-import PyQt6.sip \
    --hidden-import PyQt6.QtCore.Qt \
    --hidden-import PyQt6.QtGui.QFont \
    --hidden-import PyQt6.QtGui.QIcon \
    --hidden-import PyQt6.QtGui.QKeySequence \
    --hidden-import PyQt6.QtGui.QAction \
    --hidden-import PyQt6.QtGui.QPen \
    --hidden-import PyQt6.QtGui.QBrush \
    --hidden-import PyQt6.QtGui.QColor \
    --hidden-import PyQt6.QtGui.QPainter \
    --hidden-import PyQt6.QtCore.pyqtSignal \
    --hidden-import PyQt6.QtCore.QRectF \
    --hidden-import PyQt6.QtCore.QPointF \
    --collect-all PyQt6 \
    --collect-all lxml \
    --collect-all xmlschema \
    --collect-submodules PyQt6 \
    --collect-data PyQt6 \
    --copy-metadata PyQt6 \
    main.py

if [ $? -ne 0 ]; then
    echo "ERROR: Build failed"
    exit 1
fi

# Create distribution folder
echo "Creating distribution folder..."
mkdir -p ARXML_Editor_Windows_Fixed_v2
cp dist/ARXML_Editor ARXML_Editor_Windows_Fixed_v2/ARXML_Editor.exe
cp sample.arxml ARXML_Editor_Windows_Fixed_v2/
if [ -d "schemas" ]; then
    cp -r schemas ARXML_Editor_Windows_Fixed_v2/
fi

# Create a comprehensive README for the distribution
echo "Creating README for distribution..."
cat > ARXML_Editor_Windows_Fixed_v2/README.txt << 'EOF'
ARXML Editor - Windows Distribution (Fixed v2)
=============================================

This is a standalone Windows executable for the ARXML Editor with PyQt6 dependencies properly bundled.

CHANGES IN THIS VERSION:
- Fixed PyQt6 dependency issues that caused "no module named PyQt6" errors
- All PyQt6 libraries and platform plugins are now properly included
- Uses PyInstaller's comprehensive collection options for PyQt6
- Includes all necessary Qt6 platform plugins for Windows
- Built with clean virtual environment to avoid conflicts

TO RUN THE APPLICATION:
1. Double-click ARXML_Editor.exe
2. Or run from command line: ARXML_Editor.exe

The application includes all necessary dependencies including PyQt6, lxml, and xmlschema.

FILES INCLUDED:
- ARXML_Editor.exe: Main executable (standalone, no installation required)
- sample.arxml: Sample ARXML file for testing
- schemas/: XSD schema files for validation
- README.txt: This file

TECHNICAL DETAILS:
- Built with PyInstaller 6.16.0
- PyQt6 6.6.1 with all platform plugins
- lxml 4.9.3 for XML processing
- xmlschema 3.3.0 for XSD validation
- All dependencies statically linked
- Clean build environment to avoid conflicts

For support or issues, please refer to the project repository.
EOF

echo ""
echo "Build completed successfully!"
echo ""
echo "The executable is located in: ARXML_Editor_Windows_Fixed_v2/ARXML_Editor.exe"
echo ""
echo "You can now distribute the entire 'ARXML_Editor_Windows_Fixed_v2' folder."
echo ""

# Clean up build environment
deactivate
rm -rf build_env_clean