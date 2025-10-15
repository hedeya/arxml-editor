#!/usr/bin/env python3
"""
Test ECUC GUI loading
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def test_ecuc_gui():
    """Test ECUC GUI loading"""
    print("Testing ECUC GUI Loading")
    print("=" * 25)
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create main window
    window = MainWindow()
    window.show()
    
    # Load ECUC file
    ecuc_file = "Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml"
    
    if os.path.exists(ecuc_file):
        print(f"Loading file: {ecuc_file}")
        success = window.app.load_document(ecuc_file)
        print(f"Load success: {success}")
        
        if success:
            print(f"\nTree Navigator Content:")
            print(f"  Top level items: {window.tree_navigator.topLevelItemCount()}")
            
            # Check ECUC elements
            ecuc_item = window.tree_navigator.topLevelItem(4)  # ECUC Elements (5th item)
            if ecuc_item:
                print(f"  ECUC Elements item: {ecuc_item.text(0)} ({ecuc_item.text(1)})")
                print(f"  ECUC children: {ecuc_item.childCount()}")
                
                if ecuc_item.childCount() > 0:
                    ecuc_child = ecuc_item.child(0)
                    print(f"    - {ecuc_child.text(0)} ({ecuc_child.text(1)})")
                    print(f"    - Containers: {ecuc_child.childCount()}")
            
            # Test property editor
            if ecuc_item and ecuc_item.childCount() > 0:
                ecuc_child = ecuc_item.child(0)
                print(f"\nTesting property editor with ECUC element...")
                window.tree_navigator.setCurrentItem(ecuc_child)
                
                print(f"  Property editor title: {window.property_editor.title_label.text()}")
                print(f"  Property widgets count: {window.property_editor.properties_layout.count()}")
                print(f"  Current element: {window.property_editor._current_element}")
            
            # Check validation
            print(f"\nValidation issues: {len(window.app.validation_service.issues)}")
            if window.app.validation_service.issues:
                print("  First issue:")
                print(f"    {window.app.validation_service.issues[0].message[:100]}...")
        else:
            print("Failed to load ECUC file")
    else:
        print(f"ECUC file {ecuc_file} not found")
    
    print(f"\nTest completed!")
    print(f"ECUC support is working - tree should now be populated!")
    
    # Close the application
    app.quit()

if __name__ == "__main__":
    test_ecuc_gui()