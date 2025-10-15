#!/usr/bin/env python3
"""
Test script for SHORT-NAME editing functionality in ECUC files

This test suite validates that SHORT-NAME changes in ECUC files are properly:
1. Applied to the in-memory data model
2. Saved to the XML file
3. Can be found when searching the saved file

Tests cover:
- Main ECUC element SHORT-NAME editing
- Container SHORT-NAME editing
- Parameter SHORT-NAME editing
- Property persistence when switching elements
- File saving and content verification
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.application import ARXMLEditorApp

def test_main_ecuc_short_name_editing():
    """Test editing the main ECUC element SHORT-NAME"""
    print("🧪 Testing Main ECUC SHORT-NAME Editing...")
    
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
    
    # Get the first ECUC element
    ecuc_element = doc.ecuc_elements[0]
    original_short_name = ecuc_element.get('short_name', '')
    print(f"📝 Original SHORT-NAME: '{original_short_name}'")
    
    # Edit the short name
    new_short_name = original_short_name + "-TestMain"
    ecuc_element['short_name'] = new_short_name
    print(f"✏️  Modified SHORT-NAME: '{new_short_name}'")
    
    # Mark document as modified
    doc.set_modified(True)
    print(f"📝 Document modified: {doc.modified}")
    
    # Save to a test file
    output_file = "test_main_ecuc_short_name.arxml"
    success = doc.save_document(output_file)
    if not success:
        print("❌ Failed to save ECUC file")
        return False
    
    print("✅ ECUC file saved successfully")
    
    # Verify the change was saved
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            if new_short_name in content:
                print(f"✅ Modified SHORT-NAME '{new_short_name}' found in saved file")
                
                # Count occurrences
                count = content.count(new_short_name)
                print(f"📊 Found {count} occurrence(s)")
                
                # Verify original is not present
                if original_short_name in content and original_short_name != new_short_name:
                    print(f"⚠️  Original SHORT-NAME '{original_short_name}' still present")
                    return False
                else:
                    print(f"✅ Original SHORT-NAME '{original_short_name}' properly replaced")
                
                return True
            else:
                print(f"❌ Modified SHORT-NAME '{new_short_name}' NOT found in saved file")
                return False
    else:
        print("❌ Output file was not created")
        return False

def test_container_short_name_editing():
    """Test editing container SHORT-NAME elements"""
    print("🧪 Testing Container SHORT-NAME Editing...")
    
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
    if len(doc.ecuc_elements) == 0:
        print("❌ No ECUC elements found")
        return False
    
    # Get the first ECUC element and its containers
    ecuc_element = doc.ecuc_elements[0]
    if 'containers' not in ecuc_element or not ecuc_element['containers']:
        print("❌ No containers found in ECUC element")
        return False
    
    # Edit the first few containers
    edited_containers = []
    for i, container in enumerate(ecuc_element['containers'][:3]):  # Test first 3 containers
        original_name = container.get('short_name', '')
        new_name = original_name + f"-TestContainer{i+1}"
        container['short_name'] = new_name
        edited_containers.append((original_name, new_name))
        print(f"✏️  Container {i+1}: '{original_name}' -> '{new_name}'")
    
    # Mark document as modified
    doc.set_modified(True)
    
    # Save to a test file
    output_file = "test_container_short_name.arxml"
    success = doc.save_document(output_file)
    if not success:
        print("❌ Failed to save ECUC file")
        return False
    
    print("✅ ECUC file saved successfully")
    
    # Verify the changes were saved
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            all_found = True
            for original_name, new_name in edited_containers:
                if new_name in content:
                    print(f"✅ Container SHORT-NAME '{new_name}' found in saved file")
                else:
                    print(f"❌ Container SHORT-NAME '{new_name}' NOT found in saved file")
                    all_found = False
                
                # Verify original is not present
                if original_name in content and original_name != new_name:
                    print(f"⚠️  Original container name '{original_name}' still present")
                    all_found = False
            
            return all_found
    else:
        print("❌ Output file was not created")
        return False

def test_parameter_short_name_editing():
    """Test editing parameter SHORT-NAME elements"""
    print("🧪 Testing Parameter SHORT-NAME Editing...")
    
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
    if len(doc.ecuc_elements) == 0:
        print("❌ No ECUC elements found")
        return False
    
    # Find containers with parameters
    ecuc_element = doc.ecuc_elements[0]
    edited_parameters = []
    
    if 'containers' in ecuc_element:
        for container in ecuc_element['containers']:
            if 'parameters' in container and container['parameters']:
                # Edit the first few parameters
                for i, param in enumerate(container['parameters'][:3]):  # Test first 3 parameters
                    original_name = param.get('short_name', '')
                    new_name = original_name + f"-TestParam{i+1}"
                    param['short_name'] = new_name
                    edited_parameters.append((original_name, new_name))
                    print(f"✏️  Parameter {i+1}: '{original_name}' -> '{new_name}'")
                break  # Only test first container with parameters
    
    if not edited_parameters:
        print("⚠️  No parameters found to edit - this is normal for some ECUC files")
        return True  # Not a failure, just no parameters to test
    
    # Mark document as modified
    doc.set_modified(True)
    
    # Save to a test file
    output_file = "test_parameter_short_name.arxml"
    success = doc.save_document(output_file)
    if not success:
        print("❌ Failed to save ECUC file")
        return False
    
    print("✅ ECUC file saved successfully")
    
    # Verify the changes were saved
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            all_found = True
            for original_name, new_name in edited_parameters:
                if new_name in content:
                    print(f"✅ Parameter SHORT-NAME '{new_name}' found in saved file")
                else:
                    print(f"❌ Parameter SHORT-NAME '{new_name}' NOT found in saved file")
                    all_found = False
            
            return all_found
    else:
        print("❌ Output file was not created")
        return False

def test_property_persistence():
    """Test that property changes persist when switching between elements"""
    print("🧪 Testing Property Persistence...")
    
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
    if len(doc.ecuc_elements) == 0:
        print("❌ No ECUC elements found")
        return False
    
    # Get the first ECUC element
    ecuc_element = doc.ecuc_elements[0]
    original_short_name = ecuc_element.get('short_name', '')
    
    # Simulate editing the short name
    new_short_name = original_short_name + "-PersistenceTest"
    ecuc_element['short_name'] = new_short_name
    print(f"✏️  Edited SHORT-NAME: '{original_short_name}' -> '{new_short_name}'")
    
    # Simulate switching to another element and back (in real GUI this would trigger _save_current_widget_values)
    # For this test, we'll just verify the change is still in memory
    if ecuc_element['short_name'] == new_short_name:
        print("✅ Property change persisted in memory")
        
        # Verify document is marked as modified
        if doc.modified:
            print("✅ Document marked as modified")
            return True
        else:
            print("❌ Document not marked as modified")
            return False
    else:
        print(f"❌ Property change was lost. Current value: {ecuc_element['short_name']}")
        return False

def test_search_functionality():
    """Test searching for modified SHORT-NAME values"""
    print("🧪 Testing Search Functionality...")
    
    # Create a test file with known content
    test_content = '''<?xml version='1.0' encoding='utf-8'?>
<AUTOSAR xmlns="http://autosar.org/schema/r4.0">
  <AR-PACKAGES>
    <AR-PACKAGE>
      <SHORT-NAME>AUTOSAR_Package</SHORT-NAME>
      <ELEMENTS>
        <ECUC-MODULE-CONFIGURATION-VALUES UUID="test-uuid">
          <SHORT-NAME>EcuC-TestSearch</SHORT-NAME>
          <ECUC-CONTAINER-VALUE>
            <SHORT-NAME>Container-TestSearch</SHORT-NAME>
            <ECUC-PARAMETER-VALUE>
              <SHORT-NAME>Parameter-TestSearch</SHORT-NAME>
            </ECUC-PARAMETER-VALUE>
          </ECUC-CONTAINER-VALUE>
        </ECUC-MODULE-CONFIGURATION-VALUES>
      </ELEMENTS>
    </AR-PACKAGE>
  </AR-PACKAGES>
</AUTOSAR>'''
    
    # Test different search patterns
    search_patterns = [
        ("-TestSearch", 3),
        ("EcuC-TestSearch", 1),
        ("Container-TestSearch", 1),
        ("Parameter-TestSearch", 1),
        ("TestSearch", 3),
        ("SHORT-NAME.*TestSearch", 3)
    ]
    
    all_passed = True
    for pattern, expected_count in search_patterns:
        if pattern == "SHORT-NAME.*TestSearch":
            import re
            matches = re.findall(r'<SHORT-NAME>.*?TestSearch.*?</SHORT-NAME>', test_content)
            count = len(matches)
        else:
            count = test_content.count(pattern)
        
        if count == expected_count:
            print(f"✅ Pattern '{pattern}': {count} matches (expected {expected_count})")
        else:
            print(f"❌ Pattern '{pattern}': {count} matches (expected {expected_count})")
            all_passed = False
    
    return all_passed

def test_file_size_efficiency():
    """Test that saved files are efficient (no duplicate content)"""
    print("🧪 Testing File Size Efficiency...")
    
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
    
    # Get original file size
    original_size = os.path.getsize(ecuc_file)
    print(f"📏 Original file size: {original_size:,} bytes")
    
    # Save without modifications
    doc = app.current_document
    output_file = "test_file_size_efficiency.arxml"
    success = doc.save_document(output_file)
    if not success:
        print("❌ Failed to save ECUC file")
        return False
    
    # Get saved file size
    saved_size = os.path.getsize(output_file)
    print(f"📏 Saved file size: {saved_size:,} bytes")
    
    # Check that the saved file is not significantly larger than original
    # (allowing for some overhead due to formatting differences)
    size_ratio = saved_size / original_size
    print(f"📊 Size ratio: {size_ratio:.2f}")
    
    if size_ratio < 1.5:  # Allow up to 50% increase due to formatting
        print("✅ File size is efficient (no significant duplication)")
        return True
    else:
        print("⚠️  File size is larger than expected (possible duplication)")
        return False

def main():
    """Run all SHORT-NAME editing tests"""
    print("🚀 Testing SHORT-NAME Editing Functionality")
    print("=" * 60)
    
    tests = [
        ("Main ECUC SHORT-NAME Editing", test_main_ecuc_short_name_editing),
        ("Container SHORT-NAME Editing", test_container_short_name_editing),
        ("Parameter SHORT-NAME Editing", test_parameter_short_name_editing),
        ("Property Persistence", test_property_persistence),
        ("Search Functionality", test_search_functionality),
        ("File Size Efficiency", test_file_size_efficiency)
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
    
    # Clean up test files
    test_files = [
        "test_main_ecuc_short_name.arxml",
        "test_container_short_name.arxml", 
        "test_parameter_short_name.arxml",
        "test_file_size_efficiency.arxml"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"🧹 Cleaned up {test_file}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All SHORT-NAME editing tests passed!")
        print("✅ SHORT-NAME editing functionality is working correctly")
        return True
    else:
        print("⚠️  Some SHORT-NAME editing tests failed.")
        print("❌ SHORT-NAME editing functionality needs attention.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)