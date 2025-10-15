#!/usr/bin/env python3
"""
Test script to verify real GUI behavior

This test simulates the exact GUI workflow to verify that
the fixes work correctly in the actual application.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_property_editor_lambda_behavior():
    """Test the property editor lambda behavior directly"""
    print("🧪 Testing Property Editor Lambda Behavior...")
    
    # Import the property editor
    from src.ui.views.property_editor import PropertyEditor
    from src.core.application import ARXMLEditorApp
    from PyQt6.QtWidgets import QApplication
    
    # Create application
    app = QApplication([])
    editor_app = ARXMLEditorApp()
    property_editor = PropertyEditor(editor_app)
    
    # Load an ECUC file
    ecuc_file = "../Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml"
    if not os.path.exists(ecuc_file):
        print(f"❌ ECUC file not found: {ecuc_file}")
        return False
    
    success = editor_app.load_document(ecuc_file)
    if not success:
        print("❌ Failed to load ECUC file")
        return False
    
    # Get the document
    doc = editor_app.current_document
    if len(doc.ecuc_elements) == 0:
        print("❌ No ECUC elements found")
        return False
    
    # Get containers for testing
    ecuc_element = doc.ecuc_elements[0]
    containers = ecuc_element.get('containers', [])
    
    if len(containers) < 2:
        print("❌ Need at least 2 containers for testing")
        return False
    
    container1 = containers[0]
    container2 = containers[1]
    
    print(f"📝 Container 1: '{container1.get('short_name', '')}'")
    print(f"📝 Container 2: '{container2.get('short_name', '')}'")
    
    # Test 1: Set element and check lambda behavior
    print("\n🔄 Test 1: Lambda Behavior Test")
    
    # Set container1 as current element
    print("1. Setting Container 1 as current element...")
    property_editor.set_element(container1)
    print(f"   Current element: {property_editor._current_element}")
    print(f"   Current element short_name: '{property_editor._current_element.get('short_name', '')}'")
    
    # Check if widgets were created
    if "short_name" in property_editor._property_widgets:
        print("✅ Short name widget created")
        short_name_widget = property_editor._property_widgets["short_name"]
        print(f"   Widget text: '{short_name_widget.text()}'")
    else:
        print("❌ Short name widget not created")
        return False
    
    # Test 2: Simulate typing in the widget
    print("\n2. Simulating typing in the widget...")
    original_text = short_name_widget.text()
    new_text = original_text + "-LambdaTest"
    
    # Simulate the textChanged signal
    short_name_widget.setText(new_text)
    print(f"   Widget text changed to: '{short_name_widget.text()}'")
    print(f"   Data model short_name: '{property_editor._current_element.get('short_name', '')}'")
    
    # Check if the data model was updated
    if property_editor._current_element.get('short_name') == new_text:
        print("✅ Data model updated correctly")
    else:
        print(f"❌ Data model not updated! Expected: '{new_text}', Got: '{property_editor._current_element.get('short_name', '')}'")
        return False
    
    # Test 3: Switch to another element
    print("\n3. Switching to Container 2...")
    property_editor.set_element(container2)
    print(f"   Current element: {property_editor._current_element}")
    print(f"   Current element short_name: '{property_editor._current_element.get('short_name', '')}'")
    
    # Test 4: Switch back to Container 1
    print("\n4. Switching back to Container 1...")
    property_editor.set_element(container1)
    print(f"   Current element: {property_editor._current_element}")
    print(f"   Current element short_name: '{property_editor._current_element.get('short_name', '')}'")
    
    # Check if the edit is preserved
    if property_editor._current_element.get('short_name') == new_text:
        print("✅ Edit preserved when switching back")
    else:
        print(f"❌ Edit lost when switching back! Expected: '{new_text}', Got: '{property_editor._current_element.get('short_name', '')}'")
        return False
    
    # Test 5: Check widget text
    if "short_name" in property_editor._property_widgets:
        widget_text = property_editor._property_widgets["short_name"].text()
        print(f"   Widget text: '{widget_text}'")
        if widget_text == new_text:
            print("✅ Widget text matches data model")
        else:
            print(f"❌ Widget text doesn't match data model! Expected: '{new_text}', Got: '{widget_text}'")
            return False
    
    return True

def test_save_functionality():
    """Test the save functionality"""
    print("\n🧪 Testing Save Functionality...")
    
    from src.core.application import ARXMLEditorApp
    
    # Create application
    app = ARXMLEditorApp()
    
    # Load an ECUC file
    ecuc_file = "../Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml"
    if not os.path.exists(ecuc_file):
        print(f"❌ ECUC file not found: {ecuc_file}")
        return False
    
    success = app.load_document(ecuc_file)
    if not success:
        print("❌ Failed to load ECUC file")
        return False
    
    # Get the document
    doc = app.current_document
    ecuc_element = doc.ecuc_elements[0]
    containers = ecuc_element.get('containers', [])
    
    if len(containers) < 2:
        print("❌ Need at least 2 containers for testing")
        return False
    
    container1 = containers[0]
    
    # Make an edit
    original_name = container1.get('short_name', '')
    edit_name = original_name + "-SaveTest"
    container1['short_name'] = edit_name
    print(f"📝 Edited container name: '{edit_name}'")
    
    # Save the document
    output_file = "test_real_gui_behavior.arxml"
    success = doc.save_document(output_file)
    if not success:
        print("❌ Failed to save document")
        return False
    
    print("✅ Document saved successfully")
    
    # Verify the edit is in the saved file
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if edit_name in content:
            print(f"✅ Edit found in saved file: '{edit_name}'")
            
            # Clean up
            os.remove(output_file)
            print("🧹 Cleaned up test file")
            
            return True
        else:
            print(f"❌ Edit not found in saved file")
            print(f"   Looking for: '{edit_name}'")
            return False
    else:
        print("❌ Output file was not created")
        return False

def main():
    """Run all real GUI behavior tests"""
    print("🚀 Testing Real GUI Behavior")
    print("=" * 60)
    
    tests = [
        ("Property Editor Lambda Behavior", test_property_editor_lambda_behavior),
        ("Save Functionality", test_save_functionality)
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
        print("🎉 All real GUI behavior tests passed!")
        print("✅ The fixes should work correctly in the actual application")
        return True
    else:
        print("⚠️  Some real GUI behavior tests failed.")
        print("❌ The fixes may need more work.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)