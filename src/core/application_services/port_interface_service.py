"""
Port Interface Application Service
Orchestrates use cases for port interface management
"""

from typing import Dict, Any
from ..interfaces import IValidationService, ICommandService
from ..repositories import IPortInterfaceRepository
from ..models.autosar_elements import PortInterface, DataElement, DataType
from ..domain_events import IEventBus, PortInterfaceCreated, PortInterfaceUpdated, PortInterfaceDeleted
from . import IPortInterfaceApplicationService, ApplicationServiceResult
from ..domain.models import PortInterface as DomainPortInterface, from_qobject_port_interface, to_qobject_port_interface

class PortInterfaceApplicationService(IPortInterfaceApplicationService):
    """Port interface application service implementation"""
    
    def __init__(self, 
                 repository: IPortInterfaceRepository,
                 validation_service: IValidationService,
                 command_service: ICommandService,
                 event_bus: IEventBus = None):
        self._repository = repository
        self._validation_service = validation_service
        self._command_service = command_service
        self._event_bus = event_bus
    
    def create_port_interface(self, name: str, is_service: bool, description: str = "") -> ApplicationServiceResult:
        """Create new port interface with validation"""
        try:
            # Validate input
            if not name or not name.strip():
                return ApplicationServiceResult(False, "Interface name cannot be empty")
            
            if self._repository.exists_by_name(name):
                return ApplicationServiceResult(False, f"Interface '{name}' already exists")
            
            # Create interface
            interface = PortInterface(name, description, is_service)
            
            # Validate interface
            validation_result = self.validate_interface(interface)
            if not validation_result.success:
                return validation_result
            
            # Save through repository
            success = self._repository.save(interface)
            if success:
                # Publish domain event
                if self._event_bus:
                    event = PortInterfaceCreated(
                        interface_id=interface.id,
                        interface_name=interface.short_name,
                        is_service=interface.is_service,
                        source='PortInterfaceApplicationService'
                    )
                    self._event_bus.publish(event)
                
                return ApplicationServiceResult(True, f"Interface '{name}' created successfully", interface)
            else:
                return ApplicationServiceResult(False, "Failed to save interface")
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error creating interface: {str(e)}")

    def create_port_interface_v2(self, domain_interface: DomainPortInterface) -> ApplicationServiceResult:
        """Create port interface using domain dataclass"""
        try:
            # Convert to qobject and delegate
            def factory(name, desc, is_service):
                return PortInterface(name, desc, is_service)

            qobj = to_qobject_port_interface(domain_interface, factory)
            return self.create_port_interface(qobj.short_name, qobj.is_service, qobj.desc)
        except Exception as e:
            return ApplicationServiceResult(False, f"Error creating interface (v2): {e}")

    def update_port_interface_v2(self, domain_interface: DomainPortInterface) -> ApplicationServiceResult:
        """Update port interface from domain dataclass and return domain dataclass"""
        try:
            interface = self._repository.find_by_id(getattr(domain_interface, 'id', '') or '')
            if not interface:
                return ApplicationServiceResult(False, f"Interface with ID '{getattr(domain_interface, 'id', None)}' not found")

            updates = {}
            if domain_interface.short_name and domain_interface.short_name != interface.short_name:
                updates['short_name'] = domain_interface.short_name
                interface.short_name = domain_interface.short_name
            # apply description if present
            if getattr(domain_interface, 'desc', None) is not None and domain_interface.desc != interface.desc:
                updates['desc'] = domain_interface.desc
                interface.desc = domain_interface.desc

            # validate and save
            validation_result = self.validate_interface(interface)
            if not validation_result.success:
                return validation_result

            success = self._repository.save(interface)
            if success:
                domain = from_qobject_port_interface(interface)
                return ApplicationServiceResult(True, 'Interface updated', domain)
            else:
                return ApplicationServiceResult(False, 'Failed to save interface')
        except Exception as e:
            return ApplicationServiceResult(False, f"Error updating interface (v2): {e}")

    def search_port_interfaces_v2(self, query: str) -> ApplicationServiceResult:
        try:
            if not query or not query.strip():
                interfaces = self._repository.find_all()
            else:
                interfaces = self._repository.find_by_name_pattern(query)

            domain_results = [from_qobject_port_interface(i) for i in interfaces]
            return ApplicationServiceResult(True, f"Found {len(domain_results)} interfaces", domain_results)
        except Exception as e:
            return ApplicationServiceResult(False, f"Error searching interfaces (v2): {e}")
    
    def update_port_interface(self, interface_id: str, updates: Dict[str, Any]) -> ApplicationServiceResult:
        """Update existing port interface"""
        try:
            interface = self._repository.find_by_id(interface_id)
            if not interface:
                return ApplicationServiceResult(False, f"Interface with ID '{interface_id}' not found")
            
            # Store original values for undo
            original_values = {}
            
            # Apply updates
            for field, value in updates.items():
                if hasattr(interface, field):
                    original_values[field] = getattr(interface, field)
                    setattr(interface, field, value)
                else:
                    return ApplicationServiceResult(False, f"Invalid field: {field}")
            
            # Validate updated interface
            validation_result = self.validate_interface(interface)
            if not validation_result.success:
                # Revert changes
                for field, value in original_values.items():
                    setattr(interface, field, value)
                return validation_result
            
            # Save changes
            success = self._repository.save(interface)
            if success:
                return ApplicationServiceResult(True, f"Interface updated successfully", interface)
            else:
                return ApplicationServiceResult(False, "Failed to save interface changes")
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error updating interface: {str(e)}")
    
    def delete_port_interface(self, interface_id: str) -> ApplicationServiceResult:
        """Delete port interface with validation"""
        try:
            interface = self._repository.find_by_id(interface_id)
            if not interface:
                return ApplicationServiceResult(False, f"Interface with ID '{interface_id}' not found")
            
            # Check if interface is used by ports
            # This would require additional repository queries
            # For now, we'll assume it's safe to delete
            
            success = self._repository.delete(interface)
            if success:
                return ApplicationServiceResult(True, f"Interface '{interface.short_name}' deleted successfully")
            else:
                return ApplicationServiceResult(False, "Failed to delete interface")
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error deleting interface: {str(e)}")
    
    def add_data_element(self, interface_id: str, element_name: str, data_type: str) -> ApplicationServiceResult:
        """Add data element to interface"""
        try:
            interface = self._repository.find_by_id(interface_id)
            if not interface:
                return ApplicationServiceResult(False, f"Interface with ID '{interface_id}' not found")
            
            # Check if it's a service interface
            if interface.is_service:
                return ApplicationServiceResult(False, "Cannot add data elements to service interfaces")
            
            # Check if element already exists
            if any(elem.short_name == element_name for elem in interface.data_elements):
                return ApplicationServiceResult(False, f"Data element '{element_name}' already exists")
            
            # Validate data type
            try:
                data_type_enum = DataType(data_type)
            except ValueError:
                return ApplicationServiceResult(False, f"Invalid data type: {data_type}")
            
            # Create data element
            data_element = DataElement(element_name, data_type_enum)
            
            # Add to interface
            interface.add_data_element(data_element)
            
            # Save interface
            success = self._repository.save(interface)
            if success:
                return ApplicationServiceResult(True, f"Data element '{element_name}' added successfully", data_element)
            else:
                return ApplicationServiceResult(False, "Failed to save interface")
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error adding data element: {str(e)}")
    
    def remove_data_element(self, interface_id: str, element_name: str) -> ApplicationServiceResult:
        """Remove data element from interface"""
        try:
            interface = self._repository.find_by_id(interface_id)
            if not interface:
                return ApplicationServiceResult(False, f"Interface with ID '{interface_id}' not found")
            
            # Find data element
            data_element = next((elem for elem in interface.data_elements if elem.short_name == element_name), None)
            if not data_element:
                return ApplicationServiceResult(False, f"Data element '{element_name}' not found")
            
            # Remove from interface
            interface.remove_data_element(data_element)
            
            # Save interface
            success = self._repository.save(interface)
            if success:
                return ApplicationServiceResult(True, f"Data element '{element_name}' removed successfully")
            else:
                return ApplicationServiceResult(False, "Failed to save interface")
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error removing data element: {str(e)}")
    
    def validate_interface_compatibility(self, interface1_id: str, interface2_id: str) -> ApplicationServiceResult:
        """Validate interface compatibility"""
        try:
            interface1 = self._repository.find_by_id(interface1_id)
            interface2 = self._repository.find_by_id(interface2_id)
            
            if not interface1:
                return ApplicationServiceResult(False, f"Interface with ID '{interface1_id}' not found")
            if not interface2:
                return ApplicationServiceResult(False, f"Interface with ID '{interface2_id}' not found")
            
            # Check basic compatibility
            if interface1.is_service != interface2.is_service:
                return ApplicationServiceResult(False, "Service and sender-receiver interfaces are not compatible")
            
            # Check data element compatibility for sender-receiver interfaces
            if not interface1.is_service and not interface2.is_service:
                if len(interface1.data_elements) != len(interface2.data_elements):
                    return ApplicationServiceResult(False, "Interfaces have different numbers of data elements")
                
                # Check data element names and types
                for elem1, elem2 in zip(interface1.data_elements, interface2.data_elements):
                    if elem1.short_name != elem2.short_name or elem1.data_type != elem2.data_type:
                        return ApplicationServiceResult(False, f"Data elements '{elem1.short_name}' and '{elem2.short_name}' are not compatible")
            
            return ApplicationServiceResult(True, "Interfaces are compatible")
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error validating interface compatibility: {str(e)}")
    
    def search_port_interfaces(self, query: str) -> ApplicationServiceResult:
        """Search port interfaces"""
        try:
            if not query or not query.strip():
                # Return all interfaces if no query
                interfaces = self._repository.find_all()
            else:
                # Search by name pattern
                interfaces = self._repository.find_by_name_pattern(query)
            
            # Build search results
            results = []
            for interface in interfaces:
                results.append({
                    'id': interface.id,
                    'name': interface.short_name,
                    'description': interface.desc or "",
                    'is_service': interface.is_service,
                    'data_element_count': len(interface.data_elements),
                    'service_element_count': len(interface.service_elements)
                })
            
            return ApplicationServiceResult(True, f"Found {len(results)} interfaces", results)
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error searching interfaces: {str(e)}")
    
    def validate_interface(self, interface: PortInterface) -> ApplicationServiceResult:
        """Validate port interface"""
        try:
            issues = self._validation_service.validate_element(interface)
            
            if not issues:
                return ApplicationServiceResult(True, "Interface is valid")
            
            # Filter for errors only
            errors = [issue for issue in issues if issue.severity.value == "error"]
            if errors:
                error_messages = [issue.message for issue in errors]
                return ApplicationServiceResult(False, f"Validation errors: {'; '.join(error_messages)}")
            
            # Only warnings
            warning_messages = [issue.message for issue in issues]
            return ApplicationServiceResult(True, f"Interface valid with warnings: {'; '.join(warning_messages)}")
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error validating interface: {str(e)}")