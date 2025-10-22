"""
ARXML Editor Application Core
Manages the overall application state and coordinates between components
"""

from typing import Optional, Dict, Any
import os
from PyQt6.QtCore import QObject, pyqtSignal
from .models.arxml_document import ARXMLDocument
from .services.validation_service import ValidationService
from .services.command_service import CommandService
from .services.schema_service import SchemaService
from .services.arxml_parser import ARXMLParser
from .interfaces import ISchemaService, IValidationService, ICommandService, IARXMLParser
from .container import DIContainer
from .repositories import IRepositoryFactory
from .application_services import (
    ISwComponentTypeApplicationService, IPortInterfaceApplicationService,
    IDocumentApplicationService
)

class ARXMLEditorApp(QObject):
    """Main application controller with dependency injection support"""
    
    # Signals
    document_changed = pyqtSignal()
    validation_changed = pyqtSignal()
    command_stack_changed = pyqtSignal()
    
    def __init__(self, container: Optional[DIContainer] = None):
        super().__init__()
        self._current_document: Optional[ARXMLDocument] = None
        self._container = container
        
        # Initialize services - either from DI container or legacy way
        if container:
            self._schema_service = container.get(ISchemaService)
            self._validation_service = container.get(IValidationService) 
            self._command_service = container.get(ICommandService)
            self._arxml_parser = container.get(IARXMLParser)
            
            # Initialize application services
            self._repository_factory = container.get(IRepositoryFactory)
            self._sw_component_service = container.get(ISwComponentTypeApplicationService)
            self._port_interface_service = container.get(IPortInterfaceApplicationService)
            self._document_service = container.get(IDocumentApplicationService)
        else:
            # Legacy initialization for backward compatibility
            self._schema_service = SchemaService()
            self._validation_service = ValidationService(self._schema_service)
            self._command_service = CommandService()
            self._arxml_parser = ARXMLParser(self._schema_service)
            
            # Legacy application services (None for backward compatibility)
            self._repository_factory = None
            self._sw_component_service = None
            self._port_interface_service = None
            self._document_service = None
        
        # Connect signals
        if hasattr(self._validation_service, 'validation_changed'):
            self._validation_service.validation_changed.connect(self.validation_changed)
        if hasattr(self._command_service, 'command_stack_changed'):
            self._command_service.command_stack_changed.connect(self.command_stack_changed)
    
    @property
    def current_document(self) -> Optional[ARXMLDocument]:
        """Get current ARXML document"""
        return self._current_document
    
    @property
    def validation_service(self) -> IValidationService:
        """Get validation service"""
        return self._validation_service
    
    @property
    def command_service(self) -> ICommandService:
        """Get command service"""
        return self._command_service
    
    @property
    def schema_service(self) -> ISchemaService:
        """Get schema service"""
        return self._schema_service
    
    @property
    def arxml_parser(self) -> IARXMLParser:
        """Get ARXML parser service"""
        return self._arxml_parser
    
    @property
    def repository_factory(self) -> Optional[IRepositoryFactory]:
        """Get repository factory"""
        return self._repository_factory
    
    @property
    def sw_component_service(self) -> Optional[ISwComponentTypeApplicationService]:
        """Get software component type application service"""
        return self._sw_component_service
    
    @property
    def port_interface_service(self) -> Optional[IPortInterfaceApplicationService]:
        """Get port interface application service"""
        return self._port_interface_service
    
    @property
    def document_service(self) -> Optional[IDocumentApplicationService]:
        """Get document application service"""
        return self._document_service
    
    def new_document(self) -> ARXMLDocument:
        """Create a new ARXML document"""
        if self._document_service:
            # Use application service for new document creation
            result = self._document_service.create_new_document()
            if result.success:
                self._current_document = result.data
                self.document_changed.emit()
                return self._current_document
            else:
                print(f"Error creating new document: {result.message}")
                return None
        else:
            # Legacy mode
            self._current_document = ARXMLDocument()
            self.document_changed.emit()
            return self._current_document
    
    def load_document(self, file_path: str) -> bool:
        """Load ARXML document from file with automatic schema detection"""
        try:
            print(f"Loading document: {file_path}")
            
            if self._document_service:
                # Use application service for document loading
                result = self._document_service.load_document(file_path)
                if result.success:
                    self._current_document = result.data
                    self.document_changed.emit()
                    print("Document loaded successfully")
                    return True
                else:
                    print(f"Error loading document: {result.message}")
                    return False
            else:
                # Legacy mode
                # Check if file exists
                if not os.path.exists(file_path):
                    print(f"Error: File not found: {file_path}")
                    return False
                
                # Parse the ARXML file with automatic schema detection
                root = self._arxml_parser.parse_arxml_file(file_path)
                if root is None:
                    print("Error: Failed to parse ARXML file")
                    return False
                
                # Create document from parsed content
                self._current_document = ARXMLDocument()
                self._current_document.load_from_element(root, self._arxml_parser)
                
                # Validate the document with the detected schema
                self._validation_service.validate_document(self._current_document)
                
                self.document_changed.emit()
                print("Document loaded successfully")
                return True
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}")
            return False
        except PermissionError:
            print(f"Error: Permission denied accessing file: {file_path}")
            return False
        except Exception as e:
            print(f"Error loading document: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def save_document(self, file_path: str = None) -> bool:
        """Save current document to file"""
        if not self._current_document:
            return False
        
        try:
            if self._document_service:
                # Use application service for document saving
                result = self._document_service.save_document(file_path)
                if result.success:
                    self.document_changed.emit()
                    return True
                else:
                    print(f"Error saving document: {result.message}")
                    return False
            else:
                # Legacy mode
                success = self._current_document.save_document(file_path)
                if success:
                    self.document_changed.emit()
                return success
        except PermissionError:
            print(f"Error: Permission denied writing to file: {file_path}")
            return False
        except OSError as e:
            print(f"Error: File system error saving document: {e}")
            return False
        except Exception as e:
            print(f"Error saving document: {e}")
            return False
    
    def get_available_schema_versions(self) -> list[str]:
        """Get list of available AUTOSAR schema versions"""
        return self._schema_service.get_available_versions()
    
    def set_schema_version(self, version: str) -> bool:
        """Set the AUTOSAR schema version"""
        return self._schema_service.set_version(version)