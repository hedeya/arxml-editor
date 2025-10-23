#!/usr/bin/env python3
"""
Test script to debug property persistence issues
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from src.core.application import ARXMLEditorApp
from src.ui.views.property_editor import PropertyEditor
from src.ui.views.tree_navigator import TreeNavigator

def test_property_persistence():
    """Test property persistence when switching between elements"""
    print("=" * 60)
    print("TESTING PROPERTY PERSISTENCE")
    print("=" * 60)
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create application components
    arxml_app = ARXMLEditorApp()
    property_editor = PropertyEditor(arxml_app)
    tree_navigator = TreeNavigator(arxml_app)
    
    # Connect tree navigator to property editor
    tree_navigator.element_selected.connect(property_editor.set_element)
    
    # Try to load a sample file
    sample_files = [
        "Backup/ECUC/FCA_mPAD_Safety_Can_Can_ecuc.arxml",
        "Backup/ECUC/FCA_mPAD_Safety_CanIf_CanIf_ecuc.arxml",
        "sample.arxml",
        "master.arxml", 
        "slave.arxml",
        "test_output.arxml"
    ]
    
    loaded_file = None
    for sample_file in sample_files:
        if os.path.exists(sample_file):
            print(f"Attempting to load: {sample_file}")
            success = arxml_app.load_document(sample_file)
            if success:
                loaded_file = sample_file
                print(f"✓ Successfully loaded: {sample_file}")
                break
            else:
                print(f"✗ Failed to load: {sample_file}")
    
    if not loaded_file:
        print("No sample files could be loaded. Creating a simple test...")
        return False
    
    # Check if there are ECUC elements to test with
    if not arxml_app.current_document.ecuc_elements:
        print("No ECUC elements found in the loaded document")
        return False
    
    # Get first ECUC element
    first_element = arxml_app.current_document.ecuc_elements[0]
    
    # Create a second ECUC element for testing if only one exists
    if len(arxml_app.current_document.ecuc_elements) == 1:
        print("Only one ECUC element found, creating a second one for testing...")
        second_element = {
            'short_name': 'TestElement',
            'type': 'ECUC-MODULE-CONFIGURATION-VALUES',
            'containers': [],
            'parameters': []
        }
        arxml_app.current_document.ecuc_elements.append(second_element)
        print(f"Created second element: id={id(second_element)} short_name='TestElement'")
    print(f"\nTesting with ECUC element: id={id(first_element)} short_name='{first_element.get('short_name')}'")
    
    # Test 1: Set element in property editor
    print("\n--- TEST 1: Initial element setup ---")
    property_editor.set_element(first_element)
    
    # Simulate user editing the short_name
    if 'short_name' in property_editor._property_widgets:
        short_name_widget = property_editor._property_widgets['short_name']
        original_value = short_name_widget.text()
        test_value = f"{original_value}_EDITED"
        
        print(f"Original value: '{original_value}'")
        print(f"Setting widget to: '{test_value}'")
        
        # Simulate user typing
        short_name_widget.setText(test_value)
        short_name_widget.textChanged.emit(test_value)
        
        # Check if element was updated
        print(f"Element value after edit: '{first_element.get('short_name')}'")
        
        # Test 2: Switch to another element and back
        second_element = arxml_app.current_document.ecuc_elements[1]
        print(f"\n--- TEST 2: Switch to second element ---")
        print(f"Switching to: id={id(second_element)} short_name='{second_element.get('short_name')}'")
        property_editor.set_element(second_element)
        
        print(f"\n--- TEST 3: Switch back to first element ---")
        print(f"Switching back to: id={id(first_element)} short_name='{first_element.get('short_name')}'")
        property_editor.set_element(first_element)
        
        # Check if the widget shows the edited value
        if 'short_name' in property_editor._property_widgets:
            final_widget = property_editor._property_widgets['short_name']
            final_value = final_widget.text()
            print(f"Widget value after return: '{final_value}'")
            print(f"Element value after return: '{first_element.get('short_name')}'")
            
            if final_value == test_value:
                print("✓ SUCCESS: Property persistence worked!")
                return True
            else:
                print("✗ FAILURE: Property persistence failed!")
                print(f"Expected: '{test_value}', Got: '{final_value}'")
                return False
        else:
            print("No short_name widget found after return")
            return False
    else:
        print("✗ FAILURE: No short_name widget found")
        return False

if __name__ == "__main__":
    success = test_property_persistence()
    sys.exit(0 if success else 1)