"""
Property Editor View
Property editor for selected AUTOSAR elements
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QComboBox, QCheckBox, QSpinBox, QDoubleSpinBox,
    QGroupBox, QFormLayout, QScrollArea, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from ...core.models.autosar_elements import (
    SwComponentType, Composition, PortInterface, PortPrototype,
    SwComponentTypeCategory, PortType, DataType, DataElement
)

class PropertyEditor(QWidget):
    """Property editor for AUTOSAR elements"""
    
    # Signals
    property_changed = pyqtSignal(object, str, object)
    
    def __init__(self, app):
        super().__init__()
        self.app = app
        self._current_element = None
        self._property_widgets = {}
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Setup the property editor UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Title
        self.title_label = QLabel("Properties")
        self.title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(self.title_label)
        
        # Scroll area for properties
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Properties widget
        self.properties_widget = QWidget()
        self.properties_layout = QVBoxLayout(self.properties_widget)
        self.properties_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area.setWidget(self.properties_widget)
        layout.addWidget(scroll_area)
        
        # Initially show empty state
        self._show_empty_state()
    
    def _connect_signals(self):
        """Connect signals"""
        pass
    
    def _show_empty_state(self):
        """Show empty state when no element is selected"""
        self._clear_properties()
        
        empty_label = QLabel("No element selected")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_label.setStyleSheet("color: gray; font-style: italic;")
        self.properties_layout.addWidget(empty_label)
    
    def _clear_properties(self):
        """Clear all property widgets"""
        for i in reversed(range(self.properties_layout.count())):
            child = self.properties_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        self._property_widgets.clear()
    
    def clear(self):
        """Clear the property editor and show empty state"""
        # Save current widget values before clearing
        self._save_current_widget_values()
        self._current_element = None
        self._show_empty_state()
    
    def _save_current_widget_values(self):
        """Save current widget values to the element before switching"""
        if not self._current_element or not self._property_widgets:
            return
        
        try:
            # Save values from all property widgets
            for property_name, widget in self._property_widgets.items():
                if hasattr(widget, 'text'):
                    # QLineEdit, QTextEdit
                    if hasattr(widget, 'toPlainText'):
                        # QTextEdit
                        value = widget.toPlainText()
                    else:
                        # QLineEdit
                        value = widget.text()
                    
                    # Update the element (handle both objects and dictionaries)
                    if isinstance(self._current_element, dict):
                        # Dictionary (ECUC elements)
                        self._current_element[property_name] = value
                    elif hasattr(self._current_element, property_name):
                        # Object with attributes
                        setattr(self._current_element, property_name, value)
                    
                    # Mark document as modified
                    if hasattr(self.app, 'current_document') and self.app.current_document:
                        self.app.current_document.set_modified(True)
                
                elif hasattr(widget, 'isChecked'):
                    # QCheckBox
                    value = widget.isChecked()
                    if isinstance(self._current_element, dict):
                        # Dictionary (ECUC elements)
                        self._current_element[property_name] = value
                    elif hasattr(self._current_element, property_name):
                        # Object with attributes
                        setattr(self._current_element, property_name, value)
                    
                    if hasattr(self.app, 'current_document') and self.app.current_document:
                        self.app.current_document.set_modified(True)
                
                elif hasattr(widget, 'value'):
                    # QSpinBox, QDoubleSpinBox
                    value = widget.value()
                    if isinstance(self._current_element, dict):
                        # Dictionary (ECUC elements)
                        self._current_element[property_name] = value
                    elif hasattr(self._current_element, property_name):
                        # Object with attributes
                        setattr(self._current_element, property_name, value)
                    
                    if hasattr(self.app, 'current_document') and self.app.current_document:
                        self.app.current_document.set_modified(True)
                
                elif hasattr(widget, 'currentText'):
                    # QComboBox
                    value = widget.currentText()
                    if isinstance(self._current_element, dict):
                        # Dictionary (ECUC elements)
                        self._current_element[property_name] = value
                    elif hasattr(self._current_element, property_name):
                        # Object with attributes - Handle enum types
                        if property_name == 'port_type' and hasattr(self._current_element, 'port_type'):
                            from ...core.models.autosar_elements import PortType
                            try:
                                enum_value = PortType(value)
                                setattr(self._current_element, property_name, enum_value)
                                if hasattr(self.app, 'current_document') and self.app.current_document:
                                    self.app.current_document.set_modified(True)
                            except ValueError:
                                pass
                        elif property_name == 'data_type' and hasattr(self._current_element, 'data_type'):
                            from ...core.models.autosar_elements import DataType
                            try:
                                enum_value = DataType(value)
                                setattr(self._current_element, property_name, enum_value)
                                if hasattr(self.app, 'current_document') and self.app.current_document:
                                    self.app.current_document.set_modified(True)
                            except ValueError:
                                pass
                        else:
                            setattr(self._current_element, property_name, value)
                            if hasattr(self.app, 'current_document') and self.app.current_document:
                                self.app.current_document.set_modified(True)
        
        except Exception as e:
            print(f"Error saving widget values: {e}")
    
    def set_element(self, element):
        """Set the current element for editing"""
        # Save current widget values before switching
        self._save_current_widget_values()
        
        self._current_element = element
        self._clear_properties()
        
        if element is None:
            self._show_empty_state()
            return
        
        # Update title
        element_type = type(element).__name__
        self.title_label.setText(f"Properties - {element_type}")
        
        # Create property widgets based on element type
        if isinstance(element, SwComponentType):
            self._create_sw_component_type_properties(element)
        elif isinstance(element, Composition):
            self._create_composition_properties(element)
        elif isinstance(element, PortInterface):
            self._create_port_interface_properties(element)
        elif isinstance(element, PortPrototype):
            self._create_port_prototype_properties(element)
        elif isinstance(element, DataElement):
            self._create_data_element_properties(element)
        elif isinstance(element, dict):
            self._create_ecuc_element_properties(element)
        else:
            self._show_empty_state()
    
    def _create_sw_component_type_properties(self, component_type: SwComponentType):
        """Create properties for software component type"""
        # Basic properties group
        basic_group = QGroupBox("Basic Properties")
        basic_layout = QFormLayout(basic_group)
        
        # Short name
        short_name_edit = QLineEdit(component_type.short_name)
        short_name_edit.textChanged.connect(
            lambda text: self._on_property_changed(component_type, "short_name", text)
        )
        basic_layout.addRow("Short Name:", short_name_edit)
        self._property_widgets["short_name"] = short_name_edit
        
        # Description
        desc_edit = QTextEdit(component_type.desc or "")
        desc_edit.setMaximumHeight(80)
        desc_edit.textChanged.connect(
            lambda: self._on_property_changed(component_type, "desc", desc_edit.toPlainText())
        )
        basic_layout.addRow("Description:", desc_edit)
        self._property_widgets["desc"] = desc_edit
        
        # Category (read-only)
        category_label = QLabel(component_type.category.value)
        basic_layout.addRow("Category:", category_label)
        
        self.properties_layout.addWidget(basic_group)
        
        # Ports group
        ports_group = QGroupBox("Ports")
        ports_layout = QVBoxLayout(ports_group)
        
        if component_type.ports:
            for i, port in enumerate(component_type.ports):
                port_widget = self._create_port_widget(port, i)
                ports_layout.addWidget(port_widget)
        else:
            no_ports_label = QLabel("No ports defined")
            no_ports_label.setStyleSheet("color: gray; font-style: italic;")
            ports_layout.addWidget(no_ports_label)
        
        self.properties_layout.addWidget(ports_group)
    
    def _create_composition_properties(self, composition: Composition):
        """Create properties for composition"""
        # Basic properties group
        basic_group = QGroupBox("Basic Properties")
        basic_layout = QFormLayout(basic_group)
        
        # Short name
        short_name_edit = QLineEdit(composition.short_name)
        short_name_edit.textChanged.connect(
            lambda text: self._on_property_changed(composition, "short_name", text)
        )
        basic_layout.addRow("Short Name:", short_name_edit)
        self._property_widgets["short_name"] = short_name_edit
        
        # Description
        desc_edit = QTextEdit(composition.desc or "")
        desc_edit.setMaximumHeight(80)
        desc_edit.textChanged.connect(
            lambda: self._on_property_changed(composition, "desc", desc_edit.toPlainText())
        )
        basic_layout.addRow("Description:", desc_edit)
        self._property_widgets["desc"] = desc_edit
        
        self.properties_layout.addWidget(basic_group)
        
        # Component types group
        components_group = QGroupBox("Component Types")
        components_layout = QVBoxLayout(components_group)
        
        if composition.component_types:
            for component_type in composition.component_types:
                comp_label = QLabel(f"• {component_type.short_name} ({component_type.category.value})")
                components_layout.addWidget(comp_label)
        else:
            no_components_label = QLabel("No component types defined")
            no_components_label.setStyleSheet("color: gray; font-style: italic;")
            components_layout.addWidget(no_components_label)
        
        self.properties_layout.addWidget(components_group)
    
    def _create_port_interface_properties(self, port_interface: PortInterface):
        """Create properties for port interface"""
        # Basic properties group
        basic_group = QGroupBox("Basic Properties")
        basic_layout = QFormLayout(basic_group)
        
        # Short name
        short_name_edit = QLineEdit(port_interface.short_name)
        short_name_edit.textChanged.connect(
            lambda text: self._on_property_changed(port_interface, "short_name", text)
        )
        basic_layout.addRow("Short Name:", short_name_edit)
        self._property_widgets["short_name"] = short_name_edit
        
        # Description
        desc_edit = QTextEdit(port_interface.desc or "")
        desc_edit.setMaximumHeight(80)
        desc_edit.textChanged.connect(
            lambda: self._on_property_changed(port_interface, "desc", desc_edit.toPlainText())
        )
        basic_layout.addRow("Description:", desc_edit)
        self._property_widgets["desc"] = desc_edit
        
        # Is service
        is_service_check = QCheckBox()
        is_service_check.setChecked(port_interface.is_service)
        is_service_check.toggled.connect(
            lambda checked: self._on_property_changed(port_interface, "is_service", checked)
        )
        basic_layout.addRow("Is Service:", is_service_check)
        self._property_widgets["is_service"] = is_service_check
        
        self.properties_layout.addWidget(basic_group)
        
        # Data elements group
        data_elements_group = QGroupBox("Data Elements")
        data_elements_layout = QVBoxLayout(data_elements_group)
        
        if port_interface.data_elements:
            for data_element in port_interface.data_elements:
                data_widget = self._create_data_element_widget(data_element)
                data_elements_layout.addWidget(data_widget)
        else:
            no_data_label = QLabel("No data elements defined")
            no_data_label.setStyleSheet("color: gray; font-style: italic;")
            data_elements_layout.addWidget(no_data_label)
        
        self.properties_layout.addWidget(data_elements_group)
    
    def _create_port_prototype_properties(self, port: PortPrototype):
        """Create properties for port prototype"""
        # Basic properties group
        basic_group = QGroupBox("Basic Properties")
        basic_layout = QFormLayout(basic_group)
        
        # Short name
        short_name_edit = QLineEdit(port.short_name)
        short_name_edit.textChanged.connect(
            lambda text: self._on_property_changed(port, "short_name", text)
        )
        basic_layout.addRow("Short Name:", short_name_edit)
        self._property_widgets["short_name"] = short_name_edit
        
        # Description
        desc_edit = QTextEdit(port.desc or "")
        desc_edit.setMaximumHeight(80)
        desc_edit.textChanged.connect(
            lambda: self._on_property_changed(port, "desc", desc_edit.toPlainText())
        )
        basic_layout.addRow("Description:", desc_edit)
        self._property_widgets["desc"] = desc_edit
        
        # Port type
        port_type_combo = QComboBox()
        for port_type in PortType:
            port_type_combo.addItem(port_type.value, port_type)
        port_type_combo.setCurrentText(port.port_type.value)
        port_type_combo.currentTextChanged.connect(
            lambda text: self._on_property_changed(port, "port_type", PortType(text))
        )
        basic_layout.addRow("Port Type:", port_type_combo)
        self._property_widgets["port_type"] = port_type_combo
        
        # Interface reference
        interface_ref_edit = QLineEdit(port.interface_ref or "")
        interface_ref_edit.textChanged.connect(
            lambda text: self._on_property_changed(port, "interface_ref", text)
        )
        basic_layout.addRow("Interface Ref:", interface_ref_edit)
        self._property_widgets["interface_ref"] = interface_ref_edit
        
        self.properties_layout.addWidget(basic_group)
    
    def _create_data_element_properties(self, data_element: DataElement):
        """Create properties for data element"""
        # Basic properties group
        basic_group = QGroupBox("Basic Properties")
        basic_layout = QFormLayout(basic_group)
        
        # Short name
        short_name_edit = QLineEdit(data_element.short_name)
        short_name_edit.textChanged.connect(
            lambda text: self._on_property_changed(data_element, "short_name", text)
        )
        basic_layout.addRow("Short Name:", short_name_edit)
        self._property_widgets["short_name"] = short_name_edit
        
        # Description
        desc_edit = QTextEdit(data_element.desc or "")
        desc_edit.setMaximumHeight(80)
        desc_edit.textChanged.connect(
            lambda: self._on_property_changed(data_element, "desc", desc_edit.toPlainText())
        )
        basic_layout.addRow("Description:", desc_edit)
        self._property_widgets["desc"] = desc_edit
        
        # Data type
        data_type_combo = QComboBox()
        for data_type in DataType:
            data_type_combo.addItem(data_type.value, data_type)
        data_type_combo.setCurrentText(data_element.data_type.value)
        data_type_combo.currentTextChanged.connect(
            lambda text: self._on_property_changed(data_element, "data_type", DataType(text))
        )
        basic_layout.addRow("Data Type:", data_type_combo)
        self._property_widgets["data_type"] = data_type_combo
        
        # Is array
        is_array_check = QCheckBox()
        is_array_check.setChecked(data_element.is_array)
        is_array_check.toggled.connect(
            lambda checked: self._on_property_changed(data_element, "is_array", checked)
        )
        basic_layout.addRow("Is Array:", is_array_check)
        self._property_widgets["is_array"] = is_array_check
        
        # Array size
        if data_element.is_array:
            array_size_spin = QSpinBox()
            array_size_spin.setRange(1, 10000)
            array_size_spin.setValue(data_element.array_size or 1)
            array_size_spin.valueChanged.connect(
                lambda value: self._on_property_changed(data_element, "array_size", value)
            )
            basic_layout.addRow("Array Size:", array_size_spin)
            self._property_widgets["array_size"] = array_size_spin
        
        # Unit
        unit_edit = QLineEdit(data_element.unit or "")
        unit_edit.textChanged.connect(
            lambda text: self._on_property_changed(data_element, "unit", text)
        )
        basic_layout.addRow("Unit:", unit_edit)
        self._property_widgets["unit"] = unit_edit
        
        # Min value
        min_value_spin = QDoubleSpinBox()
        min_value_spin.setRange(-999999.0, 999999.0)
        min_value_spin.setValue(data_element.min_value or 0.0)
        min_value_spin.valueChanged.connect(
            lambda value: self._on_property_changed(data_element, "min_value", value)
        )
        basic_layout.addRow("Min Value:", min_value_spin)
        self._property_widgets["min_value"] = min_value_spin
        
        # Max value
        max_value_spin = QDoubleSpinBox()
        max_value_spin.setRange(-999999.0, 999999.0)
        max_value_spin.setValue(data_element.max_value or 0.0)
        max_value_spin.valueChanged.connect(
            lambda value: self._on_property_changed(data_element, "max_value", value)
        )
        basic_layout.addRow("Max Value:", max_value_spin)
        self._property_widgets["max_value"] = max_value_spin
        
        self.properties_layout.addWidget(basic_group)
    
    def _create_port_widget(self, port: PortPrototype, index: int):
        """Create widget for port in component type properties"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Port name
        port_label = QLabel(f"Port {index + 1}: {port.short_name}")
        port_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(port_label)
        
        # Port type
        type_label = QLabel(f"({port.port_type.value})")
        type_label.setStyleSheet("color: gray;")
        layout.addWidget(type_label)
        
        layout.addStretch()
        
        return widget
    
    def _create_data_element_widget(self, data_element: DataElement):
        """Create widget for data element in port interface properties"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Data element name
        data_label = QLabel(f"• {data_element.short_name}")
        data_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(data_label)
        
        # Data type
        type_label = QLabel(f"({data_element.data_type.value})")
        type_label.setStyleSheet("color: gray;")
        layout.addWidget(type_label)
        
        layout.addStretch()
        
        return widget
    
    def _create_ecuc_element_properties(self, ecuc_element: dict):
        """Create properties for ECUC element"""
        # Basic properties group
        basic_group = QGroupBox("Basic Properties")
        basic_layout = QFormLayout(basic_group)
        
        # Type
        type_label = QLabel(ecuc_element.get('type', 'Unknown'))
        basic_layout.addRow("Type:", type_label)
        
        # Short name
        short_name_edit = QLineEdit(ecuc_element.get('short_name', ''))
        short_name_edit.textChanged.connect(
            lambda text: self._on_ecuc_property_changed(ecuc_element, "short_name", text)
        )
        basic_layout.addRow("Short Name:", short_name_edit)
        self._property_widgets["short_name"] = short_name_edit
        
        # UUID (if available)
        if 'uuid' in ecuc_element:
            uuid_edit = QLineEdit(ecuc_element['uuid'])
            uuid_edit.setReadOnly(True)
            basic_layout.addRow("UUID:", uuid_edit)
        
        self.properties_layout.addWidget(basic_group)
        
        # Containers group
        if ecuc_element.get('containers'):
            containers_group = QGroupBox("Containers")
            containers_layout = QVBoxLayout(containers_group)
            
            for container in ecuc_element['containers']:
                container_widget = self._create_ecuc_container_widget(container)
                containers_layout.addWidget(container_widget)
            
            self.properties_layout.addWidget(containers_group)
    
    def _create_ecuc_container_widget(self, container: dict):
        """Create widget for ECUC container"""
        container_group = QGroupBox(f"Container: {container.get('short_name', 'Unknown')}")
        container_layout = QFormLayout(container_group)
        
        # Short name
        short_name_edit = QLineEdit(container.get('short_name', ''))
        short_name_edit.textChanged.connect(
            lambda text: self._on_ecuc_container_property_changed(container, "short_name", text)
        )
        container_layout.addRow("Short Name:", short_name_edit)
        
        # Definition ref
        if container.get('definition_ref'):
            def_ref_edit = QLineEdit(container['definition_ref'])
            def_ref_edit.setReadOnly(True)
            container_layout.addRow("Definition Ref:", def_ref_edit)
        
        # Parameters
        if container.get('parameters'):
            params_group = QGroupBox("Parameters")
            params_layout = QVBoxLayout(params_group)
            
            for param in container['parameters']:
                param_widget = self._create_ecuc_parameter_widget(param)
                params_layout.addWidget(param_widget)
            
            container_layout.addRow(params_group)
        
        return container_group
    
    def _create_ecuc_parameter_widget(self, param: dict):
        """Create widget for ECUC parameter"""
        param_group = QGroupBox(f"Parameter: {param.get('short_name', 'Unknown')}")
        param_layout = QFormLayout(param_group)
        
        # Short name
        short_name_edit = QLineEdit(param.get('short_name', ''))
        short_name_edit.textChanged.connect(
            lambda text: self._on_ecuc_parameter_property_changed(param, "short_name", text)
        )
        param_layout.addRow("Short Name:", short_name_edit)
        
        # Definition ref
        if param.get('definition_ref'):
            def_ref_edit = QLineEdit(param['definition_ref'])
            def_ref_edit.setReadOnly(True)
            param_layout.addRow("Definition Ref:", def_ref_edit)
        
        # Value
        if param.get('value'):
            value_edit = QLineEdit(param['value'])
            value_edit.textChanged.connect(
                lambda text: self._on_ecuc_parameter_property_changed(param, "value", text)
            )
            param_layout.addRow("Value:", value_edit)
        
        return param_group
    
    def _on_property_changed(self, element, property_name: str, new_value):
        """Handle property change"""
        # Store old value for undo
        old_value = getattr(element, property_name)
        
        # Update element
        setattr(element, property_name, new_value)
        
        # Mark document as modified
        if hasattr(self.app, 'current_document') and self.app.current_document:
            self.app.current_document.set_modified(True)
        
        # Emit signal
        self.property_changed.emit(element, property_name, new_value)
    
    def _on_ecuc_property_changed(self, ecuc_element: dict, property_name: str, new_value):
        """Handle ECUC element property change"""
        # Update element
        ecuc_element[property_name] = new_value
        
        # Mark document as modified
        if hasattr(self.app, 'current_document') and self.app.current_document:
            self.app.current_document.set_modified(True)
        
        # Emit signal
        self.property_changed.emit(ecuc_element, property_name, new_value)
    
    def _on_ecuc_container_property_changed(self, container: dict, property_name: str, new_value):
        """Handle ECUC container property change"""
        # Update container
        container[property_name] = new_value
        
        # Mark document as modified
        if hasattr(self.app, 'current_document') and self.app.current_document:
            self.app.current_document.set_modified(True)
        
        # Emit signal
        self.property_changed.emit(container, property_name, new_value)
    
    def _on_ecuc_parameter_property_changed(self, parameter: dict, property_name: str, new_value):
        """Handle ECUC parameter property change"""
        # Update parameter
        parameter[property_name] = new_value
        
        # Mark document as modified
        if hasattr(self.app, 'current_document') and self.app.current_document:
            self.app.current_document.set_modified(True)
        
        # Emit signal
        self.property_changed.emit(parameter, property_name, new_value)
    
    def clear(self):
        """Clear the property editor"""
        self.set_element(None)