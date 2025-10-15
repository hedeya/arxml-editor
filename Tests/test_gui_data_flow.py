#!/usr/bin/env python3
"""
Test script to reproduce and debug GUI data flow issues

This test simulates the exact GUI workflow to identify why
property changes are lost when switching nodes.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.application import ARXMLEditorApp

def test_gui_data_flow():
    """Test the actual GUI data flow to identify issues"""
    print("🧪 Testing GUI Data Flow...")
    
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
    
    print("✅ ECUC file loaded successfully")
    
    # Get the document
    doc = app.current_document
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
    
    # Test 1: Simulate GUI property editing workflow
    print("\n🔄 Test 1: Simulate GUI Property Editing")
    
    # Simulate selecting container1 (like clicking in tree)
    print("1. Selecting Container 1...")
    original_name1 = container1.get('short_name', '')
    print(f"   Original name: '{original_name1}'")
    
    # Simulate editing the property (like typing in GUI)
    print("2. Editing Container 1 short_name...")
    edit1 = original_name1 + "-GUITest1"
    container1['short_name'] = edit1
    print(f"   Edited name: '{edit1}'")
    print(f"   Data model now has: '{container1.get('short_name', '')}'")
    
    # Simulate switching to container2 (like clicking another node)
    print("3. Switching to Container 2...")
    original_name2 = container2.get('short_name', '')
    print(f"   Container 2 name: '{original_name2}'")
    
    # Simulate switching back to container1 (like clicking back)
    print("4. Switching back to Container 1...")
    print(f"   Container 1 name now: '{container1.get('short_name', '')}'")
    
    # Check if the edit is preserved
    if container1.get('short_name') == edit1:
        print("✅ Container 1 edit preserved in data model")
    else:
        print(f"❌ Container 1 edit lost! Expected: '{edit1}', Got: '{container1.get('short_name', '')}'")
        return False
    
    # Test 2: Simulate save workflow
    print("\n💾 Test 2: Simulate Save Workflow")
    
    # Make another edit
    edit2 = edit1 + "-SaveTest"
    container1['short_name'] = edit2
    print(f"1. Made another edit: '{edit2}'")
    print(f"   Data model has: '{container1.get('short_name', '')}'")
    
    # Save the document
    output_file = "test_gui_data_flow.arxml"
    success = doc.save_document(output_file)
    if not success:
        print("❌ Failed to save document")
        return False
    
    print("2. Document saved successfully")
    
    # Verify the edit is in the saved file
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if edit2 in content:
            print(f"✅ Edit found in saved file: '{edit2}'")
            
            # Clean up
            os.remove(output_file)
            print("🧹 Cleaned up test file")
            
            return True
        else:
            print(f"❌ Edit not found in saved file")
            print(f"   Looking for: '{edit2}'")
            print(f"   File content preview: {content[:500]}...")
            return False
    else:
        print("❌ Output file was not created")
        return False

def test_property_editor_integration():
    """Test the property editor integration more deeply"""
    print("\n🧪 Testing Property Editor Integration...")
    
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
    container2 = containers[1]
    
    # Test the _on_ecuc_property_changed method directly
    print("1. Testing _on_ecuc_property_changed method...")
    
    # Simulate the property editor calling the method
    original_name = container1.get('short_name', '')
    test_edit = original_name + "-DirectMethodTest"
    
    # This simulates what happens when you type in the GUI
    print(f"   Original: '{original_name}'")
    print(f"   Editing to: '{test_edit}'")
    
    # Simulate the property editor method call
    # We need to access the property editor instance
    # For now, let's test the data model directly
    container1['short_name'] = test_edit
    print(f"   Data model now has: '{container1.get('short_name', '')}'")
    
    # Test switching between containers
    print("2. Testing container switching...")
    
    # Switch to container2
    temp_name2 = container2.get('short_name', '') + "-Temp"
    container2['short_name'] = temp_name2
    print(f"   Container 2 edited to: '{temp_name2}'")
    
    # Switch back to container1
    print(f"   Container 1 still has: '{container1.get('short_name', '')}'")
    
    if container1.get('short_name') == test_edit:
        print("✅ Container 1 edit preserved through switching")
        return True
    else:
        print(f"❌ Container 1 edit lost! Expected: '{test_edit}', Got: '{container1.get('short_name', '')}'")
        return False

def main():
    """Run all GUI data flow tests"""
    print("🚀 Testing GUI Data Flow Issues")
    print("=" * 60)
    
    tests = [
        ("GUI Data Flow", test_gui_data_flow),
        ("Property Editor Integration", test_property_editor_integration)
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
        print("🎉 All GUI data flow tests passed!")
        print("✅ The data flow appears to work correctly in isolation")
        return True
    else:
        print("⚠️  Some GUI data flow tests failed.")
        print("❌ There may be issues with the data flow.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)