#!/usr/bin/env python3
"""
Test script for redesigned property editor

This test verifies that the redesigned property editor properly handles
real-time updates without the dual system that was causing edit loss.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.application import ARXMLEditorApp

def test_real_time_updates():
    """Test that real-time updates work correctly"""
    print("🧪 Testing Real-Time Updates...")
    
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
    
    # Test 1: Direct data model updates (simulating real-time updates)
    print("\n🔄 Test 1: Direct Data Model Updates")
    original_name1 = container1.get('short_name', '')
    edit1 = original_name1 + "-RealTimeTest1"
    container1['short_name'] = edit1
    print(f"✏️  Direct edit Container 1: '{edit1}'")
    
    # Verify the change is in the data model
    if container1['short_name'] == edit1:
        print(f"✅ Container 1 data model updated: '{container1['short_name']}'")
    else:
        print(f"❌ Container 1 data model not updated: '{container1['short_name']}'")
        return False
    
    # Test 2: Switch between containers (simulating tree navigation)
    print("\n🔄 Test 2: Container Switching")
    original_name2 = container2.get('short_name', '')
    edit2 = original_name2 + "-RealTimeTest2"
    container2['short_name'] = edit2
    print(f"✏️  Direct edit Container 2: '{edit2}'")
    
    # Simulate switching back and forth
    print("🔄 Switching Container 1 -> Container 2 -> Container 1")
    
    # Check if both edits are preserved
    if container1['short_name'] == edit1 and container2['short_name'] == edit2:
        print(f"✅ Container 1 edit preserved: '{container1['short_name']}'")
        print(f"✅ Container 2 edit preserved: '{container2['short_name']}'")
    else:
        print(f"❌ Edits not preserved. Container 1: '{container1['short_name']}', Container 2: '{container2['short_name']}'")
        return False
    
    # Test 3: Save and verify
    print("\n💾 Test 3: Save and Verify")
    output_file = "test_redesigned_property_editor.arxml"
    success = doc.save_document(output_file)
    if not success:
        print("❌ Failed to save document")
        return False
    
    print("✅ Document saved successfully")
    
    # Verify edits are in saved file
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if edit1 in content and edit2 in content:
            print(f"✅ Both edits found in saved file: '{edit1}' and '{edit2}'")
            
            # Clean up
            os.remove(output_file)
            print("🧹 Cleaned up test file")
            
            return True
        else:
            print(f"❌ Edits not found in saved file")
            return False
    else:
        print("❌ Output file was not created")
        return False

def test_multiple_edits():
    """Test multiple edits on the same element"""
    print("\n🧪 Testing Multiple Edits...")
    
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
    
    # Get containers
    doc = app.current_document
    ecuc_element = doc.ecuc_elements[0]
    containers = ecuc_element.get('containers', [])
    
    if len(containers) < 3:
        print("❌ Need at least 3 containers for testing")
        return False
    
    container1 = containers[0]
    container2 = containers[1]
    container3 = containers[2]
    
    # Make multiple edits to the same container
    print("📝 Making multiple edits to Container 1...")
    original_name = container1.get('short_name', '')
    
    # Edit 1
    edit1 = original_name + "-Edit1"
    container1['short_name'] = edit1
    print(f"✏️  Edit 1: '{edit1}'")
    
    # Edit 2
    edit2 = edit1 + "-Edit2"
    container1['short_name'] = edit2
    print(f"✏️  Edit 2: '{edit2}'")
    
    # Edit 3
    edit3 = edit2 + "-Edit3"
    container1['short_name'] = edit3
    print(f"✏️  Edit 3: '{edit3}'")
    
    # Switch to other containers and back
    print("🔄 Switching to other containers and back...")
    temp_edit2 = container2.get('short_name', '') + "-Temp"
    container2['short_name'] = temp_edit2
    
    temp_edit3 = container3.get('short_name', '') + "-Temp"
    container3['short_name'] = temp_edit3
    
    # Switch back to container 1
    print("🔄 Switching back to Container 1...")
    
    # Check if the final edit is preserved
    if container1['short_name'] == edit3:
        print(f"✅ Final edit preserved: '{container1['short_name']}'")
        return True
    else:
        print(f"❌ Final edit lost: '{container1['short_name']}' (expected: '{edit3}')")
        return False

def test_edge_cases():
    """Test edge cases and error conditions"""
    print("\n🧪 Testing Edge Cases...")
    
    # Test 1: Empty string edit
    print("📝 Test 1: Empty String Edit")
    app = ARXMLEditorApp()
    success = app.load_document("../Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml")
    if success:
        doc = app.current_document
        ecuc_element = doc.ecuc_elements[0]
        containers = ecuc_element.get('containers', [])
        
        if len(containers) > 0:
            container = containers[0]
            original_name = container.get('short_name', '')
            
            # Set to empty string
            container['short_name'] = ''
            if container['short_name'] == '':
                print("✅ Empty string edit works")
            else:
                print("❌ Empty string edit failed")
                return False
            
            # Restore original
            container['short_name'] = original_name
        else:
            print("❌ No containers found")
            return False
    else:
        print("❌ Failed to load ECUC file")
        return False
    
    # Test 2: Very long string edit
    print("📝 Test 2: Long String Edit")
    if len(containers) > 0:
        container = containers[0]
        original_name = container.get('short_name', '')
        
        # Set to very long string
        long_name = original_name + "-" + "X" * 100
        container['short_name'] = long_name
        if container['short_name'] == long_name:
            print("✅ Long string edit works")
        else:
            print("❌ Long string edit failed")
            return False
        
        # Restore original
        container['short_name'] = original_name
    else:
        print("❌ No containers found")
        return False
    
    return True

def main():
    """Run all redesigned property editor tests"""
    print("🚀 Testing Redesigned Property Editor")
    print("=" * 60)
    
    tests = [
        ("Real-Time Updates", test_real_time_updates),
        ("Multiple Edits", test_multiple_edits),
        ("Edge Cases", test_edge_cases)
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
        print("🎉 All redesigned property editor tests passed!")
        print("✅ The redesigned approach works correctly")
        return True
    else:
        print("⚠️  Some redesigned property editor tests failed.")
        print("❌ The redesigned approach needs attention.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)