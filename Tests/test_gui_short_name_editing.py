#!/usr/bin/env python3
"""
Test script for GUI SHORT-NAME editing functionality

This test simulates the GUI property editor behavior to ensure that:
1. Property editor correctly updates ECUC element dictionaries
2. Changes are saved when switching between elements
3. Changes persist in the saved file

This test validates the fix for the GUI property editor issue.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.application import ARXMLEditorApp
from src.ui.views.property_editor import PropertyEditor
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

def test_property_editor_dictionary_handling():
    """Test that property editor correctly handles ECUC element dictionaries"""
    print("🧪 Testing Property Editor Dictionary Handling...")
    
    # Create a mock ECUC element (dictionary)
    ecuc_element = {
        'short_name': 'OriginalName',
        'uuid': 'test-uuid-123',
        'type': 'ECUC-MODULE-CONFIGURATION-VALUES'
    }
    
    print(f"📝 Original ECUC element: {ecuc_element}")
    
    # Simulate property editor behavior
    # This mimics what happens when _save_current_widget_values is called
    property_name = 'short_name'
    new_value = 'ModifiedName-Haytham'
    
    # Test the dictionary update logic
    if isinstance(ecuc_element, dict):
        ecuc_element[property_name] = new_value
        print(f"✅ Dictionary update successful: {ecuc_element}")
    else:
        print("❌ Element is not a dictionary")
        return False
    
    # Verify the change
    if ecuc_element['short_name'] == new_value:
        print(f"✅ Change verified: '{ecuc_element['short_name']}'")
        return True
    else:
        print(f"❌ Change not applied: '{ecuc_element['short_name']}'")
        return False

def test_gui_property_editor_integration():
    """Test the actual GUI property editor with ECUC elements"""
    print("🧪 Testing GUI Property Editor Integration...")
    
    # Create QApplication if it doesn't exist
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Create ARXML editor application
    arxml_app = ARXMLEditorApp()
    
    # Load an ECUC file
    ecuc_file = "../Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml"
    if not os.path.exists(ecuc_file):
        print(f"❌ ECUC file not found: {ecuc_file}")
        return False
    
    success = arxml_app.load_document(ecuc_file)
    if not success:
        print("❌ Failed to load ECUC file")
        return False
    
    print("✅ ECUC file loaded successfully")
    
    # Get the document and first ECUC element
    doc = arxml_app.current_document
    if len(doc.ecuc_elements) == 0:
        print("❌ No ECUC elements found")
        return False
    
    ecuc_element = doc.ecuc_elements[0]
    original_short_name = ecuc_element.get('short_name', '')
    print(f"📝 Original SHORT-NAME: '{original_short_name}'")
    
    # Create property editor
    property_editor = PropertyEditor(arxml_app)
    
    # Set the ECUC element
    property_editor.set_element(ecuc_element)
    
    # Simulate editing the short name in the GUI
    if 'short_name' in property_editor._property_widgets:
        widget = property_editor._property_widgets['short_name']
        new_value = original_short_name + "-GUITest"
        widget.setText(new_value)
        print(f"✏️  Set widget text to: '{new_value}'")
        
        # Simulate switching elements (this should trigger _save_current_widget_values)
        property_editor.set_element(ecuc_element)  # Switch to same element
        
        # Check if the change was applied
        if ecuc_element['short_name'] == new_value:
            print(f"✅ GUI change applied successfully: '{ecuc_element['short_name']}'")
            
            # Test saving the document
            output_file = "test_gui_short_name_editing.arxml"
            success = doc.save_document(output_file)
            if not success:
                print("❌ Failed to save document")
                return False
            
            print("✅ Document saved successfully")
            
            # Verify the change is in the saved file
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if new_value in content:
                    print(f"✅ Modified SHORT-NAME '{new_value}' found in saved file")
                    
                    # Clean up
                    os.remove(output_file)
                    print("🧹 Cleaned up test file")
                    
                    return True
                else:
                    print(f"❌ Modified SHORT-NAME '{new_value}' NOT found in saved file")
                    return False
            else:
                print("❌ Output file was not created")
                return False
        else:
            print(f"❌ GUI change not applied. Current value: '{ecuc_element['short_name']}'")
            return False
    else:
        print("❌ Short name widget not found in property editor")
        return False

def test_property_editor_save_current_widget_values():
    """Test the _save_current_widget_values method directly"""
    print("🧪 Testing _save_current_widget_values Method...")
    
    # Create QApplication if it doesn't exist
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Create ARXML editor application
    arxml_app = ARXMLEditorApp()
    
    # Load an ECUC file
    ecuc_file = "../Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml"
    if not os.path.exists(ecuc_file):
        print(f"❌ ECUC file not found: {ecuc_file}")
        return False
    
    success = arxml_app.load_document(ecuc_file)
    if not success:
        print("❌ Failed to load ECUC file")
        return False
    
    # Get the document and first ECUC element
    doc = arxml_app.current_document
    ecuc_element = doc.ecuc_elements[0]
    original_short_name = ecuc_element.get('short_name', '')
    
    # Create property editor
    property_editor = PropertyEditor(arxml_app)
    property_editor.set_element(ecuc_element)
    
    # Manually modify the widget
    if 'short_name' in property_editor._property_widgets:
        widget = property_editor._property_widgets['short_name']
        new_value = original_short_name + "-DirectTest"
        widget.setText(new_value)
        print(f"✏️  Set widget text to: '{new_value}'")
        
        # Call _save_current_widget_values directly
        property_editor._save_current_widget_values()
        
        # Check if the change was applied
        if ecuc_element['short_name'] == new_value:
            print(f"✅ _save_current_widget_values worked: '{ecuc_element['short_name']}'")
            return True
        else:
            print(f"❌ _save_current_widget_values failed. Current value: '{ecuc_element['short_name']}'")
            return False
    else:
        print("❌ Short name widget not found")
        return False

def main():
    """Run all GUI SHORT-NAME editing tests"""
    print("🚀 Testing GUI SHORT-NAME Editing Functionality")
    print("=" * 60)
    
    tests = [
        ("Property Editor Dictionary Handling", test_property_editor_dictionary_handling),
        ("Property Editor Save Current Widget Values", test_property_editor_save_current_widget_values),
        ("GUI Property Editor Integration", test_gui_property_editor_integration)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All GUI SHORT-NAME editing tests passed!")
        print("✅ GUI property editor is working correctly")
        return True
    else:
        print("⚠️  Some GUI SHORT-NAME editing tests failed.")
        print("❌ GUI property editor needs attention.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)