#!/usr/bin/env python3
"""
Repository Pattern and Application Services Test
Tests the new repository pattern and application services implementation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_repository_pattern():
    """Test repository pattern implementation"""
    print("=" * 60)
    print("REPOSITORY PATTERN TEST")
    print("=" * 60)
    
    try:
        # Test 1: Repository Factory
        print("✓ Testing repository factory...")
        from src.core.repositories.memory_repositories import InMemoryRepositoryFactory
        from src.core.repositories import IRepositoryFactory
        
        factory = InMemoryRepositoryFactory()
        assert isinstance(factory, IRepositoryFactory)
        print("✅ Repository factory created successfully")
        
        # Test 2: Repository Creation
        print("✓ Testing repository creation...")
        sw_repo = factory.create_sw_component_type_repository()
        port_repo = factory.create_port_interface_repository()
        comp_repo = factory.create_composition_repository()
        
        print(f"   - Software Component Repository: {type(sw_repo).__name__}")
        print(f"   - Port Interface Repository: {type(port_repo).__name__}")
        print(f"   - Composition Repository: {type(comp_repo).__name__}")
        print("✅ All repositories created successfully")
        
        # Test 3: Repository Operations
        print("✓ Testing repository operations...")
        from src.core.models.autosar_elements import SwComponentType, SwComponentTypeCategory, PortInterface
        
        # Test software component repository
        component = SwComponentType("TestComponent", SwComponentTypeCategory.APPLICATION, "Test Description")
        assert sw_repo.save(component)
        assert sw_repo.exists_by_name("TestComponent")
        assert sw_repo.find_by_name("TestComponent") == component
        assert len(sw_repo.find_all()) == 1
        
        # Test port interface repository
        interface = PortInterface("TestInterface", "Test Description", False)
        assert port_repo.save(interface)
        assert port_repo.exists_by_name("TestInterface")
        assert port_repo.find_by_name("TestInterface") == interface
        assert len(port_repo.find_all()) == 1
        
        print("✅ Repository operations working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Repository pattern test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_application_services():
    """Test application services implementation"""
    print("\n✓ Testing application services...")
    
    try:
        # Setup DI container
        from src.core.container import setup_container
        container = setup_container()
        
        # Get application services
        from src.core.application_services import ISwComponentTypeApplicationService, IPortInterfaceApplicationService, IDocumentApplicationService
        
        sw_service = container.get(ISwComponentTypeApplicationService)
        port_service = container.get(IPortInterfaceApplicationService)
        doc_service = container.get(IDocumentApplicationService)
        
        print(f"   - Software Component Service: {type(sw_service).__name__}")
        print(f"   - Port Interface Service: {type(port_service).__name__}")
        print(f"   - Document Service: {type(doc_service).__name__}")
        
        # Test software component service
        result = sw_service.create_component_type("TestComponent", "APPLICATION", "Test Description")
        assert result.success, f"Failed to create component: {result.message}"
        print("✅ Software component service working")
        
        # Test port interface service
        result = port_service.create_port_interface("TestInterface", False, "Test Description")
        assert result.success, f"Failed to create interface: {result.message}"
        print("✅ Port interface service working")
        
        # Test document service
        result = doc_service.create_new_document()
        assert result.success, f"Failed to create document: {result.message}"
        print("✅ Document service working")
        
        return True
        
    except Exception as e:
        print(f"❌ Application services test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """Test integration between repositories and application services"""
    print("\n✓ Testing integration...")
    
    try:
        from src.core.container import setup_container
        from src.core.application import ARXMLEditorApp
        
        # Create application with DI
        container = setup_container()
        app = ARXMLEditorApp(container)
        
        # Test document creation
        document = app.new_document()
        assert document is not None
        print("✅ Document creation with DI working")
        
        # Test repository access
        if app.repository_factory:
            sw_repo = app.repository_factory.create_sw_component_type_repository()
            assert sw_repo is not None
            print("✅ Repository factory accessible from application")
        
        # Test application services
        if app.sw_component_service:
            result = app.sw_component_service.create_component_type("IntegrationTest", "APPLICATION")
            assert result.success
            print("✅ Application services accessible from application")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_backward_compatibility():
    """Test that existing functionality still works"""
    print("\n✓ Testing backward compatibility...")
    
    try:
        from src.core.application import ARXMLEditorApp
        
        # Test legacy mode
        app_legacy = ARXMLEditorApp(None)
        assert app_legacy.validation_service is not None
        assert app_legacy.command_service is not None
        assert app_legacy.schema_service is not None
        print("✅ Legacy mode still works")
        
        # Test document creation in legacy mode
        document = app_legacy.new_document()
        assert document is not None
        print("✅ Legacy document creation works")
        
        return True
        
    except Exception as e:
        print(f"❌ Backward compatibility test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("Testing Repository Pattern and Application Services Implementation")
    print("=" * 60)
    
    tests = [
        ("Repository Pattern", test_repository_pattern),
        ("Application Services", test_application_services),
        ("Integration", test_integration),
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
        print("\n🎉 ALL TESTS PASSED! Repository Pattern and Application Services are working correctly!")
        print("   - Repository pattern implemented")
        print("   - Application services layer created")
        print("   - Dependency injection working")
        print("   - Backward compatibility maintained")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the implementation.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)