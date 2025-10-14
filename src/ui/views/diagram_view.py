"""
Diagram View
Visual diagram representation of AUTOSAR elements
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem, QPushButton,
    QComboBox, QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QRectF, QPointF
from PyQt6.QtGui import QFont, QPen, QBrush, QColor, QPainter
from ...core.models.autosar_elements import SwComponentType, PortPrototype, PortType

class ComponentBox(QGraphicsRectItem):
    """Graphics item representing a software component"""
    
    def __init__(self, component: SwComponentType, x: float, y: float):
        super().__init__(x, y, 200, 120)
        self.component = component
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        
        # Set appearance
        self.setPen(QPen(QColor(0, 0, 0), 2))
        self.setBrush(QBrush(QColor(240, 240, 240)))
        
        # Add text label
        self.text_item = QGraphicsTextItem(component.short_name, self)
        self.text_item.setPos(10, 10)
        self.text_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        # Add category label
        self.category_item = QGraphicsTextItem(component.category.value, self)
        self.category_item.setPos(10, 30)
        self.category_item.setFont(QFont("Arial", 8))
        self.category_item.setDefaultTextColor(QColor(100, 100, 100))
        
        # Add port indicators
        self._add_port_indicators()
    
    def _add_port_indicators(self):
        """Add visual indicators for ports"""
        y_offset = 50
        for i, port in enumerate(self.component.ports):
            port_item = QGraphicsTextItem(f"• {port.short_name} ({port.port_type.value})", self)
            port_item.setPos(10, y_offset + i * 15)
            port_item.setFont(QFont("Arial", 8))
            
            # Color code by port type
            if port.port_type == PortType.PROVIDER:
                port_item.setDefaultTextColor(QColor(0, 150, 0))  # Green
            elif port.port_type == PortType.REQUIRER:
                port_item.setDefaultTextColor(QColor(150, 0, 0))  # Red
            else:  # PROVIDER_REQUIRER
                port_item.setDefaultTextColor(QColor(0, 0, 150))  # Blue

class DiagramView(QWidget):
    """Diagram view for visual representation"""
    
    # Signals
    element_selected = pyqtSignal(object)
    
    def __init__(self, app):
        super().__init__()
        self.app = app
        self._component_boxes = {}
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Setup the diagram view UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Title and controls
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("Diagram View")
        self.title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        # View controls
        self.zoom_in_btn = QPushButton("Zoom In")
        self.zoom_in_btn.clicked.connect(self._zoom_in)
        header_layout.addWidget(self.zoom_in_btn)
        
        self.zoom_out_btn = QPushButton("Zoom Out")
        self.zoom_out_btn.clicked.connect(self._zoom_out)
        header_layout.addWidget(self.zoom_out_btn)
        
        self.fit_view_btn = QPushButton("Fit View")
        self.fit_view_btn.clicked.connect(self._fit_view)
        header_layout.addWidget(self.fit_view_btn)
        
        layout.addLayout(header_layout)
        
        # Graphics view
        self.graphics_view = QGraphicsView()
        self.graphics_scene = QGraphicsScene()
        self.graphics_view.setScene(self.graphics_scene)
        self.graphics_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.graphics_view.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.graphics_view.setMouseTracking(True)
        
        # Set scene rect
        self.graphics_scene.setSceneRect(-1000, -1000, 2000, 2000)
        
        layout.addWidget(self.graphics_view)
        
        # Placeholder content
        self._show_placeholder()
    
    def _connect_signals(self):
        """Connect signals"""
        self.app.document_changed.connect(self.refresh)
    
    def _show_placeholder(self):
        """Show placeholder content"""
        placeholder_text = "No document loaded\n\nLoad an ARXML file to see:\n• File information\n• Element statistics\n• Visual diagrams\n• Structure overview"
        
        placeholder_item = self.graphics_scene.addText(
            placeholder_text,
            QFont("Arial", 12)
        )
        placeholder_item.setDefaultTextColor(Qt.GlobalColor.gray)
        placeholder_item.setTextWidth(400)
        
        # Center the text
        text_rect = placeholder_item.boundingRect()
        placeholder_item.setPos(-text_rect.width() / 2, -text_rect.height() / 2)
    
    def refresh(self):
        """Refresh the diagram view"""
        self.graphics_scene.clear()
        self._component_boxes.clear()
        
        if not self.app.current_document:
            self._show_placeholder()
            return
        
        # Show file information and statistics
        self._show_file_information()
    
    def _show_file_information(self):
        """Show file information and statistics"""
        doc = self.app.current_document
        if not doc:
            return
        
        y_offset = -400
        x_offset = -500
        
        # File header
        header_text = f"ARXML File Information"
        header_item = self.graphics_scene.addText(header_text, QFont("Arial", 16, QFont.Weight.Bold))
        header_item.setPos(x_offset, y_offset)
        header_item.setDefaultTextColor(QColor(0, 0, 0))
        y_offset += 40
        
        # File path
        file_path = doc.file_path or "New Document"
        path_text = f"File: {file_path}"
        path_item = self.graphics_scene.addText(path_text, QFont("Arial", 10))
        path_item.setPos(x_offset, y_offset)
        path_item.setDefaultTextColor(QColor(100, 100, 100))
        y_offset += 30
        
        # Schema version
        schema_text = f"Schema Version: {doc.schema_version}"
        schema_item = self.graphics_scene.addText(schema_text, QFont("Arial", 10))
        schema_item.setPos(x_offset, y_offset)
        schema_item.setDefaultTextColor(QColor(100, 100, 100))
        y_offset += 30
        
        # Modified status
        modified_text = f"Modified: {'Yes' if doc.modified else 'No'}"
        modified_item = self.graphics_scene.addText(modified_text, QFont("Arial", 10))
        modified_item.setPos(x_offset, y_offset)
        modified_item.setDefaultTextColor(QColor(150, 0, 0) if doc.modified else QColor(0, 150, 0))
        y_offset += 50
        
        # Statistics section
        stats_text = "Element Statistics"
        stats_header = self.graphics_scene.addText(stats_text, QFont("Arial", 14, QFont.Weight.Bold))
        stats_header.setPos(x_offset, y_offset)
        stats_header.setDefaultTextColor(QColor(0, 0, 0))
        y_offset += 30
        
        # Count elements
        sw_components = len(doc.sw_component_types)
        compositions = len(doc.compositions)
        port_interfaces = len(doc.port_interfaces)
        service_interfaces = len(doc.service_interfaces)
        ecuc_elements = len(doc.ecuc_elements)
        
        # Software Component Types
        sw_text = f"Software Component Types: {sw_components}"
        sw_item = self.graphics_scene.addText(sw_text, QFont("Arial", 10))
        sw_item.setPos(x_offset, y_offset)
        sw_item.setDefaultTextColor(QColor(0, 0, 150))
        y_offset += 25
        
        # Compositions
        comp_text = f"Compositions: {compositions}"
        comp_item = self.graphics_scene.addText(comp_text, QFont("Arial", 10))
        comp_item.setPos(x_offset, y_offset)
        comp_item.setDefaultTextColor(QColor(0, 0, 150))
        y_offset += 25
        
        # Port Interfaces
        port_text = f"Port Interfaces: {port_interfaces}"
        port_item = self.graphics_scene.addText(port_text, QFont("Arial", 10))
        port_item.setPos(x_offset, y_offset)
        port_item.setDefaultTextColor(QColor(0, 0, 150))
        y_offset += 25
        
        # Service Interfaces
        service_text = f"Service Interfaces: {service_interfaces}"
        service_item = self.graphics_scene.addText(service_text, QFont("Arial", 10))
        service_item.setPos(x_offset, y_offset)
        service_item.setDefaultTextColor(QColor(0, 0, 150))
        y_offset += 25
        
        # ECUC Elements
        ecuc_text = f"ECUC Elements: {ecuc_elements}"
        ecuc_item = self.graphics_scene.addText(ecuc_text, QFont("Arial", 10))
        ecuc_item.setPos(x_offset, y_offset)
        ecuc_item.setDefaultTextColor(QColor(0, 0, 150))
        y_offset += 50
        
        # Detailed breakdown
        if sw_components > 0 or port_interfaces > 0 or ecuc_elements > 0:
            details_text = "Detailed Breakdown"
            details_header = self.graphics_scene.addText(details_text, QFont("Arial", 12, QFont.Weight.Bold))
            details_header.setPos(x_offset, y_offset)
            details_header.setDefaultTextColor(QColor(0, 0, 0))
            y_offset += 30
            
            # Software Component Types details
            if sw_components > 0:
                sw_details_text = "Software Component Types:"
                sw_details_item = self.graphics_scene.addText(sw_details_text, QFont("Arial", 10, QFont.Weight.Bold))
                sw_details_item.setPos(x_offset, y_offset)
                sw_details_item.setDefaultTextColor(QColor(0, 0, 0))
                y_offset += 25
                
                for i, comp in enumerate(doc.sw_component_types[:5]):  # Show first 5
                    comp_detail_text = f"  • {comp.short_name} ({comp.category.value})"
                    comp_detail_item = self.graphics_scene.addText(comp_detail_text, QFont("Arial", 9))
                    comp_detail_item.setPos(x_offset + 20, y_offset)
                    comp_detail_item.setDefaultTextColor(QColor(100, 100, 100))
                    y_offset += 20
                
                if len(doc.sw_component_types) > 5:
                    more_text = f"  ... and {len(doc.sw_component_types) - 5} more"
                    more_item = self.graphics_scene.addText(more_text, QFont("Arial", 9))
                    more_item.setPos(x_offset + 20, y_offset)
                    more_item.setDefaultTextColor(QColor(150, 150, 150))
                    y_offset += 20
                
                y_offset += 10
            
            # Port Interfaces details
            if port_interfaces > 0:
                port_details_text = "Port Interfaces:"
                port_details_item = self.graphics_scene.addText(port_details_text, QFont("Arial", 10, QFont.Weight.Bold))
                port_details_item.setPos(x_offset, y_offset)
                port_details_item.setDefaultTextColor(QColor(0, 0, 0))
                y_offset += 25
                
                for i, port in enumerate(doc.port_interfaces[:5]):  # Show first 5
                    port_detail_text = f"  • {port.short_name} ({'Service' if port.is_service else 'S/R'})"
                    port_detail_item = self.graphics_scene.addText(port_detail_text, QFont("Arial", 9))
                    port_detail_item.setPos(x_offset + 20, y_offset)
                    port_detail_item.setDefaultTextColor(QColor(100, 100, 100))
                    y_offset += 20
                
                if len(doc.port_interfaces) > 5:
                    more_text = f"  ... and {len(doc.port_interfaces) - 5} more"
                    more_item = self.graphics_scene.addText(more_text, QFont("Arial", 9))
                    more_item.setPos(x_offset + 20, y_offset)
                    more_item.setDefaultTextColor(QColor(150, 150, 150))
                    y_offset += 20
                
                y_offset += 10
            
            # ECUC Elements details
            if ecuc_elements > 0:
                ecuc_details_text = "ECUC Elements:"
                ecuc_details_item = self.graphics_scene.addText(ecuc_details_text, QFont("Arial", 10, QFont.Weight.Bold))
                ecuc_details_item.setPos(x_offset, y_offset)
                ecuc_details_item.setDefaultTextColor(QColor(0, 0, 0))
                y_offset += 25
                
                for i, ecuc in enumerate(doc.ecuc_elements[:3]):  # Show first 3
                    ecuc_detail_text = f"  • {ecuc.get('short_name', 'Unknown')} ({ecuc.get('type', 'Unknown')})"
                    ecuc_detail_item = self.graphics_scene.addText(ecuc_detail_text, QFont("Arial", 9))
                    ecuc_detail_item.setPos(x_offset + 20, y_offset)
                    ecuc_detail_item.setDefaultTextColor(QColor(100, 100, 100))
                    y_offset += 20
                
                if len(doc.ecuc_elements) > 3:
                    more_text = f"  ... and {len(doc.ecuc_elements) - 3} more"
                    more_item = self.graphics_scene.addText(more_text, QFont("Arial", 9))
                    more_item.setPos(x_offset + 20, y_offset)
                    more_item.setDefaultTextColor(QColor(150, 150, 150))
                    y_offset += 20
        
        # Add visual elements if there are components
        if sw_components > 0:
            self._draw_component_diagram()
    
    def _draw_component_diagram(self):
        """Draw a simple component diagram"""
        doc = self.app.current_document
        if not doc or not doc.sw_component_types:
            return
        
        # Position for diagram
        x_offset = 200
        y_offset = -200
        components_per_row = 3
        
        for i, component in enumerate(doc.sw_component_types):
            if i > 0 and i % components_per_row == 0:
                x_offset = 200
                y_offset += 150
            
            # Create component box
            component_box = ComponentBox(component, x_offset, y_offset)
            self.graphics_scene.addItem(component_box)
            self._component_boxes[component] = component_box
            
            x_offset += 220
    
    def _draw_connections(self):
        """Draw connections between components"""
        # This is a simplified connection drawing
        # In a real implementation, you would analyze port connections
        # and draw appropriate lines between connected ports
        pass
    
    def _zoom_in(self):
        """Zoom in the view"""
        self.graphics_view.scale(1.2, 1.2)
    
    def _zoom_out(self):
        """Zoom out the view"""
        self.graphics_view.scale(0.8, 0.8)
    
    def _fit_view(self):
        """Fit all items in view"""
        self.graphics_view.fitInView(self.graphics_scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
    
    def set_element(self, element):
        """Set the current element for diagram focus"""
        # TODO: Implement element highlighting in diagram
        pass