#!/usr/bin/env python3
"""
Test script to simulate the exact user scenario:
1. Open ECUC file
2. Edit a SHORT-NAME element
3. Save the file
4. Search for the change
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.application import ARXMLEditorApp

def test_user_scenario():
    """Test the exact user scenario"""
    print("🧪 Testing User Scenario: Edit SHORT-NAME, Save, Search")
    print("=" * 60)
    
    # Step 1: Load ECUC file
    print("📁 Step 1: Loading ECUC file...")
    app = ARXMLEditorApp()
    ecuc_file = "Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml"
    
    if not os.path.exists(ecuc_file):
        print(f"❌ ECUC file not found: {ecuc_file}")
        return False
    
    success = app.load_document(ecuc_file)
    if not success:
        print("❌ Failed to load ECUC file")
        return False
    
    print("✅ ECUC file loaded successfully")
    
    # Step 2: Edit a SHORT-NAME element
    print("\n✏️  Step 2: Editing SHORT-NAME element...")
    doc = app.current_document
    
    if len(doc.ecuc_elements) == 0:
        print("❌ No ECUC elements found")
        return False
    
    # Get the first ECUC element
    ecuc_element = doc.ecuc_elements[0]
    original_short_name = ecuc_element.get('short_name', '')
    print(f"   Original SHORT-NAME: '{original_short_name}'")
    
    # Add "-Haytham" to the short name
    new_short_name = original_short_name + "-Haytham"
    ecuc_element['short_name'] = new_short_name
    print(f"   Modified SHORT-NAME: '{new_short_name}'")
    
    # Mark document as modified
    doc.set_modified(True)
    print(f"   Document marked as modified: {doc.modified}")
    
    # Step 3: Save the file
    print("\n💾 Step 3: Saving the file...")
    output_file = "user_scenario_test.arxml"
    success = doc.save_document(output_file)
    
    if not success:
        print("❌ Failed to save file")
        return False
    
    print(f"✅ File saved successfully to: {output_file}")
    
    # Step 4: Search for the change
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
    """Test different search patterns"""
    print("\n🔍 Testing Different Search Patterns...")
    
    output_file = "user_scenario_test.arxml"
    if not os.path.exists(output_file):
        print("❌ Output file not found")
        return False
    
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    search_patterns = [
        "-Haytham",
        "EcuC-Haytham", 
        "Haytham",
        "SHORT-NAME.*Haytham",
        "<SHORT-NAME>.*Haytham.*</SHORT-NAME>"
    ]
    
    for pattern in search_patterns:
        if pattern.startswith("<SHORT-NAME>") and pattern.endswith("</SHORT-NAME>"):
            import re
            matches = re.findall(pattern, content)
            count = len(matches)
        else:
            count = content.count(pattern)
        
        status = "✅" if count > 0 else "❌"
        print(f"   {status} Pattern '{pattern}': {count} matches")

def main():
    """Run the user scenario test"""
    print("🚀 Testing User Scenario: SHORT-NAME Editing")
    print("=" * 60)
    
    success = test_user_scenario()
    test_search_variations()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 User scenario test PASSED!")
        print("✅ SHORT-NAME editing, saving, and searching works correctly")
    else:
        print("❌ User scenario test FAILED!")
        print("⚠️  There may be an issue with SHORT-NAME editing or saving")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)