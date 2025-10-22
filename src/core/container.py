"""
Dependency Injection Container
Manages service registration and resolution with constructor injection
"""

from typing import Dict, Type, TypeVar, Callable, Any, get_type_hints
import inspect
from .interfaces import *
from .repositories import IRepositoryFactory
from .repositories.memory_repositories import InMemoryRepositoryFactory
from .application_services import (
    ISwComponentTypeApplicationService, IPortInterfaceApplicationService,
    IDocumentApplicationService, IValidationApplicationService
)
from .application_services.sw_component_type_service import SwComponentTypeApplicationService
from .application_services.port_interface_service import PortInterfaceApplicationService
from .application_services.document_service import DocumentApplicationService
from .domain_events import IEventBus
from .domain_events.event_bus import EventBusFactory
from .domain_events.handlers import (
    LoggingEventHandler, AuditEventHandler, ValidationEventHandler,
    UINotificationHandler, MetricsEventHandler, PersistenceEventHandler,
    EventHandlerRegistry
)

T = TypeVar('T')

class DIContainer:
    """Dependency injection container with constructor injection support"""
    
    def __init__(self):
        self._singletons: Dict[Type, Any] = {}
        self._transients: Dict[Type, Callable[[], Any]] = {}
        self._factories: Dict[Type, Callable[..., Any]] = {}
        self._registrations: Dict[Type, Type] = {}
    
    def register_singleton(self, interface: Type[T], implementation: Type[T]) -> None:
        """Register a singleton service"""
        if interface in self._singletons:
            raise ValueError(f"Service {interface.__name__} already registered as singleton")
        
        self._registrations[interface] = implementation
        # Don't create instance yet - lazy initialization
    
    def register_transient(self, interface: Type[T], implementation: Type[T]) -> None:
        """Register a transient service"""
        self._transients[interface] = lambda: self._create_instance(implementation)
    
    def register_factory(self, interface: Type[T], factory: Callable[..., T]) -> None:
        """Register a factory function"""
        self._factories[interface] = factory
    
    def register_instance(self, interface: Type[T], instance: T) -> None:
        """Register an existing instance"""
        self._singletons[interface] = instance
    
    def get(self, interface: Type[T]) -> T:
        """Get service instance"""
        # Check existing singletons first
        if interface in self._singletons:
            return self._singletons[interface]
        
        # Check if registered as singleton but not yet created
        if interface in self._registrations:
            implementation = self._registrations[interface]
            instance = self._create_instance(implementation)
            self._singletons[interface] = instance
            return instance
        
        # Check transients
        if interface in self._transients:
            return self._transients[interface]()
        
        # Check factories
        if interface in self._factories:
            return self._factories[interface]()
        
        raise ValueError(f"Service {interface.__name__} not registered")
    
    def _create_instance(self, implementation: Type[T]) -> T:
        """Create instance with constructor injection"""
        try:
            # Get constructor signature
            sig = inspect.signature(implementation.__init__)
            params = {}
            
            # Try to get type hints for better parameter resolution
            try:
                type_hints = get_type_hints(implementation.__init__)
            except (NameError, AttributeError):
                type_hints = {}
            
            # Resolve dependencies
            for param_name, param in sig.parameters.items():
                if param_name == 'self':
                    continue
                
                # Try type hint first
                param_type = type_hints.get(param_name, param.annotation)
                
                if param_type != inspect.Parameter.empty and param_type != Any:
                    # Try to resolve dependency
                    try:
                        params[param_name] = self.get(param_type)
                    except ValueError:
                        # For constructor parameters that expect a repository, use IRepositoryFactory if available.
                        # This avoids fragile string matching; instead map known repository interfaces to factory methods.
                        try:
                            repo_factory = self.get(IRepositoryFactory)
                        except ValueError:
                            repo_factory = None

                        if repo_factory is not None and (isinstance(param_type, type) and param_type.__name__.endswith('Repository') or 'Repository' in str(param_type)):
                            # mapping of repository interface name substrings to factory methods
                            mapping = {
                                'ISwComponentTypeRepository': 'create_sw_component_type_repository',
                                'IPortInterfaceRepository': 'create_port_interface_repository',
                                'IServiceInterfaceRepository': 'create_service_interface_repository',
                                'ICompositionRepository': 'create_composition_repository',
                                'IPortPrototypeRepository': 'create_port_prototype_repository',
                                'IDataElementRepository': 'create_data_element_repository',
                            }

                            chosen = None
                            # Try to match by annotated type name
                            type_name = getattr(param_type, '__name__', str(param_type))
                            for key, factory_name in mapping.items():
                                if key in type_name or key.replace('I', '') in type_name:
                                    chosen = factory_name
                                    break

                            # As a fallback, try to match common substrings
                            if not chosen:
                                if 'SwComponentType' in type_name:
                                    chosen = 'create_sw_component_type_repository'
                                elif 'PortInterface' in type_name:
                                    chosen = 'create_port_interface_repository'
                                elif 'ServiceInterface' in type_name:
                                    chosen = 'create_service_interface_repository'
                                elif 'Composition' in type_name:
                                    chosen = 'create_composition_repository'

                            if chosen and hasattr(repo_factory, chosen):
                                try:
                                    params[param_name] = getattr(repo_factory, chosen)()
                                except Exception:
                                    print(f"Warning: repository factory method {chosen} failed for {implementation.__name__}")
                            else:
                                # Nothing matched; warn but continue
                                print(f"Warning: Could not resolve repository dependency {param_name}: {param_type} for {implementation.__name__}")
                        else:
                            # Skip if dependency not registered and parameter has default
                            if param.default == inspect.Parameter.empty:
                                print(f"Warning: Could not resolve dependency {param_name}: {param_type} for {implementation.__name__}")
            
            return implementation(**params)
        
        except Exception as e:
            print(f"Error creating instance of {implementation.__name__}: {e}")
            # Fallback to parameterless constructor
            try:
                return implementation()
            except Exception as fallback_error:
                raise ValueError(f"Could not create instance of {implementation.__name__}: {fallback_error}")

def setup_container() -> DIContainer:
    """Setup dependency injection container with all services"""
    container = DIContainer()
    
    # Import concrete implementations
    from .services.schema_service import SchemaService
    from .services.validation_service import ValidationService
    from .services.command_service import CommandService
    from .services.arxml_parser import ARXMLParser
    
    # Register core services as singletons
    container.register_singleton(ISchemaService, SchemaService)
    container.register_singleton(IValidationService, ValidationService)
    container.register_singleton(ICommandService, CommandService)
    container.register_singleton(IARXMLParser, ARXMLParser)
    
    # Register repository factory
    container.register_singleton(IRepositoryFactory, InMemoryRepositoryFactory)
    
    # Register event bus
    container.register_singleton(IEventBus, EventBusFactory.create_sync_bus)

    # Register UI event bus and adapter (decouples domain -> UI signals)
    try:
        from .events.ui_event_bus import UIEventBus
        from ..ui.adapters.ui_event_adapter import UIEventAdapter
        # register a shared UIEventBus instance
        ui_bus = UIEventBus()
        container.register_instance(UIEventBus, ui_bus)
        # create and register adapter to bridge bus to Qt signals for legacy UI
        ui_adapter = UIEventAdapter(ui_bus)
        container.register_instance(UIEventAdapter, ui_adapter)
    except Exception:
        # If UI modules not available in headless contexts, skip silently
        pass
    
    # Register event handlers
    def setup_event_handlers():
        event_bus = container.get(IEventBus)
        handler_registry = EventHandlerRegistry()
        
        # Create and register handlers
        logging_handler = LoggingEventHandler()
        audit_handler = AuditEventHandler()
        validation_handler = ValidationEventHandler()
        ui_handler = UINotificationHandler()
        metrics_handler = MetricsEventHandler()
        persistence_handler = PersistenceEventHandler()
        
        handler_registry.register_handler(logging_handler)
        handler_registry.register_handler(audit_handler)
        handler_registry.register_handler(validation_handler)
        handler_registry.register_handler(ui_handler)
        handler_registry.register_handler(metrics_handler)
        handler_registry.register_handler(persistence_handler)
        
        # Subscribe handlers to event bus
        from .domain_events import DomainEvent
        for handler in handler_registry.get_all_handlers():
            event_bus.subscribe(DomainEvent, handler.handle)
        
        return handler_registry
    
    container.register_singleton(EventHandlerRegistry, setup_event_handlers)
    
    # Register application services with factory functions
    def create_sw_component_service():
        repo_factory = container.get(IRepositoryFactory)
        validation_service = container.get(IValidationService)
        command_service = container.get(ICommandService)
        event_bus = container.get(IEventBus)
        return SwComponentTypeApplicationService(
            repo_factory.create_sw_component_type_repository(),
            validation_service,
            command_service,
            event_bus
        )
    
    def create_port_interface_service():
        repo_factory = container.get(IRepositoryFactory)
        validation_service = container.get(IValidationService)
        command_service = container.get(ICommandService)
        event_bus = container.get(IEventBus)
        return PortInterfaceApplicationService(
            repo_factory.create_port_interface_repository(),
            validation_service,
            command_service,
            event_bus
        )
    
    def create_document_service():
        repo_factory = container.get(IRepositoryFactory)
        validation_service = container.get(IValidationService)
        arxml_parser = container.get(IARXMLParser)
        event_bus = container.get(IEventBus)
        return DocumentApplicationService(
            repo_factory,
            validation_service,
            arxml_parser,
            event_bus
        )
    
    container.register_factory(ISwComponentTypeApplicationService, create_sw_component_service)
    container.register_factory(IPortInterfaceApplicationService, create_port_interface_service)
    container.register_factory(IDocumentApplicationService, create_document_service)
    
    return container