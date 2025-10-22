#!/bin/bash

echo "Creating GitHub Release for PyQt6 Fixed Windows Build"
echo "====================================================="

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "ERROR: Not in a git repository"
    exit 1
fi

# Get the current version
VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "v1.2.4")
NEW_VERSION="v1.2.4-python-fixed"

echo "Creating release: $NEW_VERSION"

# Create release notes
cat > RELEASE_NOTES.md << 'EOF'
# ARXML Editor v1.2.4 - PyQt6 Fixed Release

## 🐛 Bug Fixes

### PyQt6 Dependency Issues Fixed
- **Fixed**: "No module named PyQt6" errors in Windows release
- **Fixed**: Missing Qt6 platform plugins causing startup failures
- **Fixed**: Undefined symbol errors in cross-platform builds

## 🔧 Technical Improvements

### Build System Enhancements
- Added comprehensive PyQt6 collection in PyInstaller build
- Updated spec file with proper PyQt6 hidden imports
- Created fixed build scripts for both Windows and Linux
- Added detailed Windows build guide with troubleshooting

### Build Scripts Added
- `build_windows_cross_platform.bat` - Windows batch script
- `build_windows_cross_platform.sh` - Linux/Unix script
- `build_windows_fixed.bat` - Alternative Windows script
- `build_windows_fixed.sh` - Alternative Linux script

## 📋 How to Build

### For Windows Users
1. Download the source code
2. Run `build_windows_cross_platform.bat`
3. Find the executable in `ARXML_Editor_Windows/ARXML_Editor.exe`

### For Linux Users (Cross-compilation)
1. Download the source code
2. Run `./build_windows_cross_platform.sh`
3. Find the executable in `ARXML_Editor_Windows_Fixed_v2/ARXML_Editor.exe`

## 📚 Documentation

- `WINDOWS_BUILD_GUIDE_FIXED.md` - Comprehensive build guide
- `ARXML_Editor_Source_Windows/` - Complete Windows source distribution
- Updated README files with build instructions

## ⚠️ Important Notes

- The executable files are large (~134MB) due to bundled PyQt6 libraries
- All dependencies are statically linked - no additional installation required
- Build on Windows for best compatibility (cross-compilation may have issues)
- Use the provided build scripts for optimal results

## 🔗 Files Included

- Source code with all fixes
- Build scripts for multiple platforms
- Comprehensive documentation
- Sample ARXML files and schemas
- Test suite

## 🚀 Next Steps

1. Download the source code
2. Follow the build guide for your platform
3. Build the executable using the provided scripts
4. Test the application with your ARXML files

For support or issues, please refer to the project repository.
EOF

echo "Release notes created: RELEASE_NOTES.md"
echo ""
echo "To create the release:"
echo "1. Go to https://github.com/hedeya/arxml-editor/releases"
echo "2. Click 'Create a new release'"
echo "3. Use tag: $NEW_VERSION"
echo "4. Use title: ARXML Editor v1.2.4 - PyQt6 Fixed Release"
echo "5. Copy the contents of RELEASE_NOTES.md as the description"
echo "6. Upload the built executable files as assets (if available)"
echo ""
echo "Or use GitHub CLI if installed:"
echo "gh release create $NEW_VERSION --title 'ARXML Editor v1.2.4 - PyQt6 Fixed Release' --notes-file RELEASE_NOTES.md"