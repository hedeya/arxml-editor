# Installation Guide

This guide will help you install and set up the ARXML Editor on your system.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **Memory**: At least 4GB RAM (8GB recommended)
- **Storage**: 500MB free disk space

### Python Installation
If you don't have Python installed:

**Windows:**
1. Download Python from [python.org](https://python.org)
2. Run the installer and check "Add Python to PATH"
3. Verify installation: `python --version`

**macOS:**
```bash
# Using Homebrew
brew install python3

# Or download from python.org
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

## 🚀 Installation Methods

### Method 1: From Source (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hedeya/arxml-editor.git
   cd arxml-editor
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

### Method 2: Using pip (Future)

```bash
pip install arxml-editor
arxml-editor
```

### Method 3: Pre-built Executable (Windows)

1. Download the latest release from [GitHub Releases](https://github.com/hedeya/arxml-editor/releases)
2. Extract the ZIP file
3. Run `ARXML_Editor.exe`

## 🔧 Development Setup

For developers who want to contribute:

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/your-username/arxml-editor.git
   cd arxml-editor
   ```

2. **Create a development environment:**
   ```bash
   python -m venv dev-env
   source dev-env/bin/activate  # On Windows: dev-env\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]
   ```

4. **Run tests:**
   ```bash
   pytest
   ```

## 🐛 Troubleshooting

### Common Issues

**"Python not found" error:**
- Ensure Python is installed and added to PATH
- Try using `python3` instead of `python`

**"Module not found" errors:**
- Ensure you're in the correct directory
- Activate the virtual environment
- Install dependencies: `pip install -r requirements.txt`

**Qt library errors (Linux):**
- Install Qt dependencies:
  ```bash
  sudo apt install python3-pyqt6
  # or
  sudo apt install python3-pyside6
  ```

**Permission errors:**
- On Linux/macOS, you might need to use `sudo` for system-wide installation
- Consider using a virtual environment instead

**Import errors:**
- Ensure all dependencies are installed
- Check Python version compatibility
- Verify file paths and working directory

### Getting Help

If you encounter issues:

1. **Check the Issues page**: [GitHub Issues](https://github.com/hedeya/arxml-editor/issues)
2. **Create a new issue** with:
   - Operating system and version
   - Python version
   - Error message
   - Steps to reproduce
3. **Contact the maintainer**: hedeya

## 📦 Dependencies

The application requires the following Python packages:

- **PyQt6** (6.4.0+) - GUI framework
- **lxml** (4.9.0+) - XML processing
- **xmlschema** (2.5.0+) - Schema validation
- **pydantic** (2.5.0+) - Data validation

Optional development dependencies:
- **pytest** - Testing framework
- **black** - Code formatting
- **flake8** - Linting
- **mypy** - Type checking

## 🔄 Updates

To update the application:

1. **Pull latest changes:**
   ```bash
   git pull origin main
   ```

2. **Update dependencies:**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Restart the application**

## 🗑️ Uninstallation

To remove the application:

1. **Delete the project directory:**
   ```bash
   rm -rf arxml-editor  # Linux/macOS
   rmdir /s arxml-editor  # Windows
   ```

2. **Remove virtual environment:**
   ```bash
   rm -rf venv  # Linux/macOS
   rmdir /s venv  # Windows
   ```

3. **If installed via pip:**
   ```bash
   pip uninstall arxml-editor
   ```

## ✅ Verification

To verify the installation is working:

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Test with sample file:**
   - Open `sample.arxml`
   - Verify the tree is populated
   - Check that properties can be edited
   - Test the diagram view

3. **Test editing features:**
   - Right-click on tree sections to add elements
   - Edit properties in the Properties tab
   - Save the document

If all steps work correctly, your installation is successful! 🎉