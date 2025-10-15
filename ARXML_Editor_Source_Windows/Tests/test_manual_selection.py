#!/usr/bin/env python3
"""
Test manual selection in GUI
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from src.ui.main_window import MainWindow

def test_manual_selection():
    """Test manual selection in GUI"""
    print("Testing Manual Selection in GUI")
    print("=" * 35)
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create main window
    window = MainWindow()
    window.show()
    
    # Load sample file
    sample_file = "sample.arxml"
    if os.path.exists(sample_file):
        print(f"Loading file: {sample_file}")
        success = window.app.load_document(sample_file)
        print(f"Load success: {success}")
        
        if success:
            print(f"\nInitial state:")
            print(f"  Property editor title: {window.property_editor.title_label.text()}")
            print(f"  Property widgets count: {window.property_editor.properties_layout.count()}")
            
            # Simulate clicking on the first component
            print(f"\nSimulating click on first component...")
            sw_comp_item = window.tree_navigator.topLevelItem(0)  # Software Component Types
            if sw_comp_item and sw_comp_item.childCount() > 0:
                comp_item = sw_comp_item.child(0)  # First component
                window.tree_navigator.setCurrentItem(comp_item)
                
                # Check property editor
                print(f"  After selection:")
                print(f"    Property editor title: {window.property_editor.title_label.text()}")
                print(f"    Property widgets count: {window.property_editor.properties_layout.count()}")
                print(f"    Current element: {window.property_editor._current_element}")
                
                if window.property_editor._current_element:
                    print(f"    Element type: {type(window.property_editor._current_element).__name__}")
                    print(f"    Element name: {window.property_editor._current_element.short_name}")
            
            # Simulate clicking on the first port interface
            print(f"\nSimulating click on first port interface...")
            port_if_item = window.tree_navigator.topLevelItem(2)  # Port Interfaces
            if port_if_item and port_if_item.childCount() > 0:
                interface_item = port_if_item.child(0)  # First interface
                window.tree_navigator.setCurrentItem(interface_item)
                
                # Check property editor
                print(f"  After selection:")
                print(f"    Property editor title: {window.property_editor.title_label.text()}")
                print(f"    Property widgets count: {window.property_editor.properties_layout.count()}")
                print(f"    Current element: {window.property_editor._current_element}")
                
                if window.property_editor._current_element:
                    print(f"    Element type: {type(window.property_editor._current_element).__name__}")
                    print(f"    Element name: {window.property_editor._current_element.short_name}")
    
    print(f"\nTest completed!")
    print(f"To test manually:")
    print(f"1. Run: python3 main.py")
    print(f"2. File -> Open -> select sample.arxml")
    print(f"3. Click on items in the tree navigator (left panel)")
    print(f"4. Check the Properties tab (right panel) for updates")
    
    # Close the application
    app.quit()

if __name__ == "__main__":
    test_manual_selection()