"""
Repository Interfaces
Abstract interfaces for data access layer following Repository pattern
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, TypeVar, Generic
from ..models.autosar_elements import (
    SwComponentType, PortInterface, ServiceInterface, Composition,
    PortPrototype, DataElement, ServiceElement
)

T = TypeVar('T')

class IRepository(ABC, Generic[T]):
    """Base repository interface"""
    
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[T]:
        """Find entity by ID"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[T]:
        """Find all entities"""
        pass
    
    @abstractmethod
    def save(self, entity: T) -> bool:
        """Save entity"""
        pass
    
    @abstractmethod
    def delete(self, entity: T) -> bool:
        """Delete entity"""
        pass
    
    @abstractmethod
    def exists(self, id: str) -> bool:
        """Check if entity exists by ID"""
        pass

class ISwComponentTypeRepository(IRepository[SwComponentType]):
    """Software component type repository interface"""
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[SwComponentType]:
        """Find component type by name"""
        pass
    
    @abstractmethod
    def find_by_category(self, category: str) -> List[SwComponentType]:
        """Find component types by category"""
        pass
    
    @abstractmethod
    def find_by_name_pattern(self, pattern: str) -> List[SwComponentType]:
        """Find component types by name pattern"""
        pass
    
    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        """Check if component type exists by name"""
        pass

class IPortInterfaceRepository(IRepository[PortInterface]):
    """Port interface repository interface"""
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[PortInterface]:
        """Find port interface by name"""
        pass
    
    @abstractmethod
    def find_service_interfaces(self) -> List[PortInterface]:
        """Find all service interfaces"""
        pass
    
    @abstractmethod
    def find_sender_receiver_interfaces(self) -> List[PortInterface]:
        """Find all sender-receiver interfaces"""
        pass
    
    @abstractmethod
    def find_by_name_pattern(self, pattern: str) -> List[PortInterface]:
        """Find port interfaces by name pattern"""
        pass
    
    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        """Check if port interface exists by name"""
        pass

class IServiceInterfaceRepository(IRepository[ServiceInterface]):
    """Service interface repository interface"""
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[ServiceInterface]:
        """Find service interface by name"""
        pass
    
    @abstractmethod
    def find_by_name_pattern(self, pattern: str) -> List[ServiceInterface]:
        """Find service interfaces by name pattern"""
        pass
    
    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        """Check if service interface exists by name"""
        pass

class ICompositionRepository(IRepository[Composition]):
    """Composition repository interface"""
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Composition]:
        """Find composition by name"""
        pass
    
    @abstractmethod
    def find_by_component_type(self, component_type: str) -> List[Composition]:
        """Find compositions containing specific component type"""
        pass
    
    @abstractmethod
    def find_by_name_pattern(self, pattern: str) -> List[Composition]:
        """Find compositions by name pattern"""
        pass
    
    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        """Check if composition exists by name"""
        pass

class IPortPrototypeRepository(IRepository[PortPrototype]):
    """Port prototype repository interface"""
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[PortPrototype]:
        """Find port prototype by name"""
        pass
    
    @abstractmethod
    def find_by_component(self, component_id: str) -> List[PortPrototype]:
        """Find port prototypes by component ID"""
        pass
    
    @abstractmethod
    def find_by_type(self, port_type: str) -> List[PortPrototype]:
        """Find port prototypes by type"""
        pass
    
    @abstractmethod
    def find_connected_ports(self, port_id: str) -> List[PortPrototype]:
        """Find ports connected to specific port"""
        pass
    
    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        """Check if port prototype exists by name"""
        pass

class IDataElementRepository(IRepository[DataElement]):
    """Data element repository interface"""
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[DataElement]:
        """Find data element by name"""
        pass
    
    @abstractmethod
    def find_by_interface(self, interface_id: str) -> List[DataElement]:
        """Find data elements by interface ID"""
        pass
    
    @abstractmethod
    def find_by_type(self, data_type: str) -> List[DataElement]:
        """Find data elements by type"""
        pass
    
    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        """Check if data element exists by name"""
        pass

class IRepositoryFactory(ABC):
    """Repository factory interface"""
    
    @abstractmethod
    def create_sw_component_type_repository(self) -> ISwComponentTypeRepository:
        """Create software component type repository"""
        pass
    
    @abstractmethod
    def create_port_interface_repository(self) -> IPortInterfaceRepository:
        """Create port interface repository"""
        pass
    
    @abstractmethod
    def create_service_interface_repository(self) -> IServiceInterfaceRepository:
        """Create service interface repository"""
        pass
    
    @abstractmethod
    def create_composition_repository(self) -> ICompositionRepository:
        """Create composition repository"""
        pass
    
    @abstractmethod
    def create_port_prototype_repository(self) -> IPortPrototypeRepository:
        """Create port prototype repository"""
        pass
    
    @abstractmethod
    def create_data_element_repository(self) -> IDataElementRepository:
        """Create data element repository"""
        pass