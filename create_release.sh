#!/bin/bash

echo "🚀 Creating GitHub Release for ARXML Editor"
echo "==========================================="

# Check if GitHub CLI is installed
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI found. Creating release..."
    
    # Create release
    gh release create v1.0.0 \
        --title "ARXML Editor v1.0.0 - Windows Distribution" \
        --notes "🎉 **ARXML Editor v1.0.0 - Professional AUTOSAR XML Editor**

## 🚀 **What's New**
- Complete Windows distribution package
- Self-contained executable (build required)
- Comprehensive sample files and schemas
- Professional documentation and build tools

## 📦 **Distribution Package**
- **ARXML_Editor_Windows.zip** - Complete Windows distribution
- **ARXML_Editor_Windows/** - Ready-to-run folder
- Includes sample files, schemas, and documentation

## 🛠️ **Build System**
- **build_windows_complete.bat** - Automated Windows build script
- **arxml_editor.spec** - PyInstaller configuration
- **BUILD_INSTRUCTIONS.md** - Detailed build guide

## ✨ **Features**
- Dynamic schema detection (AUTOSAR 4.6.0, 4.7.0+)
- Real-time validation and editing
- Interactive tree navigator
- Property editor with live editing
- Diagram view with file statistics
- ECUC file support
- Professional PyQt6 GUI

## 🎯 **Ready For**
- Windows distribution
- Team collaboration
- Professional development
- Standalone execution

## 📋 **Quick Start**
1. Download **ARXML_Editor_Windows.zip**
2. Extract to desired location
3. Run **build_windows_complete.bat** to build executable
4. Double-click **ARXML_Editor.exe** to run

## 📚 **Documentation**
- See **README_Windows.md** for user guide
- See **BUILD_INSTRUCTIONS.md** for build details
- See main **README.md** for development info

---
**Note:** The executable is a placeholder. Run the build script on Windows to create the actual .exe file." \
        --latest \
        ARXML_Editor_Windows.zip
    
    if [ $? -eq 0 ]; then
        echo "✅ Release created successfully!"
        echo "📍 Release URL: https://github.com/hedeya/arxml-editor/releases"
    else
        echo "❌ Failed to create release. Please check your GitHub CLI authentication."
        echo "   Run: gh auth login"
    fi
else
    echo "⚠️  GitHub CLI not found. Please create the release manually:"
    echo ""
    echo "📋 Manual Steps:"
    echo "1. Go to https://github.com/hedeya/arxml-editor/releases"
    echo "2. Click 'Create a new release'"
    echo "3. Tag version: v1.0.0"
    echo "4. Release title: ARXML Editor v1.0.0 - Windows Distribution"
    echo "5. Upload ARXML_Editor_Windows.zip"
    echo "6. Publish release"
    echo ""
    echo "📚 Or install GitHub CLI:"
    echo "   curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg"
    echo "   echo \"deb [arch=\$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main\" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null"
    echo "   sudo apt update"
    echo "   sudo apt install gh"
    echo "   gh auth login"
fi

echo ""
echo "🎯 Next Steps:"
echo "1. Visit your release: https://github.com/hedeya/arxml-editor/releases"
echo "2. Download ARXML_Editor_Windows.zip"
echo "3. Share with your team"
echo "4. Test on Windows machines"
echo ""
echo "🚀 Happy distributing!"