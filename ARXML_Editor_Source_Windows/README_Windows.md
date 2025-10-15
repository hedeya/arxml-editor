# ARXML Editor - Windows Distribution

A powerful AUTOSAR XML (ARXML) editor with dynamic schema detection and validation capabilities.

## 🚀 Quick Start

1. **Download** the `ARXML_Editor_Windows` folder
2. **Double-click** `ARXML_Editor.exe` to launch the application
3. **Open** an ARXML file using File → Open

## 📋 System Requirements

- **Windows 10/11** (64-bit)
- **No additional software required** - this is a self-contained executable

## 🎯 Features

### ✨ Core Functionality
- **Dynamic Schema Detection**: Automatically detects AUTOSAR schema version from ARXML files
- **Schema Validation**: Validates ARXML files against detected schemas
- **Multi-Format Support**: Handles both standard ARXML and ECUC configuration files
- **Clean Tree Interface**: Shows only sections with actual content

### 🔧 Supported File Types
- **Standard ARXML Files**: Software components, compositions, interfaces
- **ECUC Files**: ECU configuration files with hierarchical structure
- **Schema Versions**: AUTOSAR 4.6.0, 4.7.0+ (auto-detected)

### 🖥️ User Interface
- **Tree Navigator**: Hierarchical view of ARXML elements
- **Property Editor**: View and edit element properties
- **Validation Panel**: Real-time validation results
- **File Operations**: Open, save, and create new documents

## 📁 File Structure

```
ARXML_Editor_Windows/
├── ARXML_Editor.exe          # Main executable
├── sample.arxml              # Sample ARXML file for testing
├── Backup/                   # Sample ECUC files
│   └── ECUC/
│       └── FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml
└── README_Windows.md         # This file
```

## 🎮 How to Use

### Opening Files
1. Launch `ARXML_Editor.exe`
2. Click **File → Open** or press `Ctrl+O`
3. Select your ARXML file
4. The application will automatically detect the schema version

### Navigating Content
- **Tree View**: Click on elements in the left panel to explore
- **Properties**: Selected element properties appear in the right panel
- **Validation**: Check the Validation tab for any issues

### Supported Operations
- **View**: Browse ARXML structure and properties
- **Validate**: Check file against AUTOSAR schema
- **Export**: Save modified files (if editing is implemented)

## 🔍 Sample Files

### Test with Sample Files
- **`sample.arxml`**: Contains software components and interfaces
- **`Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml`**: ECUC configuration file

### What You'll See
- **Sample ARXML**: Software Component Types and Port Interfaces sections
- **ECUC File**: ECUC Elements section with hierarchical configuration data

## 🛠️ Troubleshooting

### Common Issues

**Application won't start:**
- Ensure you're running Windows 10/11 (64-bit)
- Try running as administrator
- Check Windows Defender isn't blocking the executable

**Files won't open:**
- Verify the file is a valid ARXML file
- Check file permissions
- Try with the included sample files first

**Schema detection fails:**
- Ensure the ARXML file has proper namespace declarations
- Check that the file isn't corrupted
- Try with the included sample files

### Getting Help
- Check the Validation panel for specific error messages
- Try opening the included sample files to verify the application works
- Ensure your ARXML files follow AUTOSAR standards

## 📊 Validation Features

The application provides comprehensive validation:
- **Schema Compliance**: Validates against detected AUTOSAR schema
- **Structure Validation**: Checks XML structure and element hierarchy
- **Content Validation**: Validates element content and attributes
- **Real-time Feedback**: Shows validation results immediately

## 🔧 Technical Details

### Built With
- **PyQt6**: Modern GUI framework
- **LXML**: High-performance XML processing
- **XMLSchema**: XSD schema validation
- **PyInstaller**: Self-contained executable packaging

### Schema Support
- **AUTOSAR 4.6.0**: Basic schema support
- **AUTOSAR 4.7.0**: Enhanced schema support
- **Auto-Detection**: Automatically identifies schema version from file

## 📝 License

This software is provided as-is for evaluation and testing purposes.

## 🎉 Enjoy!

The ARXML Editor makes working with AUTOSAR XML files simple and efficient. Start by opening the included sample files to explore the features!

---

**Version**: 1.0  
**Build Date**: $(date)  
**Platform**: Windows 64-bit