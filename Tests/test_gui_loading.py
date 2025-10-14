#!/usr/bin/env python3
"""
Test GUI loading functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def test_gui_loading():
    """Test GUI loading functionality"""
    print("Testing GUI Loading")
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
        
        if success:
            print(f"Document loaded: {window.app.current_document is not None}")
            print(f"Tree navigator items: {window.tree_navigator.topLevelItemCount()}")
            print(f"Validation issues: {len(window.app.validation_service.issues)}")
            
            # Check if tree has content
            if window.tree_navigator.topLevelItemCount() > 0:
                print("Tree navigator has content:")
                for i in range(window.tree_navigator.topLevelItemCount()):
                    item = window.tree_navigator.topLevelItem(i)
                    print(f"  - {item.text(0)} ({item.text(1)})")
                    if item.childCount() > 0:
                        for j in range(item.childCount()):
                            child = item.child(j)
                            print(f"    - {child.text(0)} ({child.text(1)})")
            else:
                print("Tree navigator is empty!")
            
            # Check validation list
            print(f"Validation list items: {window.validation_list.issues_list.count()}")
            if window.validation_list.issues_list.count() > 0:
                print("Validation issues found:")
                for i in range(window.validation_list.issues_list.count()):
                    item = window.validation_list.issues_list.item(i)
                    print(f"  - {item.text()}")
        else:
            print("Failed to load document")
    else:
        print(f"Sample file {sample_file} not found")
    
    # Close the application
    app.quit()

if __name__ == "__main__":
    test_gui_loading()