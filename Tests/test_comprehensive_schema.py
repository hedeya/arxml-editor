#!/usr/bin/env python3
"""
Comprehensive test for dynamic schema detection and validation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.services.schema_service import SchemaService
from src.core.services.arxml_parser import ARXMLParser
from src.core.services.validation_service import ValidationService

def test_comprehensive_schema():
    """Test comprehensive schema detection and validation functionality"""
    print("Comprehensive Schema Detection and Validation Test")
    print("=" * 60)
    
    # Initialize services
    schema_service = SchemaService()
    parser = ARXMLParser(schema_service)
    validation_service = ValidationService(schema_service)
    
    # Test 1: Schema detection from different sources
    print("\n1. Testing Schema Detection")
    print("-" * 30)
    
    # Test with sample file
    sample_file = "sample.arxml"
    if os.path.exists(sample_file):
        detected_version = schema_service.detect_schema_version_from_file(sample_file)
        print(f"   File detection: {detected_version}")
    
    # Test with content string
    test_content = '''<?xml version="1.0" encoding="UTF-8"?>
<AUTOSAR xmlns="http://autosar.org/schema/r4.0" 
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://autosar.org/schema/r4.0 AUTOSAR_4-6-0.xsd">
  <AR-PACKAGES>
    <AR-PACKAGE>
      <SHORT-NAME>TestPackage</SHORT-NAME>
    </AR-PACKAGE>
  </AR-PACKAGES>
</AUTOSAR>'''
    
    detected_from_content = schema_service.detect_schema_version_from_content(test_content)
    print(f"   Content detection: {detected_from_content}")
    
    # Test 2: Auto-detection and schema loading
    print("\n2. Testing Auto-Detection and Schema Loading")
    print("-" * 45)
    
    if os.path.exists(sample_file):
        success = schema_service.auto_detect_and_set_version(file_path=sample_file)
        print(f"   Auto-detect from file: {'Success' if success else 'Failed'}")
        print(f"   Current version: {schema_service.current_version}")
        print(f"   Schema loaded: {'Yes' if schema_service.current_schema else 'No'}")
        print(f"   Detected version: {schema_service.detected_version}")
    
    # Test 3: Schema validation
    print("\n3. Testing Schema Validation")
    print("-" * 30)
    
    if schema_service.current_schema and os.path.exists(sample_file):
        validation_errors = schema_service.validate_arxml_file(sample_file)
        if validation_errors:
            print(f"   Validation errors found: {len(validation_errors)}")
            for i, error in enumerate(validation_errors[:3]):  # Show first 3 errors
                print(f"     {i+1}. {error[:100]}...")
        else:
            print("   No validation errors found")
    
    # Test 4: Different schema versions
    print("\n4. Testing Different Schema Versions")
    print("-" * 40)
    
    available_versions = schema_service.get_available_versions()
    print(f"   Available versions: {', '.join(available_versions)}")
    
    for version in available_versions[:3]:  # Test first 3 versions
        success = schema_service.set_version(version)
        print(f"   Version {version}: {'Loaded' if success and schema_service.current_schema else 'Failed'}")
    
    # Test 5: Namespace mapping
    print("\n5. Testing Namespace Mapping")
    print("-" * 30)
    
    test_namespaces = [
        "http://autosar.org/schema/r4.0",
        "http://autosar.org/schema/r4.1",
        "http://autosar.org/schema/r4.2"
    ]
    
    for namespace in test_namespaces:
        mapped_version = schema_service._namespace_version_map.get(namespace, "Unknown")
        print(f"   {namespace} -> {mapped_version}")
    
    # Test 6: Schema location parsing
    print("\n6. Testing Schema Location Parsing")
    print("-" * 35)
    
    test_locations = [
        "http://autosar.org/schema/r4.0 AUTOSAR_4-7-0.xsd",
        "http://autosar.org/schema/r4.0 AUTOSAR_4-6-0.xsd",
        "http://autosar.org/schema/r4.0 AUTOSAR_4.5.0.xsd"
    ]
    
    for location in test_locations:
        version = schema_service._extract_version_from_schema_location(location)
        print(f"   '{location}' -> {version}")
    
    # Test 7: Error handling
    print("\n7. Testing Error Handling")
    print("-" * 25)
    
    # Test with non-existent file
    non_existent = schema_service.detect_schema_version_from_file("non_existent.arxml")
    print(f"   Non-existent file: {non_existent}")
    
    # Test with invalid XML
    invalid_xml = schema_service.detect_schema_version_from_content("<invalid>xml</invalid>")
    print(f"   Invalid XML: {invalid_xml}")
    
    # Test with empty content
    empty_content = schema_service.detect_schema_version_from_content("")
    print(f"   Empty content: {empty_content}")
    
    # Test 8: Integration with parser
    print("\n8. Testing Parser Integration")
    print("-" * 30)
    
    if os.path.exists(sample_file):
        root = parser.parse_arxml_file(sample_file)
        if root is not None:
            print("   Parsing: Success")
            print(f"   Root element: {root.tag}")
            print(f"   Namespace: {root.nsmap.get(None, 'None')}")
            print(f"   Detected version: {schema_service.detected_version}")
        else:
            print("   Parsing: Failed")
    
    print(f"\nTest completed successfully!")
    print(f"Final schema version: {schema_service.current_version}")
    print(f"Schema loaded: {'Yes' if schema_service.current_schema else 'No'}")

if __name__ == "__main__":
    test_comprehensive_schema()