"""
Application Factory
Creates configured ARXML Editor application instances with dependency injection
"""

from typing import Optional
from .core.container import DIContainer, setup_container
from .core.application import ARXMLEditorApp
from .ui.main_window import MainWindow

class ARXMLEditorFactory:
    """Factory for creating ARXML Editor applications with proper DI setup"""
    
    @staticmethod
    def create_application(container: Optional[DIContainer] = None) -> ARXMLEditorApp:
        """Create application with dependency injection"""
        if container is None:
            container = setup_container()
        
        return ARXMLEditorApp(container)
    
    @staticmethod
    def create_main_window(container: Optional[DIContainer] = None) -> MainWindow:
        """Create main window with dependency injection"""
        if container is None:
            container = setup_container()
        
        # Create main window with DI-enabled app
        app = ARXMLEditorApp(container)
        window = MainWindow.__new__(MainWindow)
        window._container = container
        window.app = app
        MainWindow.__init__(window)
        return window
    
    @staticmethod
    def create_legacy_application() -> ARXMLEditorApp:
        """Create application using legacy initialization for backward compatibility"""
        return ARXMLEditorApp(None)

# Convenience function for simple usage
def create_arxml_editor(use_di: bool = True) -> ARXMLEditorApp:
    """Create ARXML Editor application
    
    Args:
        use_di: Whether to use dependency injection (True) or legacy mode (False)
    
    Returns:
        Configured ARXMLEditorApp instance
    """
    if use_di:
        return ARXMLEditorFactory.create_application()
    else:
        return ARXMLEditorFactory.create_legacy_application()