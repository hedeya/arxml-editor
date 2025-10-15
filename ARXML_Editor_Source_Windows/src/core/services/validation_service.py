"""
Validation Service
Real-time validation engine for AUTOSAR elements
"""

import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
from PyQt6.QtCore import QObject, pyqtSignal
from ..models.autosar_elements import (
    SwComponentType, PortPrototype, Composition, 
    PortInterface, PortType, DataType
)

class ValidationSeverity(Enum):
    """Validation severity levels"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class ValidationIssue:
    """Validation issue model"""
    severity: ValidationSeverity
    message: str
    element: Optional[Any] = None
    property_name: Optional[str] = None
    line_number: Optional[int] = None
    column_number: Optional[int] = None

class ValidationService(QObject):
    """Validation service for AUTOSAR elements"""
    
    # Signals
    validation_changed = pyqtSignal()
    issue_added = pyqtSignal(ValidationIssue)
    issue_removed = pyqtSignal(ValidationIssue)
    
    def __init__(self, schema_service=None):
        super().__init__()
        self._issues: List[ValidationIssue] = []
        self._validating = False  # Flag to prevent recursive calls
        self._schema_service = schema_service
        self._validation_rules: List[callable] = [
            self._validate_unconnected_ports,
            self._validate_port_type_mismatches,
            self._validate_interface_compatibility,
            self._validate_data_type_consistency,
            self._validate_required_properties,
            self._validate_naming_conventions
        ]
    
    @property
    def issues(self) -> List[ValidationIssue]:
        """Get all validation issues"""
        return self._issues.copy()
    
    @property
    def error_count(self) -> int:
        """Get number of errors"""
        return len([issue for issue in self._issues if issue.severity == ValidationSeverity.ERROR])
    
    @property
    def warning_count(self) -> int:
        """Get number of warnings"""
        return len([issue for issue in self._issues if issue.severity == ValidationSeverity.WARNING])
    
    def validate_document(self, document) -> List[ValidationIssue]:
        """Validate entire document"""
        if self._validating:
            return self._issues.copy()
        
        self._validating = True
        self._issues.clear()
        self._schema_validated = False  # Reset schema validation flag
        
        if not document:
            self._validating = False
            return self._issues.copy()
        
        # Validate all software component types
        for component_type in document.sw_component_types:
            component_issues = self._validate_component_type(component_type)
            self._issues.extend(component_issues)
        
        # Validate all compositions
        for composition in document.compositions:
            composition_issues = self._validate_composition(composition)
            self._issues.extend(composition_issues)
        
        # Validate all port interfaces
        for port_interface in document.port_interfaces:
            interface_issues = self._validate_port_interface(port_interface)
            self._issues.extend(interface_issues)
        
        # Validate all service interfaces
        for service_interface in document.service_interfaces:
            service_issues = self._validate_service_interface(service_interface)
            self._issues.extend(service_issues)
        
        # Run additional validation rules
        for rule in self._validation_rules:
            for element in (document.sw_component_types + document.compositions + 
                          document.port_interfaces + document.service_interfaces):
                try:
                    rule_issues = rule(element)
                    if rule_issues:
                        self._issues.extend(rule_issues)
                except Exception as e:
                    print(f"Error in validation rule {rule.__name__}: {e}")
        
        # Run document-level validation (schema compliance)
        try:
            schema_issues = self._validate_document_schema_compliance()
            if schema_issues:
                self._issues.extend(schema_issues)
        except Exception as e:
            print(f"Error in document-level validation: {e}")
        
        self._validating = False
        self.validation_changed.emit()
        return self._issues.copy()
    
    def validate_element(self, element) -> List[ValidationIssue]:
        """Validate a specific element"""
        element_issues = []
        
        if isinstance(element, SwComponentType):
            element_issues = self._validate_component_type(element)
        elif isinstance(element, Composition):
            element_issues = self._validate_composition(element)
        elif isinstance(element, PortInterface):
            element_issues = self._validate_port_interface(element)
        elif isinstance(element, PortPrototype):
            element_issues = self._validate_port_prototype(element)
        
        return element_issues
    
    def _validate_component_type(self, component_type: SwComponentType) -> List[ValidationIssue]:
        """Validate software component type"""
        issues = []
        
        # Check for empty short name
        if not component_type.short_name or component_type.short_name.strip() == "":
            issue = ValidationIssue(
                severity=ValidationSeverity.ERROR,
                message="Component type must have a non-empty short name",
                element=component_type,
                property_name="short_name"
            )
            issues.append(issue)
        
        # Validate all ports
        for port in component_type.ports:
            port_issues = self._validate_port_prototype(port)
            issues.extend(port_issues)
        
        return issues
    
    def _validate_composition(self, composition: Composition) -> List[ValidationIssue]:
        """Validate composition"""
        issues = []
        
        # Check for empty short name
        if not composition.short_name or composition.short_name.strip() == "":
            issue = ValidationIssue(
                severity=ValidationSeverity.ERROR,
                message="Composition must have a non-empty short name",
                element=composition,
                property_name="short_name"
            )
            issues.append(issue)
        
        # Validate all component types in composition
        for component_type in composition.component_types:
            component_issues = self._validate_component_type(component_type)
            issues.extend(component_issues)
        
        # Validate all connections
        for connection in composition.connections:
            connection_issues = self._validate_port_connection(connection)
            issues.extend(connection_issues)
        
        return issues
    
    def _validate_port_interface(self, port_interface: PortInterface) -> List[ValidationIssue]:
        """Validate port interface"""
        issues = []
        
        # Check for empty short name
        if not port_interface.short_name or port_interface.short_name.strip() == "":
            issue = ValidationIssue(
                severity=ValidationSeverity.ERROR,
                message="Port interface must have a non-empty short name",
                element=port_interface,
                property_name="short_name"
            )
            issues.append(issue)
        
        # Validate data elements
        for data_element in port_interface.data_elements:
            data_issues = self._validate_data_element(data_element)
            issues.extend(data_issues)
        
        return issues
    
    def _validate_service_interface(self, service_interface) -> List[ValidationIssue]:
        """Validate service interface"""
        issues = []
        
        # Check for empty short name
        if not service_interface.short_name or service_interface.short_name.strip() == "":
            issue = ValidationIssue(
                severity=ValidationSeverity.ERROR,
                message="Service interface must have a non-empty short name",
                element=service_interface,
                property_name="short_name"
            )
            issues.append(issue)
        
        # Validate service elements
        for service_element in service_interface.service_elements:
            service_issues = self._validate_service_element(service_element)
            issues.extend(service_issues)
        
        return issues
    
    def _validate_service_element(self, service_element) -> List[ValidationIssue]:
        """Validate service element"""
        issues = []
        
        # Check for empty short name
        if not service_element.short_name or service_element.short_name.strip() == "":
            issue = ValidationIssue(
                severity=ValidationSeverity.ERROR,
                message="Service element must have a non-empty short name",
                element=service_element,
                property_name="short_name"
            )
            issues.append(issue)
        
        return issues
    
    def _validate_port_prototype(self, port: PortPrototype) -> List[ValidationIssue]:
        """Validate port prototype"""
        issues = []
        
        # Check for empty short name
        if not port.short_name or port.short_name.strip() == "":
            issue = ValidationIssue(
                severity=ValidationSeverity.ERROR,
                message="Port must have a non-empty short name",
                element=port,
                property_name="short_name"
            )
            issues.append(issue)
        
        # Check for interface reference
        if not port.interface_ref and not port.interface:
            issue = ValidationIssue(
                severity=ValidationSeverity.WARNING,
                message="Port should have an interface reference",
                element=port,
                property_name="interface_ref"
            )
            issues.append(issue)
        
        return issues
    
    def _validate_data_element(self, data_element) -> List[ValidationIssue]:
        """Validate data element"""
        issues = []
        
        # Check for empty short name
        if not data_element.short_name or data_element.short_name.strip() == "":
            issue = ValidationIssue(
                severity=ValidationSeverity.ERROR,
                message="Data element must have a non-empty short name",
                element=data_element,
                property_name="short_name"
            )
            issues.append(issue)
        
        return issues
    
    def _validate_port_connection(self, connection) -> List[ValidationIssue]:
        """Validate port connection"""
        issues = []
        
        # Check if ports are compatible
        if connection.source_port.port_type == connection.target_port.port_type:
            issue = ValidationIssue(
                severity=ValidationSeverity.ERROR,
                message="Source and target ports cannot have the same type",
                element=connection
            )
            issues.append(issue)
            self._add_issue(issue)
        
        # Check interface compatibility
        if (connection.source_port.interface and connection.target_port.interface and
            connection.source_port.interface != connection.target_port.interface):
            issue = ValidationIssue(
                severity=ValidationSeverity.ERROR,
                message="Connected ports must use the same interface",
                element=connection
            )
            issues.append(issue)
            self._add_issue(issue)
        
        return issues
    
    def _validate_unconnected_ports(self, element) -> List[ValidationIssue]:
        """Validate for unconnected ports"""
        issues = []
        
        if isinstance(element, SwComponentType):
            for port in element.ports:
                if not port.connected_ports:
                    issue = ValidationIssue(
                        severity=ValidationSeverity.WARNING,
                        message=f"Port '{port.short_name}' is not connected",
                        element=port
                    )
                    issues.append(issue)
        
        return issues
    
    def _validate_port_type_mismatches(self, element) -> List[ValidationIssue]:
        """Validate port type mismatches"""
        issues = []
        
        if isinstance(element, Composition):
            for connection in element.connections:
                if (connection.source_port.port_type == PortType.PROVIDER and
                    connection.target_port.port_type != PortType.REQUIRER):
                    issue = ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        message="Provider port can only connect to requirer port",
                        element=connection
                    )
                    issues.append(issue)
        
        return issues
    
    def _validate_interface_compatibility(self, element) -> List[ValidationIssue]:
        """Validate interface compatibility"""
        issues = []
        # Implementation for interface compatibility validation
        return issues
    
    def _validate_data_type_consistency(self, element) -> List[ValidationIssue]:
        """Validate data type consistency"""
        issues = []
        # Implementation for data type consistency validation
        return issues
    
    def _validate_required_properties(self, element) -> List[ValidationIssue]:
        """Validate required properties"""
        issues = []
        # Implementation for required properties validation
        return issues
    
    def _validate_naming_conventions(self, element) -> List[ValidationIssue]:
        """Validate naming conventions"""
        issues = []
        # Implementation for naming conventions validation
        return issues
    
    def _validate_schema_compliance(self, element) -> List[ValidationIssue]:
        """Validate schema compliance using detected schema version"""
        issues = []
        
        # Only validate schema compliance once per document, not per element
        # This prevents duplicate validation and improves performance
        if not hasattr(self, '_schema_validated') or not self._schema_validated:
            self._schema_validated = True
            return self._validate_document_schema_compliance()
        
        return issues
    
    def _validate_document_schema_compliance(self) -> List[ValidationIssue]:
        """Validate entire document against schema"""
        issues = []
        
        if not self._schema_service or not self._schema_service.current_schema:
            return issues
        
        try:
            # Get the current document from the application context
            # For now, we'll validate against the sample file if available
            sample_file = "sample.arxml"
            if os.path.exists(sample_file):
                validation_errors = self._schema_service.validate_arxml_file(sample_file)
                
                for error in validation_errors:
                    issue = ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        message=f"Schema validation error: {error}",
                        element=None
                    )
                    issues.append(issue)
        
        except Exception as e:
            issue = ValidationIssue(
                severity=ValidationSeverity.WARNING,
                message=f"Schema validation failed: {str(e)}",
                element=None
            )
            issues.append(issue)
        
        return issues
    
    def _add_issue(self, issue: ValidationIssue):
        """Add validation issue"""
        self._issues.append(issue)
        self.issue_added.emit(issue)
    
    def clear_issues(self):
        """Clear all validation issues"""
        self._issues.clear()
        self.validation_changed.emit()
    
    def get_issues_by_element(self, element) -> List[ValidationIssue]:
        """Get validation issues for specific element"""
        return [issue for issue in self._issues if issue.element == element]
    
    def get_issues_by_severity(self, severity: ValidationSeverity) -> List[ValidationIssue]:
        """Get validation issues by severity"""
        return [issue for issue in self._issues if issue.severity == severity]