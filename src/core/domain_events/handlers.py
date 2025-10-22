"""
Event Handlers
Concrete implementations of event handlers for different concerns
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
from . import (
    DomainEvent, SwComponentTypeCreated, SwComponentTypeUpdated, SwComponentTypeDeleted,
    PortInterfaceCreated, PortInterfaceUpdated, PortInterfaceDeleted,
    DataElementAdded, DataElementRemoved,
    CompositionCreated, ComponentAddedToComposition, PortsConnected,
    DocumentCreated, DocumentLoaded, DocumentSaved,
    ValidationIssueDetected, ValidationIssueResolved,
    CommandExecuted, CommandUndone,
    SystemError, SystemWarning
)

logger = logging.getLogger(__name__)

class IEventHandler(ABC):
    """Base interface for event handlers"""
    
    @abstractmethod
    def handle(self, event: DomainEvent) -> None:
        """Handle an event"""
        pass
    
    @abstractmethod
    def can_handle(self, event: DomainEvent) -> bool:
        """Check if this handler can handle the event"""
        pass

class BaseEventHandler(IEventHandler):
    """Base event handler with common functionality"""
    
    def __init__(self, name: str = None):
        self.name = name or self.__class__.__name__
        self.handled_events = 0
        self.errors = 0
    
    def handle(self, event: DomainEvent) -> None:
        """Handle an event with error handling"""
        try:
            self._handle_event(event)
            self.handled_events += 1
            logger.debug(f"{self.name} handled {type(event).__name__}")
        except Exception as e:
            self.errors += 1
            logger.error(f"Error in {self.name} handling {type(event).__name__}: {e}")
    
    def _handle_event(self, event: DomainEvent) -> None:
        """Override this method to implement specific event handling"""
        pass
    
    def can_handle(self, event: DomainEvent) -> bool:
        """Override this method to specify which events this handler can handle"""
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get handler statistics"""
        return {
            'name': self.name,
            'handled_events': self.handled_events,
            'errors': self.errors,
            'success_rate': (self.handled_events - self.errors) / max(self.handled_events, 1) * 100
        }

class LoggingEventHandler(BaseEventHandler):
    """Event handler that logs all events"""
    
    def __init__(self, log_level: int = logging.INFO):
        super().__init__("LoggingHandler")
        self.log_level = log_level
    
    def _handle_event(self, event: DomainEvent) -> None:
        """Log the event"""
        logger.log(self.log_level, f"Event: {type(event).__name__} - {event.event_id} - {event.timestamp}")
        if event.data:
            logger.log(self.log_level, f"Event data: {event.data}")

class AuditEventHandler(BaseEventHandler):
    """Event handler that maintains an audit log"""
    
    def __init__(self):
        super().__init__("AuditHandler")
        self.audit_log: List[Dict[str, Any]] = []
        self.max_log_size = 10000  # Prevent memory issues
    
    def _handle_event(self, event: DomainEvent) -> None:
        """Add event to audit log"""
        audit_entry = {
            'timestamp': event.timestamp.isoformat() if hasattr(event.timestamp, 'isoformat') else str(event.timestamp),
            'event_type': type(event).__name__,
            'event_id': event.event_id,
            'severity': event.severity.value,
            'source': event.source,
            'data': event.data
        }
        
        self.audit_log.append(audit_entry)
        
        # Trim log if it gets too large
        if len(self.audit_log) > self.max_log_size:
            self.audit_log = self.audit_log[-self.max_log_size//2:]
    
    def get_audit_log(self, event_type: str = None, limit: int = None) -> List[Dict[str, Any]]:
        """Get audit log entries"""
        log = self.audit_log
        
        if event_type:
            log = [entry for entry in log if entry['event_type'] == event_type]
        
        if limit:
            log = log[-limit:]
        
        return log

class ValidationEventHandler(BaseEventHandler):
    """Event handler for validation-related events"""
    
    def __init__(self, validation_service=None):
        super().__init__("ValidationHandler")
        self.validation_service = validation_service
        self.validation_issues: List[Dict[str, Any]] = []
    
    def can_handle(self, event: DomainEvent) -> bool:
        """Handle validation-related events"""
        return isinstance(event, (ValidationIssueDetected, ValidationIssueResolved))
    
    def _handle_event(self, event: DomainEvent) -> None:
        """Handle validation events"""
        if isinstance(event, ValidationIssueDetected):
            self._handle_validation_issue_detected(event)
        elif isinstance(event, ValidationIssueResolved):
            self._handle_validation_issue_resolved(event)
    
    def _handle_validation_issue_detected(self, event: ValidationIssueDetected) -> None:
        """Handle validation issue detected"""
        issue = {
            'issue_id': event.issue_id,
            'element_id': event.element_id,
            'element_type': event.element_type,
            'message': event.message,
            'severity': event.severity.value,
            'timestamp': event.timestamp.isoformat()
        }
        self.validation_issues.append(issue)
        logger.warning(f"Validation issue detected: {event.message}")
    
    def _handle_validation_issue_resolved(self, event: ValidationIssueResolved) -> None:
        """Handle validation issue resolved"""
        # Remove from validation issues
        self.validation_issues = [
            issue for issue in self.validation_issues 
            if issue['issue_id'] != event.issue_id
        ]
        logger.info(f"Validation issue resolved: {event.issue_id}")

class UINotificationHandler(BaseEventHandler):
    """Event handler that sends notifications to the UI"""
    
    def __init__(self, notification_callback=None):
        super().__init__("UINotificationHandler")
        self.notification_callback = notification_callback
        self.notifications: List[Dict[str, Any]] = []
    
    def _handle_event(self, event: DomainEvent) -> None:
        """Handle events by sending UI notifications"""
        notification = {
            'timestamp': event.timestamp.isoformat(),
            'type': type(event).__name__,
            'severity': event.severity.value,
            'message': self._create_notification_message(event),
            'data': event.data
        }
        
        self.notifications.append(notification)
        
        # Send to UI if callback is available
        if self.notification_callback:
            try:
                self.notification_callback(notification)
            except Exception as e:
                logger.error(f"Error sending UI notification: {e}")
    
    def _create_notification_message(self, event: DomainEvent) -> str:
        """Create a user-friendly notification message"""
        if isinstance(event, SwComponentTypeCreated):
            return f"Software component '{event.component_name}' created successfully"
        elif isinstance(event, SwComponentTypeUpdated):
            return f"Software component '{event.component_name}' updated"
        elif isinstance(event, SwComponentTypeDeleted):
            return f"Software component '{event.component_name}' deleted"
        elif isinstance(event, PortInterfaceCreated):
            return f"Port interface '{event.interface_name}' created successfully"
        elif isinstance(event, PortInterfaceUpdated):
            return f"Port interface '{event.interface_name}' updated"
        elif isinstance(event, PortInterfaceDeleted):
            return f"Port interface '{event.interface_name}' deleted"
        elif isinstance(event, DocumentLoaded):
            return f"Document loaded from {event.file_path}"
        elif isinstance(event, DocumentSaved):
            return f"Document saved to {event.file_path}"
        elif isinstance(event, ValidationIssueDetected):
            return f"Validation issue: {event.message}"
        elif isinstance(event, SystemError):
            return f"System error: {event.error_message}"
        else:
            return f"{type(event).__name__} event occurred"

class MetricsEventHandler(BaseEventHandler):
    """Event handler that collects metrics and statistics"""
    
    def __init__(self):
        super().__init__("MetricsHandler")
        self.metrics: Dict[str, Any] = {
            'total_events': 0,
            'events_by_type': {},
            'events_by_severity': {},
            'events_by_source': {},
            'error_rate': 0.0,
            'last_event_time': None
        }
    
    def _handle_event(self, event: DomainEvent) -> None:
        """Update metrics based on event"""
        self.metrics['total_events'] += 1
        self.metrics['last_event_time'] = event.timestamp.isoformat()
        
        # Count by event type
        event_type = type(event).__name__
        self.metrics['events_by_type'][event_type] = self.metrics['events_by_type'].get(event_type, 0) + 1
        
        # Count by severity
        severity = event.severity.value
        self.metrics['events_by_severity'][severity] = self.metrics['events_by_severity'].get(severity, 0) + 1
        
        # Count by source
        source = event.source or 'unknown'
        self.metrics['events_by_source'][source] = self.metrics['events_by_source'].get(source, 0) + 1
        
        # Calculate error rate
        error_count = self.metrics['events_by_severity'].get('error', 0) + self.metrics['events_by_severity'].get('critical', 0)
        self.metrics['error_rate'] = (error_count / self.metrics['total_events']) * 100
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        return self.metrics.copy()

class PersistenceEventHandler(BaseEventHandler):
    """Event handler that persists events to storage"""
    
    def __init__(self, storage_callback=None):
        super().__init__("PersistenceHandler")
        self.storage_callback = storage_callback
        self.persisted_events: List[Dict[str, Any]] = []
    
    def _handle_event(self, event: DomainEvent) -> None:
        """Persist event to storage"""
        event_data = event.to_dict()
        self.persisted_events.append(event_data)
        
        # Call storage callback if available
        if self.storage_callback:
            try:
                self.storage_callback(event_data)
            except Exception as e:
                logger.error(f"Error persisting event: {e}")
    
    def get_persisted_events(self, event_type: str = None, limit: int = None) -> List[Dict[str, Any]]:
        """Get persisted events"""
        events = self.persisted_events
        
        if event_type:
            events = [event for event in events if event['event_type'] == event_type]
        
        if limit:
            events = events[-limit:]
        
        return events

class EventHandlerRegistry:
    """Registry for managing event handlers"""
    
    def __init__(self):
        self.handlers: List[IEventHandler] = []
    
    def register_handler(self, handler: IEventHandler) -> None:
        """Register an event handler"""
        self.handlers.append(handler)
        logger.info(f"Registered event handler: {handler.name}")
    
    def unregister_handler(self, handler: IEventHandler) -> bool:
        """Unregister an event handler"""
        if handler in self.handlers:
            self.handlers.remove(handler)
            logger.info(f"Unregistered event handler: {handler.name}")
            return True
        return False
    
    def get_handlers_for_event(self, event: DomainEvent) -> List[IEventHandler]:
        """Get handlers that can handle a specific event"""
        return [handler for handler in self.handlers if handler.can_handle(event)]
    
    def get_all_handlers(self) -> List[IEventHandler]:
        """Get all registered handlers"""
        return self.handlers.copy()
    
    def get_handler_stats(self) -> List[Dict[str, Any]]:
        """Get statistics for all handlers"""
        return [handler.get_stats() for handler in self.handlers if hasattr(handler, 'get_stats')]