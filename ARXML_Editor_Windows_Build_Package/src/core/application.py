"""
ARXML Editor Application Core
Manages the overall application state and coordinates between components
"""

from typing import Optional, Dict, Any
from PyQt6.QtCore import QObject, pyqtSignal
from .models.arxml_document import ARXMLDocument
from .services.validation_service import ValidationService
from .services.command_service import CommandService
from .services.schema_service import SchemaService
from .services.arxml_parser import ARXMLParser

class ARXMLEditorApp(QObject):
    """Main application controller"""
    
    # Signals
    document_changed = pyqtSignal()
    validation_changed = pyqtSignal()
    command_stack_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self._current_document: Optional[ARXMLDocument] = None
        self._schema_service = SchemaService()
        self._validation_service = ValidationService(self._schema_service)
        self._command_service = CommandService()
        self._arxml_parser = ARXMLParser(self._schema_service)
        
        # Connect signals
        self._validation_service.validation_changed.connect(self.validation_changed)
        self._command_service.command_stack_changed.connect(self.command_stack_changed)
    
    @property
    def current_document(self) -> Optional[ARXMLDocument]:
        """Get current ARXML document"""
        return self._current_document
    
    @property
    def validation_service(self) -> ValidationService:
        """Get validation service"""
        return self._validation_service
    
    @property
    def command_service(self) -> CommandService:
        """Get command service"""
        return self._command_service
    
    @property
    def schema_service(self) -> SchemaService:
        """Get schema service"""
        return self._schema_service
    
    @property
    def arxml_parser(self) -> ARXMLParser:
        """Get ARXML parser service"""
        return self._arxml_parser
    
    def new_document(self) -> ARXMLDocument:
        """Create a new ARXML document"""
        self._current_document = ARXMLDocument()
        self.document_changed.emit()
        return self._current_document
    
    def load_document(self, file_path: str) -> bool:
        """Load ARXML document from file with automatic schema detection"""
        try:
            # Parse the ARXML file with automatic schema detection
            root = self._arxml_parser.parse_arxml_file(file_path)
            if root is None:
                return False
            
            # Create document from parsed content
            self._current_document = ARXMLDocument()
            self._current_document.load_from_element(root, self._arxml_parser)
            
            # Validate the document with the detected schema
            self._validation_service.validate_document(self._current_document)
            
            self.document_changed.emit()
            return True
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}")
            return False
        except PermissionError:
            print(f"Error: Permission denied accessing file: {file_path}")
            return False
        except Exception as e:
            print(f"Error loading document: {e}")
            return False
    
    def save_document(self, file_path: str = None) -> bool:
        """Save current document to file"""
        if not self._current_document:
            return False
        
        try:
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