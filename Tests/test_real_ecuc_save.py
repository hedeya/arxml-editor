#!/usr/bin/env python3
"""
Test script to load a real ECUC file and save it to verify all elements are preserved
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.application import ARXMLEditorApp
from src.core.services.arxml_parser import ARXMLParser

def test_real_ecuc_save():
    """Test loading and saving a real ECUC file"""
    print("🧪 Testing Real ECUC File Load and Save...")
    
    # Create application
    app = ARXMLEditorApp()
    
    # Load the ECUC file
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
    print(f"   - Software Component Types: {len(doc.sw_component_types)}")
    print(f"   - Port Interfaces: {len(doc.port_interfaces)}")
    print(f"   - Compositions: {len(doc.compositions)}")
    print(f"   - ECUC Elements: {len(doc.ecuc_elements)}")
    print(f"   - Original XML Elements: {len(doc._original_xml_elements)}")
    
    if len(doc.ecuc_elements) == 0 and len(doc._original_xml_elements) == 0:
        print("❌ No ECUC elements were loaded")
        return False
    
    # Save to a new file
    output_file = "test_real_ecuc_output.arxml"
    print(f"💾 Saving to: {output_file}")
    
    success = doc.save_document(output_file)
    if not success:
        print("❌ Failed to save ECUC file")
        return False
    
    print("✅ ECUC file saved successfully")
    
    # Check the saved file size and content
    if os.path.exists(output_file):
        original_size = os.path.getsize(ecuc_file)
        saved_size = os.path.getsize(output_file)
        
        print(f"📏 File sizes:")
        print(f"   - Original: {original_size:,} bytes")
        print(f"   - Saved: {saved_size:,} bytes")
        
        # Check if the saved file contains ECUC elements
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            if "ECUC-MODULE-CONFIGURATION-VALUES" in content:
                print("✅ ECUC elements found in saved file")
            else:
                print("❌ ECUC elements missing from saved file")
                return False
            
            if "EcuC" in content:
                print("✅ ECUC configuration found in saved file")
            else:
                print("❌ ECUC configuration missing from saved file")
                return False
            
            # Count ECUC elements in saved file
            ecuc_count = content.count("ECUC-MODULE-CONFIGURATION-VALUES")
            print(f"📊 ECUC elements in saved file: {ecuc_count}")
            
            if ecuc_count > 0:
                print("✅ ECUC elements preserved in save")
            else:
                print("❌ No ECUC elements in saved file")
                return False
            
            # Count total ECUC-related elements
            total_ecuc_elements = content.count("ECUC-")
            print(f"📊 Total ECUC elements in saved file: {total_ecuc_elements}")
            
            # Check if we preserved most of the original content
            if total_ecuc_elements > 1000:  # Should have thousands of ECUC elements
                print("✅ Significant number of ECUC elements preserved")
            else:
                print(f"⚠️  Only {total_ecuc_elements} ECUC elements found (expected thousands)")
    
    # Clean up
    if os.path.exists(output_file):
        os.remove(output_file)
        print("🧹 Test file cleaned up")
    
    print("✅ Real ECUC save test passed")
    return True

def test_ecuc_element_preservation():
    """Test that specific ECUC elements are preserved"""
    print("🧪 Testing ECUC Element Preservation...")
    
    # Create application
    app = ARXMLEditorApp()
    
    # Load the ECUC file
    ecuc_file = "Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml"
    if not os.path.exists(ecuc_file):
        print(f"❌ ECUC file not found: {ecuc_file}")
        return False
    
    success = app.load_document(ecuc_file)
    if not success:
        print("❌ Failed to load ECUC file")
        return False
    
    doc = app.current_document
    
    # Check that we have original XML elements
    if len(doc._original_xml_elements) == 0:
        print("❌ No original XML elements loaded")
        return False
    
    print(f"✅ Loaded {len(doc._original_xml_elements)} original XML elements")
    
    # Check that we have ECUC elements
    if len(doc.ecuc_elements) == 0:
        print("❌ No ECUC elements loaded")
        return False
    
    print(f"✅ Loaded {len(doc.ecuc_elements)} ECUC elements")
    
    # Test save and verify content
    output_file = "test_ecuc_preservation.arxml"
    success = doc.save_document(output_file)
    if not success:
        print("❌ Failed to save ECUC file")
        return False
    
    # Verify the saved file has the expected content
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Check for specific ECUC elements that should be present
        required_elements = [
            "ECUC-MODULE-CONFIGURATION-VALUES",
            "ECUC-CONTAINER-VALUE",
            "ECUC-NUMERICAL-PARAM-VALUE",
            "ECUC-TEXTUAL-PARAM-VALUE",
            "ECUC-REFERENCE-VALUE"
        ]
        
        for element in required_elements:
            if element in content:
                count = content.count(element)
                print(f"✅ Found {count} {element} elements")
            else:
                print(f"❌ Missing {element} elements")
                return False
    
    # Clean up
    if os.path.exists(output_file):
        os.remove(output_file)
    
    print("✅ ECUC element preservation test passed")
    return True

def main():
    """Run all tests"""
    print("🚀 Testing Real ECUC File Load and Save")
    print("=" * 60)
    
    tests = [
        test_real_ecuc_save,
        test_ecuc_element_preservation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All ECUC save tests passed!")
        return True
    else:
        print("⚠️  Some ECUC save tests failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)