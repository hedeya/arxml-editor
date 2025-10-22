"""
In-Memory Repository Implementations
Concrete implementations of repository interfaces using in-memory storage
"""

import re
from typing import Dict, List, Optional, TypeVar, Generic
from . import (
    IRepository, ISwComponentTypeRepository, IPortInterfaceRepository,
    IServiceInterfaceRepository, ICompositionRepository, IPortPrototypeRepository,
    IDataElementRepository, IRepositoryFactory
)
from ..models.autosar_elements import (
    SwComponentType, PortInterface, ServiceInterface, Composition,
    PortPrototype, DataElement, ServiceElement, SwComponentTypeCategory
)

T = TypeVar('T')

class InMemoryRepository(IRepository[T], Generic[T]):
    """Base in-memory repository implementation"""
    
    def __init__(self):
        self._entities: Dict[str, T] = {}
        self._name_index: Dict[str, str] = {}  # name -> id mapping
        self._next_id = 1
    
    def _generate_id(self) -> str:
        """Generate unique ID"""
        id = f"{self.__class__.__name__.lower()}_{self._next_id}"
        self._next_id += 1
        return id
    
    def _get_entity_name(self, entity: T) -> str:
        """Get entity name for indexing"""
        if hasattr(entity, 'short_name'):
            return entity.short_name
        return str(entity)
    
    def find_by_id(self, id: str) -> Optional[T]:
        """Find entity by ID"""
        return self._entities.get(id)
    
    def find_all(self) -> List[T]:
        """Find all entities"""
        return list(self._entities.values())
    
    def save(self, entity: T) -> bool:
        """Save entity"""
        try:
            # Generate ID if not present
            if not hasattr(entity, 'id') or not entity.id:
                entity.id = self._generate_id()
            
            # Update name index
            entity_name = self._get_entity_name(entity)
            if entity_name in self._name_index:
                # Update existing entry
                old_id = self._name_index[entity_name]
                if old_id != entity.id:
                    # Name changed, remove old entry
                    if old_id in self._entities:
                        del self._entities[old_id]
            
            self._entities[entity.id] = entity
            self._name_index[entity_name] = entity.id
            return True
        except Exception as e:
            print(f"Error saving entity: {e}")
            return False
    
    def delete(self, entity: T) -> bool:
        """Delete entity"""
        try:
            if hasattr(entity, 'id') and entity.id in self._entities:
                # Remove from name index
                entity_name = self._get_entity_name(entity)
                if entity_name in self._name_index:
                    del self._name_index[entity_name]
                
                del self._entities[entity.id]
                return True
            return False
        except Exception as e:
            print(f"Error deleting entity: {e}")
            return False
    
    def exists(self, id: str) -> bool:
        """Check if entity exists by ID"""
        return id in self._entities
    
    def find_by_name_pattern(self, pattern: str) -> List[T]:
        """Find entities by name pattern using regex"""
        try:
            regex = re.compile(pattern, re.IGNORECASE)
            matches = []
            for entity in self._entities.values():
                entity_name = self._get_entity_name(entity)
                if regex.search(entity_name):
                    matches.append(entity)
            return matches
        except Exception as e:
            print(f"Error searching by pattern: {e}")
            return []

class InMemorySwComponentTypeRepository(InMemoryRepository[SwComponentType], ISwComponentTypeRepository):
    """In-memory software component type repository"""
    
    def find_by_name(self, name: str) -> Optional[SwComponentType]:
        """Find component type by name"""
        component_id = self._name_index.get(name)
        return self._entities.get(component_id) if component_id else None
    
    def find_by_category(self, category: str) -> List[SwComponentType]:
        """Find component types by category"""
        results = []
        for comp in self._entities.values():
            cat = getattr(comp, 'category', None)
            # support Enum with .value or plain string
            if cat is None:
                continue
            if hasattr(cat, 'value') and cat.value == category:
                results.append(comp)
            elif isinstance(cat, str) and cat == category:
                results.append(comp)
            else:
                # also allow name match
                if hasattr(cat, 'name') and cat.name == category:
                    results.append(comp)
        return results
    
    def exists_by_name(self, name: str) -> bool:
        """Check if component type exists by name"""
        return name in self._name_index

class InMemoryPortInterfaceRepository(InMemoryRepository[PortInterface], IPortInterfaceRepository):
    """In-memory port interface repository"""
    
    def find_by_name(self, name: str) -> Optional[PortInterface]:
        """Find port interface by name"""
        interface_id = self._name_index.get(name)
        return self._entities.get(interface_id) if interface_id else None
    
    def find_service_interfaces(self) -> List[PortInterface]:
        """Find all service interfaces"""
        return [iface for iface in self._entities.values() if iface.is_service]
    
    def find_sender_receiver_interfaces(self) -> List[PortInterface]:
        """Find all sender-receiver interfaces"""
        return [iface for iface in self._entities.values() if not iface.is_service]
    
    def exists_by_name(self, name: str) -> bool:
        """Check if port interface exists by name"""
        return name in self._name_index

class InMemoryServiceInterfaceRepository(InMemoryRepository[ServiceInterface], IServiceInterfaceRepository):
    """In-memory service interface repository"""
    
    def find_by_name(self, name: str) -> Optional[ServiceInterface]:
        """Find service interface by name"""
        interface_id = self._name_index.get(name)
        return self._entities.get(interface_id) if interface_id else None
    
    def exists_by_name(self, name: str) -> bool:
        """Check if service interface exists by name"""
        return name in self._name_index

class InMemoryCompositionRepository(InMemoryRepository[Composition], ICompositionRepository):
    """In-memory composition repository"""
    
    def find_by_name(self, name: str) -> Optional[Composition]:
        """Find composition by name"""
        composition_id = self._name_index.get(name)
        return self._entities.get(composition_id) if composition_id else None
    
    def find_by_component_type(self, component_type: str) -> List[Composition]:
        """Find compositions containing specific component type"""
        matches = []
        for composition in self._entities.values():
            for comp_type in composition.component_types:
                if comp_type.short_name == component_type:
                    matches.append(composition)
                    break
        return matches
    
    def exists_by_name(self, name: str) -> bool:
        """Check if composition exists by name"""
        return name in self._name_index

class InMemoryPortPrototypeRepository(InMemoryRepository[PortPrototype], IPortPrototypeRepository):
    """In-memory port prototype repository"""
    
    def find_by_name(self, name: str) -> Optional[PortPrototype]:
        """Find port prototype by name"""
        port_id = self._name_index.get(name)
        return self._entities.get(port_id) if port_id else None
    
    def find_by_component(self, component_id: str) -> List[PortPrototype]:
        """Find port prototypes by component ID"""
        # This would require a component_id field on PortPrototype
        # For now, return empty list
        return []
    
    def find_by_type(self, port_type: str) -> List[PortPrototype]:
        """Find port prototypes by type"""
        return [port for port in self._entities.values() 
                if port.port_type and port.port_type.value == port_type]
    
    def find_connected_ports(self, port_id: str) -> List[PortPrototype]:
        """Find ports connected to specific port"""
        port = self._entities.get(port_id)
        if port and hasattr(port, 'connected_ports'):
            return port.connected_ports
        return []
    
    def exists_by_name(self, name: str) -> bool:
        """Check if port prototype exists by name"""
        return name in self._name_index

class InMemoryDataElementRepository(InMemoryRepository[DataElement], IDataElementRepository):
    """In-memory data element repository"""
    
    def find_by_name(self, name: str) -> Optional[DataElement]:
        """Find data element by name"""
        element_id = self._name_index.get(name)
        return self._entities.get(element_id) if element_id else None
    
    def find_by_interface(self, interface_id: str) -> List[DataElement]:
        """Find data elements by interface ID"""
        # This would require tracking interface relationships
        # For now, return empty list
        return []
    
    def find_by_type(self, data_type: str) -> List[DataElement]:
        """Find data elements by type"""
        results = []
        for elem in self._entities.values():
            dt = getattr(elem, 'data_type', None)
            if dt is None:
                continue
            if hasattr(dt, 'value') and dt.value == data_type:
                results.append(elem)
            elif isinstance(dt, str) and dt == data_type:
                results.append(elem)
        return results
    
    def exists_by_name(self, name: str) -> bool:
        """Check if data element exists by name"""
        return name in self._name_index

class InMemoryRepositoryFactory(IRepositoryFactory):
    """In-memory repository factory"""
    
    def create_sw_component_type_repository(self) -> ISwComponentTypeRepository:
        """Create software component type repository"""
        return InMemorySwComponentTypeRepository()
    
    def create_port_interface_repository(self) -> IPortInterfaceRepository:
        """Create port interface repository"""
        return InMemoryPortInterfaceRepository()
    
    def create_service_interface_repository(self) -> IServiceInterfaceRepository:
        """Create service interface repository"""
        return InMemoryServiceInterfaceRepository()
    
    def create_composition_repository(self) -> ICompositionRepository:
        """Create composition repository"""
        return InMemoryCompositionRepository()
    
    def create_port_prototype_repository(self) -> IPortPrototypeRepository:
        """Create port prototype repository"""
        return InMemoryPortPrototypeRepository()
    
    def create_data_element_repository(self) -> IDataElementRepository:
        """Create data element repository"""
        return InMemoryDataElementRepository()