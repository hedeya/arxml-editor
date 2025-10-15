#!/usr/bin/env python3
"""
Test loading ECUC ARXML file
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.application import ARXMLEditorApp

def test_ecuc_file():
    """Test loading ECUC ARXML file"""
    print("Testing ECUC ARXML File Loading")
    print("=" * 35)
    
    # Initialize application
    app = ARXMLEditorApp()
    
    # Test loading ECUC file
    ecuc_file = "Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml"
    
    if os.path.exists(ecuc_file):
        print(f"Loading file: {ecuc_file}")
        
        # Load document
        success = app.load_document(ecuc_file)
        print(f"Load success: {success}")
        
        if success and app.current_document:
            doc = app.current_document
            print(f"Document loaded successfully")
            print(f"Schema version: {doc.schema_version}")
            print(f"Detected version: {app.schema_service.detected_version}")
            print(f"Schema loaded: {'Yes' if app.schema_service.current_schema else 'No'}")
            
            print(f"\nDocument content:")
            print(f"  Software component types: {len(doc.sw_component_types)}")
            print(f"  Compositions: {len(doc.compositions)}")
            print(f"  Port interfaces: {len(doc.port_interfaces)}")
            print(f"  Service interfaces: {len(doc.service_interfaces)}")
            print(f"  ECUC elements: {len(doc.ecuc_elements)}")
            
            if doc.ecuc_elements:
                print(f"\nECUC elements found:")
                for i, ecuc in enumerate(doc.ecuc_elements[:3]):  # Show first 3
                    print(f"  {i+1}. {ecuc['short_name']} ({ecuc['type']})")
                    print(f"     Containers: {len(ecuc.get('containers', []))}")
                    if ecuc.get('containers'):
                        for j, container in enumerate(ecuc['containers'][:2]):  # Show first 2 containers
                            print(f"       {j+1}. {container['short_name']} ({container['type']})")
                            print(f"          Parameters: {len(container.get('parameters', []))}")
            
            print(f"\nValidation issues: {len(app.validation_service.issues)}")
            for i, issue in enumerate(app.validation_service.issues[:3]):
                print(f"  {i+1}. [{issue.severity.value}] {issue.message[:100]}...")
        else:
            print("Failed to load document")
    else:
        print(f"ECUC file {ecuc_file} not found")

if __name__ == "__main__":
    test_ecuc_file()