#!/usr/bin/env python3
"""
Test GUI with ECUC file
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def test_gui_ecuc():
    """Test GUI with ECUC file"""
    print("Testing GUI with ECUC File")
    print("=" * 30)
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create main window
    window = MainWindow()
    window.show()
    
    # Load ECUC file
    ecuc_file = "Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml"
    if os.path.exists(ecuc_file):
        print(f"Loading file: {ecuc_file}")
        
        # Load document through the GUI
        success = window.app.load_document(ecuc_file)
        print(f"Load success: {success}")
        
        if success and window.app.current_document:
            doc = window.app.current_document
            print(f"Document loaded successfully")
            print(f"ECUC elements: {len(doc.ecuc_elements)}")
            
            # Check tree navigator content
            print(f"\nTree Navigator Content:")
            print(f"  Top level items: {window.tree_navigator.topLevelItemCount()}")
            
            # Check ECUC elements section
            ecuc_item = window.tree_navigator.topLevelItem(4)  # ECUC Elements (5th item)
            if ecuc_item:
                print(f"  ECUC Elements item: {ecuc_item.text(0)} ({ecuc_item.text(1)})")
                print(f"  ECUC children count: {ecuc_item.childCount()}")
                
                if ecuc_item.childCount() > 0:
                    print("  ECUC children:")
                    for i in range(min(3, ecuc_item.childCount())):  # Show first 3
                        child = ecuc_item.child(i)
                        print(f"    - {child.text(0)} ({child.text(1)})")
                        print(f"      Grandchildren: {child.childCount()}")
                        
                        if child.childCount() > 0:
                            print("      Containers:")
                            for j in range(min(2, child.childCount())):  # Show first 2
                                grandchild = child.child(j)
                                print(f"        - {grandchild.text(0)} ({grandchild.text(1)})")
                                print(f"          Parameters: {grandchild.childCount()}")
                else:
                    print("  No ECUC children found!")
            else:
                print("  ECUC Elements item not found!")
            
            # Check validation
            print(f"\nValidation issues: {len(window.app.validation_service.issues)}")
            if window.app.validation_service.issues:
                print("  First issue:")
                issue = window.app.validation_service.issues[0]
                print(f"    [{issue.severity.value}] {issue.message[:100]}...")
        else:
            print("Failed to load document")
    else:
        print(f"ECUC file {ecuc_file} not found")
    
    print(f"\nTest completed!")
    print(f"To test manually:")
    print(f"1. Run: python3 main.py")
    print(f"2. File -> Open -> select Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml")
    print(f"3. Check the tree navigator for ECUC Elements")
    
    # Close the application
    app.quit()

if __name__ == "__main__":
    test_gui_ecuc()