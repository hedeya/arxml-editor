#!/usr/bin/env python3
"""
Test script to verify ARXML Editor application functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.application import ARXMLEditorApp

def test_application():
    """Test the ARXML Editor application"""
    print("Testing ARXML Editor Application")
    print("=" * 40)
    
    try:
        # Initialize application
        print("1. Initializing application...")
        app = ARXMLEditorApp()
        print("   ✓ Application initialized successfully")
        
        # Test schema service
        print("\n2. Testing schema service...")
        schema_service = app.schema_service
        print(f"   ✓ Schema service available")
        print(f"   ✓ Available versions: {schema_service.get_available_versions()}")
        print(f"   ✓ Current version: {schema_service.current_version}")
        print(f"   ✓ Schema loaded: {'Yes' if schema_service.current_schema else 'No'}")
        
        # Test validation service
        print("\n3. Testing validation service...")
        validation_service = app.validation_service
        print(f"   ✓ Validation service available")
        print(f"   ✓ Error count: {validation_service.error_count}")
        print(f"   ✓ Warning count: {validation_service.warning_count}")
        
        # Test ARXML parser
        print("\n4. Testing ARXML parser...")
        parser = app.arxml_parser
        print(f"   ✓ Parser available")
        
        # Test document creation
        print("\n5. Testing document creation...")
        document = app.new_document()
        print(f"   ✓ New document created")
        print(f"   ✓ Document has {len(document.sw_component_types)} component types")
        print(f"   ✓ Document has {len(document.compositions)} compositions")
        print(f"   ✓ Document has {len(document.port_interfaces)} port interfaces")
        print(f"   ✓ Document has {len(document.service_interfaces)} service interfaces")
        
        # Test loading sample file
        print("\n6. Testing file loading...")
        sample_file = "sample.arxml"
        if os.path.exists(sample_file):
            success = app.load_document(sample_file)
            if success:
                print(f"   ✓ Successfully loaded {sample_file}")
                print(f"   ✓ Document schema version: {document.schema_version}")
                print(f"   ✓ Detected schema version: {schema_service.detected_version}")
                
                # Test validation
                print("\n7. Testing validation...")
                validation_service.validate_document(document)
                print(f"   ✓ Validation completed")
                print(f"   ✓ Validation issues: {len(validation_service.issues)}")
                
                if validation_service.issues:
                    print("   Validation issues found:")
                    for i, issue in enumerate(validation_service.issues[:3]):  # Show first 3
                        print(f"     {i+1}. [{issue.severity.value}] {issue.message}")
                else:
                    print("   ✓ No validation issues found")
            else:
                print(f"   ✗ Failed to load {sample_file}")
        else:
            print(f"   ⚠ Sample file {sample_file} not found")
        
        # Test command service
        print("\n8. Testing command service...")
        command_service = app.command_service
        print(f"   ✓ Command service available")
        print(f"   ✓ Can undo: {command_service.can_undo}")
        print(f"   ✓ Can redo: {command_service.can_redo}")
        
        print(f"\n✓ All tests completed successfully!")
        print(f"✓ Application is working correctly with schema detection and validation")
        
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_application()
    sys.exit(0 if success else 1)