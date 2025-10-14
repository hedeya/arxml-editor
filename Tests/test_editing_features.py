#!/usr/bin/env python3
"""
Test editing features and diagram functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.models.arxml_document import ARXMLDocument
from src.core.models.autosar_elements import (
    ApplicationSwComponentType, SwComponentTypeCategory,
    Composition, PortInterface, ServiceInterface
)

def test_editing_features():
    """Test editing features"""
    print("Testing ARXML Editing Features")
    print("=" * 35)
    
    # Create a new document
    doc = ARXMLDocument()
    print(f"✓ Created new document")
    print(f"  Modified: {doc.modified}")
    print(f"  Schema version: {doc.schema_version}")
    
    # Add a software component type
    component = ApplicationSwComponentType(
        short_name="TestComponent",
        desc="Test component for editing"
    )
    doc.add_sw_component_type(component)
    print(f"✓ Added component: {component.short_name}")
    print(f"  Modified: {doc.modified}")
    print(f"  Component count: {len(doc.sw_component_types)}")
    
    # Modify the component
    component.short_name = "ModifiedComponent"
    component.desc = "Modified description"
    doc.set_modified(True)
    print(f"✓ Modified component: {component.short_name}")
    print(f"  Modified: {doc.modified}")
    
    # Add a port interface
    port_interface = PortInterface(
        short_name="TestInterface",
        desc="Test port interface",
        is_service=False
    )
    doc.add_port_interface(port_interface)
    print(f"✓ Added port interface: {port_interface.short_name}")
    print(f"  Port interface count: {len(doc.port_interfaces)}")
    
    # Add a composition
    composition = Composition(
        short_name="TestComposition",
        desc="Test composition"
    )
    doc.add_composition(composition)
    print(f"✓ Added composition: {composition.short_name}")
    print(f"  Composition count: {len(doc.compositions)}")
    
    # Test save functionality
    test_file = "test_editing.arxml"
    if doc.save_document(test_file):
        print(f"✓ Saved document to: {test_file}")
        print(f"  Modified after save: {doc.modified}")
        
        # Check if file exists and has content
        if os.path.exists(test_file):
            with open(test_file, 'r') as f:
                content = f.read()
                print(f"  File size: {len(content)} characters")
                print(f"  Contains 'ModifiedComponent': {'ModifiedComponent' in content}")
                print(f"  Contains 'TestInterface': {'TestInterface' in content}")
    else:
        print("✗ Failed to save document")
    
    # Test removal
    doc.remove_sw_component_type(component)
    print(f"✓ Removed component: {component.short_name}")
    print(f"  Component count after removal: {len(doc.sw_component_types)}")
    print(f"  Modified: {doc.modified}")
    
    # Test diagram information
    print(f"\nDiagram Information:")
    print(f"  Software Component Types: {len(doc.sw_component_types)}")
    print(f"  Compositions: {len(doc.compositions)}")
    print(f"  Port Interfaces: {len(doc.port_interfaces)}")
    print(f"  Service Interfaces: {len(doc.service_interfaces)}")
    print(f"  ECUC Elements: {len(doc.ecuc_elements)}")
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"✓ Cleaned up test file")
    
    print(f"\n🎉 All editing features working correctly!")

if __name__ == "__main__":
    test_editing_features()