#!/bin/bash

echo "Building ARXML Editor for Windows..."
echo "===================================="

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

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist build

# Build the executable
echo "Building executable..."
pyinstaller --clean arxml_editor.spec
if [ $? -ne 0 ]; then
    echo "ERROR: Build failed"
    exit 1
fi

# Create distribution folder
echo "Creating distribution folder..."
mkdir -p ARXML_Editor_Windows
cp dist/ARXML_Editor.exe ARXML_Editor_Windows/
cp README_Windows.md ARXML_Editor_Windows/
cp sample.arxml ARXML_Editor_Windows/
if [ -d "Backup" ]; then
    cp -r Backup ARXML_Editor_Windows/
fi

echo ""
echo "Build completed successfully!"
echo ""
echo "The executable is located in: ARXML_Editor_Windows/ARXML_Editor.exe"
echo ""
echo "You can now distribute the entire 'ARXML_Editor_Windows' folder."
echo ""