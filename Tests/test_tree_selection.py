#!/usr/bin/env python3
"""
Test Tree Selection and Property Editor Connection
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QGroupBox
from PyQt6.QtCore import QTimer
from src.ui.main_window import MainWindow

def test_tree_selection():
    """Test tree selection and property editor connection"""
    print("Testing Tree Selection and Property Editor")
    print("=" * 45)
    
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
            
            # Check tree navigator content
            print(f"\nTree Navigator Content:")
            print(f"  Top level items: {window.tree_navigator.topLevelItemCount()}")
            
            # Get the first software component type item
            sw_comp_item = window.tree_navigator.topLevelItem(0)  # Software Component Types
            if sw_comp_item and sw_comp_item.childCount() > 0:
                comp_item = sw_comp_item.child(0)  # First component
                print(f"  Component item: {comp_item.text(0)} ({comp_item.text(1)})")
                
                # Simulate selection
                print(f"\nSimulating selection of component...")
                window.tree_navigator.setCurrentItem(comp_item)
                
                # Check if property editor was updated
                print(f"Property editor current element: {window.property_editor._current_element}")
                print(f"Property editor title: {window.property_editor.title_label.text()}")
                
                # Check property widgets
                property_widgets_count = window.property_editor.properties_layout.count()
                print(f"Property widgets count: {property_widgets_count}")
                
                if property_widgets_count > 0:
                    print("Property editor widgets:")
                    for i in range(property_widgets_count):
                        item = window.property_editor.properties_layout.itemAt(i)
                        if item and item.widget():
                            widget = item.widget()
                            print(f"  Widget {i}: {type(widget).__name__}")
                            if isinstance(widget, QGroupBox):
                                print(f"    Group title: {widget.title()}")
                                # Check group content
                                group_layout = widget.layout()
                                if group_layout:
                                    print(f"    Group items: {group_layout.count()}")
                                    for j in range(group_layout.count()):
                                        group_item = group_layout.itemAt(j)
                                        if group_item and group_item.widget():
                                            group_widget = group_item.widget()
                                            print(f"      Item {j}: {type(group_widget).__name__}")
                                            if hasattr(group_widget, 'text'):
                                                print(f"        Text: {group_widget.text()}")
                                            elif hasattr(group_widget, 'toPlainText'):
                                                print(f"        Text: {group_widget.toPlainText()}")
                else:
                    print("Property editor is empty!")
            
            # Test port interface selection
            port_if_item = window.tree_navigator.topLevelItem(2)  # Port Interfaces
            if port_if_item and port_if_item.childCount() > 0:
                interface_item = port_if_item.child(0)  # First interface
                print(f"\nPort Interface item: {interface_item.text(0)} ({interface_item.text(1)})")
                
                # Simulate selection
                print(f"Simulating selection of port interface...")
                window.tree_navigator.setCurrentItem(interface_item)
                
                # Check if property editor was updated
                print(f"Property editor current element: {window.property_editor._current_element}")
                print(f"Property editor title: {window.property_editor.title_label.text()}")
        else:
            print("Failed to load document")
    else:
        print(f"Sample file {sample_file} not found")
    
    # Close the application
    app.quit()

if __name__ == "__main__":
    test_tree_selection()