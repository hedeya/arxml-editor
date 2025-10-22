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
import os
from datetime import datetime

class PropertyEditor(QWidget):
    """Property editor for AUTOSAR elements"""
    
    # Signals
    property_changed = pyqtSignal(object, str, object)
    
    def __init__(self, app):
        super().__init__()
        self.app = app
        self._current_element = None
        self._original_element = None  # Store reference to original element in document
        self._property_widgets = {}
        self._setup_ui()
        self._connect_signals()
        
        # Enable monitoring
        self._monitoring_enabled = True
        self._monitor_log("PropertyEditor initialized")
    
    def _monitor_log(self, message):
        """Log property changes for live debugging"""
        if not self._monitoring_enabled:
            return
        try:
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            log_file = "/tmp/arxml_property_monitor.log"
            with open(log_file, "a") as f:
                f.write(f"PROPERTY_MONITOR [{timestamp}] {message}\n")
        except:
            pass
    
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
        # Save current values before clearing
        self._save_current_widget_values()
        self._current_element = None
        self._show_empty_state()
    
    def _save_current_widget_values(self):
        """Save current widget values to the element before switching"""
        if not self._current_element:
            return
        
        # If no property widgets exist, there's nothing to save
        if not self._property_widgets:
            return
        
        try:
            print(f"[PropertyEditor] _save_current_widget_values: saving {len(self._property_widgets)} properties")
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
                        # Dictionary (ECUC elements) - should already be resolved, but double-check
                        resolved = self._resolve_to_document(self._current_element)
                        target_element = resolved if resolved is not None else self._current_element
                        
                        # Store old value for comparison
                        old_value = target_element.get(property_name, '')
                        target_element[property_name] = value
                        
                        print(f"[PropertyEditor] Saved {property_name}: '{old_value}' -> '{value}' on element id={id(target_element)} short_name='{target_element.get('short_name')}'")
                    elif hasattr(self._current_element, property_name):
                        # Object with attributes
                        old_value = getattr(self._current_element, property_name, '')
                        setattr(self._current_element, property_name, value)
                        print(f"[PropertyEditor] Saved {property_name}: '{old_value}' -> '{value}' on object {type(self._current_element).__name__}")
                    
                    # Mark document as modified
                    if hasattr(self.app, 'current_document') and self.app.current_document:
                        self.app.current_document.set_modified(True)
                
                elif hasattr(widget, 'isChecked'):
                    # QCheckBox
                    value = widget.isChecked()
                    if isinstance(self._current_element, dict):
                        # Dictionary (ECUC elements) - resolve to document instance
                        resolved = self._resolve_to_document(self._current_element)
                        if resolved is not None:
                            resolved[property_name] = value
                        else:
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
                        # Dictionary (ECUC elements) - resolve to document instance
                        resolved = self._resolve_to_document(self._current_element)
                        if resolved is not None:
                            resolved[property_name] = value
                        else:
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
                        # Dictionary (ECUC elements) - resolve to document instance
                        resolved = self._resolve_to_document(self._current_element)
                        if resolved is not None:
                            resolved[property_name] = value
                        else:
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
        # Resolve the element first to ensure consistency
        resolved_element = element
        if isinstance(element, dict) and hasattr(self.app, 'current_document') and self.app.current_document:
            resolved_instance = self._resolve_to_document(element)
            if resolved_instance is not None:
                resolved_element = resolved_instance
                print(f"[PropertyEditor] Resolved element id={id(element)} to document instance id={id(resolved_element)}")
        
        # If setting the same resolved element, no need to recreate widgets
        if self._current_element is resolved_element:
            print(f"[PropertyEditor] Same element, skipping recreation")
            return
        
        # Save current widget values before switching to ensure persistence
        if self._current_element is not None and self._property_widgets:
            try:
                if isinstance(self._current_element, dict):
                    print(f"[PropertyEditor] Saving values for element id={id(self._current_element)} short_name='{self._current_element.get('short_name')}'")
                    self._monitor_log(f"SAVE_START: element id={id(self._current_element)} short_name='{self._current_element.get('short_name')}'")
                else:
                    print(f"[PropertyEditor] Saving values for element type={type(self._current_element).__name__}")
                    self._monitor_log(f"SAVE_START: element type={type(self._current_element).__name__}")
            except Exception:
                pass
            self._save_current_widget_values()
        
        # Log the incoming element
        try:
            if isinstance(element, dict):
                self._monitor_log(f"SET_ELEMENT: id={id(element)} short_name='{element.get('short_name')}' type='{element.get('type')}'")
            else:
                self._monitor_log(f"SET_ELEMENT: element type={type(element).__name__}")
        except Exception:
            pass
        
        # Clear properties and set the current element to the resolved one
        self._clear_properties()
        self._current_element = resolved_element
        
        if element is None:
            self._show_empty_state()
            return

        # If this is an ECUC dict, try to find and store a reference to the
        # corresponding top-level element in the current document so edits
        # can be applied to the document model even if the editor received
        # a copy or a nested dict.
        self._original_element = None
        if isinstance(element, dict) and hasattr(self.app, 'current_document') and self.app.current_document:
            for doc_elem in self.app.current_document.ecuc_elements:
                # If the passed element is the top-level element itself
                if doc_elem is element:
                    self._original_element = doc_elem
                    break
                # Otherwise search nested containers/parameters for identity or best-match
                found = self._find_dict_in(doc_elem, element)
                if found is not None:
                    # store the top-level document element as the original
                    self._original_element = doc_elem
                    break

        
        # Update title
        element_type = type(element).__name__
        self.title_label.setText(f"Properties - {element_type}")
        
        # Set original element reference for ECUC elements
        if isinstance(self._current_element, dict):
            for doc_elem in self.app.current_document.ecuc_elements:
                if doc_elem is self._current_element:
                    self._original_element = doc_elem
                    break
                if self._find_dict_in(doc_elem, self._current_element) is not None:
                    self._original_element = doc_elem
                    break
        
        # Use the current element (which is already resolved) for widgets
        element_for_widgets = self._current_element

        # Debug: log final element being used for widgets and verify persistence
        try:
            if isinstance(element_for_widgets, dict):
                print(f"[PropertyEditor] Creating widgets for element id={id(element_for_widgets)} short_name='{element_for_widgets.get('short_name')}' type='{element_for_widgets.get('type')}'")
                self._verify_element_persistence(element_for_widgets)
            else:
                print(f"[PropertyEditor] Creating widgets for element id={id(element_for_widgets)} type='{type(element_for_widgets).__name__}'")
        except Exception:
            pass

        # Create property widgets based on element type
        if isinstance(element_for_widgets, SwComponentType):
            self._create_sw_component_type_properties(element_for_widgets)
        elif isinstance(element_for_widgets, Composition):
            self._create_composition_properties(element_for_widgets)
        elif isinstance(element_for_widgets, PortInterface):
            self._create_port_interface_properties(element_for_widgets)
        elif isinstance(element_for_widgets, PortPrototype):
            self._create_port_prototype_properties(element_for_widgets)
        elif isinstance(element_for_widgets, DataElement):
            self._create_data_element_properties(element_for_widgets)
        elif isinstance(element_for_widgets, dict):
            self._create_ecuc_element_properties(element_for_widgets)
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
        try:
            print(f"[PropertyEditor] Creating ECUC element widgets for id={id(ecuc_element)} short_name='{ecuc_element.get('short_name')}' type='{ecuc_element.get('type')}' containers={len(ecuc_element.get('containers', []))}")
            
            # Verify this is the document instance
            if hasattr(self.app, 'current_document') and self.app.current_document:
                is_doc_instance = any(doc_elem is ecuc_element for doc_elem in self.app.current_document.ecuc_elements)
                is_nested_instance = any(self._find_dict_in(doc_elem, ecuc_element) is not None for doc_elem in self.app.current_document.ecuc_elements)
                print(f"[PropertyEditor] Element is document instance: {is_doc_instance}, is nested in document: {is_nested_instance}")
        except Exception as e:
            print(f"[PropertyEditor] Error in ECUC element debug: {e}")
        # Basic properties group
        basic_group = QGroupBox("Basic Properties")
        basic_layout = QFormLayout(basic_group)
        
        # Type
        type_label = QLabel(ecuc_element.get('type', 'Unknown'))
        basic_layout.addRow("Type:", type_label)
        
        # Short name
        short_name_value = ecuc_element.get('short_name', '')
        self._monitor_log(f"RECREATE_WIDGET: short_name='{short_name_value}' from element id={id(ecuc_element)}")
        print(f"[PropertyEditor] Creating short_name widget with value '{short_name_value}' for element id={id(ecuc_element)}")
        short_name_edit = QLineEdit(short_name_value)
        
        # Store element reference with the widget to ensure we're always editing the right element
        short_name_edit.setProperty("ecuc_element", ecuc_element)
        
        # Use editingFinished signal for better validation
        short_name_edit.editingFinished.connect(
            lambda: self._on_ecuc_property_changed(
                self._current_element, 
                "short_name", 
                short_name_edit.text()
            )
        )
        # Also connect textChanged for real-time updates
        short_name_edit.textChanged.connect(
            lambda text: self._on_ecuc_property_changed(
                self._current_element, 
                "short_name", 
                text
            )
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
        try:
            print(f"[PropertyEditor] creating container widget id={id(container)} short_name='{container.get('short_name')}' type='{container.get('type')}'")
        except Exception:
            pass

        container_group = QGroupBox(f"Container: {container.get('short_name', 'Unknown')}")
        container_layout = QVBoxLayout()
        form = QFormLayout()

        # Short name
        short_name_edit = QLineEdit(container.get('short_name', ''))
        # Store container reference for signal handler
        short_name_edit.setProperty("container_element", container)
        short_name_edit.textChanged.connect(
            lambda text, widget=short_name_edit: self._on_ecuc_container_property_changed(
                widget.property("container_element"), "short_name", text
            )
        )
        form.addRow("Short Name:", short_name_edit)

        # Definition ref
        if container.get('definition_ref'):
            def_ref_edit = QLineEdit(container['definition_ref'])
            def_ref_edit.setReadOnly(True)
            form.addRow("Definition Ref:", def_ref_edit)

        container_layout.addLayout(form)

        # Parameters
        if container.get('parameters'):
            params_group = QGroupBox("Parameters")
            params_layout = QVBoxLayout(params_group)

            for param in container['parameters']:
                param_widget = self._create_ecuc_parameter_widget(param)
                params_layout.addWidget(param_widget)

            container_layout.addWidget(params_group)

        # Nested containers: render recursively
        if container.get('containers'):
            nested_group = QGroupBox("Nested Containers")
            nested_layout = QVBoxLayout(nested_group)
            for nested in container['containers']:
                nested_widget = self._create_ecuc_container_widget(nested)
                nested_layout.addWidget(nested_widget)
            container_layout.addWidget(nested_group)

        container_group.setLayout(container_layout)
        return container_group
    
    def _create_ecuc_parameter_widget(self, param: dict):
        """Create widget for ECUC parameter"""
        param_group = QGroupBox(f"Parameter: {param.get('short_name', 'Unknown')}")
        param_layout = QFormLayout(param_group)
        
        # Short name
        short_name_edit = QLineEdit(param.get('short_name', ''))
        # Store parameter reference for signal handler
        short_name_edit.setProperty("parameter_element", param)
        short_name_edit.textChanged.connect(
            lambda text, widget=short_name_edit: self._on_ecuc_parameter_property_changed(
                widget.property("parameter_element"), "short_name", text
            )
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
            # Store parameter reference for signal handler
            value_edit.setProperty("parameter_element", param)
            value_edit.textChanged.connect(
                lambda text, widget=value_edit: self._on_ecuc_parameter_property_changed(
                    widget.property("parameter_element"), "value", text
                )
            )
            param_layout.addRow("Value:", value_edit)
        
        return param_group

    def _find_dict_in(self, container: dict, target: dict):
        """Recursively search for target dict inside container; return target if found else None.

        This checks identity first, then tries best-effort matching by short_name and type.
        """
        # Identity match
        if container is target:
            return container

        # Check direct children lists and dict values
        for key, val in container.items():
            if val is target:
                return val
            if isinstance(val, dict):
                found = self._find_dict_in(val, target)
                if found is not None:
                    return found
            elif isinstance(val, list):
                for item in val:
                    if item is target:
                        return item
                    if isinstance(item, dict):
                        found = self._find_dict_in(item, target)
                        if found is not None:
                            return found

        # As fallback, match by short_name/type if present
        try:
            tname = target.get('short_name')
            ttype = target.get('type')
            if tname:
                # shallow search by short_name/type
                for key, val in container.items():
                    if isinstance(val, list):
                        for item in val:
                            if isinstance(item, dict) and item.get('short_name') == tname and item.get('type') == ttype:
                                return item
        except Exception:
            pass

        return None
    
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
        # Validate input
        if not isinstance(ecuc_element, dict):
            print(f"Warning: ecuc_element is not a dict: {type(ecuc_element)}")
            return
        
        # Always use the current element if it matches, as it should be the resolved instance
        target_element = ecuc_element
        resolved = None  # Initialize resolved variable to avoid UnboundLocalError
        
        if self._current_element is not None and isinstance(self._current_element, dict):
            # Log the property change attempt
            old_value = ecuc_element.get(property_name, '')
            self._monitor_log(f"PROPERTY_CHANGED: '{old_value}' -> '{new_value}' on element id={id(ecuc_element)} short_name='{ecuc_element.get('short_name')}'")
            self._monitor_log(f"CURRENT_ELEMENT: id={id(self._current_element)} short_name='{self._current_element.get('short_name')}'")
            self._monitor_log(f"ELEMENT_MATCH: {ecuc_element is self._current_element}")
            # If the current element is the same as or contains the ecuc_element, use current element
            if self._current_element is ecuc_element:
                target_element = self._current_element
                resolved = self._current_element
            else:
                # Try to resolve to ensure we're updating the document instance
                resolved = self._resolve_to_document(ecuc_element)
                if resolved is not None:
                    target_element = resolved
        
        old_value = target_element.get(property_name, '')
        target_element[property_name] = new_value
        
        try:
            print(f"[PropertyEditor] _on_ecuc_property_changed: '{old_value}' -> '{new_value}' on element id={id(target_element)} short_name='{target_element.get('short_name')}'")
        except Exception:
            pass

        # Log after saving - use target_element to avoid UnboundLocalError
        self._monitor_log(f"SAVED_PROPERTY: {property_name}='{new_value}' on element id={id(target_element)}")

        # Mark document as modified
        if hasattr(self.app, 'current_document') and self.app.current_document:
            self.app.current_document.set_modified(True)
        
        # After writing the change, try to canonicalize duplicates in the
        # document so the UI doesn't end up with multiple dict copies for
        # the same logical element (which was causing the "edits lost" bug).
        try:
            doc = getattr(self.app, 'current_document', None)
            if doc and resolved is not None:
                self._dedupe_document(resolved)
        except Exception:
            pass

        # Emit signal with the resolved element that was actually updated
        self.property_changed.emit(target_element, property_name, new_value)
    
    def _on_ecuc_container_property_changed(self, container: dict, property_name: str, new_value):
        """Handle ECUC container property change"""
        # Update container: resolve to document instance if possible
        resolved = None
        doc = getattr(self.app, 'current_document', None)
        if doc:
            resolved = self._resolve_to_document(container)

        if resolved is not None:
            try:
                print(f"[PropertyEditor] _on_ecuc_container_property_changed resolved id={id(resolved)} short_name='{resolved.get('short_name')}' -> setting {property_name}={new_value}")
            except Exception:
                pass
            resolved[property_name] = new_value
            target_for_emit = resolved
        else:
            # Try to find matching containers in the document by short_name/type
            updated = False
            if doc:
                try:
                    tname = container.get('short_name')
                    ttype = container.get('type')
                    matches = []
                    for doc_elem in doc.ecuc_elements:
                        # search nested
                        found = self._find_dict_in(doc_elem, container)
                        if found is not None:
                            matches.append(found)
                        else:
                            # fallback shallow match
                            if tname and doc_elem.get('short_name') == tname and doc_elem.get('type') == ttype:
                                matches.append(doc_elem)
                    if matches:
                        for m in matches:
                            try:
                                print(f"[PropertyEditor] _on_ecuc_container_property_changed fallback updating match id={id(m)} short_name='{m.get('short_name')}'")
                            except Exception:
                                pass
                            m[property_name] = new_value
                            updated = True
                        target_for_emit = matches[0]
                    else:
                        # No doc match found; update the passed container as a last resort
                        container[property_name] = new_value
                        target_for_emit = container
                except Exception:
                    container[property_name] = new_value
                    target_for_emit = container
            else:
                container[property_name] = new_value
                target_for_emit = container

        # Mark document as modified
        if doc:
            doc.set_modified(True)

        # After writing the change, canonicalize duplicates to prevent
        # transient copies from being selected later.
        try:
            if doc and target_for_emit is not None and isinstance(target_for_emit, dict):
                self._dedupe_document(target_for_emit)
        except Exception:
            pass

        # Emit signal
        self.property_changed.emit(target_for_emit, property_name, new_value)
        # Debug: dump document ECUC elements to show where the change landed
        try:
            if doc:
                print("[PropertyEditor] Document ECUC elements after change:")
                for e in doc.ecuc_elements:
                    try:
                        print(f"  id={id(e)} short_name='{e.get('short_name')}' containers={len(e.get('containers', []))}")
                    except Exception:
                        print(f"  id={id(e)} (unreadable)")
        except Exception:
            pass
    
    def _on_ecuc_parameter_property_changed(self, parameter: dict, property_name: str, new_value):
        """Handle ECUC parameter property change"""
        # Update parameter: resolve to document instance if possible
        resolved = None
        doc = getattr(self.app, 'current_document', None)
        if doc:
            resolved = self._resolve_to_document(parameter)

        if resolved is not None:
            try:
                print(f"[PropertyEditor] _on_ecuc_parameter_property_changed resolved id={id(resolved)} short_name='{resolved.get('short_name')}' -> setting {property_name}={new_value}")
            except Exception:
                pass
            resolved[property_name] = new_value
            target_for_emit = resolved
        else:
            # Try to find matching parameters in the document by short_name/type
            updated = False
            if doc:
                try:
                    tname = parameter.get('short_name')
                    ttype = parameter.get('type')
                    matches = []
                    for doc_elem in doc.ecuc_elements:
                        found = self._find_dict_in(doc_elem, parameter)
                        if found is not None:
                            matches.append(found)
                    if matches:
                        for m in matches:
                            try:
                                print(f"[PropertyEditor] _on_ecuc_parameter_property_changed fallback updating match id={id(m)} short_name='{m.get('short_name')}'")
                            except Exception:
                                pass
                            m[property_name] = new_value
                            updated = True
                        target_for_emit = matches[0]
                    else:
                        parameter[property_name] = new_value
                        target_for_emit = parameter
                except Exception:
                    parameter[property_name] = new_value
                    target_for_emit = parameter
            else:
                parameter[property_name] = new_value
                target_for_emit = parameter

        # Mark document as modified
        if doc:
            doc.set_modified(True)

        # After writing the change, canonicalize duplicates to prevent
        # transient copies from being selected later.
        try:
            if doc and target_for_emit is not None and isinstance(target_for_emit, dict):
                self._dedupe_document(target_for_emit)
        except Exception:
            pass

        # Emit signal
        self.property_changed.emit(target_for_emit, property_name, new_value)

    def _replace_in_container(self, container: dict, old: dict, new: dict):
        """Recursively replace references to old with new inside container dicts/lists."""
        if not isinstance(container, dict):
            return
        for key, val in list(container.items()):
            if val is old:
                container[key] = new
            elif isinstance(val, dict):
                self._replace_in_container(val, old, new)
            elif isinstance(val, list):
                for idx, item in enumerate(val):
                    if item is old:
                        val[idx] = new
                    elif isinstance(item, dict):
                        self._replace_in_container(item, old, new)

    def _dedupe_document(self, canonical: dict):
        """Replace duplicate dict instances in the current document with canonical."""
        doc = getattr(self.app, 'current_document', None)
        if not doc or not isinstance(canonical, dict):
            return

        try:
            c_name = canonical.get('short_name')
            c_type = canonical.get('type')
        except Exception:
            return

        # Replace duplicates inside top-level elements and remove duplicate top-levels
        new_top = []
        seen_top = set()
        for elem in doc.ecuc_elements:
            if elem is canonical:
                new_top.append(elem)
                seen_top.add((elem.get('short_name'), elem.get('type')))
            else:
                try:
                    if elem.get('short_name') == c_name and elem.get('type') == c_type:
                        # Found a duplicate top-level; replace references to it across doc
                        for top in doc.ecuc_elements:
                            self._replace_in_container(top, elem, canonical)
                        # Don't add duplicate to new_top (we keep canonical)
                        continue
                except Exception:
                    pass
                new_top.append(elem)

        # Update the document's ecuc_elements list if it changed
        if len(new_top) != len(doc.ecuc_elements) or any(x is not y for x, y in zip(new_top, doc.ecuc_elements)):
            try:
                doc._ecuc_elements = new_top
                print(f"[PropertyEditor] deduped document ECUC elements; now {len(new_top)} top-level elements")
            except Exception:
                pass
        # Debug: dump document ECUC elements after parameter change
        try:
            if doc:
                print("[PropertyEditor] Document ECUC elements after parameter change:")
                for e in doc.ecuc_elements:
                    try:
                        print(f"  id={id(e)} short_name='{e.get('short_name')}' containers={len(e.get('containers', []))}")
                    except Exception:
                        print(f"  id={id(e)} (unreadable)")
        except Exception:
            pass

    def _resolve_to_document(self, target: dict):
        """Resolve a dict (possibly a transient copy) to the corresponding dict
        instance inside the current document, or return None if not found.
        """
        if not hasattr(self.app, 'current_document') or not self.app.current_document:
            return None

        for doc_elem in self.app.current_document.ecuc_elements:
            # direct identity
            try:
                if doc_elem is target:
                    print(f"[PropertyEditor] _resolve_to_document: direct identity match id={id(doc_elem)} short_name='{doc_elem.get('short_name')}'")
                    self._monitor_log(f"RESOLVE_TO_DOC: direct identity match id={id(doc_elem)} short_name='{doc_elem.get('short_name')}'")
                    return doc_elem
            except Exception:
                pass
            # search nested structures
            found = self._find_dict_in(doc_elem, target)
            if found is not None:
                try:
                    print(f"[PropertyEditor] _resolve_to_document: nested match id={id(found)} short_name='{found.get('short_name')}' (contained in top-level id={id(doc_elem)})")
                    self._monitor_log(f"RESOLVE_TO_DOC: nested match id={id(found)} short_name='{found.get('short_name')}' (contained in top-level id={id(doc_elem)})")
                except Exception:
                    pass
                return found

        # Fallback: try to match top-level by short_name/type
        try:
            tname = target.get('short_name')
            ttype = target.get('type')
            if tname:
                for doc_elem in self.app.current_document.ecuc_elements:
                    if doc_elem.get('short_name') == tname and doc_elem.get('type') == ttype:
                        return doc_elem
        except Exception:
            pass

        return None
    
    def _verify_element_persistence(self, element):
        """Debug method to verify element values are persisted correctly"""
        if not isinstance(element, dict):
            return
        
        try:
            # Check if this element exists in the document
            if hasattr(self.app, 'current_document') and self.app.current_document:
                for doc_elem in self.app.current_document.ecuc_elements:
                    if doc_elem is element:
                        print(f"[PropertyEditor] VERIFY: Element id={id(element)} is document instance, short_name='{element.get('short_name')}'")
                        return
                    found = self._find_dict_in(doc_elem, element)
                    if found is not None:
                        print(f"[PropertyEditor] VERIFY: Element id={id(element)} found as nested, short_name='{element.get('short_name')}', doc_short_name='{found.get('short_name')}'")
                        return
                print(f"[PropertyEditor] VERIFY: Element id={id(element)} NOT FOUND in document, short_name='{element.get('short_name')}'")
        except Exception as e:
            print(f"[PropertyEditor] VERIFY ERROR: {e}")
    
    def clear(self):
        """Clear the property editor"""
        self.set_element(None)