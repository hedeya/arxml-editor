"""
Software Component Type Application Service
Orchestrates use cases for software component type management
"""

from typing import Dict, Any
from ..interfaces import IValidationService, ICommandService
from ..repositories import ISwComponentTypeRepository
from ..models.autosar_elements import SwComponentType, SwComponentTypeCategory
from ..domain_events import IEventBus, SwComponentTypeCreated, SwComponentTypeUpdated, SwComponentTypeDeleted
from . import ISwComponentTypeApplicationService, ApplicationServiceResult
from ..domain.models import SwComponentType as DomainSwComponentType
from ..domain.models import to_qobject_sw_component_type

class SwComponentTypeApplicationService(ISwComponentTypeApplicationService):
    """Software component type application service implementation"""
    
    def __init__(self, 
                 repository: ISwComponentTypeRepository,
                 validation_service: IValidationService,
                 command_service: ICommandService,
                 event_bus: IEventBus = None,
                 ui_event_bus: 'UIEventBus' = None):
        self._repository = repository
        self._validation_service = validation_service
        self._command_service = command_service
        self._event_bus = event_bus
        self._ui_event_bus = ui_event_bus
    
    def create_component_type(self, name: str, category: str, description: str = "") -> ApplicationServiceResult:
        """Create new software component type with validation"""
        try:
            # Validate input
            if not name or not name.strip():
                return ApplicationServiceResult(False, "Component name cannot be empty")
            
            if self._repository.exists_by_name(name):
                return ApplicationServiceResult(False, f"Component '{name}' already exists")
            
            # Validate category - handle both enum values and string names
            try:
                if category.upper() == "APPLICATION":
                    category_enum = SwComponentTypeCategory.APPLICATION
                elif category.upper() == "ATOMIC":
                    category_enum = SwComponentTypeCategory.ATOMIC
                elif category.upper() == "COMPOSITION":
                    category_enum = SwComponentTypeCategory.COMPOSITION
                elif category == "ApplicationSwComponentType":
                    category_enum = SwComponentTypeCategory.APPLICATION
                elif category == "AtomicSwComponentType":
                    category_enum = SwComponentTypeCategory.ATOMIC
                elif category == "CompositionSwComponentType":
                    category_enum = SwComponentTypeCategory.COMPOSITION
                else:
                    # Try direct enum creation
                    category_enum = SwComponentTypeCategory(category)
            except (ValueError, AttributeError):
                return ApplicationServiceResult(False, f"Invalid category: {category}. Valid options: APPLICATION, ATOMIC, COMPOSITION")
            
            # Create component
            # Create component (existing QObject-based model)
            component = SwComponentType(name, category_enum, description)
            
            # Set UI event bus for decoupled UI notifications
            if self._ui_event_bus:
                component.set_ui_event_bus(self._ui_event_bus)
            
            # Validate component
            validation_result = self.validate_component_type(component)
            if not validation_result.success:
                return validation_result
            
            # Save through repository
            success = self._repository.save(component)
            if success:
                # Publish domain event
                if self._event_bus:
                    event = SwComponentTypeCreated(
                        component_id=component.id,
                        component_name=component.short_name,
                        category=component.category.value,
                        source='SwComponentTypeApplicationService'
                    )
                    self._event_bus.publish(event)
                
                return ApplicationServiceResult(True, f"Component '{name}' created successfully", component)
            else:
                return ApplicationServiceResult(False, "Failed to save component")
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error creating component: {str(e)}")

    def create_component_type_v2(self, domain_component: DomainSwComponentType) -> ApplicationServiceResult:
        """Create component using pure-domain dataclass and adapt to existing model for persistence."""
        try:
            # Convert domain dataclass to QObject model using adapter factory
            def factory(short_name, desc):
                return SwComponentType(short_name, desc, SwComponentTypeCategory.APPLICATION)

            qobj = to_qobject_sw_component_type(domain_component, factory)

            # Validate and save using existing logic
            return self.create_component_type(qobj.short_name, qobj.category.name if hasattr(qobj, 'category') else domain_component.category, qobj.desc)

        except Exception as e:
            return ApplicationServiceResult(False, f"Error creating component (v2): {str(e)}")
    
    def update_component_type(self, component_id: str, updates: Dict[str, Any]) -> ApplicationServiceResult:
        """Update existing component type"""
        try:
            component = self._repository.find_by_id(component_id)
            if not component:
                return ApplicationServiceResult(False, f"Component with ID '{component_id}' not found")
            
            # Store original values for undo
            original_values = {}
            
            # Apply updates
            for field, value in updates.items():
                if hasattr(component, field):
                    original_values[field] = getattr(component, field)
                    setattr(component, field, value)
                else:
                    return ApplicationServiceResult(False, f"Invalid field: {field}")
            
            # Validate updated component
            validation_result = self.validate_component_type(component)
            if not validation_result.success:
                # Revert changes
                for field, value in original_values.items():
                    setattr(component, field, value)
                return validation_result
            
            # Save changes
            success = self._repository.save(component)
            if success:
                # Publish domain event
                if self._event_bus:
                    event = SwComponentTypeUpdated(
                        component_id=component.id,
                        component_name=component.short_name,
                        changes=updates,
                        source='SwComponentTypeApplicationService'
                    )
                    self._event_bus.publish(event)
                
                return ApplicationServiceResult(True, f"Component updated successfully", component)
            else:
                return ApplicationServiceResult(False, "Failed to save component changes")
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error updating component: {str(e)}")

    def update_component_type_v2(self, domain_component: DomainSwComponentType) -> ApplicationServiceResult:
        """Update component using pure-domain dataclass. Returns domain dataclass on success."""
        try:
            # Find existing component
            component = self._repository.find_by_id(getattr(domain_component, 'id', None) or '')
            if not component:
                return ApplicationServiceResult(False, f"Component with ID '{getattr(domain_component, 'id', None)}' not found")

            # Apply updates from domain dataclass
            updates = {}
            if domain_component.short_name and domain_component.short_name != component.short_name:
                updates['short_name'] = domain_component.short_name
                component.short_name = domain_component.short_name
            if domain_component.desc is not None and domain_component.desc != component.desc:
                updates['desc'] = domain_component.desc
                component.desc = domain_component.desc

            # Validate updated component
            validation_result = self.validate_component_type(component)
            if not validation_result.success:
                return validation_result

            # Save changes
            success = self._repository.save(component)
            if success:
                # Publish domain event
                if self._event_bus:
                    event = SwComponentTypeUpdated(
                        component_id=component.id,
                        component_name=component.short_name,
                        changes=updates,
                        source='SwComponentTypeApplicationService_v2'
                    )
                    self._event_bus.publish(event)

                # Convert saved qobject to domain dataclass and return
                from ..domain.models import from_qobject_sw_component_type
                domain = from_qobject_sw_component_type(component)
                return ApplicationServiceResult(True, "Component updated successfully", domain)
            else:
                return ApplicationServiceResult(False, "Failed to save component changes")

        except Exception as e:
            return ApplicationServiceResult(False, f"Error updating component (v2): {str(e)}")
    
    def delete_component_type(self, component_id: str) -> ApplicationServiceResult:
        """Delete component type with validation"""
        try:
            component = self._repository.find_by_id(component_id)
            if not component:
                return ApplicationServiceResult(False, f"Component with ID '{component_id}' not found")
            
            # Check if component is used in compositions
            # This would require additional repository queries
            # For now, we'll assume it's safe to delete
            
            success = self._repository.delete(component)
            if success:
                # Publish domain event
                if self._event_bus:
                    event = SwComponentTypeDeleted(
                        component_id=component.id,
                        component_name=component.short_name,
                        source='SwComponentTypeApplicationService'
                    )
                    self._event_bus.publish(event)
                
                return ApplicationServiceResult(True, f"Component '{component.short_name}' deleted successfully")
            else:
                return ApplicationServiceResult(False, "Failed to delete component")
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error deleting component: {str(e)}")
    
    def get_component_type_details(self, component_id: str) -> ApplicationServiceResult:
        """Get detailed component information"""
        try:
            component = self._repository.find_by_id(component_id)
            if not component:
                return ApplicationServiceResult(False, f"Component with ID '{component_id}' not found")
            
            # Build detailed information
            details = {
                'id': component_id,
                'name': component.short_name,
                'description': component.desc or "",
                'category': component.category.value if component.category else "Unknown",
                'port_count': len(component.ports) if hasattr(component, 'ports') else 0,
                'composition_count': len(component.compositions) if hasattr(component, 'compositions') else 0,
                'created_at': getattr(component, 'created_at', None),
                'modified_at': getattr(component, 'modified_at', None)
            }
            
            return ApplicationServiceResult(True, "Component details retrieved", details)
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error retrieving component details: {str(e)}")

    def get_component_type_details_v2(self, component_id: str) -> ApplicationServiceResult:
        """Get component details as pure-domain dataclass"""
        try:
            component = self._repository.find_by_id(component_id)
            if not component:
                return ApplicationServiceResult(False, f"Component with ID '{component_id}' not found")

            from ..domain.models import from_qobject_sw_component_type
            domain = from_qobject_sw_component_type(component)
            return ApplicationServiceResult(True, "Component details retrieved", domain)

        except Exception as e:
            return ApplicationServiceResult(False, f"Error retrieving component details (v2): {str(e)}")
    
    def search_component_types(self, query: str) -> ApplicationServiceResult:
        """Search component types"""
        try:
            if not query or not query.strip():
                # Return all components if no query
                components = self._repository.find_all()
            else:
                # Search by name pattern
                components = self._repository.find_by_name_pattern(query)
            
            # Build search results
            results = []
            for component in components:
                results.append({
                    'id': component.id,
                    'name': component.short_name,
                    'description': component.desc or "",
                    'category': component.category.value if component.category else "Unknown"
                })
            
            return ApplicationServiceResult(True, f"Found {len(results)} components", results)
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error searching components: {str(e)}")

    def search_component_types_v2(self, query: str) -> ApplicationServiceResult:
        """Search component types and return list of pure-domain dataclasses"""
        try:
            if not query or not query.strip():
                components = self._repository.find_all()
            else:
                components = self._repository.find_by_name_pattern(query)

            from ..domain.models import from_qobject_sw_component_type
            domain_results = [from_qobject_sw_component_type(c) for c in components]
            return ApplicationServiceResult(True, f"Found {len(domain_results)} components", domain_results)

        except Exception as e:
            return ApplicationServiceResult(False, f"Error searching components (v2): {str(e)}")
    
    def validate_component_type(self, component: SwComponentType) -> ApplicationServiceResult:
        """Validate component type"""
        try:
            issues = self._validation_service.validate_element(component)
            
            if not issues:
                return ApplicationServiceResult(True, "Component is valid")
            
            # Filter for errors only
            errors = [issue for issue in issues if issue.severity.value == "error"]
            if errors:
                error_messages = [issue.message for issue in errors]
                return ApplicationServiceResult(False, f"Validation errors: {'; '.join(error_messages)}")
            
            # Only warnings
            warning_messages = [issue.message for issue in issues]
            return ApplicationServiceResult(True, f"Component valid with warnings: {'; '.join(warning_messages)}")
        
        except Exception as e:
            return ApplicationServiceResult(False, f"Error validating component: {str(e)}")