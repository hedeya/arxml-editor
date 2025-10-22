#!/usr/bin/env python3
"""
Test script to verify property persistence in ARXML editor
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.application import ARXMLEditorApp

def test_property_persistence():
    """Test that property changes persist when switching between elements"""
    print("Testing property persistence...")
    
    # Create application
    app = ARXMLEditorApp()
    
    # Load a test document
    test_file = "Backup/ECUC/FCA_mPAD_Safety_CanTp_CanTp_ecuc.arxml"
    if not os.path.exists(test_file):
        print(f"Test file not found: {test_file}")
        return False
    
    print(f"Loading document: {test_file}")
    success = app.load_document(test_file)
    if not success:
        print("Failed to load document")
        return False
    
    print("Document loaded successfully")
    
    # Get the first ECUC element
    if not app.current_document.ecuc_elements:
        print("No ECUC elements found")
        return False
    
    ecuc_element = app.current_document.ecuc_elements[0]
    print(f"First ECUC element: {ecuc_element.get('short_name')} (id={id(ecuc_element)})")
    
    # Modify the element
    original_name = ecuc_element.get('short_name', '')
    new_name = original_name + "_MODIFIED"
    ecuc_element['short_name'] = new_name
    print(f"Modified short_name: '{original_name}' -> '{new_name}'")
    
    # Verify the change is in the element
    if ecuc_element.get('short_name') != new_name:
        print("ERROR: Element was not modified correctly")
        return False
    
    # Save the document
    print("Saving document...")
    success = app.save_document("test_output.arxml")
    if not success:
        print("Failed to save document")
        return False
    
    print("Document saved successfully")
    
    # Load the saved document and verify the change persisted
    print("Loading saved document to verify changes...")
    app2 = ARXMLEditorApp()
    success = app2.load_document("test_output.arxml")
    if not success:
        print("Failed to load saved document")
        return False
    
    # Check if the change persisted
    if not app2.current_document.ecuc_elements:
        print("No ECUC elements found in saved document")
        return False
    
    saved_element = app2.current_document.ecuc_elements[0]
    saved_name = saved_element.get('short_name', '')
    print(f"Saved element short_name: '{saved_name}'")
    
    if saved_name == new_name:
        print("SUCCESS: Property changes persisted correctly!")
        return True
    else:
        print(f"ERROR: Property changes did not persist. Expected '{new_name}', got '{saved_name}'")
        return False

if __name__ == "__main__":
    success = test_property_persistence()
    sys.exit(0 if success else 1)