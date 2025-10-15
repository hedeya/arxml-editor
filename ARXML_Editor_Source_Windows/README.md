# ARXML Editor

A professional AUTOSAR XML (ARXML) editor with dynamic schema detection, validation, and comprehensive editing capabilities.

## 🚀 Features

### Core Functionality
- **Dynamic Schema Detection** - Automatically detects AUTOSAR schema version from ARXML files
- **Schema Validation** - Validates ARXML files against detected schemas
- **Multi-Format Support** - Handles both standard ARXML and ECUC configuration files
- **Clean Tree Interface** - Shows only sections with actual content

### Editing Capabilities
- **Add Elements** - Right-click context menu to add new components, interfaces, compositions
- **Remove Elements** - Delete elements with confirmation dialog
- **Modify Properties** - Real-time editing of element properties
- **Save Functionality** - Save and Save As with proper XML generation

### Visualization
- **Diagram View** - Comprehensive file information and statistics
- **Element Statistics** - Detailed breakdown of all elements
- **Visual Diagrams** - Component diagrams for software components
- **Interactive Navigation** - Zoom controls and scrollable content

### Supported File Types
- **Standard ARXML Files** - Software components, compositions, interfaces
- **ECUC Files** - ECU configuration files with hierarchical structure
- **Schema Versions** - AUTOSAR 4.6.0, 4.7.0+ (auto-detected)

## 📋 Requirements

- Python 3.8+
- PyQt6
- lxml
- xmlschema

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hedeya/arxml-editor.git
   cd arxml-editor
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## 🎮 Usage

### Opening Files
1. Launch the application
2. Click **File → Open** or press `Ctrl+O`
3. Select your ARXML file
4. The application will automatically detect the schema version

### Editing Elements
1. **Add Elements:** Right-click on tree sections and select "Add [Element Type]"
2. **Edit Properties:** Select an element and modify properties in the Properties tab
3. **Delete Elements:** Right-click on elements and select "Delete"
4. **Save Changes:** Use File → Save or `Ctrl+S`

### Viewing Information
1. **Tree Navigator:** Browse ARXML structure in the left panel
2. **Properties:** View and edit element properties in the Properties tab
3. **Validation:** Check validation results in the Validation tab
4. **Diagram:** View file statistics and visual diagrams in the Diagram tab

## 📁 Project Structure

```
arxml-editor/
├── src/
│   ├── core/
│   │   ├── models/          # AUTOSAR element models
│   │   └── services/        # Core services (parsing, validation, etc.)
│   └── ui/
│       ├── views/           # UI components
│       └── main_window.py   # Main application window
├── schemas/                 # AUTOSAR XSD schemas
├── sample.arxml            # Sample ARXML file
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔧 Development

### Architecture
The application follows a clean architecture pattern:
- **Models** - AUTOSAR element data structures
- **Services** - Business logic (parsing, validation, commands)
- **Views** - UI components and user interaction
- **Application** - Main controller coordinating all components

### Key Components
- **ARXMLDocument** - Main document model with editing capabilities
- **SchemaService** - Dynamic schema detection and validation
- **ValidationService** - Real-time validation engine
- **TreeNavigator** - Hierarchical element browser
- **PropertyEditor** - Element property editor
- **DiagramView** - File information and statistics

## 🎯 Supported AUTOSAR Elements

- **Software Component Types** (Application, Atomic, Composition)
- **Port Interfaces** (Sender-Receiver, Service)
- **Port Prototypes** (Provider, Requirer, Provider-Requirer)
- **Data Elements** with type information
- **ECUC Elements** (Modules, Containers, Parameters)

## 📊 Validation Features

- **Schema Compliance** - Validates against detected AUTOSAR schema
- **Structure Validation** - Checks XML structure and element hierarchy
- **Content Validation** - Validates element content and attributes
- **Real-time Feedback** - Shows validation results immediately

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **hedeya** - Project maintainer and lead developer

## 🆘 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/hedeya/arxml-editor/issues) page
2. Create a new issue with detailed description
3. Contact the development team

## 🎉 Acknowledgments

- AUTOSAR consortium for the XML schema standards
- PyQt6 team for the excellent GUI framework
- Python community for the robust XML processing libraries

---

**Happy ARXML editing!** 🚀