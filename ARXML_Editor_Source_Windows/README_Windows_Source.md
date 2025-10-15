# ARXML Editor - Windows Source Distribution

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
