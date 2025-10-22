#!/usr/bin/env python3
"""
Test script to verify UI property persistence in ARXML editor
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.application import ARXMLEditorApp
from src.ui.views.property_editor import PropertyEditor
from src.ui.views.tree_navigator import TreeNavigator
from PyQt6.QtWidgets import QApplication

def test_ui_property_persistence():
    """Test that property changes persist in the UI"""
    print("Testing UI property persistence...")
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create application
    arxml_app = ARXMLEditorApp()
    
    # Load a test document
    test_file = "Backup/ECUC/FCA_mPAD_Safety_Can_Can_ecuc.arxml"
    if not os.path.exists(test_file):
        print(f"Test file not found: {test_file}")
        return False
    
    print(f"Loading document: {test_file}")
    success = arxml_app.load_document(test_file)
    if not success:
        print("Failed to load document")
        return False
    
    print("Document loaded successfully")
    
    # Get the first ECUC element
    if not arxml_app.current_document.ecuc_elements:
        print("No ECUC elements found")
        return False
    
    original_element = arxml_app.current_document.ecuc_elements[0]
    print(f"Original element: {original_element.get('short_name')} (id={id(original_element)})")
    
    # Create property editor
    property_editor = PropertyEditor(arxml_app)
    
    # Set the element in the property editor
    property_editor.set_element(original_element)
    print(f"Property editor original element: {property_editor._original_element.get('short_name')} (id={id(property_editor._original_element)})")
    
    # Verify that the original element reference is correct
    if property_editor._original_element is not original_element:
        print("ERROR: Property editor original element reference is incorrect")
        return False
    
    # Modify the element through the property editor
    new_name = original_element.get('short_name', '') + "_UI_MODIFIED"
    property_editor._on_ecuc_property_changed(original_element, "short_name", new_name)
    
    # Verify the change is in the original element
    if original_element.get('short_name') != new_name:
        print(f"ERROR: Original element was not modified correctly. Expected '{new_name}', got '{original_element.get('short_name')}'")
        return False
    
    print(f"Original element modified successfully: '{original_element.get('short_name')}'")
    
    # Save the document
    print("Saving document...")
    success = arxml_app.save_document("test_ui_output.arxml")
    if not success:
        print("Failed to save document")
        return False
    
    print("Document saved successfully")
    
    # Load the saved document and verify the change persisted
    print("Loading saved document to verify changes...")
    arxml_app2 = ARXMLEditorApp()
    success = arxml_app2.load_document("test_ui_output.arxml")
    if not success:
        print("Failed to load saved document")
        return False
    
    # Check if the change persisted
    if not arxml_app2.current_document.ecuc_elements:
        print("No ECUC elements found in saved document")
        return False
    
    saved_element = arxml_app2.current_document.ecuc_elements[0]
    saved_name = saved_element.get('short_name', '')
    print(f"Saved element short_name: '{saved_name}'")
    
    if saved_name == new_name:
        print("SUCCESS: UI property changes persisted correctly!")
        return True
    else:
        print(f"ERROR: UI property changes did not persist. Expected '{new_name}', got '{saved_name}'")
        return False

if __name__ == "__main__":
    success = test_ui_property_persistence()
    sys.exit(0 if success else 1)