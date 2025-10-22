"""
Domain Events System
Implements domain events for loose coupling and better DDD compliance
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable, Type
from dataclasses import dataclass, field
from datetime import datetime
import uuid
from enum import Enum

class EventSeverity(Enum):
    """Event severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class DomainEvent(ABC):
    """Base class for all domain events"""
    
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    event_type: str = field(init=False)
    severity: EventSeverity = EventSeverity.INFO
    source: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        self.event_type = self.__class__.__name__
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary for serialization"""
        return {
            'event_id': self.event_id,
            'timestamp': self.timestamp.isoformat(),
            'event_type': self.event_type,
            'severity': self.severity.value,
            'source': self.source,
            'data': self.data
        }

# Software Component Type Events
@dataclass
class SwComponentTypeCreated(DomainEvent):
    """Event raised when a software component type is created"""
    component_id: str = ""
    component_name: str = ""
    category: str = ""
    
    def __post_init__(self):
        super().__post_init__()
        self.data.update({
            'component_id': self.component_id,
            'component_name': self.component_name,
            'category': self.category
        })

@dataclass
class SwComponentTypeUpdated(DomainEvent):
    """Event raised when a software component type is updated"""
    component_id: str = ""
    component_name: str = ""
    changes: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()
        self.data.update({
            'component_id': self.component_id,
            'component_name': self.component_name,
            'changes': self.changes
        })

@dataclass
class SwComponentTypeDeleted(DomainEvent):
    """Event raised when a software component type is deleted"""
    component_id: str = ""
    component_name: str = ""
    
    def __post_init__(self):
        super().__post_init__()
        self.data.update({
            'component_id': self.component_id,
            'component_name': self.component_name
        })

# Port Interface Events
@dataclass
class PortInterfaceCreated(DomainEvent):
    """Event raised when a port interface is created"""
    interface_id: str = ""
    interface_name: str = ""
    is_service: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        self.data.update({
            'interface_id': self.interface_id,
            'interface_name': self.interface_name,
            'is_service': self.is_service
        })

@dataclass
class PortInterfaceUpdated(DomainEvent):
    """Event raised when a port interface is updated"""
    interface_id: str = ""
    interface_name: str = ""
    changes: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()
        self.data.update({
            'interface_id': self.interface_id,
            'interface_name': self.interface_name,
            'changes': self.changes
        })

@dataclass
class PortInterfaceDeleted(DomainEvent):
    """Event raised when a port interface is deleted"""
    interface_id: str = ""
    interface_name: str = ""
    
    def __post_init__(self):
        super().__post_init__()
        self.data.update({
            'interface_id': self.interface_id,
            'interface_name': self.interface_name
        })

# Data Element Events
@dataclass
class DataElementAdded(DomainEvent):
    """Event raised when a data element is added to an interface"""
    interface_id: str = ""
    interface_name: str = ""
    element_name: str = ""
    data_type: str = ""
    
    def __post_init__(self):
        super().__post_init__()
        self.data.update({
            'interface_id': self.interface_id,
            'interface_name': self.interface_name,
            'element_name': self.element_name,
            'data_type': self.data_type
        })

@dataclass
class DataElementRemoved(DomainEvent):
    """Event raised when a data element is removed from an interface"""
    interface_id: str = ""
    interface_name: str = ""
    element_name: str = ""
    
    def __post_init__(self):
        super().__post_init__()
        self.data.update({
            'interface_id': self.interface_id,
            'interface_name': self.interface_name,
            'element_name': self.element_name
        })

# Composition Events
@dataclass
class CompositionCreated(DomainEvent):
    """Event raised when a composition is created"""
    composition_id: str = ""
    composition_name: str = ""
    
    def __post_init__(self):
        super().__post_init__()
        self.data.update({
            'composition_id': self.composition_id,
            'composition_name': self.composition_name
        })

@dataclass
class ComponentAddedToComposition(DomainEvent):
    """Event raised when a component is added to a composition"""
    composition_id: str = ""
    composition_name: str = ""
    component_id: str = ""
    component_name: str = ""
    
    def __post_init__(self):
        super().__post_init__()
        self.data.update({
            'composition_id': self.composition_id,
            'composition_name': self.composition_name,
            'component_id': self.component_id,
            'component_name': self.component_name
        })

@dataclass
class PortsConnected(DomainEvent):
    """Event raised when ports are connected"""
    composition_id: str = ""
    source_port_id: str = ""
    target_port_id: str = ""
    source_port_name: str = ""
    target_port_name: str = ""
    
    def __post_init__(self):
        super().__post_init__()
        self.data.update({
            'composition_id': self.composition_id,
            'source_port_id': self.source_port_id,
            'target_port_id': self.target_port_id,
            'source_port_name': self.source_port_name,
            'target_port_name': self.target_port_name
        })

# Document Events
@dataclass
class DocumentCreated(DomainEvent):
    """Event raised when a new document is created"""
    document_id: str = ""
    
    def __post_init__(self):
        super().__post_init__()
        self.data.update({
            'document_id': self.document_id
        })

@dataclass
class DocumentLoaded(DomainEvent):
    """Event raised when a document is loaded"""
    file_path: str = ""
    document_id: str = ""
    
    def __post_init__(self):
        super().__post_init__()
        self.data.update({
            'file_path': self.file_path,
            'document_id': self.document_id
        })

@dataclass
class DocumentSaved(DomainEvent):
    """Event raised when a document is saved"""
    file_path: str = ""
    document_id: str = ""
    
    def __post_init__(self):
        super().__post_init__()
        self.data.update({
            'file_path': self.file_path,
            'document_id': self.document_id
        })

# Validation Events
@dataclass
class ValidationIssueDetected(DomainEvent):
    """Event raised when a validation issue is detected"""
    issue_id: str = ""
    element_id: str = ""
    element_type: str = ""
    message: str = ""
    severity: EventSeverity = EventSeverity.WARNING
    
    def __post_init__(self):
        super().__post_init__()
        self.data.update({
            'issue_id': self.issue_id,
            'element_id': self.element_id,
            'element_type': self.element_type,
            'message': self.message
        })

@dataclass
class ValidationIssueResolved(DomainEvent):
    """Event raised when a validation issue is resolved"""
    issue_id: str = ""
    element_id: str = ""
    element_type: str = ""
    
    def __post_init__(self):
        super().__post_init__()
        self.data.update({
            'issue_id': self.issue_id,
            'element_id': self.element_id,
            'element_type': self.element_type
        })

# Command Events
@dataclass
class CommandExecuted(DomainEvent):
    """Event raised when a command is executed"""
    command_id: str = ""
    command_type: str = ""
    success: bool = True
    message: str = ""
    
    def __post_init__(self):
        super().__post_init__()
        self.data.update({
            'command_id': self.command_id,
            'command_type': self.command_type,
            'success': self.success,
            'message': self.message
        })

@dataclass
class CommandUndone(DomainEvent):
    """Event raised when a command is undone"""
    command_id: str = ""
    command_type: str = ""
    
    def __post_init__(self):
        super().__post_init__()
        self.data.update({
            'command_id': self.command_id,
            'command_type': self.command_type
        })

# System Events
@dataclass
class SystemError(DomainEvent):
    """Event raised when a system error occurs"""
    error_type: str = ""
    error_message: str = ""
    stack_trace: str = ""
    severity: EventSeverity = EventSeverity.ERROR
    
    def __post_init__(self):
        super().__post_init__()
        self.data.update({
            'error_type': self.error_type,
            'error_message': self.error_message,
            'stack_trace': self.stack_trace
        })

@dataclass
class SystemWarning(DomainEvent):
    """Event raised when a system warning occurs"""
    warning_type: str = ""
    warning_message: str = ""
    severity: EventSeverity = EventSeverity.WARNING
    
    def __post_init__(self):
        super().__post_init__()
        self.data.update({
            'warning_type': self.warning_type,
            'warning_message': self.warning_message
        })

# Import event bus interface at the end to avoid circular imports
from .event_bus import IEventBus