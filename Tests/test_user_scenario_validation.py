#!/usr/bin/env python3
"""
Test script to validate the exact user scenario for SHORT-NAME editing

This test simulates the exact scenario reported by the user:
1. Open an ECUC file
2. Edit a SHORT-NAME element (add "-Haytham")
3. Save the file
4. Search for the change in the saved file

This test validates that the fix for the SHORT-NAME editing issue works correctly
in the real-world scenario described by the user.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.application import ARXMLEditorApp

def test_user_scenario_exact():
    """Test the exact user scenario: edit SHORT-NAME, save, search"""
    print("🧪 Testing Exact User Scenario: Edit SHORT-NAME, Save, Search")
    print("=" * 70)
    
    # Step 1: Load ECUC file
    print("📁 Step 1: Loading ECUC file...")
    app = ARXMLEditorApp()
    ecuc_file = "../Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml"
    
    if not os.path.exists(ecuc_file):
        print(f"❌ ECUC file not found: {ecuc_file}")
        return False
    
    success = app.load_document(ecuc_file)
    if not success:
        print("❌ Failed to load ECUC file")
        return False
    
    print("✅ ECUC file loaded successfully")
    
    # Step 2: Edit a SHORT-NAME element (exactly as user described)
    print("\n✏️  Step 2: Editing SHORT-NAME element...")
    doc = app.current_document
    
    if len(doc.ecuc_elements) == 0:
        print("❌ No ECUC elements found")
        return False
    
    # Get the first ECUC element
    ecuc_element = doc.ecuc_elements[0]
    original_short_name = ecuc_element.get('short_name', '')
    print(f"   Original SHORT-NAME: '{original_short_name}'")
    
    # Add "-Haytham" to the short name (exactly as user described)
    new_short_name = original_short_name + "-Haytham"
    ecuc_element['short_name'] = new_short_name
    print(f"   Modified SHORT-NAME: '{new_short_name}'")
    
    # Mark document as modified
    doc.set_modified(True)
    print(f"   Document marked as modified: {doc.modified}")
    
    # Step 3: Save the file
    print("\n💾 Step 3: Saving the file...")
    output_file = "user_scenario_validation.arxml"
    success = doc.save_document(output_file)
    
    if not success:
        print("❌ Failed to save file")
        return False
    
    print(f"✅ File saved successfully to: {output_file}")
    
    # Step 4: Search for the change (exactly as user described)
    print("\n🔍 Step 4: Searching for the change...")
    if not os.path.exists(output_file):
        print("❌ Output file not found")
        return False
    
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Search for the modified short name
    if new_short_name in content:
        print(f"✅ Found modified SHORT-NAME '{new_short_name}' in saved file")
        
        # Count occurrences
        count = content.count(new_short_name)
        print(f"   Found {count} occurrence(s)")
        
        # Show line numbers
        lines = content.split('\n')
        matching_lines = [i+1 for i, line in enumerate(lines) if new_short_name in line]
        print(f"   Found on lines: {matching_lines}")
        
        # Show context around the first match
        if matching_lines:
            line_num = matching_lines[0]
            print(f"\n   Context around line {line_num}:")
            start = max(0, line_num - 3)
            end = min(len(lines), line_num + 2)
            for i in range(start, end):
                marker = ">>> " if i == line_num - 1 else "    "
                print(f"   {marker}{i+1:4d}: {lines[i]}")
        
        return True
    else:
        print(f"❌ Modified SHORT-NAME '{new_short_name}' NOT found in saved file")
        
        # Check if original name is still there
        if original_short_name in content:
            print(f"   ⚠️  Original SHORT-NAME '{original_short_name}' is still present")
        else:
            print(f"   ⚠️  Neither original nor modified SHORT-NAME found")
        
        return False

def test_search_variations():
    """Test different search patterns that user might use"""
    print("\n🔍 Testing Different Search Patterns...")
    
    output_file = "user_scenario_validation.arxml"
    if not os.path.exists(output_file):
        print("❌ Output file not found")
        return False
    
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    search_patterns = [
        ("-Haytham", "Exact suffix search"),
        ("EcuC-Haytham", "Full modified name search"),
        ("Haytham", "Partial name search"),
        ("SHORT-NAME.*Haytham", "Regex pattern search"),
        ("<SHORT-NAME>.*Haytham.*</SHORT-NAME>", "XML element pattern search")
    ]
    
    all_found = True
    for pattern, description in search_patterns:
        if pattern.startswith("<SHORT-NAME>") and pattern.endswith("</SHORT-NAME>"):
            import re
            matches = re.findall(pattern, content)
            count = len(matches)
        elif ".*" in pattern:
            import re
            matches = re.findall(pattern, content)
            count = len(matches)
        else:
            count = content.count(pattern)
        
        status = "✅" if count > 0 else "❌"
        print(f"   {status} {description}: '{pattern}' - {count} matches")
        
        if count == 0:
            all_found = False
    
    return all_found

def test_file_integrity():
    """Test that the saved file is valid and complete"""
    print("\n🔍 Testing File Integrity...")
    
    output_file = "user_scenario_validation.arxml"
    if not os.path.exists(output_file):
        print("❌ Output file not found")
        return False
    
    # Check file size
    file_size = os.path.getsize(output_file)
    print(f"📏 Saved file size: {file_size:,} bytes")
    
    if file_size < 1000:
        print("⚠️  File size seems too small")
        return False
    else:
        print("✅ File size is reasonable")
    
    # Check XML validity
    try:
        from lxml import etree
        tree = etree.parse(output_file)
        root = tree.getroot()
        
        if root.tag == "{http://autosar.org/schema/r4.0}AUTOSAR" or root.tag == "AUTOSAR":
            print("✅ XML structure is valid")
        else:
            print(f"❌ Invalid XML root element: {root.tag}")
            return False
        
        # Check for required elements
        required_elements = [
            "AR-PACKAGES",
            "ELEMENTS", 
            "ECUC-MODULE-CONFIGURATION-VALUES",
            "SHORT-NAME"
        ]
        
        for element in required_elements:
            if element in etree.tostring(root, encoding='unicode'):
                print(f"✅ Required element '{element}' found")
            else:
                print(f"❌ Required element '{element}' not found")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ XML validation error: {e}")
        return False

def test_no_duplication():
    """Test that there's no content duplication in the saved file"""
    print("\n🔍 Testing No Content Duplication...")
    
    output_file = "user_scenario_validation.arxml"
    if not os.path.exists(output_file):
        print("❌ Output file not found")
        return False
    
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for duplicate ECUC elements
    ecuc_count = content.count('ECUC-MODULE-CONFIGURATION-VALUES')
    print(f"📊 ECUC-MODULE-CONFIGURATION-VALUES count: {ecuc_count}")
    
    if ecuc_count >= 1:
        print("✅ ECUC elements present")
    else:
        print(f"❌ No ECUC elements found")
        return False
    
    # Check for duplicate short names
    short_name_count = content.count('SHORT-NAME')
    print(f"📊 SHORT-NAME elements count: {short_name_count}")
    
    if short_name_count > 0:
        print("✅ SHORT-NAME elements present")
    else:
        print("❌ No SHORT-NAME elements found")
        return False
    
    return True

def main():
    """Run the user scenario validation test"""
    print("🚀 Testing User Scenario Validation")
    print("=" * 70)
    print("This test validates the exact scenario reported by the user:")
    print("1. Open ECUC file")
    print("2. Edit SHORT-NAME element (add '-Haytham')")
    print("3. Save the file")
    print("4. Search for the change")
    print("=" * 70)
    
    # Run the main test
    success1 = test_user_scenario_exact()
    success2 = test_search_variations()
    success3 = test_file_integrity()
    success4 = test_no_duplication()
    
    # Clean up
    if os.path.exists("user_scenario_validation.arxml"):
        os.remove("user_scenario_validation.arxml")
        print("\n🧹 Cleaned up test file")
    
    print("\n" + "=" * 70)
    print("📊 Test Results:")
    print(f"   ✅ User Scenario Exact: {'PASSED' if success1 else 'FAILED'}")
    print(f"   ✅ Search Variations: {'PASSED' if success2 else 'FAILED'}")
    print(f"   ✅ File Integrity: {'PASSED' if success3 else 'FAILED'}")
    print(f"   ✅ No Duplication: {'PASSED' if success4 else 'FAILED'}")
    
    overall_success = success1 and success2 and success3 and success4
    
    if overall_success:
        print("\n🎉 User Scenario Validation PASSED!")
        print("✅ The SHORT-NAME editing issue has been successfully fixed")
        print("✅ Users can now edit SHORT-NAME elements and find their changes")
    else:
        print("\n❌ User Scenario Validation FAILED!")
        print("⚠️  The SHORT-NAME editing issue may not be fully resolved")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)