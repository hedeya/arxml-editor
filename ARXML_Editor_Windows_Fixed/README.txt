ARXML Editor - Windows Distribution (Fixed)
===========================================

This is a standalone Windows executable for the ARXML Editor with PyQt6 dependencies properly bundled.

CHANGES IN THIS VERSION:
- Fixed PyQt6 dependency issues that caused "no module named PyQt6" errors
- All PyQt6 libraries and platform plugins are now properly included
- Uses PyInstaller's --collect-all PyQt6 option for comprehensive dependency collection
- Includes all necessary Qt6 platform plugins for Windows

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

For support or issues, please refer to the project repository.