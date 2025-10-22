#!/usr/bin/env python3
"""
ARXML Editor - Tkinter Version
Main entry point for the Tkinter-based ARXML Editor
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from src.ui.tkinter_main_window import main
    main()
except ImportError as e:
    print(f"Error importing Tkinter UI: {e}")
    print("Falling back to console mode...")
    
    # Fallback to console version
    import argparse
    
    def console_main():
        """Console-based ARXML editor"""
        parser = argparse.ArgumentParser(description="ARXML Editor - Console Version")
        parser.add_argument("command", choices=["validate", "parse"], help="Command to execute")
        parser.add_argument("file", help="ARXML file to process")
        
        args = parser.parse_args()
        
        if not os.path.exists(args.file):
            print(f"ERROR: File not found: {args.file}")
            return 1
            
        try:
            from src.core.services.arxml_parser import ARXMLParser
            from src.core.services.schema_service import SchemaService
            from src.core.services.validation_service import ValidationService
            
            if args.command == "validate":
                print(f"Validating: {args.file}")
                
                # Parse the file
                arxml_parser = ARXMLParser()
                root = arxml_parser.parse_arxml_file(args.file)
                if root is None:
                    print("ERROR: Failed to parse ARXML file")
                    return 1
                
                # Validate against schema
                schema_service = SchemaService()
                schema_version = schema_service.detect_schema_version(args.file)
                if schema_version:
                    print(f"Detected schema version: {schema_version}")
                    is_valid, errors = schema_service.validate_arxml_file(args.file)
                    if is_valid:
                        print("✓ ARXML file is valid")
                    else:
                        print("✗ ARXML file has validation errors:")
                        for error in errors:
                            print(f"  - {error}")
                else:
                    print("WARNING: Could not detect schema version")
                    print("File parsed successfully but validation skipped")
                    
            elif args.command == "parse":
                print(f"Parsing: {args.file}")
                
                # Parse the file
                arxml_parser = ARXMLParser()
                root = arxml_parser.parse_arxml_file(args.file)
                if root is None:
                    print("ERROR: Failed to parse ARXML file")
                    return 1
                
                print("✓ ARXML file parsed successfully")
                
                # Extract basic information
                sw_components = arxml_parser.extract_sw_component_types(root)
                compositions = arxml_parser.extract_compositions(root)
                port_interfaces = arxml_parser.extract_port_interfaces(root)
                
                print(f"Found {len(sw_components)} software components")
                print(f"Found {len(compositions)} compositions")
                print(f"Found {len(port_interfaces)} port interfaces")
                
        except Exception as e:
            print(f"ERROR: {e}")
            return 1
            
        return 0
    
    sys.exit(console_main())