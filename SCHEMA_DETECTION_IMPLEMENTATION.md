# Dynamic Schema Version Detection and Validation Implementation

## Overview

This implementation adds dynamic schema version detection and validation capabilities to the ARXML Editor Python project. The system automatically detects the AUTOSAR schema version from ARXML files and validates them according to the appropriate schema.

## Features Implemented

### 1. Dynamic Schema Version Detection

- **Multiple Detection Methods**: The system uses multiple methods to detect schema versions:
  - Namespace URI mapping (`http://autosar.org/schema/r4.0` → `4.7.0`)
  - XSI schema location parsing (`AUTOSAR_4-7-0.xsd` → `4.7.0`)
  - Version-specific element detection
  - AUTOSAR version attribute parsing

- **File and Content Support**: Detection works with both file paths and XML content strings

### 2. Schema Loading and Management

- **Dynamic Schema Loading**: Automatically loads the appropriate XSD schema based on detected version
- **Fallback Schema**: Creates basic validation schemas when XSD files are not available
- **Multiple Version Support**: Supports AUTOSAR versions 4.3.0 through 4.7.0

### 3. Enhanced Validation

- **Schema-Based Validation**: Validates ARXML files against the detected schema version
- **Integration with Existing Validation**: Works alongside the existing validation service
- **Real-time Validation**: Provides immediate feedback on schema compliance

### 4. Error Handling

- **Comprehensive Error Handling**: Handles various error scenarios:
  - File not found errors
  - Invalid XML syntax
  - Permission denied errors
  - Empty content errors
  - Unicode decoding errors

## Files Modified

### Core Services

1. **`src/core/services/schema_service.py`**
   - Added dynamic schema detection methods
   - Enhanced schema loading with version detection
   - Added namespace to version mapping
   - Improved error handling

2. **`src/core/services/arxml_parser.py`**
   - Integrated with schema service for automatic detection
   - Updated namespace handling based on detected version
   - Enhanced validation integration

3. **`src/core/services/validation_service.py`**
   - Added schema compliance validation
   - Integrated with schema service for validation

4. **`src/core/application.py`**
   - Updated to use integrated services
   - Enhanced document loading with schema detection

5. **`src/core/models/arxml_document.py`**
   - Added `load_from_element` method for parser integration
   - Enhanced schema version detection

### Schema Files

6. **`schemas/autosar_4-7-0.xsd`**
   - Basic XSD schema for AUTOSAR 4.7.0 validation
   - Includes common AUTOSAR elements

7. **`schemas/autosar_4-6-0.xsd`**
   - Basic XSD schema for AUTOSAR 4.6.0 validation

## Usage Examples

### Basic Schema Detection

```python
from src.core.services.schema_service import SchemaService

# Initialize schema service
schema_service = SchemaService()

# Detect version from file
version = schema_service.detect_schema_version_from_file("sample.arxml")
print(f"Detected version: {version}")

# Auto-detect and set version
success = schema_service.auto_detect_and_set_version(file_path="sample.arxml")
```

### Schema Validation

```python
# Validate ARXML file against detected schema
validation_errors = schema_service.validate_arxml_file("sample.arxml")
if validation_errors:
    for error in validation_errors:
        print(f"Validation error: {error}")
else:
    print("No validation errors found")
```

### Parser Integration

```python
from src.core.services.arxml_parser import ARXMLParser

# Initialize parser with schema service
parser = ARXMLParser(schema_service)

# Parse file with automatic schema detection
root = parser.parse_arxml_file("sample.arxml")
```

## Testing

The implementation includes comprehensive tests:

- **`test_comprehensive_schema.py`**: Full test suite covering all functionality
- **`test_schema_detection.py`**: Basic detection and validation tests

Run tests with:
```bash
python3 test_comprehensive_schema.py
```

## Benefits

1. **Automatic Detection**: No manual schema version selection required
2. **Accurate Validation**: Validates against the correct schema version
3. **Error Prevention**: Catches schema compliance issues early
4. **User-Friendly**: Seamless integration with existing workflow
5. **Extensible**: Easy to add support for new AUTOSAR versions

## Future Enhancements

1. **Additional Schema Files**: Add more comprehensive XSD files for all versions
2. **Version-Specific Validation**: Implement version-specific validation rules
3. **Schema Migration**: Add tools for migrating between schema versions
4. **Performance Optimization**: Optimize schema loading for large files
5. **Advanced Error Reporting**: Enhanced error messages with line numbers and suggestions

## Dependencies

- `lxml`: XML parsing and processing
- `xmlschema`: XSD schema validation
- `PyQt6`: GUI framework (for signals)

The implementation is fully integrated with the existing ARXML Editor architecture and maintains backward compatibility.