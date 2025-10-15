# ARXML Editor API Documentation

## Core Modules

### Application Module
The main application controller that orchestrates the entire ARXML editor.

### ARXML Document Model
Handles the in-memory representation of ARXML documents and manages modifications.

### ARXML Parser
Parses ARXML files into the internal document model.

### Schema Service
Manages AUTOSAR schema detection and validation.

### Validation Service
Provides validation functionality for ARXML documents.

## UI Modules

### Main Window
The main application window that coordinates all UI components.

### Tree Navigator
Displays the hierarchical structure of ARXML documents.

### Property Editor
Allows editing of selected element properties.

### Validation List
Shows validation errors and warnings.

### Diagram View
Displays visual representation of ARXML structure.

## Usage Examples

### Loading an ARXML File
```python
from src.core.application import Application

app = Application()
document = app.load_document("path/to/file.arxml")
```

### Validating a Document
```python
validation_service = ValidationService()
errors = validation_service.validate_document(document)
```

### Saving a Document
```python
document.save_as("path/to/output.arxml")
```
