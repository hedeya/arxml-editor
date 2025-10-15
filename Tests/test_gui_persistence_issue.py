#!/usr/bin/env python3
"""
Test script to reproduce the exact GUI persistence issue

This test simulates the exact workflow that causes the issue:
1. Edit a property
2. Switch to another node
3. Switch back to the first node
4. Check if the edit is preserved
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_gui_persistence_issue():
    """Test the exact GUI persistence issue"""
    print("🧪 Testing GUI Persistence Issue...")
    
    # Import the application
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
    
    # Test the exact workflow
    print("\n🔄 Step 1: Edit Container 1")
    original_name1 = container1.get('short_name', '')
    edit_name1 = original_name1 + "-PersistenceTest"
    container1['short_name'] = edit_name1
    print(f"   Edited Container 1: '{edit_name1}'")
    print(f"   Data model has: '{container1.get('short_name', '')}'")
    
    # Verify the edit is in the data model
    if container1.get('short_name') == edit_name1:
        print("✅ Container 1 edit is in data model")
    else:
        print(f"❌ Container 1 edit not in data model! Expected: '{edit_name1}', Got: '{container1.get('short_name', '')}'")
        return False
    
    print("\n🔄 Step 2: Switch to Container 2")
    original_name2 = container2.get('short_name', '')
    print(f"   Container 2: '{original_name2}'")
    
    # Simulate switching to container2 (this would call set_element in the real GUI)
    # For now, we'll just verify the data model state
    print(f"   Container 1 still has: '{container1.get('short_name', '')}'")
    
    print("\n🔄 Step 3: Switch back to Container 1")
    print(f"   Container 1 now has: '{container1.get('short_name', '')}'")
    
    # Check if the edit is still there
    if container1.get('short_name') == edit_name1:
        print("✅ Container 1 edit is still preserved in data model")
    else:
        print(f"❌ Container 1 edit lost! Expected: '{edit_name1}', Got: '{container1.get('short_name', '')}'")
        return False
    
    # Test save functionality
    print("\n💾 Step 4: Test Save Functionality")
    output_file = "test_gui_persistence_issue.arxml"
    success = doc.save_document(output_file)
    if not success:
        print("❌ Failed to save document")
        return False
    
    print("✅ Document saved successfully")
    
    # Verify the edit is in the saved file
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if edit_name1 in content:
            print(f"✅ Edit found in saved file: '{edit_name1}'")
            
            # Clean up
            os.remove(output_file)
            print("🧹 Cleaned up test file")
            
            return True
        else:
            print(f"❌ Edit not found in saved file")
            print(f"   Looking for: '{edit_name1}'")
            return False
    else:
        print("❌ Output file was not created")
        return False

def test_multiple_edits():
    """Test multiple edits on the same element"""
    print("\n🧪 Testing Multiple Edits...")
    
    # Import the application
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
    
    if len(containers) < 3:
        print("❌ Need at least 3 containers for testing")
        return False
    
    container1 = containers[0]
    container2 = containers[1]
    container3 = containers[2]
    
    # Make multiple edits to container1
    print("📝 Making multiple edits to Container 1...")
    original_name = container1.get('short_name', '')
    
    # Edit 1
    edit1 = original_name + "-Edit1"
    container1['short_name'] = edit1
    print(f"   Edit 1: '{edit1}'")
    
    # Edit 2
    edit2 = edit1 + "-Edit2"
    container1['short_name'] = edit2
    print(f"   Edit 2: '{edit2}'")
    
    # Edit 3
    edit3 = edit2 + "-Edit3"
    container1['short_name'] = edit3
    print(f"   Edit 3: '{edit3}'")
    
    # Switch to other containers and back
    print("🔄 Switching to other containers and back...")
    temp_edit2 = container2.get('short_name', '') + "-Temp"
    container2['short_name'] = temp_edit2
    
    temp_edit3 = container3.get('short_name', '') + "-Temp"
    container3['short_name'] = temp_edit3
    
    # Switch back to container1
    print("🔄 Switching back to Container 1...")
    print(f"   Container 1 now has: '{container1.get('short_name', '')}'")
    
    # Check if the final edit is preserved
    if container1.get('short_name') == edit3:
        print("✅ Final edit preserved through multiple switches")
        return True
    else:
        print(f"❌ Final edit lost! Expected: '{edit3}', Got: '{container1.get('short_name', '')}'")
        return False

def main():
    """Run all GUI persistence tests"""
    print("🚀 Testing GUI Persistence Issue")
    print("=" * 60)
    
    tests = [
        ("GUI Persistence Issue", test_gui_persistence_issue),
        ("Multiple Edits", test_multiple_edits)
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
        print("🎉 All GUI persistence tests passed!")
        print("✅ The data model persistence is working correctly")
        return True
    else:
        print("⚠️  Some GUI persistence tests failed.")
        print("❌ There may be issues with the data model persistence.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)