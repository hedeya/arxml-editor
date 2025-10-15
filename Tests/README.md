# ARXML Editor - Test Suite

This directory contains all test files for the ARXML Editor project. The tests are organized by functionality and can be run individually or as a suite.

## 📋 Test Files Overview

### Core Functionality Tests
- **`test_application.py`** - Tests the main application controller and document loading
- **`test_arxml_editor.py`** - Tests the complete ARXML editor functionality
- **`test_editing_features.py`** - Tests add/edit/remove/save functionality
- **`test_new_features.py`** - Tests enhanced user interaction features (editable properties, drag & drop, delete confirmation, save as)
- **`test_save_functionality.py`** - Tests basic save functionality and property persistence
- **`test_property_persistence.py`** - Tests property persistence fixes and save with changes
- **`test_fixes.py`** - Tests the three main fixes: ECUC saving, property persistence, and drag & drop
- **`test_real_ecuc_save.py`** - Tests loading and saving real ECUC files with complete element preservation
- **`test_short_name_editing.py`** - Tests SHORT-NAME editing functionality in ECUC files
- **`test_ecuc_save_fidelity.py`** - Tests ECUC file save fidelity and content preservation
- **`test_user_scenario_validation.py`** - Tests the exact user scenario for SHORT-NAME editing

### Schema and Validation Tests
- **`test_schema_detection.py`** - Tests automatic schema version detection
- **`test_comprehensive_schema.py`** - Tests comprehensive schema validation

### GUI Component Tests
- **`test_gui_loading.py`** - Tests GUI loading and initial state
- **`test_property_editor.py`** - Tests property editor functionality
- **`test_tree_selection.py`** - Tests tree navigator selection behavior
- **`test_manual_selection.py`** - Tests manual selection in GUI
- **`test_tree_clearing.py`** - Tests tree clearing functionality
- **`test_clean_tree.py`** - Tests clean tree interface (no empty sections)

### ECUC File Tests
- **`test_ecuc_file.py`** - Tests ECUC file parsing and element extraction
- **`test_ecuc_gui.py`** - Tests GUI population with ECUC files
- **`test_gui_ecuc.py`** - Tests ECUC file loading in GUI

### Debug and Development Tests
- **`debug_document_loading.py`** - Debug script for document loading issues

## 🚀 Running Tests

### Run All Tests
```bash
# From the Tests directory
cd Tests
python test_editing_features.py  # Main functionality test
```

### Run Individual Tests
```bash
# Test specific functionality
python test_schema_detection.py
python test_gui_loading.py
python test_ecuc_file.py
```

### Run Tests with Output
```bash
# Run with verbose output
python -u test_editing_features.py
```

## 📊 Test Categories

### ✅ Core Tests (Essential)
- `test_editing_features.py` - **MUST PASS** - Core editing functionality
- `test_application.py` - **MUST PASS** - Application startup and loading
- `test_schema_detection.py` - **MUST PASS** - Schema detection
- `test_new_features.py` - **MUST PASS** - Enhanced user interaction features
- `test_save_functionality.py` - **MUST PASS** - Basic save functionality and property persistence
- `test_property_persistence.py` - **MUST PASS** - Property persistence fixes and save with changes
- `test_fixes.py` - **MUST PASS** - Tests the three main fixes: ECUC saving, property persistence, and drag & drop
- `test_real_ecuc_save.py` - **MUST PASS** - Tests real ECUC file loading and saving with complete element preservation
- `test_short_name_editing.py` - **MUST PASS** - Tests SHORT-NAME editing functionality in ECUC files
- `test_ecuc_save_fidelity.py` - **MUST PASS** - Tests ECUC file save fidelity and content preservation
- `test_user_scenario_validation.py` - **MUST PASS** - Tests the exact user scenario for SHORT-NAME editing

### ✅ GUI Tests (Important)
- `test_gui_loading.py` - GUI initialization
- `test_property_editor.py` - Property editing
- `test_tree_clearing.py` - Tree interface

### ✅ ECUC Tests (Feature-specific)
- `test_ecuc_file.py` - ECUC file parsing
- `test_gui_ecuc.py` - ECUC GUI integration

### 🔧 Debug Tests (Development)
- `debug_document_loading.py` - Debugging tools

## 🎯 Test Results

### Expected Output
All tests should show:
- ✅ **Success indicators** for passed tests
- 📊 **Statistics** and counts
- 🎉 **Completion messages**

### Common Issues
- **Import errors**: Ensure you're running from the correct directory
- **File not found**: Check that sample files exist in the parent directory
- **GUI errors**: Some tests may not work in headless environments

## 🛠️ Test Development

### Adding New Tests
1. **Create test file** with descriptive name
2. **Follow naming convention**: `test_[functionality].py`
3. **Include docstring** explaining what the test does
4. **Add to this README** in the appropriate category

### Test Structure
```python
#!/usr/bin/env python3
"""
Test [Functionality Name]
[Description of what this test does]
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_functionality():
    """Test the specific functionality"""
    print("Testing [Functionality Name]")
    print("=" * 30)
    
    # Test code here
    
    print("🎉 Test completed successfully!")

if __name__ == "__main__":
    test_functionality()
```

## 📝 Test Data

### Sample Files Used
- **`../sample.arxml`** - Basic ARXML file for testing
- **`../Backup/ECUC/`** - ECUC files for testing
- **`../schemas/`** - XSD schema files

### Test Environment
- **Python 3.8+** required
- **PyQt6** for GUI tests
- **Working directory** should be the Tests directory

## 🔍 Troubleshooting

### Common Issues
1. **ImportError**: Run from Tests directory or adjust sys.path
2. **FileNotFoundError**: Ensure sample files exist in parent directory
3. **GUI errors**: Some tests require display (not headless)

### Debug Mode
```bash
# Run with debug output
python -u test_editing_features.py 2>&1 | tee test_output.log
```

## 📈 Test Coverage

### Covered Areas
- ✅ Document loading and parsing
- ✅ Schema detection and validation
- ✅ Element editing (add/edit/remove)
- ✅ File saving and XML generation
- ✅ GUI component functionality
- ✅ ECUC file support
- ✅ Tree navigation and selection
- ✅ Enhanced user interaction features (editable properties, drag & drop, delete confirmation, save as)
- ✅ Property persistence and widget value saving
- ✅ Save functionality with property changes
- ✅ ECUC file complete preservation (14,059+ elements)
- ✅ Drag and drop visual indicators and validation
- ✅ Real ECUC file loading and saving with fidelity verification
- ✅ SHORT-NAME editing functionality in ECUC files
- ✅ ECUC file save fidelity and content preservation
- ✅ User scenario validation for SHORT-NAME editing
- ✅ Property persistence when switching between elements
- ✅ File integrity and XML structure validation

### Areas Needing More Tests
- 🔄 Error handling and edge cases
- 🔄 Performance with large files
- 🔄 Cross-platform compatibility
- 🔄 Memory usage and cleanup

## 🎉 Success Criteria

A test is considered successful when:
- ✅ **No exceptions** are raised
- ✅ **Expected output** is displayed
- ✅ **Success message** is shown
- ✅ **All assertions** pass
- ✅ **Files are created/modified** as expected

---

**Happy Testing!** 🚀

For questions about specific tests, check the individual test files or contact the development team.