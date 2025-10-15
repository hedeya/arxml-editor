#!/usr/bin/env python3
"""
Test script for dynamic schema version detection and validation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.services.schema_service import SchemaService
from src.core.services.arxml_parser import ARXMLParser
from src.core.services.validation_service import ValidationService

def test_schema_detection():
    """Test schema detection functionality"""
    print("Testing Dynamic Schema Detection and Validation")
    print("=" * 50)
    
    # Initialize services
    schema_service = SchemaService()
    parser = ARXMLParser(schema_service)
    validation_service = ValidationService(schema_service)
    
    # Test with sample ARXML file
    sample_file = "sample.arxml"
    
    print(f"Current working directory: {os.getcwd()}")
    print(f"Schema files directory: {os.path.abspath('schemas')}")
    print(f"XSD file exists: {os.path.exists('schemas/autosar_4-7-0.xsd')}")
    
    if os.path.exists(sample_file):
        print(f"\n1. Testing schema detection from file: {sample_file}")
        
        # Detect schema version
        detected_version = schema_service.detect_schema_version_from_file(sample_file)
        print(f"   Detected version: {detected_version}")
        
        # Auto-detect and set version
        print("   Calling auto_detect_and_set_version...")
        success = schema_service.auto_detect_and_set_version(file_path=sample_file)
        print(f"   Auto-detect and set: {'Success' if success else 'Failed'}")
        print(f"   Current schema version: {schema_service.current_version}")
        print(f"   Schema loaded: {'Yes' if schema_service.current_schema else 'No'}")
        
        # Try manually setting version
        print("   Manually setting version 4.7.0...")
        manual_success = schema_service.set_version("4.7.0")
        print(f"   Manual set: {'Success' if manual_success else 'Failed'}")
        print(f"   Schema loaded after manual set: {'Yes' if schema_service.current_schema else 'No'}")
        
        # Parse the file
        print(f"\n2. Parsing ARXML file with detected schema")
        root = parser.parse_arxml_file(sample_file)
        if root:
            print("   Parsing: Success")
            print(f"   Root element: {root.tag}")
            print(f"   Namespace: {root.nsmap.get(None, 'None')}")
        else:
            print("   Parsing: Failed")
        
        # Test validation
        print(f"\n3. Testing schema validation")
        if schema_service.current_schema:
            validation_errors = schema_service.validate_arxml_file(sample_file)
            if validation_errors:
                print("   Validation errors found:")
                for error in validation_errors:
                    print(f"     - {error}")
            else:
                print("   Validation: No errors found")
        else:
            print("   Validation: No schema loaded")
    
    else:
        print(f"Sample file {sample_file} not found")
    
    # Test with different namespace scenarios
    print(f"\n4. Testing namespace mapping")
    test_namespaces = [
        "http://autosar.org/schema/r4.0",
        "http://autosar.org/schema/r4.1", 
        "http://autosar.org/schema/r4.2",
        "http://autosar.org/schema/r4.3",
        "http://autosar.org/schema/r4.4"
    ]
    
    for namespace in test_namespaces:
        mapped_version = schema_service._namespace_version_map.get(namespace, "Unknown")
        print(f"   {namespace} -> {mapped_version}")
    
    # Test schema location parsing
    print(f"\n5. Testing schema location parsing")
    test_schema_locations = [
        "http://autosar.org/schema/r4.0 AUTOSAR_4-7-0.xsd",
        "http://autosar.org/schema/r4.0 AUTOSAR_4-6-0.xsd",
        "http://autosar.org/schema/r4.0 AUTOSAR_4.5.0.xsd",
        "http://autosar.org/schema/r4.0 AUTOSAR_4_4_0.xsd"
    ]
    
    for schema_location in test_schema_locations:
        version = schema_service._extract_version_from_schema_location(schema_location)
        print(f"   '{schema_location}' -> {version}")
    
    print(f"\n6. Available schema versions:")
    for version in schema_service.get_available_versions():
        version_info = schema_service.get_version_info(version)
        print(f"   {version}: {version_info.display_name} ({version_info.namespace})")
    
    print(f"\nTest completed!")

if __name__ == "__main__":
    test_schema_detection()