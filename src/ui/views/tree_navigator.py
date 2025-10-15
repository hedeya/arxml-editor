"""
Tree Navigator View
Hierarchical tree view of AUTOSAR elements
"""

from PyQt6.QtWidgets import (
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, 
    QHeaderView, QMenu, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction
from ...core.models.autosar_elements import (
    SwComponentType, Composition, PortInterface, PortPrototype,
    SwComponentTypeCategory, PortType
)

class TreeNavigator(QTreeWidget):
    """Tree navigator for AUTOSAR elements"""
    
    # Signals
    element_selected = pyqtSignal(object)
    element_double_clicked = pyqtSignal(object)
    
    def __init__(self, app):
        super().__init__()
        self.app = app
        self._setup_ui()
        self._connect_signals()
        self._setup_context_menu()
    
    def _setup_ui(self):
        """Setup the tree UI"""
        self.setHeaderLabel("AUTOSAR Elements")
        self.setRootIsDecorated(True)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
        
        # Setup columns
        self.setColumnCount(2)
        self.setHeaderLabels(["Name", "Type"])
        
        # Configure header
        header = self.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        
        # Enable drag and drop
        self.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        
        # Root items are created dynamically in refresh()
    
    
    def _connect_signals(self):
        """Connect signals"""
        self.itemSelectionChanged.connect(self._on_selection_changed)
        self.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.app.document_changed.connect(self.refresh)
    
    def _setup_context_menu(self):
        """Setup context menu"""
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
    
    def _show_context_menu(self, position):
        """Show context menu"""
        item = self.itemAt(position)
        if not item:
            return
        
        menu = QMenu(self)
        
        # Get item data
        item_data = item.data(0, Qt.ItemDataRole.UserRole)
        
        if item_data == "sw_component_types":
            # Add new component type actions
            add_app_action = QAction("Add Application Component", self)
            add_app_action.triggered.connect(self._add_application_component)
            menu.addAction(add_app_action)
            
            add_atomic_action = QAction("Add Atomic Component", self)
            add_atomic_action.triggered.connect(self._add_atomic_component)
            menu.addAction(add_atomic_action)
            
            add_composition_action = QAction("Add Composition Component", self)
            add_composition_action.triggered.connect(self._add_composition_component)
            menu.addAction(add_composition_action)
        
        elif item_data == "compositions":
            add_action = QAction("Add Composition", self)
            add_action.triggered.connect(self._add_composition)
            menu.addAction(add_action)
        
        elif item_data == "port_interfaces":
            add_action = QAction("Add Port Interface", self)
            add_action.triggered.connect(self._add_port_interface)
            menu.addAction(add_action)
        
        elif item_data == "service_interfaces":
            add_action = QAction("Add Service Interface", self)
            add_action.triggered.connect(self._add_service_interface)
            menu.addAction(add_action)
        
        elif isinstance(item_data, (SwComponentType, Composition, PortInterface)):
            # Element-specific actions
            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(lambda: self._delete_element(item_data))
            menu.addAction(delete_action)
        
        if menu.actions():
            menu.exec(self.mapToGlobal(position))
    
    def refresh(self):
        """Refresh the tree view"""
        self.clear()
        
        if not self.app.current_document:
            return
        
        # Only create root items for sections that have content
        has_sw_components = len(self.app.current_document.sw_component_types) > 0
        has_compositions = len(self.app.current_document.compositions) > 0
        has_port_interfaces = len(self.app.current_document.port_interfaces) > 0
        has_service_interfaces = len(self.app.current_document.service_interfaces) > 0
        has_ecuc_elements = len(self.app.current_document.ecuc_elements) > 0
        
        # Create root items only for non-empty sections
        if has_sw_components:
            self.sw_component_types_item = QTreeWidgetItem(self)
            self.sw_component_types_item.setText(0, "Software Component Types")
            self.sw_component_types_item.setText(1, f"{len(self.app.current_document.sw_component_types)} items")
            self.sw_component_types_item.setData(0, Qt.ItemDataRole.UserRole, "sw_component_types")
            
            for component_type in self.app.current_document.sw_component_types:
                self._add_component_type_item(component_type)
        
        if has_compositions:
            self.compositions_item = QTreeWidgetItem(self)
            self.compositions_item.setText(0, "Compositions")
            self.compositions_item.setText(1, f"{len(self.app.current_document.compositions)} items")
            self.compositions_item.setData(0, Qt.ItemDataRole.UserRole, "compositions")
            
            for composition in self.app.current_document.compositions:
                self._add_composition_item(composition)
        
        if has_port_interfaces:
            self.port_interfaces_item = QTreeWidgetItem(self)
            self.port_interfaces_item.setText(0, "Port Interfaces")
            self.port_interfaces_item.setText(1, f"{len(self.app.current_document.port_interfaces)} items")
            self.port_interfaces_item.setData(0, Qt.ItemDataRole.UserRole, "port_interfaces")
            
            for port_interface in self.app.current_document.port_interfaces:
                self._add_port_interface_item(port_interface)
        
        if has_service_interfaces:
            self.service_interfaces_item = QTreeWidgetItem(self)
            self.service_interfaces_item.setText(0, "Service Interfaces")
            self.service_interfaces_item.setText(1, f"{len(self.app.current_document.service_interfaces)} items")
            self.service_interfaces_item.setData(0, Qt.ItemDataRole.UserRole, "service_interfaces")
            
            for service_interface in self.app.current_document.service_interfaces:
                self._add_service_interface_item(service_interface)
        
        if has_ecuc_elements:
            self.ecuc_elements_item = QTreeWidgetItem(self)
            self.ecuc_elements_item.setText(0, "ECUC Elements")
            self.ecuc_elements_item.setText(1, f"{len(self.app.current_document.ecuc_elements)} items")
            self.ecuc_elements_item.setData(0, Qt.ItemDataRole.UserRole, "ecuc_elements")
            
            for ecuc_element in self.app.current_document.ecuc_elements:
                self._add_ecuc_element_item(ecuc_element)
        
        # Expand all root items
        self.expandAll()
    
    
    def _add_component_type_item(self, component_type: SwComponentType):
        """Add component type to tree"""
        item = QTreeWidgetItem(self.sw_component_types_item)
        item.setText(0, component_type.short_name)
        item.setText(1, component_type.category.value)
        item.setData(0, Qt.ItemDataRole.UserRole, component_type)
        
        # Add ports as children
        for port in component_type.ports:
            port_item = QTreeWidgetItem(item)
            port_item.setText(0, port.short_name)
            port_item.setText(1, port.port_type.value)
            port_item.setData(0, Qt.ItemDataRole.UserRole, port)
    
    def _add_composition_item(self, composition: Composition):
        """Add composition to tree"""
        item = QTreeWidgetItem(self.compositions_item)
        item.setText(0, composition.short_name)
        item.setText(1, "Composition")
        item.setData(0, Qt.ItemDataRole.UserRole, composition)
        
        # Add component types as children
        for component_type in composition.component_types:
            comp_item = QTreeWidgetItem(item)
            comp_item.setText(0, component_type.short_name)
            comp_item.setText(1, component_type.category.value)
            comp_item.setData(0, Qt.ItemDataRole.UserRole, component_type)
    
    def _add_port_interface_item(self, port_interface: PortInterface):
        """Add port interface to tree"""
        item = QTreeWidgetItem(self.port_interfaces_item)
        item.setText(0, port_interface.short_name)
        item.setText(1, "Port Interface")
        item.setData(0, Qt.ItemDataRole.UserRole, port_interface)
        
        # Add data elements as children
        for data_element in port_interface.data_elements:
            data_item = QTreeWidgetItem(item)
            data_item.setText(0, data_element.short_name)
            data_item.setText(1, data_element.data_type.value)
            data_item.setData(0, Qt.ItemDataRole.UserRole, data_element)
    
    def _add_service_interface_item(self, service_interface):
        """Add service interface to tree"""
        item = QTreeWidgetItem(self.service_interfaces_item)
        item.setText(0, service_interface.short_name)
        item.setText(1, "Service Interface")
        item.setData(0, Qt.ItemDataRole.UserRole, service_interface)
    
    def _add_ecuc_element_item(self, ecuc_element: dict):
        """Add ECUC element to tree"""
        item = QTreeWidgetItem(self.ecuc_elements_item)
        item.setText(0, ecuc_element['short_name'])
        item.setText(1, ecuc_element['type'])
        item.setData(0, Qt.ItemDataRole.UserRole, ecuc_element)
        
        # Add containers as children
        for container in ecuc_element.get('containers', []):
            container_item = QTreeWidgetItem(item)
            container_item.setText(0, container['short_name'])
            container_item.setText(1, container['type'])
            container_item.setData(0, Qt.ItemDataRole.UserRole, container)
            
            # Add parameters as children of containers
            for param in container.get('parameters', []):
                param_item = QTreeWidgetItem(container_item)
                param_item.setText(0, param['short_name'])
                param_item.setText(1, param['type'])
                param_item.setData(0, Qt.ItemDataRole.UserRole, param)
    
    def _on_selection_changed(self):
        """Handle selection changed"""
        current_item = self.currentItem()
        if current_item:
            item_data = current_item.data(0, Qt.ItemDataRole.UserRole)
            if isinstance(item_data, (SwComponentType, Composition, PortInterface, PortPrototype)) or isinstance(item_data, dict):
                self.element_selected.emit(item_data)
    
    def _on_item_double_clicked(self, item, column):
        """Handle item double click"""
        item_data = item.data(0, Qt.ItemDataRole.UserRole)
        if isinstance(item_data, (SwComponentType, Composition, PortInterface, PortPrototype)):
            self.element_double_clicked.emit(item_data)
    
    def _add_application_component(self):
        """Add application component type"""
        from ...core.models.autosar_elements import ApplicationSwComponentType
        component = ApplicationSwComponentType(short_name="NewApplicationComponent")
        self.app.current_document.add_sw_component_type(component)
        self.refresh()
    
    def _add_atomic_component(self):
        """Add atomic component type"""
        from ...core.models.autosar_elements import AtomicSwComponentType
        component = AtomicSwComponentType(short_name="NewAtomicComponent")
        self.app.current_document.add_sw_component_type(component)
        self.refresh()
    
    def _add_composition_component(self):
        """Add composition component type"""
        from ...core.models.autosar_elements import CompositionSwComponentType
        component = CompositionSwComponentType(short_name="NewCompositionComponent")
        self.app.current_document.add_sw_component_type(component)
        self.refresh()
    
    def _add_composition(self):
        """Add composition"""
        from ...core.models.autosar_elements import Composition
        composition = Composition(short_name="NewComposition")
        self.app.current_document.add_composition(composition)
        self.refresh()
    
    def _add_port_interface(self):
        """Add port interface"""
        from ...core.models.autosar_elements import PortInterface
        port_interface = PortInterface(short_name="NewPortInterface")
        self.app.current_document.add_port_interface(port_interface)
        self.refresh()
    
    def _add_service_interface(self):
        """Add service interface"""
        from ...core.models.autosar_elements import ServiceInterface
        service_interface = ServiceInterface(short_name="NewServiceInterface")
        self.app.current_document.add_service_interface(service_interface)
        self.refresh()
    
    def contextMenuEvent(self, event):
        """Handle context menu event"""
        item = self.itemAt(event.pos())
        if not item:
            return
        
        menu = QMenu(self)
        
        # Get element data
        element_data = item.data(0, Qt.ItemDataRole.UserRole)
        element = item.data(0, Qt.ItemDataRole.UserRole + 1)
        
        if element_data == "sw_component_types":
            # Add new component type
            add_action = QAction("Add Component Type", self)
            add_action.triggered.connect(self._add_component_type)
            menu.addAction(add_action)
        elif element_data == "compositions":
            # Add new composition
            add_action = QAction("Add Composition", self)
            add_action.triggered.connect(self._add_composition)
            menu.addAction(add_action)
        elif element_data == "port_interfaces":
            # Add new port interface
            add_action = QAction("Add Port Interface", self)
            add_action.triggered.connect(self._add_port_interface)
            menu.addAction(add_action)
        elif element_data == "service_interfaces":
            # Add new service interface
            add_action = QAction("Add Service Interface", self)
            add_action.triggered.connect(self._add_service_interface)
            menu.addAction(add_action)
        elif element and hasattr(element, 'short_name'):
            # Delete existing element
            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(lambda: self._delete_element(element))
            menu.addAction(delete_action)
        
        if menu.actions():
            menu.exec(self.mapToGlobal(event.pos()))
    
    def _add_component_type(self):
        """Add new component type"""
        from ...core.models.autosar_elements import ApplicationSwComponentType, SwComponentTypeCategory
        
        # Create new component type
        new_component = ApplicationSwComponentType(
            short_name="NewComponent",
            desc="New component type",
            category=SwComponentTypeCategory.APPLICATION
        )
        
        # Add to document
        self.app.current_document.add_sw_component_type(new_component)
        self.refresh()
        
        # Select the new item
        self._select_element(new_component)
    
    def _add_composition(self):
        """Add new composition"""
        from ...core.models.autosar_elements import Composition
        
        # Create new composition
        new_composition = Composition(
            short_name="NewComposition",
            desc="New composition"
        )
        
        # Add to document
        self.app.current_document.add_composition(new_composition)
        self.refresh()
        
        # Select the new item
        self._select_element(new_composition)
    
    def _add_port_interface(self):
        """Add new port interface"""
        from ...core.models.autosar_elements import PortInterface
        
        # Create new port interface
        new_interface = PortInterface(
            short_name="NewInterface",
            desc="New port interface",
            is_service=False
        )
        
        # Add to document
        self.app.current_document.add_port_interface(new_interface)
        self.refresh()
        
        # Select the new item
        self._select_element(new_interface)
    
    def _add_service_interface(self):
        """Add new service interface"""
        from ...core.models.autosar_elements import ServiceInterface
        
        # Create new service interface
        new_interface = ServiceInterface(
            short_name="NewServiceInterface",
            desc="New service interface"
        )
        
        # Add to document
        self.app.current_document.add_service_interface(new_interface)
        self.refresh()
        
        # Select the new item
        self._select_element(new_interface)
    
    def _select_element(self, element):
        """Select an element in the tree"""
        # Find and select the item corresponding to the element
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            if self._find_element_in_item(item, element):
                self.setCurrentItem(item)
                break
    
    def _find_element_in_item(self, item, element):
        """Find element in item hierarchy"""
        if item.data(0, Qt.ItemDataRole.UserRole + 1) == element:
            return True
        
        for i in range(item.childCount()):
            if self._find_element_in_item(item.child(i), element):
                return True
        
        return False
    
    def _delete_element(self, element):
        """Delete element with confirmation and children warning"""
        # Check if element has children
        has_children = False
        children_info = ""
        
        if isinstance(element, SwComponentType):
            if element.ports:
                has_children = True
                children_info = f"\n\n⚠️  This component has {len(element.ports)} port(s) that will also be deleted."
        elif isinstance(element, Composition):
            if element.component_types:
                has_children = True
                children_info = f"\n\n⚠️  This composition has {len(element.component_types)} component type(s) that will also be deleted."
        elif isinstance(element, PortInterface):
            if element.data_elements:
                has_children = True
                children_info = f"\n\n⚠️  This port interface has {len(element.data_elements)} data element(s) that will also be deleted."
        
        # Create confirmation message
        message = f"Are you sure you want to delete '{element.short_name}'?"
        if has_children:
            message += children_info
            message += "\n\nThis action cannot be undone."
        
        # Create custom message box with detailed buttons
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Delete Element")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        
        # Add custom buttons
        delete_button = msg_box.addButton("Delete", QMessageBox.ButtonRole.AcceptRole)
        cancel_button = msg_box.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        
        # Set default button
        msg_box.setDefaultButton(cancel_button)
        
        # Show dialog
        result = msg_box.exec()
        
        if result == 0:  # Delete button clicked
            if isinstance(element, SwComponentType):
                self.app.current_document.remove_sw_component_type(element)
            elif isinstance(element, Composition):
                self.app.current_document.remove_composition(element)
            elif isinstance(element, PortInterface):
                self.app.current_document.remove_port_interface(element)
            elif isinstance(element, ServiceInterface):
                self.app.current_document.remove_service_interface(element)
            
            self.refresh()
    
    def dragEnterEvent(self, event):
        """Handle drag enter event"""
        if event.source() == self:
            event.accept()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        """Handle drag move event"""
        if event.source() == self:
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        """Handle drop event"""
        if event.source() != self:
            event.ignore()
            return
        
        # Get the dragged item
        dragged_item = self.currentItem()
        if not dragged_item:
            event.ignore()
            return
        
        # Get the target item
        target_item = self.itemAt(event.pos())
        if not target_item:
            event.ignore()
            return
        
        # Get the dragged element
        dragged_element = dragged_item.data(0, Qt.ItemDataRole.UserRole + 1)
        if not dragged_element:
            event.ignore()
            return
        
        # Get target item data
        target_data = target_item.data(0, Qt.ItemDataRole.UserRole)
        
        # Only allow moving elements within the same category or to a different category
        if self._can_move_element(dragged_element, target_data):
            self._move_element(dragged_element, target_data)
            event.accept()
        else:
            event.ignore()
    
    def _can_move_element(self, element, target_data):
        """Check if element can be moved to target"""
        # Allow moving elements to category roots
        if target_data in ["sw_component_types", "compositions", "port_interfaces", "service_interfaces"]:
            return True
        
        # Allow moving elements to other elements of the same type
        if isinstance(element, SwComponentType) and isinstance(target_data, SwComponentType):
            return True
        elif isinstance(element, Composition) and isinstance(target_data, Composition):
            return True
        elif isinstance(element, PortInterface) and isinstance(target_data, PortInterface):
            return True
        
        return False
    
    def _move_element(self, element, target_data):
        """Move element to target location"""
        # For now, we'll just refresh the tree to show the move
        # In a more sophisticated implementation, we could reorder elements
        # or move them between different categories
        self.refresh()
        
        # Mark document as modified
        if hasattr(self.app, 'current_document') and self.app.current_document:
            self.app.current_document.set_modified(True)