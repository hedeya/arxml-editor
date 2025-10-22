# ARXML Editor - Architecture Improvement Roadmap

## Implementation Plan for SOLID & DDD Compliance

This document provides a detailed roadmap for implementing SOLID principles and Domain-Driven Design patterns in the ARXML Editor project.

---

## Phase 1: Dependency Injection & Service Abstractions (Weeks 1-2)

### Priority: HIGH | Impact: HIGH | Effort: MEDIUM

### 1.1 Create Service Interfaces

**Goal**: Abstract service dependencies to enable dependency inversion

**Implementation:**

```python
# File: src/core/interfaces/__init__.py
from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.arxml_document import ARXMLDocument
from ..models.autosar_elements import BaseElement

class ISchemaService(ABC):
    """Schema service interface"""
    
    @abstractmethod
    def set_version(self, version: str) -> bool:
        """Set AUTOSAR schema version"""
        pass
    
    @abstractmethod
    def validate_arxml(self, content: str) -> bool:
        """Validate ARXML content against schema"""
        pass
    
    @abstractmethod
    def detect_schema_version_from_file(self, file_path: str) -> Optional[str]:
        """Detect schema version from file"""
        pass
    
    @abstractmethod
    def get_available_versions(self) -> List[str]:
        """Get available schema versions"""
        pass

class IValidationService(ABC):
    """Validation service interface"""
    
    @abstractmethod
    def validate_document(self, document: ARXMLDocument) -> List['ValidationIssue']:
        """Validate entire document"""
        pass
    
    @abstractmethod
    def validate_element(self, element: BaseElement) -> List['ValidationIssue']:
        """Validate single element"""
        pass
    
    @abstractmethod
    def clear_issues(self) -> None:
        """Clear all validation issues"""
        pass

class ICommandService(ABC):
    """Command service interface"""
    
    @abstractmethod
    def execute_command(self, command: 'Command') -> bool:
        """Execute a command"""
        pass
    
    @abstractmethod
    def undo(self) -> bool:
        """Undo last command"""
        pass
    
    @abstractmethod
    def redo(self) -> bool:
        """Redo last undone command"""
        pass
    
    @abstractmethod
    def can_undo(self) -> bool:
        """Check if undo is possible"""
        pass
    
    @abstractmethod
    def can_redo(self) -> bool:
        """Check if redo is possible"""
        pass

class IARXMLParser(ABC):
    """ARXML parser interface"""
    
    @abstractmethod
    def parse_arxml_file(self, file_path: str) -> Optional['etree.Element']:
        """Parse ARXML file and return root element"""
        pass
    
    @abstractmethod
    def parse_sw_component_types(self, root: 'etree.Element') -> List['SwComponentType']:
        """Parse software component types from XML"""
        pass
```

### 1.2 Implement Dependency Injection Container

```python
# File: src/core/container.py
from typing import Dict, Type, TypeVar, Callable, Any
from .interfaces import *

T = TypeVar('T')

class DIContainer:
    """Dependency injection container"""
    
    def __init__(self):
        self._singletons: Dict[Type, Any] = {}
        self._transients: Dict[Type, Callable[[], Any]] = {}
        self._factories: Dict[Type, Callable[..., Any]] = {}
    
    def register_singleton(self, interface: Type[T], implementation: Type[T]) -> None:
        """Register a singleton service"""
        if interface in self._singletons:
            raise ValueError(f"Service {interface.__name__} already registered")
        
        # Create instance with dependency injection
        instance = self._create_instance(implementation)
        self._singletons[interface] = instance
    
    def register_transient(self, interface: Type[T], implementation: Type[T]) -> None:
        """Register a transient service"""
        self._transients[interface] = lambda: self._create_instance(implementation)
    
    def register_factory(self, interface: Type[T], factory: Callable[..., T]) -> None:
        """Register a factory function"""
        self._factories[interface] = factory
    
    def get(self, interface: Type[T]) -> T:
        """Get service instance"""
        # Check singletons first
        if interface in self._singletons:
            return self._singletons[interface]
        
        # Check transients
        if interface in self._transients:
            return self._transients[interface]()
        
        # Check factories
        if interface in self._factories:
            return self._factories[interface]()
        
        raise ValueError(f"Service {interface.__name__} not registered")
    
    def _create_instance(self, implementation: Type[T]) -> T:
        """Create instance with constructor injection"""
        import inspect
        
        # Get constructor signature
        sig = inspect.signature(implementation.__init__)
        params = {}
        
        # Resolve dependencies
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            
            param_type = param.annotation
            if param_type != inspect.Parameter.empty:
                # Try to resolve dependency
                try:
                    params[param_name] = self.get(param_type)
                except ValueError:
                    # Skip if dependency not registered
                    pass
        
        return implementation(**params)

# Container setup function
def setup_container() -> DIContainer:
    """Setup dependency injection container"""
    container = DIContainer()
    
    # Register services
    from .services.schema_service import SchemaService
    from .services.validation_service import ValidationService
    from .services.command_service import CommandService
    from .services.arxml_parser import ARXMLParser
    
    container.register_singleton(ISchemaService, SchemaService)
    container.register_singleton(IValidationService, ValidationService)
    container.register_singleton(ICommandService, CommandService)
    container.register_singleton(IARXMLParser, ARXMLParser)
    
    return container
```

### 1.3 Update Application Class

```python
# File: src/core/application.py (Updated)
from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal
from .container import DIContainer
from .interfaces import ISchemaService, IValidationService, ICommandService, IARXMLParser
from .models.arxml_document import ARXMLDocument

class ARXMLEditorApp(QObject):
    """Main application controller with dependency injection"""
    
    # Signals
    document_changed = pyqtSignal()
    validation_changed = pyqtSignal()
    command_stack_changed = pyqtSignal()
    
    def __init__(self, container: DIContainer):
        super().__init__()
        self._container = container
        self._current_document: Optional[ARXMLDocument] = None
        
        # Inject dependencies
        self._schema_service = container.get(ISchemaService)
        self._validation_service = container.get(IValidationService)
        self._command_service = container.get(ICommandService)
        self._arxml_parser = container.get(IARXMLParser)
        
        # Connect signals
        if hasattr(self._validation_service, 'validation_changed'):
            self._validation_service.validation_changed.connect(self.validation_changed)
        if hasattr(self._command_service, 'command_stack_changed'):
            self._command_service.command_stack_changed.connect(self.command_stack_changed)
    
    # Properties remain the same but return interfaces
    @property
    def validation_service(self) -> IValidationService:
        return self._validation_service
    
    @property
    def command_service(self) -> ICommandService:
        return self._command_service
    
    @property
    def schema_service(self) -> ISchemaService:
        return self._schema_service
    
    @property
    def arxml_parser(self) -> IARXMLParser:
        return self._arxml_parser
    
    # Methods remain largely the same
    def load_document(self, file_path: str) -> bool:
        """Load ARXML document with injected dependencies"""
        try:
            root = self._arxml_parser.parse_arxml_file(file_path)
            if root is None:
                return False
            
            self._current_document = ARXMLDocument()
            self._current_document.load_from_element(root, self._arxml_parser)
            
            self._validation_service.validate_document(self._current_document)
            self.document_changed.emit()
            return True
        except Exception as e:
            print(f"Error loading document: {e}")
            return False
```

---

## Phase 2: Repository Pattern Implementation (Weeks 3-4)

### Priority: HIGH | Impact: HIGH | Effort: MEDIUM

### 2.1 Create Repository Interfaces

```python
# File: src/core/repositories/__init__.py
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..models.autosar_elements import SwComponentType, PortInterface, ServiceInterface, Composition

class IRepository(ABC):
    """Base repository interface"""
    
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Any]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[Any]:
        pass
    
    @abstractmethod
    def save(self, entity: Any) -> bool:
        pass
    
    @abstractmethod
    def delete(self, entity: Any) -> bool:
        pass

class ISwComponentTypeRepository(IRepository):
    """Software component type repository interface"""
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[SwComponentType]:
        pass
    
    @abstractmethod
    def find_by_category(self, category: str) -> List[SwComponentType]:
        pass
    
    @abstractmethod
    def exists(self, name: str) -> bool:
        pass

class IPortInterfaceRepository(IRepository):
    """Port interface repository interface"""
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[PortInterface]:
        pass
    
    @abstractmethod
    def find_service_interfaces(self) -> List[PortInterface]:
        pass
    
    @abstractmethod
    def find_sender_receiver_interfaces(self) -> List[PortInterface]:
        pass

class ICompositionRepository(IRepository):
    """Composition repository interface"""
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Composition]:
        pass
    
    @abstractmethod
    def find_by_component_type(self, component_type: str) -> List[Composition]:
        pass
```

### 2.2 Implement In-Memory Repositories

```python
# File: src/core/repositories/memory_repositories.py
from typing import Dict, List, Optional, Callable, Any
from ..models.autosar_elements import SwComponentType, PortInterface, Composition
from . import ISwComponentTypeRepository, IPortInterfaceRepository, ICompositionRepository

class InMemorySwComponentTypeRepository(ISwComponentTypeRepository):
    """In-memory software component type repository"""
    
    def __init__(self):
        self._components: Dict[str, SwComponentType] = {}
        self._name_index: Dict[str, str] = {}  # name -> id mapping
    
    def find_by_id(self, id: str) -> Optional[SwComponentType]:
        return self._components.get(id)
    
    def find_by_name(self, name: str) -> Optional[SwComponentType]:
        component_id = self._name_index.get(name)
        return self._components.get(component_id) if component_id else None
    
    def find_by_category(self, category: str) -> List[SwComponentType]:
        return [comp for comp in self._components.values() 
                if comp.category and comp.category.value == category]
    
    def find_all(self) -> List[SwComponentType]:
        return list(self._components.values())
    
    def exists(self, name: str) -> bool:
        return name in self._name_index
    
    def save(self, component: SwComponentType) -> bool:
        try:
            # Generate ID if not present
            if not hasattr(component, 'id') or not component.id:
                component.id = f"comp_{len(self._components)}"
            
            self._components[component.id] = component
            self._name_index[component.short_name] = component.id
            return True
        except Exception:
            return False
    
    def delete(self, component: SwComponentType) -> bool:
        try:
            if hasattr(component, 'id') and component.id in self._components:
                del self._components[component.id]
                # Remove from name index
                for name, comp_id in list(self._name_index.items()):
                    if comp_id == component.id:
                        del self._name_index[name]
                        break
                return True
            return False
        except Exception:
            return False

class InMemoryPortInterfaceRepository(IPortInterfaceRepository):
    """In-memory port interface repository"""
    
    def __init__(self):
        self._interfaces: Dict[str, PortInterface] = {}
        self._name_index: Dict[str, str] = {}
    
    def find_by_id(self, id: str) -> Optional[PortInterface]:
        return self._interfaces.get(id)
    
    def find_by_name(self, name: str) -> Optional[PortInterface]:
        interface_id = self._name_index.get(name)
        return self._interfaces.get(interface_id) if interface_id else None
    
    def find_service_interfaces(self) -> List[PortInterface]:
        return [iface for iface in self._interfaces.values() if iface.is_service]
    
    def find_sender_receiver_interfaces(self) -> List[PortInterface]:
        return [iface for iface in self._interfaces.values() if not iface.is_service]
    
    def find_all(self) -> List[PortInterface]:
        return list(self._interfaces.values())
    
    def save(self, interface: PortInterface) -> bool:
        try:
            if not hasattr(interface, 'id') or not interface.id:
                interface.id = f"iface_{len(self._interfaces)}"
            
            self._interfaces[interface.id] = interface
            self._name_index[interface.short_name] = interface.id
            return True
        except Exception:
            return False
    
    def delete(self, interface: PortInterface) -> bool:
        try:
            if hasattr(interface, 'id') and interface.id in self._interfaces:
                del self._interfaces[interface.id]
                for name, iface_id in list(self._name_index.items()):
                    if iface_id == interface.id:
                        del self._name_index[name]
                        break
                return True
            return False
        except Exception:
            return False
```

### 2.3 Update ARXMLDocument with Repository Pattern

```python
# File: src/core/models/arxml_document.py (Updated sections)
from typing import Optional, List
from PyQt6.QtCore import QObject, pyqtSignal
from ..repositories import ISwComponentTypeRepository, IPortInterfaceRepository, ICompositionRepository
from .autosar_elements import SwComponentType, PortInterface, Composition

class ARXMLDocument(QObject):
    """ARXML document with repository pattern"""
    
    # Signals
    element_added = pyqtSignal(object)
    element_removed = pyqtSignal(object)
    element_modified = pyqtSignal(object)
    
    def __init__(self, 
                 sw_component_repo: ISwComponentTypeRepository,
                 port_interface_repo: IPortInterfaceRepository,
                 composition_repo: ICompositionRepository):
        super().__init__()
        self._sw_component_repo = sw_component_repo
        self._port_interface_repo = port_interface_repo
        self._composition_repo = composition_repo
        self._modified = False
        self._file_path: Optional[str] = None
    
    # Software Component Type operations
    def add_sw_component_type(self, component: SwComponentType) -> bool:
        """Add software component type through repository"""
        if self._sw_component_repo.exists(component.short_name):
            return False  # Already exists
        
        success = self._sw_component_repo.save(component)
        if success:
            self._modified = True
            self.element_added.emit(component)
        return success
    
    def remove_sw_component_type(self, component: SwComponentType) -> bool:
        """Remove software component type through repository"""
        success = self._sw_component_repo.delete(component)
        if success:
            self._modified = True
            self.element_removed.emit(component)
        return success
    
    def get_sw_component_type(self, name: str) -> Optional[SwComponentType]:
        """Get software component type by name"""
        return self._sw_component_repo.find_by_name(name)
    
    def get_all_sw_component_types(self) -> List[SwComponentType]:
        """Get all software component types"""
        return self._sw_component_repo.find_all()
    
    # Port Interface operations
    def add_port_interface(self, interface: PortInterface) -> bool:
        """Add port interface through repository"""
        success = self._port_interface_repo.save(interface)
        if success:
            self._modified = True
            self.element_added.emit(interface)
        return success
    
    def remove_port_interface(self, interface: PortInterface) -> bool:
        """Remove port interface through repository"""
        success = self._port_interface_repo.delete(interface)
        if success:
            self._modified = True
            self.element_removed.emit(interface)
        return success
    
    def get_port_interface(self, name: str) -> Optional[PortInterface]:
        """Get port interface by name"""
        return self._port_interface_repo.find_by_name(name)
    
    def get_all_port_interfaces(self) -> List[PortInterface]:
        """Get all port interfaces"""
        return self._port_interface_repo.find_all()
    
    def get_service_interfaces(self) -> List[PortInterface]:
        """Get only service interfaces"""
        return self._port_interface_repo.find_service_interfaces()
    
    # Properties for backward compatibility
    @property
    def sw_component_types(self) -> List[SwComponentType]:
        return self._sw_component_repo.find_all()
    
    @property
    def port_interfaces(self) -> List[PortInterface]:
        return self._port_interface_repo.find_all()
    
    @property
    def service_interfaces(self) -> List[PortInterface]:
        return self._port_interface_repo.find_service_interfaces()
    
    @property
    def modified(self) -> bool:
        return self._modified
    
    def set_modified(self, modified: bool):
        self._modified = modified
```

---

## Phase 3: Application Services Layer (Weeks 5-6)

### Priority: MEDIUM | Impact: MEDIUM | Effort: HIGH

### 3.1 Create Application Service Interfaces

```python
# File: src/core/application_services/__init__.py
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..models.autosar_elements import SwComponentType, PortInterface
from ..models.arxml_document import ARXMLDocument

class ApplicationServiceResult:
    """Result of application service operation"""
    
    def __init__(self, success: bool, message: str = "", data: Any = None):
        self.success = success
        self.message = message
        self.data = data

class ISwComponentTypeApplicationService(ABC):
    """Software component type application service interface"""
    
    @abstractmethod
    def create_component_type(self, name: str, category: str, description: str = "") -> ApplicationServiceResult:
        pass
    
    @abstractmethod
    def update_component_type(self, component_id: str, updates: Dict[str, Any]) -> ApplicationServiceResult:
        pass
    
    @abstractmethod
    def delete_component_type(self, component_id: str) -> ApplicationServiceResult:
        pass
    
    @abstractmethod
    def get_component_type_details(self, component_id: str) -> ApplicationServiceResult:
        pass
    
    @abstractmethod
    def validate_component_type(self, component: SwComponentType) -> ApplicationServiceResult:
        pass

class IPortInterfaceApplicationService(ABC):
    """Port interface application service interface"""
    
    @abstractmethod
    def create_port_interface(self, name: str, is_service: bool, description: str = "") -> ApplicationServiceResult:
        pass
    
    @abstractmethod
    def add_data_element(self, interface_id: str, element_name: str, data_type: str) -> ApplicationServiceResult:
        pass
    
    @abstractmethod
    def remove_data_element(self, interface_id: str, element_name: str) -> ApplicationServiceResult:
        pass
    
    @abstractmethod
    def validate_interface_compatibility(self, interface1_id: str, interface2_id: str) -> ApplicationServiceResult:
        pass

class IDocumentApplicationService(ABC):
    """Document application service interface"""
    
    @abstractmethod
    def create_new_document(self) -> ApplicationServiceResult:
        pass
    
    @abstractmethod
    def load_document(self, file_path: str) -> ApplicationServiceResult:
        pass
    
    @abstractmethod
    def save_document(self, file_path: str = None) -> ApplicationServiceResult:
        pass
    
    @abstractmethod
    def validate_document(self) -> ApplicationServiceResult:
        pass
    
    @abstractmethod
    def get_document_statistics(self) -> ApplicationServiceResult:
        pass
```

### 3.2 Implement Application Services

```python
# File: src/core/application_services/sw_component_type_service.py
from typing import Dict, Any
from ..interfaces import IValidationService, ICommandService
from ..repositories import ISwComponentTypeRepository
from ..models.autosar_elements import SwComponentType, SwComponentTypeCategory
from . import ISwComponentTypeApplicationService, ApplicationServiceResult

class SwComponentTypeApplicationService(ISwComponentTypeApplicationService):
    """Software component type application service implementation"""
    
    def __init__(self, 
                 repository: ISwComponentTypeRepository,
                 validation_service: IValidationService,
                 command_service: ICommandService):
        self._repository = repository
        self._validation_service = validation_service
        self._command_service = command_service
    
    def create_component_type(self, name: str, category: str, description: str = "") -> ApplicationServiceResult:
        """Create new software component type with validation"""
        try:
            # Validate input
            if not name or not name.strip():
                return ApplicationServiceResult(False, "Component name cannot be empty")
            
            if self._repository.exists(name):
                return ApplicationServiceResult(False, f"Component '{name}' already exists")
            
            # Validate category
            try:
                category_enum = SwComponentTypeCategory(category)
            except ValueError:
                return ApplicationServiceResult(False, f"Invalid category: {category}")
            
            # Create component
            component = SwComponentType(name, description, category_enum)
            
            # Validate component
            validation_result = self.validate_component_type(component)
            if not validation_result.success:
                return validation_result
            
            # Save through repository
            success = self._repository.save(component)
            if success:
                return ApplicationServiceResult(True, f"Component '{name}' created successfully", component)
            else:
                return ApplicationServiceResult(False, "Failed to save component")
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error creating component: {str(e)}")
    
    def update_component_type(self, component_id: str, updates: Dict[str, Any]) -> ApplicationServiceResult:
        """Update existing component type"""
        try:
            component = self._repository.find_by_id(component_id)
            if not component:
                return ApplicationServiceResult(False, f"Component with ID '{component_id}' not found")
            
            # Apply updates
            for field, value in updates.items():
                if hasattr(component, field):
                    setattr(component, field, value)
                else:
                    return ApplicationServiceResult(False, f"Invalid field: {field}")
            
            # Validate updated component
            validation_result = self.validate_component_type(component)
            if not validation_result.success:
                return validation_result
            
            # Save changes
            success = self._repository.save(component)
            if success:
                return ApplicationServiceResult(True, f"Component updated successfully", component)
            else:
                return ApplicationServiceResult(False, "Failed to save component changes")
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error updating component: {str(e)}")
    
    def delete_component_type(self, component_id: str) -> ApplicationServiceResult:
        """Delete component type with validation"""
        try:
            component = self._repository.find_by_id(component_id)
            if not component:
                return ApplicationServiceResult(False, f"Component with ID '{component_id}' not found")
            
            # Check if component is used in compositions
            # This would require additional repository queries
            # For now, we'll assume it's safe to delete
            
            success = self._repository.delete(component)
            if success:
                return ApplicationServiceResult(True, f"Component '{component.short_name}' deleted successfully")
            else:
                return ApplicationServiceResult(False, "Failed to delete component")
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error deleting component: {str(e)}")
    
    def get_component_type_details(self, component_id: str) -> ApplicationServiceResult:
        """Get detailed component information"""
        try:
            component = self._repository.find_by_id(component_id)
            if not component:
                return ApplicationServiceResult(False, f"Component with ID '{component_id}' not found")
            
            # Build detailed information
            details = {
                'id': component_id,
                'name': component.short_name,
                'description': component.desc or "",
                'category': component.category.value if component.category else "Unknown",
                'port_count': len(component.ports) if hasattr(component, 'ports') else 0,
                'composition_count': len(component.compositions) if hasattr(component, 'compositions') else 0
            }
            
            return ApplicationServiceResult(True, "Component details retrieved", details)
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error retrieving component details: {str(e)}")
    
    def validate_component_type(self, component: SwComponentType) -> ApplicationServiceResult:
        """Validate component type"""
        try:
            issues = self._validation_service.validate_element(component)
            
            if not issues:
                return ApplicationServiceResult(True, "Component is valid")
            
            # Filter for errors only
            errors = [issue for issue in issues if issue.severity.value == "error"]
            if errors:
                error_messages = [issue.message for issue in errors]
                return ApplicationServiceResult(False, f"Validation errors: {'; '.join(error_messages)}")
            
            # Only warnings
            warning_messages = [issue.message for issue in issues]
            return ApplicationServiceResult(True, f"Component valid with warnings: {'; '.join(warning_messages)}")
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error validating component: {str(e)}")
```

---

## Phase 4: Domain Events (Weeks 7-8)

### Priority: MEDIUM | Impact: MEDIUM | Effort: MEDIUM

### 4.1 Create Domain Event System

```python
# File: src/core/domain_events/__init__.py
from abc import ABC, abstractmethod
from typing import Any, List, Callable, Dict, Type
from datetime import datetime
import uuid

class DomainEvent(ABC):
    """Base domain event"""
    
    def __init__(self, aggregate_id: str, event_data: Dict[str, Any] = None):
        self.event_id = str(uuid.uuid4())
        self.aggregate_id = aggregate_id
        self.occurred_at = datetime.utcnow()
        self.event_data = event_data or {}

class SwComponentTypeCreated(DomainEvent):
    """Event raised when software component type is created"""
    
    def __init__(self, component_id: str, component_name: str, category: str):
        super().__init__(component_id, {
            'component_name': component_name,
            'category': category
        })

class SwComponentTypeDeleted(DomainEvent):
    """Event raised when software component type is deleted"""
    
    def __init__(self, component_id: str, component_name: str):
        super().__init__(component_id, {
            'component_name': component_name
        })

class PortInterfaceCreated(DomainEvent):
    """Event raised when port interface is created"""
    
    def __init__(self, interface_id: str, interface_name: str, is_service: bool):
        super().__init__(interface_id, {
            'interface_name': interface_name,
            'is_service': is_service
        })

class ValidationIssueDetected(DomainEvent):
    """Event raised when validation issue is detected"""
    
    def __init__(self, element_id: str, severity: str, message: str):
        super().__init__(element_id, {
            'severity': severity,
            'message': message
        })

class IDomainEventHandler(ABC):
    """Domain event handler interface"""
    
    @abstractmethod
    def handle(self, event: DomainEvent) -> None:
        pass

class DomainEventBus:
    """Domain event bus for publishing and subscribing to events"""
    
    def __init__(self):
        self._handlers: Dict[Type[DomainEvent], List[IDomainEventHandler]] = {}
    
    def subscribe(self, event_type: Type[DomainEvent], handler: IDomainEventHandler) -> None:
        """Subscribe handler to event type"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
    
    def publish(self, event: DomainEvent) -> None:
        """Publish event to all subscribers"""
        event_type = type(event)
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                try:
                    handler.handle(event)
                except Exception as e:
                    print(f"Error handling event {event_type.__name__}: {e}")
    
    def unsubscribe(self, event_type: Type[DomainEvent], handler: IDomainEventHandler) -> None:
        """Unsubscribe handler from event type"""
        if event_type in self._handlers:
            try:
                self._handlers[event_type].remove(handler)
            except ValueError:
                pass  # Handler not found
```

### 4.2 Create Event Handlers

```python
# File: src/core/domain_events/handlers.py
from ..interfaces import IValidationService
from . import IDomainEventHandler, DomainEvent, SwComponentTypeCreated, SwComponentTypeDeleted, PortInterfaceCreated

class ValidationEventHandler(IDomainEventHandler):
    """Handler for validation-related events"""
    
    def __init__(self, validation_service: IValidationService):
        self._validation_service = validation_service
    
    def handle(self, event: DomainEvent) -> None:
        """Handle validation events"""
        if isinstance(event, (SwComponentTypeCreated, PortInterfaceCreated)):
            # Trigger validation when new elements are created
            print(f"Triggering validation for new element: {event.aggregate_id}")
            # In real implementation, would validate the specific element

class AuditEventHandler(IDomainEventHandler):
    """Handler for audit logging"""
    
    def handle(self, event: DomainEvent) -> None:
        """Log all domain events for audit purposes"""
        print(f"AUDIT: {type(event).__name__} - {event.aggregate_id} at {event.occurred_at}")
        if hasattr(event, 'event_data'):
            print(f"  Data: {event.event_data}")

class UINotificationHandler(IDomainEventHandler):
    """Handler for UI notifications"""
    
    def __init__(self, notification_callback: Callable[[str], None]):
        self._notify = notification_callback
    
    def handle(self, event: DomainEvent) -> None:
        """Send notifications to UI"""
        if isinstance(event, SwComponentTypeCreated):
            self._notify(f"Component '{event.event_data['component_name']}' created")
        elif isinstance(event, SwComponentTypeDeleted):
            self._notify(f"Component '{event.event_data['component_name']}' deleted")
        elif isinstance(event, PortInterfaceCreated):
            interface_type = "Service" if event.event_data['is_service'] else "Sender-Receiver"
            self._notify(f"{interface_type} interface '{event.event_data['interface_name']}' created")
```

---

## Phase 5: Rich Domain Models (Weeks 9-10)

### Priority: MEDIUM | Impact: MEDIUM | Effort: MEDIUM

### 5.1 Enrich Domain Models with Behavior

```python
# File: src/core/models/autosar_elements.py (Enhanced)
from typing import List, Optional, Dict, Any
from enum import Enum
from PyQt6.QtCore import QObject, pyqtSignal
from ..domain_events import DomainEvent, DomainEventBus

class BaseElement(QObject):
    """Enhanced base class with domain behavior"""
    
    def __init__(self, short_name: str, desc: Optional[str] = None):
        super().__init__()
        self.id = None  # Will be set by repository
        self.short_name = short_name
        self.desc = desc
        self._domain_events: List[DomainEvent] = []
    
    def add_domain_event(self, event: DomainEvent) -> None:
        """Add domain event to be published"""
        self._domain_events.append(event)
    
    def clear_domain_events(self) -> List[DomainEvent]:
        """Clear and return domain events"""
        events = self._domain_events.copy()
        self._domain_events.clear()
        return events
    
    def validate_name(self, name: str) -> bool:
        """Validate element name according to AUTOSAR rules"""
        if not name or not name.strip():
            return False
        
        # AUTOSAR naming rules: alphanumeric + underscore, no spaces
        import re
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'
        return bool(re.match(pattern, name))
    
    def change_name(self, new_name: str) -> bool:
        """Change name with validation"""
        if not self.validate_name(new_name):
            return False
        
        old_name = self.short_name
        self.short_name = new_name
        
        # Raise domain event
        from ..domain_events import ElementNameChanged
        event = ElementNameChanged(self.id or "unknown", old_name, new_name)
        self.add_domain_event(event)
        
        return True

class SwComponentType(BaseElement):
    """Enhanced software component type with rich behavior"""
    
    def __init__(self, short_name: str, desc: Optional[str] = None, 
                 category: SwComponentTypeCategory = None):
        super().__init__(short_name, desc)
        self.category = category or SwComponentTypeCategory.APPLICATION
        self.ports: List[PortPrototype] = []
        self.compositions: List[Composition] = []
    
    def add_port(self, port: 'PortPrototype') -> bool:
        """Add port with validation"""
        # Validate port name uniqueness
        if any(p.short_name == port.short_name for p in self.ports):
            return False
        
        # Validate port type compatibility with component category
        if not self._is_port_compatible(port):
            return False
        
        self.ports.append(port)
        
        # Raise domain event
        from ..domain_events import PortAddedToComponent
        event = PortAddedToComponent(self.id or "unknown", port.short_name, port.port_type.value)
        self.add_domain_event(event)
        
        return True
    
    def remove_port(self, port_name: str) -> bool:
        """Remove port by name"""
        port_to_remove = next((p for p in self.ports if p.short_name == port_name), None)
        if not port_to_remove:
            return False
        
        self.ports.remove(port_to_remove)
        
        # Raise domain event
        from ..domain_events import PortRemovedFromComponent
        event = PortRemovedFromComponent(self.id or "unknown", port_name)
        self.add_domain_event(event)
        
        return True
    
    def get_provider_ports(self) -> List['PortPrototype']:
        """Get all provider ports"""
        return [p for p in self.ports if p.port_type == PortType.PROVIDER]
    
    def get_requirer_ports(self) -> List['PortPrototype']:
        """Get all requirer ports"""
        return [p for p in self.ports if p.port_type == PortType.REQUIRER]
    
    def can_connect_to(self, other: 'SwComponentType') -> bool:
        """Check if this component can connect to another component"""
        # Basic compatibility check: matching interfaces
        provider_interfaces = {p.interface_ref for p in self.get_provider_ports() if p.interface_ref}
        requirer_interfaces = {p.interface_ref for p in other.get_requirer_ports() if p.interface_ref}
        
        return bool(provider_interfaces.intersection(requirer_interfaces))
    
    def _is_port_compatible(self, port: 'PortPrototype') -> bool:
        """Check if port is compatible with component category"""
        # Composition components can have any port type
        if self.category == SwComponentTypeCategory.COMPOSITION:
            return True
        
        # Application components typically have provider or requirer ports
        if self.category == SwComponentTypeCategory.APPLICATION:
            return port.port_type in [PortType.PROVIDER, PortType.REQUIRER]
        
        return True
    
    def validate_invariants(self) -> List[str]:
        """Validate domain invariants"""
        violations = []
        
        # Rule 1: Component must have a valid name
        if not self.validate_name(self.short_name):
            violations.append("Component name must follow AUTOSAR naming conventions")
        
        # Rule 2: Application components should have at least one port
        if self.category == SwComponentTypeCategory.APPLICATION and not self.ports:
            violations.append("Application components should have at least one port")
        
        # Rule 3: Port names must be unique
        port_names = [p.short_name for p in self.ports]
        if len(port_names) != len(set(port_names)):
            violations.append("Port names must be unique within component")
        
        return violations

class PortInterface(BaseElement):
    """Enhanced port interface with rich behavior"""
    
    def __init__(self, short_name: str, desc: Optional[str] = None, is_service: bool = False):
        super().__init__(short_name, desc)
        self.is_service = is_service
        self.data_elements: List[DataElement] = []
        self.service_elements: List[ServiceElement] = []
    
    def add_data_element(self, data_element: 'DataElement') -> bool:
        """Add data element with validation"""
        # Check for name uniqueness
        if any(de.short_name == data_element.short_name for de in self.data_elements):
            return False
        
        # Service interfaces should not have data elements
        if self.is_service:
            return False
        
        self.data_elements.append(data_element)
        
        # Raise domain event
        from ..domain_events import DataElementAddedToInterface
        event = DataElementAddedToInterface(self.id or "unknown", data_element.short_name)
        self.add_domain_event(event)
        
        return True
    
    def add_service_element(self, service_element: 'ServiceElement') -> bool:
        """Add service element with validation"""
        # Check for name uniqueness
        if any(se.short_name == service_element.short_name for se in self.service_elements):
            return False
        
        # Only service interfaces can have service elements
        if not self.is_service:
            return False
        
        self.service_elements.append(service_element)
        
        # Raise domain event
        from ..domain_events import ServiceElementAddedToInterface
        event = ServiceElementAddedToInterface(self.id or "unknown", service_element.short_name)
        self.add_domain_event(event)
        
        return True
    
    def is_compatible_with(self, other: 'PortInterface') -> bool:
        """Check compatibility with another interface"""
        # Basic compatibility: same type and similar elements
        if self.is_service != other.is_service:
            return False
        
        if self.is_service:
            # Service interface compatibility based on service elements
            self_operations = {se.short_name for se in self.service_elements}
            other_operations = {se.short_name for se in other.service_elements}
            return self_operations == other_operations
        else:
            # Sender-receiver compatibility based on data elements
            self_data = {de.short_name for de in self.data_elements}
            other_data = {de.short_name for de in other.data_elements}
            return self_data == other_data
    
    def validate_invariants(self) -> List[str]:
        """Validate domain invariants"""
        violations = []
        
        # Rule 1: Interface name must be valid
        if not self.validate_name(self.short_name):
            violations.append("Interface name must follow AUTOSAR naming conventions")
        
        # Rule 2: Service interfaces must have service elements
        if self.is_service and not self.service_elements:
            violations.append("Service interfaces must have at least one service element")
        
        # Rule 3: Sender-receiver interfaces must have data elements
        if not self.is_service and not self.data_elements:
            violations.append("Sender-receiver interfaces must have at least one data element")
        
        return violations
```

---

## Implementation Timeline Summary

| Phase | Duration | Priority | Key Deliverables |
|-------|----------|----------|------------------|
| 1: DI & Interfaces | 2 weeks | HIGH | Service abstractions, DI container, loose coupling |
| 2: Repository Pattern | 2 weeks | HIGH | Data access abstraction, better testability |
| 3: Application Services | 2 weeks | MEDIUM | Business logic orchestration, use case handling |
| 4: Domain Events | 2 weeks | MEDIUM | Event-driven architecture, loose coupling |
| 5: Rich Domain Models | 2 weeks | MEDIUM | Domain behavior, business rule enforcement |

**Total Timeline: 10 weeks**

## Success Metrics

### Phase 1 Success Criteria:
- [ ] All services have interfaces
- [ ] DI container manages all dependencies  
- [ ] No hard-coded service instantiation
- [ ] Unit tests can mock dependencies

### Phase 2 Success Criteria:
- [ ] All data access goes through repositories
- [ ] Repository interfaces enable different implementations
- [ ] Domain logic separated from data access
- [ ] Query capabilities abstracted

### Phase 3 Success Criteria:
- [ ] Business logic orchestrated in application services
- [ ] UI only handles presentation concerns
- [ ] Complex operations properly coordinated
- [ ] Cross-cutting concerns handled consistently

### Phase 4 Success Criteria:
- [ ] Domain events published for all significant operations
- [ ] Event handlers process events independently
- [ ] Loose coupling between domain objects
- [ ] Audit trail and notifications working

### Phase 5 Success Criteria:
- [ ] Domain models contain business behavior
- [ ] Business rules enforced in domain objects
- [ ] Domain invariants validated consistently
- [ ] Rich domain vocabulary expressed in code

This roadmap provides a structured approach to transforming the ARXML Editor into a fully SOLID and DDD-compliant application while maintaining functionality and enabling future extensibility.