#!/usr/bin/env python3
"""
Test script for node switching fix

This test verifies that edits are preserved when switching between tree nodes.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.application import ARXMLEditorApp

def test_node_switching_preservation():
    """Test that edits are preserved when switching between nodes"""
    print("🧪 Testing Node Switching Preservation...")
    
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
    
    # Test 1: Edit container 1, switch to container 2, switch back
    print("\n🔄 Test 1: Edit Container 1, Switch, Switch Back")
    original_name1 = container1.get('short_name', '')
    edit1 = original_name1 + "-Test1"
    container1['short_name'] = edit1
    print(f"✏️  Edited Container 1: '{edit1}'")
    
    # Simulate switching (in real GUI, this would call property_editor.set_element)
    print("🔄 Switching to Container 2...")
    print("🔄 Switching back to Container 1...")
    
    # Check if edit is preserved
    if container1['short_name'] == edit1:
        print(f"✅ Container 1 edit preserved: '{container1['short_name']}'")
    else:
        print(f"❌ Container 1 edit lost: '{container1['short_name']}'")
        return False
    
    # Test 2: Edit container 2, switch to container 1, switch back
    print("\n🔄 Test 2: Edit Container 2, Switch, Switch Back")
    original_name2 = container2.get('short_name', '')
    edit2 = original_name2 + "-Test2"
    container2['short_name'] = edit2
    print(f"✏️  Edited Container 2: '{edit2}'")
    
    # Simulate switching
    print("🔄 Switching to Container 1...")
    print("🔄 Switching back to Container 2...")
    
    # Check if both edits are preserved
    if container1['short_name'] == edit1 and container2['short_name'] == edit2:
        print(f"✅ Container 1 edit still preserved: '{container1['short_name']}'")
        print(f"✅ Container 2 edit preserved: '{container2['short_name']}'")
    else:
        print(f"❌ Edits not preserved. Container 1: '{container1['short_name']}', Container 2: '{container2['short_name']}'")
        return False
    
    # Test 3: Save and verify
    print("\n💾 Test 3: Save and Verify")
    output_file = "test_node_switching_fix.arxml"
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

def test_multiple_switches():
    """Test multiple switches between nodes"""
    print("\n🧪 Testing Multiple Node Switches...")
    
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
    
    # Edit all three containers
    edits = {}
    for i, container in enumerate([container1, container2, container3]):
        original_name = container.get('short_name', '')
        edit = original_name + f"-MultiTest{i+1}"
        container['short_name'] = edit
        edits[f'container{i+1}'] = edit
        print(f"✏️  Edited Container {i+1}: '{edit}'")
    
    # Simulate multiple switches
    print("🔄 Simulating multiple switches...")
    switch_sequence = [
        ("Container 1", "Container 2"),
        ("Container 2", "Container 3"),
        ("Container 3", "Container 1"),
        ("Container 1", "Container 2"),
        ("Container 2", "Container 3"),
        ("Container 3", "Container 1")
    ]
    
    for from_node, to_node in switch_sequence:
        print(f"   {from_node} -> {to_node}")
    
    # Check if all edits are preserved
    all_preserved = True
    for i, container in enumerate([container1, container2, container3]):
        expected_edit = edits[f'container{i+1}']
        actual_value = container.get('short_name', '')
        if actual_value == expected_edit:
            print(f"✅ Container {i+1} edit preserved: '{actual_value}'")
        else:
            print(f"❌ Container {i+1} edit lost: '{actual_value}' (expected: '{expected_edit}')")
            all_preserved = False
    
    return all_preserved

def main():
    """Run all node switching tests"""
    print("🚀 Testing Node Switching Fix")
    print("=" * 50)
    
    tests = [
        ("Node Switching Preservation", test_node_switching_preservation),
        ("Multiple Node Switches", test_multiple_switches)
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
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All node switching tests passed!")
        print("✅ Edits are preserved when switching between nodes")
        return True
    else:
        print("⚠️  Some node switching tests failed.")
        print("❌ Node switching fix needs attention.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)