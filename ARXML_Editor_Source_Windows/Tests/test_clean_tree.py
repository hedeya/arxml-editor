#!/usr/bin/env python3
"""
Test clean tree functionality - only show sections with content
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def test_clean_tree():
    """Test clean tree functionality"""
    print("Testing Clean Tree Functionality")
    print("=" * 35)
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create main window
    window = MainWindow()
    window.show()
    
    print("1. Initial state (no document loaded):")
    print(f"   Top level items: {window.tree_navigator.topLevelItemCount()}")
    for i in range(window.tree_navigator.topLevelItemCount()):
        item = window.tree_navigator.topLevelItem(i)
        print(f"   - {item.text(0)} ({item.text(1)})")
    
    # Load sample file
    sample_file = "sample.arxml"
    if os.path.exists(sample_file):
        print(f"\n2. Loading sample file: {sample_file}")
        success = window.app.load_document(sample_file)
        print(f"   Load success: {success}")
        
        if success:
            print(f"   After loading sample file:")
            print(f"   Top level items: {window.tree_navigator.topLevelItemCount()}")
            for i in range(window.tree_navigator.topLevelItemCount()):
                item = window.tree_navigator.topLevelItem(i)
                print(f"   - {item.text(0)} ({item.text(1)})")
                if item.childCount() > 0:
                    print(f"     Children: {item.childCount()}")
                    for j in range(min(2, item.childCount())):
                        child = item.child(j)
                        print(f"       - {child.text(0)} ({child.text(1)})")
    
    # Load ECUC file
    ecuc_file = "Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml"
    if os.path.exists(ecuc_file):
        print(f"\n3. Loading ECUC file: {ecuc_file}")
        success = window.app.load_document(ecuc_file)
        print(f"   Load success: {success}")
        
        if success:
            print(f"   After loading ECUC file:")
            print(f"   Top level items: {window.tree_navigator.topLevelItemCount()}")
            for i in range(window.tree_navigator.topLevelItemCount()):
                item = window.tree_navigator.topLevelItem(i)
                print(f"   - {item.text(0)} ({item.text(1)})")
                if item.childCount() > 0:
                    print(f"     Children: {item.childCount()}")
                    for j in range(min(2, item.childCount())):
                        child = item.child(j)
                        print(f"       - {child.text(0)} ({child.text(1)})")
    
    # Create new document (should clear everything)
    print(f"\n4. Creating new document:")
    window.app.new_document()
    print(f"   After creating new document:")
    print(f"   Top level items: {window.tree_navigator.topLevelItemCount()}")
    for i in range(window.tree_navigator.topLevelItemCount()):
        item = window.tree_navigator.topLevelItem(i)
        print(f"   - {item.text(0)} ({item.text(1)})")
    
    print(f"\nTest completed!")
    
    # Close the application
    app.quit()

if __name__ == "__main__":
    test_clean_tree()