"""
AUTOSAR Element Models
Strongly-typed classes for AUTOSAR elements
"""

from typing import List, Optional, Dict, Any, Union, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum
from PyQt6.QtCore import QObject, pyqtSignal
try:
    from ..events.ui_event_bus import UIEventBus
except Exception:
    UIEventBus = None

if TYPE_CHECKING:
    from ..domain_events import DomainEvent, IEventBus

class PortType(Enum):
    """Port type enumeration"""
    PROVIDER = "P-PORT"
    REQUIRER = "R-PORT"
    PROVIDER_REQUIRER = "PR-PORT"

class DataType(Enum):
    """Data type enumeration"""
    BOOLEAN = "boolean"
    INTEGER = "integer"
    FLOAT = "float"
    STRING = "string"
    ARRAY = "array"
    STRUCTURE = "structure"

class SwComponentTypeCategory(Enum):
    """Software component type category"""
    APPLICATION = "ApplicationSwComponentType"
    ATOMIC = "AtomicSwComponentType"
    COMPOSITION = "CompositionSwComponentType"

class BaseElement(QObject):
    """Base class for all AUTOSAR elements with event support"""
    
    # Signals
    element_changed = pyqtSignal(object)  # Emitted when element changes
    
    def __init__(self, short_name: str, desc: Optional[str] = None):
        super().__init__()
        self.short_name = short_name
        self.desc = desc
        self.id = ""
        self._event_bus: Optional['IEventBus'] = None
        self._domain_events: List['DomainEvent'] = []
        # Optional UI event bus to decouple UI signal emission
        self._ui_event_bus: Optional['UIEventBus'] = None
    
    def set_event_bus(self, event_bus: 'IEventBus') -> None:
        """Set the event bus for this element"""
        self._event_bus = event_bus
    
    def add_domain_event(self, event: 'DomainEvent') -> None:
        """Add a domain event to be published"""
        self._domain_events.append(event)
    
    def get_domain_events(self) -> List['DomainEvent']:
        """Get all pending domain events"""
        return self._domain_events.copy()
    
    def clear_domain_events(self) -> None:
        """Clear all pending domain events"""
        self._domain_events.clear()
    
    def publish_domain_events(self) -> None:
        """Publish all pending domain events"""
        if self._event_bus:
            for event in self._domain_events:
                self._event_bus.publish(event)
        self.clear_domain_events()
    
    def _notify_changed(self) -> None:
        """Notify that the element has changed"""
        # Emit legacy Qt signal for backward compatibility
        try:
            self.element_changed.emit(self)
        except Exception:
            # If running in non-Qt context, ignore
            pass

        # Publish a UI-level event (decoupled) if bus available
        if self._ui_event_bus and UIEventBus is not None:
            try:
                self._ui_event_bus.publish('element_changed', self)
            except Exception:
                pass

        # Publish domain events via domain event bus
        self.publish_domain_events()

    def set_ui_event_bus(self, ui_event_bus: 'UIEventBus') -> None:
        """Set an optional UI event bus for decoupling UI updates"""
        self._ui_event_bus = ui_event_bus

class DataElement(BaseElement):
    """Data element model"""
    def __init__(self, short_name: str, data_type: DataType, desc: Optional[str] = None, 
                 is_array: bool = False, array_size: Optional[int] = None, 
                 unit: Optional[str] = None, min_value: Optional[float] = None, 
                 max_value: Optional[float] = None):
        super().__init__(short_name, desc)
        self.data_type = data_type
        self.is_array = is_array
        self.array_size = array_size
        self.unit = unit
        self.min_value = min_value
        self.max_value = max_value

class PortInterface(BaseElement):
    """Port interface model with event publishing"""
    def __init__(self, short_name: str, desc: Optional[str] = None, is_service: bool = False):
        super().__init__(short_name, desc)
        self.is_service = is_service
        self.data_elements: List[DataElement] = []
        self.service_elements: List['ServiceElement'] = []
    
    def add_data_element(self, data_element: DataElement):
        """Add a data element to the interface"""
        self.data_elements.append(data_element)
        
        # Add domain event
        from ..domain_events import DataElementAdded
        event = DataElementAdded(
            interface_id=self.id,
            interface_name=self.short_name,
            element_name=data_element.short_name,
            data_type=data_element.data_type.value if data_element.data_type else "unknown",
            source='PortInterface'
        )
        self.add_domain_event(event)
        self._notify_changed()
    
    def remove_data_element(self, data_element: DataElement):
        """Remove a data element from the interface"""
        if data_element in self.data_elements:
            self.data_elements.remove(data_element)
            
            # Add domain event
            from ..domain_events import DataElementRemoved
            event = DataElementRemoved(
                interface_id=self.id,
                interface_name=self.short_name,
                element_name=data_element.short_name,
                source='PortInterface'
            )
            self.add_domain_event(event)
            self._notify_changed()
    
    def change_name(self, new_name: str) -> None:
        """Change the interface name and publish event"""
        old_name = self.short_name
        self.short_name = new_name
        
        # Add domain event
        from ..domain_events import PortInterfaceUpdated
        event = PortInterfaceUpdated(
            interface_id=self.id,
            interface_name=new_name,
            changes={'short_name': {'old': old_name, 'new': new_name}},
            source='PortInterface'
        )
        self.add_domain_event(event)
        self._notify_changed()
    
    def validate_invariants(self) -> List[str]:
        """Validate business invariants"""
        violations = []
        
        if not self.short_name or not self.short_name.strip():
            violations.append("Interface name cannot be empty")
        
        # Check for duplicate data element names
        element_names = [elem.short_name for elem in self.data_elements]
        if len(element_names) != len(set(element_names)):
            violations.append("Data element names must be unique within an interface")
        
        # Check for duplicate service element names
        service_names = [elem.short_name for elem in self.service_elements]
        if len(service_names) != len(set(service_names)):
            violations.append("Service element names must be unique within an interface")
        
        return violations

class ServiceElement(BaseElement):
    """Service element model"""
    def __init__(self, short_name: str, service_kind: str, desc: Optional[str] = None):
        super().__init__(short_name, desc)
        self.service_kind = service_kind
        self.operations: List['ServiceOperation'] = []

class ServiceOperation(BaseElement):
    """Service operation model"""
    def __init__(self, short_name: str, desc: Optional[str] = None, return_type: Optional[DataType] = None):
        super().__init__(short_name, desc)
        self.input_arguments: List[DataElement] = []
        self.output_arguments: List[DataElement] = []
        self.return_type = return_type

class ServiceInterface(BaseElement):
    """Service interface model"""
    def __init__(self, short_name: str, desc: Optional[str] = None):
        super().__init__(short_name, desc)
        self.service_elements: List[ServiceElement] = []
    
    def add_service_element(self, service_element: ServiceElement):
        """Add a service element to the interface"""
        self.service_elements.append(service_element)

class PortPrototype(BaseElement):
    """Port prototype model"""
    def __init__(self, short_name: str, port_type: PortType, desc: Optional[str] = None, 
                 interface_ref: Optional[str] = None, interface: Optional[PortInterface] = None):
        super().__init__(short_name, desc)
        self.port_type = port_type
        self.interface_ref = interface_ref
        self.interface = interface
        self.connected_ports: List['PortPrototype'] = []
    
    def connect_to(self, other_port: 'PortPrototype'):
        """Connect this port to another port"""
        if other_port not in self.connected_ports:
            self.connected_ports.append(other_port)
        if self not in other_port.connected_ports:
            other_port.connected_ports.append(self)
    
    def disconnect_from(self, other_port: 'PortPrototype'):
        """Disconnect this port from another port"""
        if other_port in self.connected_ports:
            self.connected_ports.remove(other_port)
        if self in other_port.connected_ports:
            other_port.connected_ports.remove(self)

class SwComponentType(BaseElement):
    """Base software component type model with event publishing"""
    def __init__(self, short_name: str, category: SwComponentTypeCategory, desc: Optional[str] = None):
        super().__init__(short_name, desc)
        self.category = category
        self.ports: List[PortPrototype] = []
        self.compositions: List['Composition'] = []
    
    def add_port(self, port: PortPrototype):
        """Add a port to the component"""
        self.ports.append(port)
        self._notify_changed()
    
    def remove_port(self, port: PortPrototype):
        """Remove a port from the component"""
        if port in self.ports:
            self.ports.remove(port)
            self._notify_changed()
    
    def change_name(self, new_name: str) -> None:
        """Change the component name and publish event"""
        old_name = self.short_name
        self.short_name = new_name
        
        # Add domain event
        from ..domain_events import SwComponentTypeUpdated
        event = SwComponentTypeUpdated(
            component_id=self.id,
            component_name=new_name,
            changes={'short_name': {'old': old_name, 'new': new_name}},
            source='SwComponentType'
        )
        self.add_domain_event(event)
        self._notify_changed()
    
    def change_category(self, new_category: SwComponentTypeCategory) -> None:
        """Change the component category and publish event"""
        old_category = self.category
        self.category = new_category
        
        # Add domain event
        from ..domain_events import SwComponentTypeUpdated
        event = SwComponentTypeUpdated(
            component_id=self.id,
            component_name=self.short_name,
            changes={'category': {'old': old_category.value, 'new': new_category.value}},
            source='SwComponentType'
        )
        self.add_domain_event(event)
        self._notify_changed()
    
    def validate_invariants(self) -> List[str]:
        """Validate business invariants"""
        violations = []
        
        if not self.short_name or not self.short_name.strip():
            violations.append("Component name cannot be empty")
        
        if not self.category:
            violations.append("Component category must be specified")
        
        # Check for duplicate port names
        port_names = [port.short_name for port in self.ports]
        if len(port_names) != len(set(port_names)):
            violations.append("Port names must be unique within a component")
        
        return violations
    
    def get_ports_by_type(self, port_type: PortType) -> List[PortPrototype]:
        """Get ports by type"""
        return [port for port in self.ports if port.port_type == port_type]

class ApplicationSwComponentType(SwComponentType):
    """Application software component type"""
    def __init__(self, short_name: str, desc: Optional[str] = None):
        super().__init__(short_name, SwComponentTypeCategory.APPLICATION, desc)

class AtomicSwComponentType(SwComponentType):
    """Atomic software component type"""
    def __init__(self, short_name: str, desc: Optional[str] = None, implementation_ref: Optional[str] = None):
        super().__init__(short_name, SwComponentTypeCategory.ATOMIC, desc)
        self.implementation_ref = implementation_ref

class CompositionSwComponentType(SwComponentType):
    """Composition software component type"""
    def __init__(self, short_name: str, desc: Optional[str] = None):
        super().__init__(short_name, SwComponentTypeCategory.COMPOSITION, desc)

class Composition(BaseElement):
    """Composition model"""
    def __init__(self, short_name: str, desc: Optional[str] = None):
        super().__init__(short_name, desc)
        self.component_types: List[SwComponentType] = []
        self.connections: List['PortConnection'] = []
    
    def add_component_type(self, component_type: SwComponentType):
        """Add a component type to the composition"""
        self.component_types.append(component_type)
    
    def remove_component_type(self, component_type: SwComponentType):
        """Remove a component type from the composition"""
        if component_type in self.component_types:
            self.component_types.remove(component_type)
    
    def add_connection(self, connection: 'PortConnection'):
        """Add a port connection to the composition"""
        self.connections.append(connection)
    
    def remove_connection(self, connection: 'PortConnection'):
        """Remove a port connection from the composition"""
        if connection in self.connections:
            self.connections.remove(connection)

class PortConnection:
    """Port connection model"""
    def __init__(self, source_port: PortPrototype, target_port: PortPrototype, connection_name: str):
        self.source_port = source_port
        self.target_port = target_port
        self.connection_name = connection_name
        # Automatically connect the ports
        self.source_port.connect_to(self.target_port)