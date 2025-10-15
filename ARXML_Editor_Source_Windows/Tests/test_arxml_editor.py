#!/usr/bin/env python3
"""
Test script for ARXML Editor
Creates a sample ARXML document and tests basic functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.models.arxml_document import ARXMLDocument
from src.core.models.autosar_elements import (
    ApplicationSwComponentType, AtomicSwComponentType, CompositionSwComponentType,
    PortInterface, DataElement, PortPrototype, PortType, DataType
)

def create_sample_document():
    """Create a sample ARXML document for testing"""
    doc = ARXMLDocument()
    
    # Create a sample application component
    app_comp = ApplicationSwComponentType(
        short_name="SampleAppComponent",
        desc="A sample application component for testing"
    )
    
    # Create port interface
    port_interface = PortInterface(
        short_name="SamplePortInterface",
        desc="A sample port interface"
    )
    
    # Add data element to interface
    data_element = DataElement(
        short_name="SampleData",
        data_type=DataType.STRING,
        desc="Sample data element"
    )
    port_interface.add_data_element(data_element)
    
    # Add port to component
    port = PortPrototype(
        short_name="SamplePort",
        port_type=PortType.PROVIDER,
        desc="Sample port",
        interface=port_interface
    )
    app_comp.add_port(port)
    
    # Add to document
    doc.add_sw_component_type(app_comp)
    doc.add_port_interface(port_interface)
    
    return doc

def test_serialization():
    """Test ARXML serialization"""
    print("Creating sample document...")
    doc = create_sample_document()
    
    print("Serializing to ARXML...")
    arxml_content = doc._parser.serialize_to_arxml(doc)
    
    print("ARXML Content:")
    print("=" * 50)
    print(arxml_content)
    print("=" * 50)
    
    return doc

def test_validation():
    """Test validation functionality"""
    print("\nTesting validation...")
    doc = create_sample_document()
    
    # Import validation service
    from src.core.services.validation_service import ValidationService
    
    # Create validation service and run validation
    validation_service = ValidationService()
    issues = validation_service.validate_document(doc)
    
    print(f"Validation found {len(issues)} issues:")
    for issue in issues:
        print(f"  [{issue.severity.value.upper()}] {issue.message}")
    
    return len(issues) == 0

if __name__ == "__main__":
    print("ARXML Editor Test Script")
    print("=" * 30)
    
    try:
        # Test serialization
        doc = test_serialization()
        
        # Test validation
        validation_passed = test_validation()
        
        print(f"\nTest Results:")
        print(f"  Serialization: {'PASS' if doc else 'FAIL'}")
        print(f"  Validation: {'PASS' if validation_passed else 'FAIL'}")
        
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()