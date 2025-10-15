#!/bin/bash

echo "Building ARXML Editor for Windows with PyQt6 fixes..."
echo "====================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" &> /dev/null; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install PyInstaller"
        exit 1
    fi
fi

# Install required packages
echo "Installing required packages..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install required packages"
    exit 1
fi

# Install PyQt6 explicitly to ensure all dependencies are available
echo "Installing PyQt6 with all dependencies..."
pip3 install PyQt6==6.6.1 --upgrade
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install PyQt6"
    exit 1
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist build

# Build the executable with PyQt6 hooks
echo "Building executable with PyQt6 support..."
pyinstaller --clean --onefile --windowed --name ARXML_Editor \
    --add-data "schemas:schemas" \
    --add-data "sample.arxml:." \
    --hidden-import PyQt6 \
    --hidden-import PyQt6.QtCore \
    --hidden-import PyQt6.QtGui \
    --hidden-import PyQt6.QtWidgets \
    --hidden-import PyQt6.sip \
    --collect-all PyQt6 \
    --collect-all lxml \
    --collect-all xmlschema \
    main.py
if [ $? -ne 0 ]; then
    echo "ERROR: Build failed"
    exit 1
fi

# Create distribution folder
echo "Creating distribution folder..."
mkdir -p ARXML_Editor_Windows
cp dist/ARXML_Editor ARXML_Editor_Windows/ARXML_Editor.exe
cp sample.arxml ARXML_Editor_Windows/
if [ -d "schemas" ]; then
    cp -r schemas ARXML_Editor_Windows/
fi

# Create a simple README for the distribution
echo "Creating README for distribution..."
cat > ARXML_Editor_Windows/README.txt << 'EOF'
ARXML Editor - Windows Distribution
===================================

This is a standalone Windows executable for the ARXML Editor.
No additional installation is required.

To run the application:
1. Double-click ARXML_Editor.exe
2. Or run from command line: ARXML_Editor.exe

The application includes all necessary dependencies including PyQt6.

For support or issues, please refer to the project repository.
EOF

echo ""
echo "Build completed successfully!"
echo ""
echo "The executable is located in: ARXML_Editor_Windows/ARXML_Editor.exe"
echo ""
echo "You can now distribute the entire 'ARXML_Editor_Windows' folder."
echo ""