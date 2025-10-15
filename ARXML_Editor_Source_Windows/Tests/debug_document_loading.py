#!/usr/bin/env python3
"""
Debug script to check document loading
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.application import ARXMLEditorApp

def debug_document_loading():
    """Debug document loading process"""
    print("Debugging Document Loading")
    print("=" * 40)
    
    # Initialize application
    app = ARXMLEditorApp()
    
    # Test loading sample file
    sample_file = "sample.arxml"
    if os.path.exists(sample_file):
        print(f"Loading file: {sample_file}")
        
        # Load document
        success = app.load_document(sample_file)
        print(f"Load success: {success}")
        
        if success and app.current_document:
            doc = app.current_document
            print(f"Document loaded successfully")
            print(f"Schema version: {doc.schema_version}")
            print(f"Detected version: {app.schema_service.detected_version}")
            print(f"Schema loaded: {'Yes' if app.schema_service.current_schema else 'No'}")
            
            print(f"\nDocument content:")
            print(f"  Software component types: {len(doc.sw_component_types)}")
            for comp in doc.sw_component_types:
                print(f"    - {comp.short_name} ({comp.category.value})")
                print(f"      Ports: {len(comp.ports)}")
                for port in comp.ports:
                    print(f"        - {port.short_name} ({port.port_type.value})")
            
            print(f"  Compositions: {len(doc.compositions)}")
            for comp in doc.compositions:
                print(f"    - {comp.short_name}")
            
            print(f"  Port interfaces: {len(doc.port_interfaces)}")
            for port_if in doc.port_interfaces:
                print(f"    - {port_if.short_name}")
                print(f"      Data elements: {len(port_if.data_elements)}")
                for data_elem in port_if.data_elements:
                    print(f"        - {data_elem.short_name} ({data_elem.data_type.value})")
            
            print(f"  Service interfaces: {len(doc.service_interfaces)}")
            for svc_if in doc.service_interfaces:
                print(f"    - {svc_if.short_name}")
            
            print(f"\nValidation issues: {len(app.validation_service.issues)}")
            for i, issue in enumerate(app.validation_service.issues):
                print(f"  {i+1}. [{issue.severity.value}] {issue.message[:100]}...")
        else:
            print("Failed to load document or document is None")
    else:
        print(f"Sample file {sample_file} not found")

if __name__ == "__main__":
    debug_document_loading()