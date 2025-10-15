#!/usr/bin/env python3
"""
Test script to reproduce the SHORT-NAME editing issue
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.application import ARXMLEditorApp

def test_short_name_editing():
    """Test SHORT-NAME editing and saving"""
    print("🧪 Testing SHORT-NAME Editing Issue...")
    
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
    
    # Get the first ECUC element
    ecuc_element = doc.ecuc_elements[0]
    original_short_name = ecuc_element.get('short_name', '')
    print(f"📝 Original short name: '{original_short_name}'")
    
    # Simulate editing the short name (like in GUI)
    new_short_name = original_short_name + "-Haytham"
    ecuc_element['short_name'] = new_short_name
    print(f"✏️  Modified short name: '{new_short_name}'")
    
    # Mark document as modified
    doc.set_modified(True)
    print(f"📝 Document modified: {doc.modified}")
    
    # Save to a new file
    output_file = "test_short_name_output.arxml"
    print(f"💾 Saving to: {output_file}")
    
    success = doc.save_document(output_file)
    if not success:
        print("❌ Failed to save ECUC file")
        return False
    
    print("✅ ECUC file saved successfully")
    
    # Check if the change was saved
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            if new_short_name in content:
                print(f"✅ Modified short name '{new_short_name}' found in saved file")
                return True
            else:
                print(f"❌ Modified short name '{new_short_name}' NOT found in saved file")
                print(f"   Original short name '{original_short_name}' found: {original_short_name in content}")
                
                # Show some context around the short name
                if original_short_name in content:
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if original_short_name in line:
                            print(f"   Line {i+1}: {line.strip()}")
                            if i > 0:
                                print(f"   Line {i}: {lines[i-1].strip()}")
                            if i < len(lines) - 1:
                                print(f"   Line {i+2}: {lines[i+1].strip()}")
                            break
                
                return False
    else:
        print("❌ Output file was not created")
        return False

def main():
    """Run the test"""
    print("🚀 Testing SHORT-NAME Editing Issue")
    print("=" * 50)
    
    success = test_short_name_editing()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 SHORT-NAME editing test passed!")
    else:
        print("❌ SHORT-NAME editing test failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)