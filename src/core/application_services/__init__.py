"""
Application Services Layer
Orchestrates use cases and coordinates between domain and infrastructure layers
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from ..models.autosar_elements import SwComponentType, PortInterface, ServiceInterface, Composition
from ..models.arxml_document import ARXMLDocument

@dataclass
class ApplicationServiceResult:
    """Result of application service operation"""
    
    success: bool
    message: str = ""
    data: Any = None
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
    
    def add_error(self, error: str):
        """Add error to result"""
        self.errors.append(error)
        self.success = False
    
    def has_errors(self) -> bool:
        """Check if result has errors"""
        return len(self.errors) > 0

class ISwComponentTypeApplicationService(ABC):
    """Software component type application service interface"""
    
    @abstractmethod
    def create_component_type(self, name: str, category: str, description: str = "") -> ApplicationServiceResult:
        """Create new software component type"""
        pass
    
    @abstractmethod
    def update_component_type(self, component_id: str, updates: Dict[str, Any]) -> ApplicationServiceResult:
        """Update existing component type"""
        pass
    
    @abstractmethod
    def delete_component_type(self, component_id: str) -> ApplicationServiceResult:
        """Delete component type"""
        pass
    
    @abstractmethod
    def get_component_type_details(self, component_id: str) -> ApplicationServiceResult:
        """Get detailed component information"""
        pass
    
    @abstractmethod
    def search_component_types(self, query: str) -> ApplicationServiceResult:
        """Search component types"""
        pass
    
    @abstractmethod
    def validate_component_type(self, component: SwComponentType) -> ApplicationServiceResult:
        """Validate component type"""
        pass

class IPortInterfaceApplicationService(ABC):
    """Port interface application service interface"""
    
    @abstractmethod
    def create_port_interface(self, name: str, is_service: bool, description: str = "") -> ApplicationServiceResult:
        """Create new port interface"""
        pass
    
    @abstractmethod
    def update_port_interface(self, interface_id: str, updates: Dict[str, Any]) -> ApplicationServiceResult:
        """Update existing port interface"""
        pass
    
    @abstractmethod
    def delete_port_interface(self, interface_id: str) -> ApplicationServiceResult:
        """Delete port interface"""
        pass
    
    @abstractmethod
    def add_data_element(self, interface_id: str, element_name: str, data_type: str) -> ApplicationServiceResult:
        """Add data element to interface"""
        pass
    
    @abstractmethod
    def remove_data_element(self, interface_id: str, element_name: str) -> ApplicationServiceResult:
        """Remove data element from interface"""
        pass
    
    @abstractmethod
    def validate_interface_compatibility(self, interface1_id: str, interface2_id: str) -> ApplicationServiceResult:
        """Validate interface compatibility"""
        pass
    
    @abstractmethod
    def search_port_interfaces(self, query: str) -> ApplicationServiceResult:
        """Search port interfaces"""
        pass

class ICompositionApplicationService(ABC):
    """Composition application service interface"""
    
    @abstractmethod
    def create_composition(self, name: str, description: str = "") -> ApplicationServiceResult:
        """Create new composition"""
        pass
    
    @abstractmethod
    def update_composition(self, composition_id: str, updates: Dict[str, Any]) -> ApplicationServiceResult:
        """Update existing composition"""
        pass
    
    @abstractmethod
    def delete_composition(self, composition_id: str) -> ApplicationServiceResult:
        """Delete composition"""
        pass
    
    @abstractmethod
    def add_component_to_composition(self, composition_id: str, component_id: str) -> ApplicationServiceResult:
        """Add component to composition"""
        pass
    
    @abstractmethod
    def remove_component_from_composition(self, composition_id: str, component_id: str) -> ApplicationServiceResult:
        """Remove component from composition"""
        pass
    
    @abstractmethod
    def connect_ports(self, composition_id: str, source_port_id: str, target_port_id: str) -> ApplicationServiceResult:
        """Connect ports in composition"""
        pass
    
    @abstractmethod
    def disconnect_ports(self, composition_id: str, source_port_id: str, target_port_id: str) -> ApplicationServiceResult:
        """Disconnect ports in composition"""
        pass

class IDocumentApplicationService(ABC):
    """Document application service interface"""
    
    @abstractmethod
    def create_new_document(self) -> ApplicationServiceResult:
        """Create new ARXML document"""
        pass
    
    @abstractmethod
    def load_document(self, file_path: str) -> ApplicationServiceResult:
        """Load ARXML document from file"""
        pass
    
    @abstractmethod
    def save_document(self, file_path: str = None) -> ApplicationServiceResult:
        """Save ARXML document to file"""
        pass
    
    @abstractmethod
    def validate_document(self) -> ApplicationServiceResult:
        """Validate entire document"""
        pass
    
    @abstractmethod
    def get_document_statistics(self) -> ApplicationServiceResult:
        """Get document statistics"""
        pass
    
    @abstractmethod
    def export_document(self, format: str, file_path: str) -> ApplicationServiceResult:
        """Export document in different format"""
        pass

class IValidationApplicationService(ABC):
    """Validation application service interface"""
    
    @abstractmethod
    def validate_element(self, element_id: str, element_type: str) -> ApplicationServiceResult:
        """Validate specific element"""
        pass
    
    @abstractmethod
    def validate_document(self) -> ApplicationServiceResult:
        """Validate entire document"""
        pass
    
    @abstractmethod
    def get_validation_issues(self, severity: str = None) -> ApplicationServiceResult:
        """Get validation issues"""
        pass
    
    @abstractmethod
    def clear_validation_issues(self) -> ApplicationServiceResult:
        """Clear all validation issues"""
        pass
    
    @abstractmethod
    def fix_validation_issues(self, issue_ids: List[str]) -> ApplicationServiceResult:
        """Fix specific validation issues"""
        pass