"""
Command Service
Command pattern implementation for undo/redo functionality
"""

from typing import List, Optional, Any, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass
from PyQt6.QtCore import QObject, pyqtSignal

class Command(ABC):
    """Abstract base class for commands"""
    
    @abstractmethod
    def execute(self) -> bool:
        """Execute the command"""
        pass
    
    @abstractmethod
    def undo(self) -> bool:
        """Undo the command"""
        pass
    
    @abstractmethod
    def redo(self) -> bool:
        """Redo the command (usually same as execute)"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Get command description"""
        pass

@dataclass
class CommandResult:
    """Command execution result"""
    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None

class AddElementCommand(Command):
    """Command to add an element"""
    
    def __init__(self, document, element, element_type: str):
        self.document = document
        self.element = element
        self.element_type = element_type
        self._executed = False
    
    def execute(self) -> bool:
        """Execute add element command"""
        try:
            if self.element_type == "sw_component_type":
                self.document.add_sw_component_type(self.element)
            elif self.element_type == "composition":
                self.document.add_composition(self.element)
            elif self.element_type == "port_interface":
                self.document.add_port_interface(self.element)
            
            self._executed = True
            return True
        except Exception as e:
            print(f"Error executing add command: {e}")
            return False
    
    def undo(self) -> bool:
        """Undo add element command"""
        if not self._executed:
            return False
        
        try:
            if self.element_type == "sw_component_type":
                self.document.remove_sw_component_type(self.element)
            elif self.element_type == "composition":
                self.document.remove_composition(self.element)
            elif self.element_type == "port_interface":
                self.document.remove_port_interface(self.element)
            
            self._executed = False
            return True
        except Exception as e:
            print(f"Error undoing add command: {e}")
            return False
    
    def redo(self) -> bool:
        """Redo add element command"""
        return self.execute()
    
    @property
    def description(self) -> str:
        """Get command description"""
        return f"Add {self.element_type}: {self.element.short_name}"

class RemoveElementCommand(Command):
    """Command to remove an element"""
    
    def __init__(self, document, element, element_type: str):
        self.document = document
        self.element = element
        self.element_type = element_type
        self._executed = False
    
    def execute(self) -> bool:
        """Execute remove element command"""
        try:
            if self.element_type == "sw_component_type":
                self.document.remove_sw_component_type(self.element)
            elif self.element_type == "composition":
                self.document.remove_composition(self.element)
            elif self.element_type == "port_interface":
                self.document.remove_port_interface(self.element)
            
            self._executed = True
            return True
        except Exception as e:
            print(f"Error executing remove command: {e}")
            return False
    
    def undo(self) -> bool:
        """Undo remove element command"""
        if not self._executed:
            return False
        
        try:
            if self.element_type == "sw_component_type":
                self.document.add_sw_component_type(self.element)
            elif self.element_type == "composition":
                self.document.add_composition(self.element)
            elif self.element_type == "port_interface":
                self.document.add_port_interface(self.element)
            
            self._executed = False
            return True
        except Exception as e:
            print(f"Error undoing remove command: {e}")
            return False
    
    def redo(self) -> bool:
        """Redo remove element command"""
        return self.execute()
    
    @property
    def description(self) -> str:
        """Get command description"""
        return f"Remove {self.element_type}: {self.element.short_name}"

class ModifyPropertyCommand(Command):
    """Command to modify an element property"""
    
    def __init__(self, element, property_name: str, old_value: Any, new_value: Any):
        self.element = element
        self.property_name = property_name
        self.old_value = old_value
        self.new_value = new_value
        self._executed = False
    
    def execute(self) -> bool:
        """Execute modify property command"""
        try:
            setattr(self.element, self.property_name, self.new_value)
            self._executed = True
            return True
        except Exception as e:
            print(f"Error executing modify command: {e}")
            return False
    
    def undo(self) -> bool:
        """Undo modify property command"""
        if not self._executed:
            return False
        
        try:
            setattr(self.element, self.property_name, self.old_value)
            self._executed = False
            return True
        except Exception as e:
            print(f"Error undoing modify command: {e}")
            return False
    
    def redo(self) -> bool:
        """Redo modify property command"""
        return self.execute()
    
    @property
    def description(self) -> str:
        """Get command description"""
        return f"Modify {self.property_name}: {self.old_value} → {self.new_value}"

class ConnectPortsCommand(Command):
    """Command to connect two ports"""
    
    def __init__(self, source_port, target_port):
        self.source_port = source_port
        self.target_port = target_port
        self._executed = False
    
    def execute(self) -> bool:
        """Execute connect ports command"""
        try:
            self.source_port.connect_to(self.target_port)
            self._executed = True
            return True
        except Exception as e:
            print(f"Error executing connect command: {e}")
            return False
    
    def undo(self) -> bool:
        """Undo connect ports command"""
        if not self._executed:
            return False
        
        try:
            self.source_port.disconnect_from(self.target_port)
            self._executed = False
            return True
        except Exception as e:
            print(f"Error undoing connect command: {e}")
            return False
    
    def redo(self) -> bool:
        """Redo connect ports command"""
        return self.execute()
    
    @property
    def description(self) -> str:
        """Get command description"""
        return f"Connect ports: {self.source_port.short_name} → {self.target_port.short_name}"

class CommandService(QObject):
    """Command service for managing undo/redo functionality"""
    
    # Signals
    command_stack_changed = pyqtSignal()
    command_executed = pyqtSignal(Command)
    command_undone = pyqtSignal(Command)
    command_redone = pyqtSignal(Command)
    
    def __init__(self, max_stack_size: int = 100):
        super().__init__()
        self._undo_stack: List[Command] = []
        self._redo_stack: List[Command] = []
        self._max_stack_size = max_stack_size
        self._executing = False
    
    @property
    def can_undo(self) -> bool:
        """Check if undo is possible"""
        return len(self._undo_stack) > 0 and not self._executing
    
    @property
    def can_redo(self) -> bool:
        """Check if redo is possible"""
        return len(self._redo_stack) > 0 and not self._executing
    
    @property
    def undo_stack_size(self) -> int:
        """Get undo stack size"""
        return len(self._undo_stack)
    
    @property
    def redo_stack_size(self) -> int:
        """Get redo stack size"""
        return len(self._redo_stack)
    
    def execute_command(self, command: Command) -> CommandResult:
        """Execute a command"""
        if self._executing:
            return CommandResult(success=False, message="Command already executing")
        
        self._executing = True
        
        try:
            success = command.execute()
            if success:
                # Add to undo stack
                self._undo_stack.append(command)
                
                # Clear redo stack
                self._redo_stack.clear()
                
                # Limit stack size
                if len(self._undo_stack) > self._max_stack_size:
                    self._undo_stack.pop(0)
                
                self.command_executed.emit(command)
                self.command_stack_changed.emit()
                
                return CommandResult(success=True, message="Command executed successfully")
            else:
                return CommandResult(success=False, message="Command execution failed")
        
        except Exception as e:
            return CommandResult(success=False, message=f"Command execution error: {e}")
        
        finally:
            self._executing = False
    
    def undo(self) -> CommandResult:
        """Undo last command"""
        if not self.can_undo:
            return CommandResult(success=False, message="Nothing to undo")
        
        self._executing = True
        
        try:
            command = self._undo_stack.pop()
            success = command.undo()
            
            if success:
                self._redo_stack.append(command)
                self.command_undone.emit(command)
                self.command_stack_changed.emit()
                return CommandResult(success=True, message="Command undone successfully")
            else:
                # Put command back on undo stack if undo failed
                self._undo_stack.append(command)
                return CommandResult(success=False, message="Command undo failed")
        
        except Exception as e:
            return CommandResult(success=False, message=f"Command undo error: {e}")
        
        finally:
            self._executing = False
    
    def redo(self) -> CommandResult:
        """Redo last undone command"""
        if not self.can_redo:
            return CommandResult(success=False, message="Nothing to redo")
        
        self._executing = True
        
        try:
            command = self._redo_stack.pop()
            success = command.redo()
            
            if success:
                self._undo_stack.append(command)
                self.command_redone.emit(command)
                self.command_stack_changed.emit()
                return CommandResult(success=True, message="Command redone successfully")
            else:
                # Put command back on redo stack if redo failed
                self._redo_stack.append(command)
                return CommandResult(success=False, message="Command redo failed")
        
        except Exception as e:
            return CommandResult(success=False, message=f"Command redo error: {e}")
        
        finally:
            self._executing = False
    
    def clear_history(self):
        """Clear command history"""
        self._undo_stack.clear()
        self._redo_stack.clear()
        self.command_stack_changed.emit()
    
    def get_undo_commands(self) -> List[Command]:
        """Get list of commands that can be undone"""
        return self._undo_stack.copy()
    
    def get_redo_commands(self) -> List[Command]:
        """Get list of commands that can be redone"""
        return self._redo_stack.copy()
    
    def get_last_command(self) -> Optional[Command]:
        """Get the last executed command"""
        return self._undo_stack[-1] if self._undo_stack else None