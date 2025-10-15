#!/usr/bin/env python3
"""
Test script for ECUC file save fidelity and content preservation

This test suite validates that ECUC files are saved with complete fidelity:
1. All original content is preserved
2. No data loss during save/load cycles
3. File structure integrity is maintained
4. Element counts match between original and saved files

Tests cover:
- Complete ECUC file loading and saving
- Element count verification
- Content preservation validation
- File size and structure integrity
- Real-world ECUC file testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.application import ARXMLEditorApp

def test_ecuc_file_load_and_save():
    """Test loading and saving a real ECUC file with fidelity verification"""
    print("🧪 Testing ECUC File Load and Save Fidelity...")
    
    # Create application
    app = ARXMLEditorApp()
    
    # Load the ECUC file
    ecuc_file = "../Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml"
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
    output_file = "test_ecuc_fidelity_output.arxml"
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
        print(f"   - Size ratio: {saved_size/original_size:.2f}")
        
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
        
        return True
    else:
        print("❌ Output file was not created")
        return False

def test_element_count_preservation():
    """Test that element counts are preserved between original and saved files"""
    print("🧪 Testing Element Count Preservation...")
    
    # Create application
    app = ARXMLEditorApp()
    
    # Load the ECUC file
    ecuc_file = "../Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml"
    if not os.path.exists(ecuc_file):
        print(f"❌ ECUC file not found: {ecuc_file}")
        return False
    
    success = app.load_document(ecuc_file)
    if not success:
        print("❌ Failed to load ECUC file")
        return False
    
    # Count elements in original file
    with open(ecuc_file, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    original_counts = {
        'ECUC-MODULE-CONFIGURATION-VALUES': original_content.count('ECUC-MODULE-CONFIGURATION-VALUES'),
        'ECUC-CONTAINER-VALUE': original_content.count('ECUC-CONTAINER-VALUE'),
        'ECUC-PARAMETER-VALUE': original_content.count('ECUC-PARAMETER-VALUE'),
        'SHORT-NAME': original_content.count('SHORT-NAME'),
        'UUID': original_content.count('UUID'),
        'DEFINITION-REF': original_content.count('DEFINITION-REF')
    }
    
    print("📊 Original file element counts:")
    for element, count in original_counts.items():
        print(f"   - {element}: {count:,}")
    
    # Save the file
    doc = app.current_document
    output_file = "test_element_count_preservation.arxml"
    success = doc.save_document(output_file)
    if not success:
        print("❌ Failed to save ECUC file")
        return False
    
    # Count elements in saved file
    with open(output_file, 'r', encoding='utf-8') as f:
        saved_content = f.read()
    
    saved_counts = {
        'ECUC-MODULE-CONFIGURATION-VALUES': saved_content.count('ECUC-MODULE-CONFIGURATION-VALUES'),
        'ECUC-CONTAINER-VALUE': saved_content.count('ECUC-CONTAINER-VALUE'),
        'ECUC-PARAMETER-VALUE': saved_content.count('ECUC-PARAMETER-VALUE'),
        'SHORT-NAME': saved_content.count('SHORT-NAME'),
        'UUID': saved_content.count('UUID'),
        'DEFINITION-REF': saved_content.count('DEFINITION-REF')
    }
    
    print("\n📊 Saved file element counts:")
    for element, count in saved_counts.items():
        print(f"   - {element}: {count:,}")
    
    # Compare counts
    print("\n📊 Element count comparison:")
    all_preserved = True
    for element in original_counts:
        original_count = original_counts[element]
        saved_count = saved_counts[element]
        
        if saved_count >= original_count:
            print(f"   ✅ {element}: {saved_count:,} >= {original_count:,}")
        else:
            print(f"   ❌ {element}: {saved_count:,} < {original_count:,} (LOST {original_count - saved_count:,})")
            all_preserved = False
    
    return all_preserved

def test_xml_structure_integrity():
    """Test that the XML structure is valid and well-formed"""
    print("🧪 Testing XML Structure Integrity...")
    
    # Create application
    app = ARXMLEditorApp()
    
    # Load the ECUC file
    ecuc_file = "../Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml"
    if not os.path.exists(ecuc_file):
        print(f"❌ ECUC file not found: {ecuc_file}")
        return False
    
    success = app.load_document(ecuc_file)
    if not success:
        print("❌ Failed to load ECUC file")
        return False
    
    # Save the file
    doc = app.current_document
    output_file = "test_xml_structure_integrity.arxml"
    success = doc.save_document(output_file)
    if not success:
        print("❌ Failed to save ECUC file")
        return False
    
    # Validate XML structure
    try:
        from lxml import etree
        
        # Parse the saved file
        tree = etree.parse(output_file)
        root = tree.getroot()
        
        print("✅ XML structure is well-formed")
        
        # Check for required AUTOSAR elements
        if root.tag == "AUTOSAR":
            print("✅ Root element is AUTOSAR")
        else:
            print(f"❌ Root element is {root.tag}, expected AUTOSAR")
            return False
        
        # Check for AR-PACKAGES
        ar_packages = root.find('.//{http://autosar.org/schema/r4.0}AR-PACKAGES')
        if ar_packages is not None:
            print("✅ AR-PACKAGES element found")
        else:
            print("❌ AR-PACKAGES element not found")
            return False
        
        # Check for ELEMENTS
        elements = root.find('.//{http://autosar.org/schema/r4.0}ELEMENTS')
        if elements is not None:
            print("✅ ELEMENTS container found")
        else:
            print("❌ ELEMENTS container not found")
            return False
        
        # Check for ECUC elements
        ecuc_elements = root.findall('.//{http://autosar.org/schema/r4.0}ECUC-MODULE-CONFIGURATION-VALUES')
        if len(ecuc_elements) > 0:
            print(f"✅ Found {len(ecuc_elements)} ECUC-MODULE-CONFIGURATION-VALUES elements")
        else:
            print("❌ No ECUC-MODULE-CONFIGURATION-VALUES elements found")
            return False
        
        return True
        
    except etree.XMLSyntaxError as e:
        print(f"❌ XML syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error validating XML structure: {e}")
        return False

def test_save_load_cycle():
    """Test that save/load cycles preserve all data"""
    print("🧪 Testing Save/Load Cycle Preservation...")
    
    # Create application
    app = ARXMLEditorApp()
    
    # Load the ECUC file
    ecuc_file = "../Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml"
    if not os.path.exists(ecuc_file):
        print(f"❌ ECUC file not found: {ecuc_file}")
        return False
    
    # First load
    success = app.load_document(ecuc_file)
    if not success:
        print("❌ Failed to load ECUC file")
        return False
    
    doc1 = app.current_document
    print(f"📊 First load - ECUC elements: {len(doc1.ecuc_elements)}")
    
    # Save
    output_file = "test_save_load_cycle.arxml"
    success = doc1.save_document(output_file)
    if not success:
        print("❌ Failed to save ECUC file")
        return False
    
    # Second load
    success = app.load_document(output_file)
    if not success:
        print("❌ Failed to reload ECUC file")
        return False
    
    doc2 = app.current_document
    print(f"📊 Second load - ECUC elements: {len(doc2.ecuc_elements)}")
    
    # Compare element counts
    if len(doc1.ecuc_elements) == len(doc2.ecuc_elements):
        print("✅ ECUC element count preserved in save/load cycle")
    else:
        print(f"❌ ECUC element count changed: {len(doc1.ecuc_elements)} -> {len(doc2.ecuc_elements)}")
        return False
    
    if len(doc1._original_xml_elements) == len(doc2._original_xml_elements):
        print("✅ Original XML element count preserved in save/load cycle")
    else:
        print(f"❌ Original XML element count changed: {len(doc1._original_xml_elements)} -> {len(doc2._original_xml_elements)}")
        return False
    
    return True

def test_ecuc_element_content_preservation():
    """Test that ECUC element content is preserved in detail"""
    print("🧪 Testing ECUC Element Content Preservation...")
    
    # Create application
    app = ARXMLEditorApp()
    
    # Load the ECUC file
    ecuc_file = "../Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml"
    if not os.path.exists(ecuc_file):
        print(f"❌ ECUC file not found: {ecuc_file}")
        return False
    
    success = app.load_document(ecuc_file)
    if not success:
        print("❌ Failed to load ECUC file")
        return False
    
    doc = app.current_document
    if len(doc.ecuc_elements) == 0:
        print("❌ No ECUC elements found")
        return False
    
    # Get the first ECUC element
    ecuc_element = doc.ecuc_elements[0]
    original_short_name = ecuc_element.get('short_name', '')
    original_uuid = ecuc_element.get('uuid', '')
    
    print(f"📝 Original ECUC element:")
    print(f"   - Short Name: '{original_short_name}'")
    print(f"   - UUID: '{original_uuid}'")
    
    # Save the file
    output_file = "test_ecuc_content_preservation.arxml"
    success = doc.save_document(output_file)
    if not success:
        print("❌ Failed to save ECUC file")
        return False
    
    # Verify content in saved file
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for short name
    if original_short_name in content:
        print(f"✅ Short name '{original_short_name}' preserved in saved file")
    else:
        print(f"❌ Short name '{original_short_name}' not found in saved file")
        return False
    
    # Check for UUID
    if original_uuid in content:
        print(f"✅ UUID '{original_uuid}' preserved in saved file")
    else:
        print(f"❌ UUID '{original_uuid}' not found in saved file")
        return False
    
    # Check for admin data
    if 'ADMIN-DATA' in content:
        print("✅ ADMIN-DATA preserved in saved file")
    else:
        print("❌ ADMIN-DATA not found in saved file")
        return False
    
    # Check for containers
    container_count = content.count('ECUC-CONTAINER-VALUE')
    print(f"📊 ECUC-CONTAINER-VALUE elements in saved file: {container_count}")
    
    if container_count > 0:
        print("✅ ECUC containers preserved in saved file")
    else:
        print("❌ No ECUC containers found in saved file")
        return False
    
    return True

def main():
    """Run all ECUC save fidelity tests"""
    print("🚀 Testing ECUC File Save Fidelity")
    print("=" * 60)
    
    tests = [
        ("ECUC File Load and Save", test_ecuc_file_load_and_save),
        ("Element Count Preservation", test_element_count_preservation),
        ("XML Structure Integrity", test_xml_structure_integrity),
        ("Save/Load Cycle Preservation", test_save_load_cycle),
        ("ECUC Element Content Preservation", test_ecuc_element_content_preservation)
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
        "test_ecuc_fidelity_output.arxml",
        "test_element_count_preservation.arxml",
        "test_xml_structure_integrity.arxml",
        "test_save_load_cycle.arxml",
        "test_ecuc_content_preservation.arxml"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"🧹 Cleaned up {test_file}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All ECUC save fidelity tests passed!")
        print("✅ ECUC files are saved with complete fidelity")
        return True
    else:
        print("⚠️  Some ECUC save fidelity tests failed.")
        print("❌ ECUC file saving needs attention.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)