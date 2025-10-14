#!/usr/bin/env python3
"""
ARXML Editor - Professional Desktop AUTOSAR XML Editor
Main application entry point
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from src.ui.main_window import MainWindow
from src.core.application import ARXMLEditorApp

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("ARXML Editor")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("AUTOSAR Tools")
    
    # Create and show main window
    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()