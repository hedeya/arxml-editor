"""
AUTOSAR Element Models
Strongly-typed classes for AUTOSAR elements
"""

from typing import List, Optional, Dict, Any, Union, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum
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

class BaseElement:
    """Base class for all AUTOSAR elements with event support"""
    
    def __init__(self, short_name: str, desc: Optional[str] = None):
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
    
    def set_ui_event_bus(self, ui_event_bus: 'UIEventBus') -> None:
        """Set the UI event bus for decoupled UI notifications"""
        self._ui_event_bus = ui_event_bus
    
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
        # Publish to UI event bus for decoupled UI notifications
        if self._ui_event_bus:
            self._ui_event_bus.publish("element_changed", self)

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
    
    def validate_invariants(self) -> List[str]:
        """Validate business invariants - to be overridden by subclasses"""
        violations = []
        
        # Common validation rules for all elements
        if not self.short_name or not self.short_name.strip():
            violations.append("Element name cannot be empty")
        
        if not self._is_valid_element_name(self.short_name):
            violations.append("Element name must follow AUTOSAR naming conventions")
        
        return violations
    
    def _is_valid_element_name(self, name: str) -> bool:
        """Validate element name follows AUTOSAR conventions"""
        if not name or not name.strip():
            return False
        
        import re
        # AUTOSAR names should be alphanumeric with underscores, no spaces
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'
        return bool(re.match(pattern, name.strip())) and len(name.strip()) <= 128
    
    def is_valid(self) -> bool:
        """Check if element is valid according to business rules"""
        return len(self.validate_invariants()) == 0
    
    def get_validation_errors(self) -> List[str]:
        """Get list of validation errors"""
        return [error for error in self.validate_invariants() if 'error' in error.lower() or 'cannot' in error.lower() or 'must' in error.lower()]
    
    def get_validation_warnings(self) -> List[str]:
        """Get list of validation warnings"""
        return [warning for warning in self.validate_invariants() if 'warning' in warning.lower()]
    
    def can_be_renamed(self, new_name: str) -> bool:
        """Check if element can be renamed to new name"""
        if not new_name or not new_name.strip():
            return False
        
        if not self._is_valid_element_name(new_name):
            return False
        
        # Additional checks can be added by subclasses
        return True
    
    def rename(self, new_name: str) -> bool:
        """Rename element with validation"""
        if not self.can_be_renamed(new_name):
            return False
        
        old_name = self.short_name
        self.short_name = new_name.strip()
        
        # Add domain event for rename
        from ..domain_events import ElementRenamed
        event = ElementRenamed(
            element_id=self.id,
            element_type=self.__class__.__name__,
            old_name=old_name,
            new_name=new_name.strip(),
            source=self.__class__.__name__
        )
        self.add_domain_event(event)
        self._notify_changed()
        
        return True
    
    def can_be_deleted(self) -> bool:
        """Check if element can be safely deleted - to be overridden by subclasses"""
        return True
    
    def get_dependencies(self) -> List[str]:
        """Get list of element dependencies - to be overridden by subclasses"""
        return []
    
    def has_dependencies(self) -> bool:
        """Check if element has dependencies"""
        return len(self.get_dependencies()) > 0

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
    
    def validate_invariants(self) -> List[str]:
        """Validate data element business invariants"""
        violations = super().validate_invariants()
        
        if not self.data_type:
            violations.append("Data type must be specified")
        
        if self.is_array and (not self.array_size or self.array_size <= 0):
            violations.append("Array size must be positive for array elements")
        
        if not self.is_array and self.array_size is not None:
            violations.append("Array size should not be specified for non-array elements")
        
        if self.min_value is not None and self.max_value is not None:
            if self.min_value > self.max_value:
                violations.append("Minimum value cannot be greater than maximum value")
        
        if self.unit and not self._is_valid_unit(self.unit):
            violations.append("Unit must follow AUTOSAR conventions")
        
        return violations
    
    def _is_valid_unit(self, unit: str) -> bool:
        """Validate unit follows AUTOSAR conventions"""
        import re
        # Units should be alphanumeric with common symbols
        pattern = r'^[a-zA-Z0-9/\\*^\-_]+$'
        return bool(re.match(pattern, unit)) and len(unit) <= 16
    
    def is_compatible_with(self, other: 'DataElement') -> bool:
        """Check if this data element is compatible with another"""
        if not other:
            return False
        
        # Check data type compatibility
        if self.data_type != other.data_type:
            return False
        
        # Check array compatibility
        if self.is_array != other.is_array:
            return False
        
        if self.is_array and self.array_size != other.array_size:
            return False
        
        return True
    
    def get_size_in_bytes(self) -> int:
        """Get estimated size in bytes based on data type"""
        type_sizes = {
            DataType.BOOLEAN: 1,
            DataType.INTEGER: 4,
            DataType.FLOAT: 4,
            DataType.STRING: 1,  # Per character
            DataType.ARRAY: 4,   # Per element
            DataType.STRUCTURE: 1  # Variable
        }
        
        base_size = type_sizes.get(self.data_type, 1)
        
        if self.is_array and self.array_size:
            return base_size * self.array_size
        
        return base_size
    
    def can_be_used_in_interface(self, interface: 'PortInterface') -> bool:
        """Check if this data element can be used in the given interface"""
        if not interface:
            return False
        
        # Service interfaces should not have data elements
        if interface.is_service:
            return False
        
        # Check for duplicate names
        if any(elem.short_name == self.short_name for elem in interface.data_elements):
            return False
        
        return True

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
        
        # Check naming conventions
        if not self._is_valid_interface_name(self.short_name):
            violations.append("Interface name must follow AUTOSAR naming conventions")
        
        # Check interface consistency
        if self.is_service and self.data_elements:
            violations.append("Service interfaces should not have data elements")
        
        if not self.is_service and self.service_elements:
            violations.append("Sender-receiver interfaces should not have service elements")
        
        # Validate data elements
        for elem in self.data_elements:
            if not self._is_valid_data_element_name(elem.short_name):
                violations.append(f"Data element '{elem.short_name}' has invalid name")
        
        return violations
    
    def _is_valid_interface_name(self, name: str) -> bool:
        """Validate interface name follows AUTOSAR conventions"""
        import re
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'
        return bool(re.match(pattern, name)) and len(name) <= 64
    
    def _is_valid_data_element_name(self, name: str) -> bool:
        """Validate data element name follows AUTOSAR conventions"""
        import re
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'
        return bool(re.match(pattern, name)) and len(name) <= 64
    
    def can_add_data_element(self, element: 'DataElement') -> bool:
        """Check if data element can be added to this interface"""
        if not element or not element.short_name:
            return False
        
        # Service interfaces cannot have data elements
        if self.is_service:
            return False
        
        # Check for duplicate names
        if any(elem.short_name == element.short_name for elem in self.data_elements):
            return False
        
        # Check naming conventions
        if not self._is_valid_data_element_name(element.short_name):
            return False
        
        return True
    
    def can_add_service_element(self, element: 'ServiceElement') -> bool:
        """Check if service element can be added to this interface"""
        if not element or not element.short_name:
            return False
        
        # Sender-receiver interfaces cannot have service elements
        if not self.is_service:
            return False
        
        # Check for duplicate names
        if any(elem.short_name == element.short_name for elem in self.service_elements):
            return False
        
        return True
    
    def get_data_types(self) -> List[str]:
        """Get all data types used in this interface"""
        return [elem.data_type.value if hasattr(elem.data_type, 'value') else str(elem.data_type) 
                for elem in self.data_elements if elem.data_type]
    
    def get_elements_by_type(self, data_type: str) -> List['DataElement']:
        """Get data elements by type"""
        return [elem for elem in self.data_elements 
                if elem.data_type and (elem.data_type.value == data_type if hasattr(elem.data_type, 'value') else str(elem.data_type) == data_type)]
    
    def is_compatible_with(self, other: 'PortInterface') -> bool:
        """Check if this interface is compatible with another interface"""
        if self.is_service != other.is_service:
            return False
        
        if self.is_service:
            # For service interfaces, check service elements
            return self._service_elements_compatible(other)
        else:
            # For sender-receiver interfaces, check data elements
            return self._data_elements_compatible(other)
    
    def _data_elements_compatible(self, other: 'PortInterface') -> bool:
        """Check if data elements are compatible"""
        if len(self.data_elements) != len(other.data_elements):
            return False
        
        # Check if all data elements match
        for elem in self.data_elements:
            matching = [e for e in other.data_elements if e.short_name == elem.short_name]
            if not matching:
                return False
            
            match = matching[0]
            if elem.data_type != match.data_type:
                return False
        
        return True
    
    def _service_elements_compatible(self, other: 'PortInterface') -> bool:
        """Check if service elements are compatible"""
        if len(self.service_elements) != len(other.service_elements):
            return False
        
        # Check if all service elements match
        for elem in self.service_elements:
            matching = [e for e in other.service_elements if e.short_name == elem.short_name]
            if not matching:
                return False
            
            match = matching[0]
            if elem.service_kind != match.service_kind:
                return False
        
        return True
    
    def get_usage_count(self) -> int:
        """Get number of times this interface is used (placeholder for future implementation)"""
        # This would require tracking interface usage across the document
        # For now, return 0 as a placeholder
        return 0
    
    def can_be_deleted(self) -> bool:
        """Check if interface can be safely deleted"""
        # Check if interface is used by any ports
        usage_count = self.get_usage_count()
        return usage_count == 0

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
    
    def connect_to(self, other_port: 'PortPrototype') -> bool:
        """Connect this port to another port"""
        if not self.can_connect_to(other_port):
            return False
        
        if other_port not in self.connected_ports:
            self.connected_ports.append(other_port)
        if self not in other_port.connected_ports:
            other_port.connected_ports.append(self)
        
        self._notify_changed()
        return True
    
    def disconnect_from(self, other_port: 'PortPrototype') -> bool:
        """Disconnect this port from another port"""
        if other_port not in self.connected_ports:
            return False
        
        self.connected_ports.remove(other_port)
        if self in other_port.connected_ports:
            other_port.connected_ports.remove(self)
        
        self._notify_changed()
        return True
    
    def can_connect_to(self, other_port: 'PortPrototype') -> bool:
        """Check if this port can connect to another port"""
        if not other_port or other_port == self:
            return False
        
        # Check port type compatibility
        if not self._are_port_types_compatible(self.port_type, other_port.port_type):
            return False
        
        # Check interface compatibility
        if self.interface and other_port.interface:
            if not self.interface.is_compatible_with(other_port.interface):
                return False
        
        # Check if already connected
        if other_port in self.connected_ports:
            return False
        
        return True
    
    def _are_port_types_compatible(self, type1: PortType, type2: PortType) -> bool:
        """Check if two port types are compatible for connection"""
        # P-PORT can connect to R-PORT
        if type1 == PortType.PROVIDER and type2 == PortType.REQUIRER:
            return True
        if type1 == PortType.REQUIRER and type2 == PortType.PROVIDER:
            return True
        
        # PR-PORT can connect to both P-PORT and R-PORT
        if type1 == PortType.PROVIDER_REQUIRER:
            return type2 in [PortType.PROVIDER, PortType.REQUIRER]
        if type2 == PortType.PROVIDER_REQUIRER:
            return type1 in [PortType.PROVIDER, PortType.REQUIRER]
        
        return False
    
    def validate_invariants(self) -> List[str]:
        """Validate port prototype business invariants"""
        violations = super().validate_invariants()
        
        if not self.port_type:
            violations.append("Port type must be specified")
        
        # Check interface reference consistency
        if self.interface_ref and not self.interface:
            violations.append("Port has interface reference but no interface object")
        
        if self.interface and not self.interface_ref:
            violations.append("Port has interface object but no interface reference")
        
        # Check connection consistency
        for connected_port in self.connected_ports:
            if not self._are_port_types_compatible(self.port_type, connected_port.port_type):
                violations.append(f"Port '{self.short_name}' has incompatible connection to '{connected_port.short_name}'")
        
        return violations
    
    def get_connection_count(self) -> int:
        """Get number of connections for this port"""
        return len(self.connected_ports)
    
    def is_connected(self) -> bool:
        """Check if port is connected"""
        return len(self.connected_ports) > 0
    
    def can_be_deleted(self) -> bool:
        """Check if port can be safely deleted"""
        # Ports with connections cannot be deleted
        return len(self.connected_ports) == 0
    
    def get_connected_port_names(self) -> List[str]:
        """Get names of all connected ports"""
        return [port.short_name for port in self.connected_ports]

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
        
        # Check naming conventions
        if not self._is_valid_component_name(self.short_name):
            violations.append("Component name must follow AUTOSAR naming conventions (alphanumeric, underscore, no spaces)")
        
        # Check port type consistency
        for port in self.ports:
            if port.port_type == PortType.PROVIDER_REQUIRER:
                # PR-PORTs should have both provider and requirer capabilities
                if not hasattr(port, 'interface') or not port.interface:
                    violations.append(f"PR-PORT '{port.short_name}' must have a valid interface reference")
        
        return violations
    
    def _is_valid_component_name(self, name: str) -> bool:
        """Validate component name follows AUTOSAR conventions"""
        import re
        # AUTOSAR names should be alphanumeric with underscores, no spaces
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'
        return bool(re.match(pattern, name)) and len(name) <= 128
    
    def can_add_port(self, port: 'PortPrototype') -> bool:
        """Check if port can be added to this component"""
        if not port or not port.short_name:
            return False
        
        # Check for duplicate names
        if any(p.short_name == port.short_name for p in self.ports):
            return False
        
        # Check naming conventions
        if not self._is_valid_port_name(port.short_name):
            return False
        
        return True
    
    def _is_valid_port_name(self, name: str) -> bool:
        """Validate port name follows AUTOSAR conventions"""
        import re
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'
        return bool(re.match(pattern, name)) and len(name) <= 64
    
    def get_ports_by_interface_type(self, is_service: bool) -> List['PortPrototype']:
        """Get ports by interface type (service vs sender-receiver)"""
        return [port for port in self.ports 
                if port.interface and port.interface.is_service == is_service]
    
    def get_connected_ports(self) -> List['PortPrototype']:
        """Get all ports that have connections"""
        return [port for port in self.ports if port.connected_ports]
    
    def get_unconnected_ports(self) -> List['PortPrototype']:
        """Get all ports that are not connected"""
        return [port for port in self.ports if not port.connected_ports]
    
    def is_fully_connected(self) -> bool:
        """Check if all ports are connected"""
        return len(self.get_unconnected_ports()) == 0
    
    def get_connection_count(self) -> int:
        """Get total number of port connections"""
        return sum(len(port.connected_ports) for port in self.ports)
    
    def can_be_deleted(self) -> bool:
        """Check if component can be safely deleted"""
        # Check if component is used in any compositions
        for composition in self.compositions:
            if self in composition.component_types:
                return False
        return True
    
    def get_dependencies(self) -> List[str]:
        """Get list of interface dependencies"""
        dependencies = []
        for port in self.ports:
            if port.interface_ref:
                dependencies.append(port.interface_ref)
        return list(set(dependencies))  # Remove duplicates
    
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
    
    def add_component_type(self, component_type: SwComponentType) -> bool:
        """Add a component type to the composition"""
        if not self.can_add_component_type(component_type):
            return False
        
        self.component_types.append(component_type)
        self._notify_changed()
        return True
    
    def remove_component_type(self, component_type: SwComponentType) -> bool:
        """Remove a component type from the composition"""
        if component_type not in self.component_types:
            return False
        
        # Remove all connections involving this component
        self._remove_connections_for_component(component_type)
        
        self.component_types.remove(component_type)
        self._notify_changed()
        return True
    
    def add_connection(self, connection: 'PortConnection') -> bool:
        """Add a port connection to the composition"""
        if not self.can_add_connection(connection):
            return False
        
        self.connections.append(connection)
        self._notify_changed()
        return True
    
    def remove_connection(self, connection: 'PortConnection') -> bool:
        """Remove a port connection from the composition"""
        if connection not in self.connections:
            return False
        
        self.connections.remove(connection)
        self._notify_changed()
        return True
    
    def can_add_component_type(self, component_type: SwComponentType) -> bool:
        """Check if component type can be added to this composition"""
        if not component_type:
            return False
        
        # Check for duplicate names
        if any(comp.short_name == component_type.short_name for comp in self.component_types):
            return False
        
        # Check if component is already in another composition
        if hasattr(component_type, 'compositions') and self in component_type.compositions:
            return False
        
        return True
    
    def can_add_connection(self, connection: 'PortConnection') -> bool:
        """Check if connection can be added to this composition"""
        if not connection or not connection.source_port or not connection.target_port:
            return False
        
        # Check if both ports belong to components in this composition
        source_component = self._find_component_for_port(connection.source_port)
        target_component = self._find_component_for_port(connection.target_port)
        
        if not source_component or not target_component:
            return False
        
        if source_component not in self.component_types or target_component not in self.component_types:
            return False
        
        # Check for duplicate connections
        if any(conn.source_port == connection.source_port and conn.target_port == connection.target_port 
               for conn in self.connections):
            return False
        
        return True
    
    def _find_component_for_port(self, port: 'PortPrototype') -> Optional[SwComponentType]:
        """Find the component that owns the given port"""
        for component in self.component_types:
            if port in component.ports:
                return component
        return None
    
    def _remove_connections_for_component(self, component: SwComponentType):
        """Remove all connections involving the given component"""
        connections_to_remove = []
        for connection in self.connections:
            source_component = self._find_component_for_port(connection.source_port)
            target_component = self._find_component_for_port(connection.target_port)
            
            if source_component == component or target_component == component:
                connections_to_remove.append(connection)
        
        for connection in connections_to_remove:
            self.connections.remove(connection)
    
    def get_connections_for_component(self, component: SwComponentType) -> List['PortConnection']:
        """Get all connections involving the given component"""
        connections = []
        for connection in self.connections:
            source_component = self._find_component_for_port(connection.source_port)
            target_component = self._find_component_for_port(connection.target_port)
            
            if source_component == component or target_component == component:
                connections.append(connection)
        
        return connections
    
    def get_connection_count(self) -> int:
        """Get total number of connections in this composition"""
        return len(self.connections)
    
    def get_component_count(self) -> int:
        """Get total number of components in this composition"""
        return len(self.component_types)
    
    def is_fully_connected(self) -> bool:
        """Check if all components are fully connected"""
        for component in self.component_types:
            if not component.is_fully_connected():
                return False
        return True
    
    def get_unconnected_ports(self) -> List['PortPrototype']:
        """Get all unconnected ports in this composition"""
        unconnected = []
        for component in self.component_types:
            unconnected.extend(component.get_unconnected_ports())
        return unconnected
    
    def validate_composition_integrity(self) -> List[str]:
        """Validate composition-level business rules"""
        violations = []
        
        # Check for duplicate component names
        component_names = [comp.short_name for comp in self.component_types]
        if len(component_names) != len(set(component_names)):
            violations.append("Component names must be unique within a composition")
        
        # Check for orphaned connections
        for connection in self.connections:
            source_component = self._find_component_for_port(connection.source_port)
            target_component = self._find_component_for_port(connection.target_port)
            
            if not source_component:
                violations.append(f"Connection source port '{connection.source_port.short_name}' not found in composition")
            
            if not target_component:
                violations.append(f"Connection target port '{connection.target_port.short_name}' not found in composition")
        
        # Check for interface compatibility
        for connection in self.connections:
            if connection.source_port.interface and connection.target_port.interface:
                if not connection.source_port.interface.is_compatible_with(connection.target_port.interface):
                    violations.append(f"Interface mismatch between '{connection.source_port.short_name}' and '{connection.target_port.short_name}'")
        
        return violations

class PortConnection:
    """Port connection model"""
    def __init__(self, source_port: PortPrototype, target_port: PortPrototype, connection_name: str):
        self.source_port = source_port
        self.target_port = target_port
        self.connection_name = connection_name
        # Automatically connect the ports
        self.source_port.connect_to(self.target_port)