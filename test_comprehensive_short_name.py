#!/usr/bin/env python3
"""
Comprehensive test for SHORT-NAME editing in ECUC files
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.application import ARXMLEditorApp

def test_comprehensive_short_name_editing():
    """Test comprehensive SHORT-NAME editing scenarios"""
    print("🧪 Testing Comprehensive SHORT-NAME Editing...")
    
    # Create application
    app = ARXMLEditorApp()
    
    # Load an ECUC file
    ecuc_file = "Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml"
    if not os.path.exists(ecuc_file):
        print(f"❌ ECUC file not found: {ecuc_file}")
        return False
    
    print(f"📁 Loading ECUC file: {ecuc_file}")
    success = app.load_document(ecuc_file)
    
    if not success:
        print("❌ Failed to load ECUC file")
        return False
    
    print("✅ ECUC file loaded successfully")
    
    # Check what was loaded
    doc = app.current_document
    print(f"📊 Loaded elements:")
    print(f"   - ECUC Elements: {len(doc.ecuc_elements)}")
    print(f"   - Original XML Elements: {len(doc._original_xml_elements)}")
    
    if len(doc.ecuc_elements) == 0:
        print("❌ No ECUC elements were loaded")
        return False
    
    # Test 1: Edit the main ECUC element short name
    print("\n🔧 Test 1: Editing main ECUC element short name")
    ecuc_element = doc.ecuc_elements[0]
    original_short_name = ecuc_element.get('short_name', '')
    print(f"   Original: '{original_short_name}'")
    
    new_short_name = original_short_name + "-Haytham"
    ecuc_element['short_name'] = new_short_name
    print(f"   Modified: '{new_short_name}'")
    
    # Test 2: Edit a container short name if available
    print("\n🔧 Test 2: Editing container short names")
    if 'containers' in ecuc_element and ecuc_element['containers']:
        for i, container in enumerate(ecuc_element['containers'][:3]):  # Test first 3 containers
            original_container_name = container.get('short_name', '')
            new_container_name = original_container_name + "-Haytham"
            container['short_name'] = new_container_name
            print(f"   Container {i+1}: '{original_container_name}' -> '{new_container_name}'")
    else:
        print("   No containers found to edit")
    
    # Test 3: Edit parameter short names if available
    print("\n🔧 Test 3: Editing parameter short names")
    if 'containers' in ecuc_element and ecuc_element['containers']:
        for container in ecuc_element['containers']:
            if 'parameters' in container and container['parameters']:
                for i, param in enumerate(container['parameters'][:3]):  # Test first 3 parameters
                    original_param_name = param.get('short_name', '')
                    new_param_name = original_param_name + "-Haytham"
                    param['short_name'] = new_param_name
                    print(f"   Parameter {i+1}: '{original_param_name}' -> '{new_param_name}'")
                break  # Only test first container with parameters
    else:
        print("   No parameters found to edit")
    
    # Mark document as modified
    doc.set_modified(True)
    print(f"\n📝 Document modified: {doc.modified}")
    
    # Save to a new file
    output_file = "test_comprehensive_short_name_output.arxml"
    print(f"\n💾 Saving to: {output_file}")
    
    success = doc.save_document(output_file)
    if not success:
        print("❌ Failed to save ECUC file")
        return False
    
    print("✅ ECUC file saved successfully")
    
    # Verify all changes were saved
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            print(f"\n🔍 Verifying saved changes:")
            
            # Check main ECUC element
            if new_short_name in content:
                print(f"   ✅ Main ECUC short name '{new_short_name}' found")
            else:
                print(f"   ❌ Main ECUC short name '{new_short_name}' NOT found")
                return False
            
            # Check for any "-Haytham" occurrences
            haytham_count = content.count("-Haytham")
            print(f"   📊 Found {haytham_count} occurrences of '-Haytham'")
            
            if haytham_count > 0:
                print("   ✅ Changes were saved successfully")
                
                # Show some examples
                lines = content.split('\n')
                haytham_lines = [i+1 for i, line in enumerate(lines) if "-Haytham" in line]
                print(f"   📍 Found on lines: {haytham_lines[:10]}{'...' if len(haytham_lines) > 10 else ''}")
                
                return True
            else:
                print("   ❌ No '-Haytham' occurrences found in saved file")
                return False
    else:
        print("❌ Output file was not created")
        return False

def test_search_functionality():
    """Test searching for modified content"""
    print("\n🔍 Testing Search Functionality...")
    
    output_file = "test_comprehensive_short_name_output.arxml"
    if not os.path.exists(output_file):
        print("❌ Output file not found")
        return False
    
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test different search patterns
    search_patterns = [
        "-Haytham",
        "EcuC-Haytham",
        "Haytham",
        "SHORT-NAME.*Haytham"
    ]
    
    for pattern in search_patterns:
        if pattern == "SHORT-NAME.*Haytham":
            import re
            matches = re.findall(r'<SHORT-NAME>.*?Haytham.*?</SHORT-NAME>', content)
            count = len(matches)
        else:
            count = content.count(pattern)
        
        print(f"   Pattern '{pattern}': {count} matches")
        
        if count > 0:
            print(f"   ✅ Found {count} matches for '{pattern}'")
        else:
            print(f"   ❌ No matches for '{pattern}'")
    
    return True

def main():
    """Run the comprehensive test"""
    print("🚀 Testing Comprehensive SHORT-NAME Editing")
    print("=" * 60)
    
    success1 = test_comprehensive_short_name_editing()
    success2 = test_search_functionality()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 Comprehensive SHORT-NAME editing test passed!")
        print("✅ All changes were saved and can be found in the file")
    else:
        print("❌ Comprehensive SHORT-NAME editing test failed!")
        print("⚠️  Some changes may not have been saved correctly")
    
    return success1 and success2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)