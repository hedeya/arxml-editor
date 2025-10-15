#!/usr/bin/env python3
"""
Test Property Editor functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def test_property_editor():
    """Test Property Editor functionality"""
    print("Testing Property Editor")
    print("=" * 30)
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create main window
    window = MainWindow()
    window.show()
    
    # Test loading sample file
    sample_file = "sample.arxml"
    if os.path.exists(sample_file):
        print(f"Loading file: {sample_file}")
        
        # Load document through the GUI
        success = window.app.load_document(sample_file)
        print(f"Load success: {success}")
        
        if success and window.app.current_document:
            doc = window.app.current_document
            print(f"Document loaded successfully")
            print(f"Software component types: {len(doc.sw_component_types)}")
            print(f"Port interfaces: {len(doc.port_interfaces)}")
            
            # Test property editor with first component
            if doc.sw_component_types:
                component = doc.sw_component_types[0]
                print(f"\nTesting property editor with component: {component.short_name}")
                
                # Set element in property editor
                window.property_editor.set_element(component)
                print(f"Property editor current element: {window.property_editor._current_element}")
                print(f"Property editor title: {window.property_editor.title_label.text()}")
                
                # Check if properties are displayed
                property_widgets_count = window.property_editor.properties_layout.count()
                print(f"Property widgets count: {property_widgets_count}")
                
                if property_widgets_count > 0:
                    print("Property editor has content!")
                    for i in range(property_widgets_count):
                        item = window.property_editor.properties_layout.itemAt(i)
                        if item and item.widget():
                            widget = item.widget()
                            print(f"  Widget {i}: {type(widget).__name__}")
                            if hasattr(widget, 'text'):
                                print(f"    Text: {widget.text()}")
                else:
                    print("Property editor is empty!")
            
            # Test property editor with first port interface
            if doc.port_interfaces:
                port_interface = doc.port_interfaces[0]
                print(f"\nTesting property editor with port interface: {port_interface.short_name}")
                
                # Set element in property editor
                window.property_editor.set_element(port_interface)
                print(f"Property editor current element: {window.property_editor._current_element}")
                print(f"Property editor title: {window.property_editor.title_label.text()}")
                
                # Check if properties are displayed
                property_widgets_count = window.property_editor.properties_layout.count()
                print(f"Property widgets count: {property_widgets_count}")
                
                if property_widgets_count > 0:
                    print("Property editor has content!")
                    for i in range(property_widgets_count):
                        item = window.property_editor.properties_layout.itemAt(i)
                        if item and item.widget():
                            widget = item.widget()
                            print(f"  Widget {i}: {type(widget).__name__}")
                            if hasattr(widget, 'text'):
                                print(f"    Text: {widget.text()}")
                else:
                    print("Property editor is empty!")
        else:
            print("Failed to load document")
    else:
        print(f"Sample file {sample_file} not found")
    
    # Close the application
    app.quit()

if __name__ == "__main__":
    test_property_editor()