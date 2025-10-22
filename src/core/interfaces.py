"""
Service Interfaces for Dependency Injection
Protocol-based interfaces for all core services to enable dependency inversion
"""

from typing import List, Optional, Any, Dict, Protocol, runtime_checkable
from PyQt6.QtCore import QObject, pyqtSignal

@runtime_checkable
class ISchemaService(Protocol):
    """Schema service interface"""
    
    def set_version(self, version: str) -> bool:
        """Set AUTOSAR schema version"""
        ...
    
    def validate_arxml(self, content: str) -> bool:
        """Validate ARXML content against schema"""
        ...
    
    def detect_schema_version_from_file(self, file_path: str) -> Optional[str]:
        """Detect schema version from file"""
        ...
    
    def get_available_versions(self) -> List[str]:
        """Get available schema versions"""
        ...

@runtime_checkable
class IValidationService(Protocol):
    """Validation service interface"""
    
    def validate_document(self, document: Any) -> List[Any]:
        """Validate entire document"""
        ...
    
    def validate_element(self, element: Any) -> List[Any]:
        """Validate single element"""
        ...
    
    def clear_issues(self) -> None:
        """Clear all validation issues"""
        ...
    
    @property
    def error_count(self) -> int:
        """Get number of errors"""
        ...
    
    @property
    def warning_count(self) -> int:
        """Get number of warnings"""
        ...
    
    @property
    def issues(self) -> List[Any]:
        """Get all validation issues"""
        ...

@runtime_checkable
class ICommandService(Protocol):
    """Command service interface"""
    
    def execute_command(self, command: Any) -> bool:
        """Execute a command"""
        ...
    
    def undo(self) -> bool:
        """Undo last command"""
        ...
    
    def redo(self) -> bool:
        """Redo last undone command"""
        ...
    
    def can_undo(self) -> bool:
        """Check if undo is possible"""
        ...
    
    def can_redo(self) -> bool:
        """Check if redo is possible"""
        ...

@runtime_checkable
class IARXMLParser(Protocol):
    """ARXML parser interface"""
    
    def parse_arxml_file(self, file_path: str) -> Optional[Any]:
        """Parse ARXML file and return root element"""
        ...
    
    def parse_sw_component_types(self, root: Any) -> List[Any]:
        """Parse software component types from XML"""
        ...
    
    def parse_port_interfaces(self, root: Any) -> List[Any]:
        """Parse port interfaces from XML"""
        ...
    
    def parse_service_interfaces(self, root: Any) -> List[Any]:
        """Parse service interfaces from XML"""
        ...
    
    def parse_compositions(self, root: Any) -> List[Any]:
        """Parse compositions from XML"""
        ...