"""
Document Application Service
Orchestrates use cases for document management
"""

import os
from typing import Optional
from ..interfaces import IValidationService, IARXMLParser
from ..repositories import IRepositoryFactory
from ..models.arxml_document import ARXMLDocument
from ..domain_events import IEventBus, DocumentCreated, DocumentLoaded, DocumentSaved
from . import IDocumentApplicationService, ApplicationServiceResult

class DocumentApplicationService(IDocumentApplicationService):
    """Document application service implementation"""
    
    def __init__(self, 
                 repository_factory: IRepositoryFactory,
                 validation_service: IValidationService,
                 arxml_parser: IARXMLParser,
                 event_bus: IEventBus = None):
        self._repository_factory = repository_factory
        self._validation_service = validation_service
        self._arxml_parser = arxml_parser
        self._event_bus = event_bus
        self._current_document: Optional[ARXMLDocument] = None
    
    def create_new_document(self) -> ApplicationServiceResult:
        """Create new ARXML document"""
        try:
            # Create new document with repositories
            self._current_document = ARXMLDocument()
            
            # Initialize repositories for the document
            self._initialize_document_repositories()
            
            # Publish domain event
            if self._event_bus:
                event = DocumentCreated(
                    document_id=self._current_document.id if hasattr(self._current_document, 'id') else "new",
                    source='DocumentApplicationService'
                )
                self._event_bus.publish(event)
            
            return ApplicationServiceResult(True, "New document created successfully", self._current_document)
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error creating new document: {str(e)}")
    
    def load_document(self, file_path: str) -> ApplicationServiceResult:
        """Load ARXML document from file"""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return ApplicationServiceResult(False, f"File not found: {file_path}")
            
            # Parse the ARXML file
            root = self._arxml_parser.parse_arxml_file(file_path)
            if root is None:
                return ApplicationServiceResult(False, "Failed to parse ARXML file")
            
            # Create document from parsed content
            self._current_document = ARXMLDocument()
            self._current_document.load_from_element(root, self._arxml_parser)
            
            # Initialize repositories for the document
            self._initialize_document_repositories()
            
            # Load data into repositories
            self._load_document_data_to_repositories()
            
            # Validate the document
            validation_result = self.validate_document()
            if not validation_result.success:
                return ApplicationServiceResult(False, f"Document loaded but validation failed: {validation_result.message}")
            
            # Publish domain event
            if self._event_bus:
                event = DocumentLoaded(
                    file_path=file_path,
                    document_id=self._current_document.id if hasattr(self._current_document, 'id') else "loaded",
                    source='DocumentApplicationService'
                )
                self._event_bus.publish(event)
            
            return ApplicationServiceResult(True, f"Document loaded successfully from {file_path}", self._current_document)
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error loading document: {str(e)}")
    
    def save_document(self, file_path: str = None) -> ApplicationServiceResult:
        """Save ARXML document to file"""
        try:
            if not self._current_document:
                return ApplicationServiceResult(False, "No document to save")
            
            # Save data from repositories to document
            self._save_repository_data_to_document()
            
            # Use provided file path or current document path
            target_path = file_path or self._current_document.file_path
            if not target_path:
                return ApplicationServiceResult(False, "No file path specified for saving")
            
            # Save document
            success = self._current_document.save_document(target_path)
            if success:
                # Publish domain event
                if self._event_bus:
                    event = DocumentSaved(
                        file_path=target_path,
                        document_id=self._current_document.id if hasattr(self._current_document, 'id') else "saved",
                        source='DocumentApplicationService'
                    )
                    self._event_bus.publish(event)
                
                return ApplicationServiceResult(True, f"Document saved successfully to {target_path}")
            else:
                return ApplicationServiceResult(False, "Failed to save document")
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error saving document: {str(e)}")
    
    def validate_document(self) -> ApplicationServiceResult:
        """Validate entire document"""
        try:
            if not self._current_document:
                return ApplicationServiceResult(False, "No document to validate")
            
            # Validate document
            issues = self._validation_service.validate_document(self._current_document)
            
            if not issues:
                return ApplicationServiceResult(True, "Document is valid")
            
            # Count issues by severity
            error_count = len([issue for issue in issues if issue.severity.value == "error"])
            warning_count = len([issue for issue in issues if issue.severity.value == "warning"])
            
            if error_count > 0:
                return ApplicationServiceResult(False, f"Document has {error_count} errors and {warning_count} warnings")
            else:
                return ApplicationServiceResult(True, f"Document is valid with {warning_count} warnings")
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error validating document: {str(e)}")
    
    def get_document_statistics(self) -> ApplicationServiceResult:
        """Get document statistics"""
        try:
            if not self._current_document:
                return ApplicationServiceResult(False, "No document loaded")
            
            # Get statistics from repositories
            sw_component_repo = self._repository_factory.create_sw_component_type_repository()
            port_interface_repo = self._repository_factory.create_port_interface_repository()
            composition_repo = self._repository_factory.create_composition_repository()
            
            statistics = {
                'file_path': self._current_document.file_path,
                'schema_version': self._current_document.schema_version,
                'modified': self._current_document.modified,
                'sw_component_types': len(sw_component_repo.find_all()),
                'port_interfaces': len(port_interface_repo.find_all()),
                'compositions': len(composition_repo.find_all()),
                'total_elements': 0
            }
            
            # Calculate total elements
            statistics['total_elements'] = (
                statistics['sw_component_types'] + 
                statistics['port_interfaces'] + 
                statistics['compositions']
            )
            
            return ApplicationServiceResult(True, "Document statistics retrieved", statistics)
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error getting document statistics: {str(e)}")
    
    def export_document(self, format: str, file_path: str) -> ApplicationServiceResult:
        """Export document in different format"""
        try:
            if not self._current_document:
                return ApplicationServiceResult(False, "No document to export")
            
            # For now, only support ARXML format
            if format.lower() != 'arxml':
                return ApplicationServiceResult(False, f"Unsupported export format: {format}")
            
            # Save document with new file path
            success = self._current_document.save_document(file_path)
            if success:
                return ApplicationServiceResult(True, f"Document exported successfully to {file_path}")
            else:
                return ApplicationServiceResult(False, "Failed to export document")
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error exporting document: {str(e)}")
    
    def _initialize_document_repositories(self):
        """Initialize repositories for the current document"""
        if not self._current_document:
            return
        
        # Create repositories
        self._sw_component_repo = self._repository_factory.create_sw_component_type_repository()
        self._port_interface_repo = self._repository_factory.create_port_interface_repository()
        self._service_interface_repo = self._repository_factory.create_service_interface_repository()
        self._composition_repo = self._repository_factory.create_composition_repository()
        
        # Store repositories in document for access
        self._current_document._repositories = {
            'sw_component_types': self._sw_component_repo,
            'port_interfaces': self._port_interface_repo,
            'service_interfaces': self._service_interface_repo,
            'compositions': self._composition_repo
        }
    
    def _load_document_data_to_repositories(self):
        """Load document data into repositories"""
        if not self._current_document:
            return
        
        # Load software component types
        for component in self._current_document.sw_component_types:
            self._sw_component_repo.save(component)
        
        # Load port interfaces
        for interface in self._current_document.port_interfaces:
            self._port_interface_repo.save(interface)
        
        # Load service interfaces
        for interface in self._current_document.service_interfaces:
            self._service_interface_repo.save(interface)
        
        # Load compositions
        for composition in self._current_document.compositions:
            self._composition_repo.save(composition)
    
    def _save_repository_data_to_document(self):
        """Save repository data back to document"""
        if not self._current_document:
            return
        
        # Update document collections from repositories
        self._current_document._sw_component_types = self._sw_component_repo.find_all()
        self._current_document._port_interfaces = self._port_interface_repo.find_all()
        self._current_document._service_interfaces = self._service_interface_repo.find_all()
        self._current_document._compositions = self._composition_repo.find_all()
    
    @property
    def current_document(self) -> Optional[ARXMLDocument]:
        """Get current document"""
        return self._current_document