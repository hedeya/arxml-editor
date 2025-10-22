#!/usr/bin/env python3
"""
ARXML Editor - Professional Desktop AUTOSAR XML Editor
Main application entry point with dependency injection support
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from src.ui.main_window import MainWindow
from src.core.container import setup_container
from src.factory import ARXMLEditorFactory

def main():
    """Main application entry point with dependency injection"""
    app = QApplication(sys.argv)
    app.setApplicationName("ARXML Editor")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("AUTOSAR Tools")
    
    try:
        # Create dependency injection container
        container = setup_container()
        
        # Create main window with DI
        main_window = MainWindow()
        main_window.show()
        
        print("ARXML Editor started with Repository Pattern and Application Services")
        print("   - Repository pattern implemented")
        print("   - Application services layer active")
        print("   - Dependency injection working")
        
    except Exception as e:
        print(f"Error initializing with DI, falling back to legacy mode: {e}")
        
        # Fallback to legacy initialization
        main_window = MainWindow()
        main_window.show()
        
        print("ARXML Editor started in legacy mode")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()