#!/usr/bin/env python3
"""
Dependency Injection Test
Tests the new DI system while ensuring backward compatibility
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_di_container():
    """Test dependency injection container functionality"""
    print("=" * 60)
    print("DEPENDENCY INJECTION SYSTEM TEST")
    print("=" * 60)
    
    try:
        # Test 1: Container Setup
        print("✓ Testing container setup...")
        from src.core.container import setup_container
        container = setup_container()
        print("✅ Container setup successful")
        
        # Test 2: Service Registration
        print("✓ Testing service registration...")
        from src.core.interfaces import ISchemaService, IValidationService, ICommandService, IARXMLParser
        
        schema_service = container.get(ISchemaService)
        validation_service = container.get(IValidationService)
        command_service = container.get(ICommandService)
        parser_service = container.get(IARXMLParser)
        
        print(f"   - Schema Service: {type(schema_service).__name__}")
        print(f"   - Validation Service: {type(validation_service).__name__}")
        print(f"   - Command Service: {type(command_service).__name__}")
        print(f"   - Parser Service: {type(parser_service).__name__}")
        print("✅ All services resolved successfully")
        
        # Test 3: Singleton Behavior
        print("✓ Testing singleton behavior...")
        schema_service2 = container.get(ISchemaService)
        if schema_service is schema_service2:
            print("✅ Singleton behavior working correctly")
        else:
            print("❌ Singleton behavior not working")
            return False
        
        # Test 4: Service Interface Compliance
        print("✓ Testing interface compliance...")
        
        # Check if services implement required methods
        required_methods = {
            ISchemaService: ['set_version', 'validate_arxml', 'detect_schema_version_from_file', 'get_available_versions'],
            IValidationService: ['validate_document', 'validate_element', 'clear_issues'],
            ICommandService: ['execute_command', 'undo', 'redo', 'can_undo', 'can_redo'],
            IARXMLParser: ['parse_arxml_file', 'parse_sw_component_types', 'parse_port_interfaces']
        }
        
        services = {
            ISchemaService: schema_service,
            IValidationService: validation_service,
            ICommandService: command_service,
            IARXMLParser: parser_service
        }
        
        for interface, service in services.items():
            missing_methods = []
            for method_name in required_methods[interface]:
                if not hasattr(service, method_name):
                    missing_methods.append(method_name)
            
            if missing_methods:
                print(f"❌ {interface.__name__} missing methods: {missing_methods}")
                return False
            else:
                print(f"   - {interface.__name__}: All methods present ✓")
        
        print("✅ All services implement required interfaces")
        
        return True
        
    except Exception as e:
        print(f"❌ Container test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_application_with_di():
    """Test application creation with dependency injection"""
    print("\n✓ Testing application with DI...")
    
    try:
        from src.core.container import setup_container
        from src.core.application import ARXMLEditorApp
        
        # Test with DI container
        container = setup_container()
        app_with_di = ARXMLEditorApp(container)
        
        # Verify services are injected
        assert hasattr(app_with_di, 'validation_service')
        assert hasattr(app_with_di, 'schema_service')
        assert hasattr(app_with_di, 'command_service')
        assert hasattr(app_with_di, 'arxml_parser')
        
        print("✅ Application with DI created successfully")
        
        # Test legacy mode (backward compatibility)
        app_legacy = ARXMLEditorApp(None)
        
        # Verify services are still available
        assert hasattr(app_legacy, 'validation_service')
        assert hasattr(app_legacy, 'schema_service')
        assert hasattr(app_legacy, 'command_service')
        assert hasattr(app_legacy, 'arxml_parser')
        
        print("✅ Legacy application mode still works")
        
        return True
        
    except Exception as e:
        print(f"❌ Application test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_factory():
    """Test factory methods"""
    print("\n✓ Testing factory methods...")
    
    try:
        from src.factory import ARXMLEditorFactory, create_arxml_editor
        
        # Test factory creation
        app1 = ARXMLEditorFactory.create_application()
        app2 = ARXMLEditorFactory.create_legacy_application()
        
        print("✅ Factory methods work correctly")
        
        # Test convenience function
        app3 = create_arxml_editor(use_di=True)
        app4 = create_arxml_editor(use_di=False)
        
        print("✅ Convenience functions work correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Factory test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_backward_compatibility():
    """Test that existing functionality still works"""
    print("\n✓ Testing backward compatibility...")
    
    try:
        # Test that old imports still work
        from src.core.services.schema_service import SchemaService
        from src.core.services.validation_service import ValidationService
        from src.core.services.command_service import CommandService
        from src.core.services.arxml_parser import ARXMLParser
        
        # Test that services can still be created directly
        schema = SchemaService()
        validation = ValidationService(schema)
        command = CommandService()
        parser = ARXMLParser(schema)
        
        # Test that they have expected methods
        assert hasattr(schema, 'set_version')
        assert hasattr(validation, 'validate_document')
        assert hasattr(command, 'execute_command')
        assert hasattr(parser, 'parse_arxml_file')
        
        print("✅ Direct service instantiation still works")
        
        # Test that application can still be created without DI
        from src.core.application import ARXMLEditorApp
        app = ARXMLEditorApp()
        
        assert hasattr(app, 'validation_service')
        assert hasattr(app, 'schema_service')
        
        print("✅ Legacy application creation still works")
        
        return True
        
    except Exception as e:
        print(f"❌ Backward compatibility test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("Testing Dependency Injection Implementation")
    print("=" * 60)
    
    tests = [
        ("DI Container", test_di_container),
        ("Application with DI", test_application_with_di),
        ("Factory Methods", test_factory),
        ("Backward Compatibility", test_backward_compatibility)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n[{test_name}]")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            failed += 1
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    print(f"✅ PASSED: {passed}")
    print(f"❌ FAILED: {failed}")
    print(f"📊 SUCCESS RATE: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Dependency Injection is working correctly!")
        print("   - Services are properly abstracted")
        print("   - Dependency injection container works")
        print("   - Backward compatibility maintained")
        print("   - Factory methods available")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the implementation.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)