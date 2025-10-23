#!/usr/bin/env python3
"""
Test DDD Improvements
Tests the enhanced domain models, aggregate boundaries, and business invariants
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_aggregate_boundaries():
    """Test strengthened aggregate boundaries"""
    print("=" * 60)
    print("TESTING AGGREGATE BOUNDARIES")
    print("=" * 60)
    
    try:
        from src.core.models.arxml_document import ARXMLDocument
        from src.core.models.autosar_elements import SwComponentType, SwComponentTypeCategory, PortInterface, DataElement, DataType
        
        # Test 1: Read-only collections
        print("✓ Testing read-only collections...")
        doc = ARXMLDocument()
        
        # Collections should return copies, not references
        comp_types = doc.sw_component_types
        comp_types.append("test")  # This should not affect the original
        assert len(doc.sw_component_types) == 0
        print("✅ Read-only collections working")
        
        # Test 2: Aggregate business methods
        print("✓ Testing aggregate business methods...")
        
        # Test statistics
        stats = doc.get_document_statistics()
        assert 'component_types' in stats
        assert 'interfaces' in stats
        assert 'compositions' in stats
        assert stats['component_types']['total'] == 0
        print("✅ Aggregate business methods working")
        
        # Test 3: Document consistency validation
        print("✓ Testing document consistency validation...")
        
        # Add some elements
        comp1 = SwComponentType("TestComponent1", SwComponentTypeCategory.APPLICATION)
        comp2 = SwComponentType("TestComponent2", SwComponentTypeCategory.ATOMIC)
        doc.add_sw_component_type(comp1)
        doc.add_sw_component_type(comp2)
        
        # Test duplicate name detection
        comp3 = SwComponentType("TestComponent1", SwComponentTypeCategory.APPLICATION)  # Duplicate name
        doc.add_sw_component_type(comp3)
        
        violations = doc.validate_document_consistency()
        assert any("Duplicate name" in v for v in violations)
        print("✅ Document consistency validation working")
        
        return True
        
    except Exception as e:
        print(f"❌ Aggregate boundaries test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_enriched_domain_models():
    """Test enriched domain models with business logic"""
    print("\n" + "=" * 60)
    print("TESTING ENRICHED DOMAIN MODELS")
    print("=" * 60)
    
    try:
        from src.core.models.autosar_elements import (
            SwComponentType, SwComponentTypeCategory, PortInterface, 
            DataElement, DataType, PortPrototype, PortType, Composition
        )
        
        # Test 1: SwComponentType business logic
        print("✓ Testing SwComponentType business logic...")
        
        comp = SwComponentType("TestComponent", SwComponentTypeCategory.APPLICATION)
        
        # Test naming validation
        assert comp._is_valid_component_name("ValidName123")
        assert not comp._is_valid_component_name("Invalid Name")
        assert not comp._is_valid_component_name("123Invalid")
        print("✅ Component naming validation working")
        
        # Test port management
        from src.core.models.autosar_elements import PortPrototype, PortType
        port = PortPrototype("TestPort", PortType.PROVIDER)
        
        assert comp.can_add_port(port)
        comp.add_port(port)
        assert not comp.can_add_port(port)  # Duplicate name
        print("✅ Port management working")
        
        # Test 2: PortInterface business logic
        print("✓ Testing PortInterface business logic...")
        
        interface = PortInterface("TestInterface", False)  # Sender-receiver interface
        
        # Test data element management
        data_elem = DataElement("TestData", DataType.INTEGER)
        assert interface.can_add_data_element(data_elem)
        interface.add_data_element(data_elem)
        assert not interface.can_add_data_element(data_elem)  # Duplicate name
        print("✅ Interface data element management working")
        
        # Test interface compatibility
        interface2 = PortInterface("TestInterface2", False)
        data_elem2 = DataElement("TestData", DataType.INTEGER)
        interface2.add_data_element(data_elem2)
        
        assert interface.is_compatible_with(interface2)
        print("✅ Interface compatibility working")
        
        # Test 3: DataElement business logic
        print("✓ Testing DataElement business logic...")
        
        data_elem = DataElement("TestData", DataType.INTEGER, is_array=True, array_size=10)
        assert data_elem.is_valid()
        
        # Test invalid array
        invalid_data = DataElement("InvalidData", DataType.INTEGER, is_array=True, array_size=0)
        assert not invalid_data.is_valid()
        print("✅ Data element validation working")
        
        # Test 4: PortPrototype business logic
        print("✓ Testing PortPrototype business logic...")
        
        port1 = PortPrototype("Port1", PortType.PROVIDER)
        port2 = PortPrototype("Port2", PortType.REQUIRER)
        
        assert port1.can_connect_to(port2)
        assert port1.connect_to(port2)
        assert not port1.can_connect_to(port2)  # Already connected
        print("✅ Port connection logic working")
        
        # Test 5: Composition business logic
        print("✓ Testing Composition business logic...")
        
        comp1 = SwComponentType("Comp1", SwComponentTypeCategory.APPLICATION)
        comp2 = SwComponentType("Comp2", SwComponentTypeCategory.APPLICATION)
        composition = Composition("TestComposition")
        
        assert composition.can_add_component_type(comp1)
        assert composition.add_component_type(comp1)
        assert not composition.can_add_component_type(comp1)  # Duplicate
        print("✅ Composition management working")
        
        return True
        
    except Exception as e:
        print(f"❌ Enriched domain models test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_domain_invariants():
    """Test domain invariants and business rules"""
    print("\n" + "=" * 60)
    print("TESTING DOMAIN INVARIANTS")
    print("=" * 60)
    
    try:
        from src.core.models.autosar_elements import (
            SwComponentType, SwComponentTypeCategory, PortInterface, 
            DataElement, DataType, PortPrototype, PortType, Composition
        )
        
        # Test 1: Base element invariants
        print("✓ Testing base element invariants...")
        
        from src.core.models.autosar_elements import BaseElement
        
        # Test valid element
        class TestElement(BaseElement):
            pass
        
        valid_elem = TestElement("ValidName123")
        assert valid_elem.is_valid()
        assert len(valid_elem.get_validation_errors()) == 0
        print("✅ Base element validation working")
        
        # Test invalid element
        invalid_elem = TestElement("Invalid Name")
        assert not invalid_elem.is_valid()
        assert len(invalid_elem.get_validation_errors()) > 0
        print("✅ Base element validation working")
        
        # Test 2: Component type invariants
        print("✓ Testing component type invariants...")
        
        comp = SwComponentType("", SwComponentTypeCategory.APPLICATION)  # Empty name
        violations = comp.validate_invariants()
        assert any("name cannot be empty" in v.lower() for v in violations)
        print("✅ Component type validation working")
        
        # Test 3: Port interface invariants
        print("✓ Testing port interface invariants...")
        
        # Test service interface with data elements (invalid)
        service_interface = PortInterface("ServiceInterface", is_service=True)  # Service interface
        data_elem = DataElement("TestData", DataType.INTEGER)
        # Add directly to test validation (bypassing can_add_data_element check)
        service_interface.data_elements.append(data_elem)
        
        violations = service_interface.validate_invariants()
        assert any("service interfaces should not have data elements" in v.lower() for v in violations)
        print("✅ Port interface validation working")
        
        # Test 4: Data element invariants
        print("✓ Testing data element invariants...")
        
        # Test invalid array
        invalid_data = DataElement("TestData", DataType.INTEGER, is_array=True, array_size=0)
        violations = invalid_data.validate_invariants()
        assert any("array size must be positive" in v.lower() for v in violations)
        print("✅ Data element validation working")
        
        # Test 5: Port prototype invariants
        print("✓ Testing port prototype invariants...")
        
        port = PortPrototype("", PortType.PROVIDER)  # Empty name
        violations = port.validate_invariants()
        assert any("name cannot be empty" in v.lower() for v in violations)
        print("✅ Port prototype validation working")
        
        # Test 6: Composition invariants
        print("✓ Testing composition invariants...")
        
        composition = Composition("TestComposition")
        comp1 = SwComponentType("Comp1", SwComponentTypeCategory.APPLICATION)
        comp2 = SwComponentType("Comp1", SwComponentTypeCategory.APPLICATION)  # Duplicate name
        
        composition.add_component_type(comp1)
        # Add duplicate directly to test validation (bypassing can_add_component_type check)
        composition.component_types.append(comp2)
        
        violations = composition.validate_composition_integrity()
        assert any("component names must be unique" in v.lower() for v in violations)
        print("✅ Composition validation working")
        
        return True
        
    except Exception as e:
        print(f"❌ Domain invariants test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_business_operations():
    """Test business operations and domain behavior"""
    print("\n" + "=" * 60)
    print("TESTING BUSINESS OPERATIONS")
    print("=" * 60)
    
    try:
        from src.core.models.autosar_elements import (
            SwComponentType, SwComponentTypeCategory, PortInterface, 
            DataElement, DataType, PortPrototype, PortType, Composition
        )
        
        # Test 1: Element renaming
        print("✓ Testing element renaming...")
        
        comp = SwComponentType("OldName", SwComponentTypeCategory.APPLICATION)
        assert comp.can_be_renamed("NewName")
        assert comp.rename("NewName")
        assert comp.short_name == "NewName"
        assert not comp.can_be_renamed("")  # Invalid name
        print("✅ Element renaming working")
        
        # Test 2: Dependency tracking
        print("✓ Testing dependency tracking...")
        
        comp = SwComponentType("TestComponent", SwComponentTypeCategory.APPLICATION)
        port = PortPrototype("TestPort", PortType.PROVIDER, interface_ref="TestInterface")
        comp.add_port(port)
        
        dependencies = comp.get_dependencies()
        assert "TestInterface" in dependencies
        print("✅ Dependency tracking working")
        
        # Test 3: Connection management
        print("✓ Testing connection management...")
        
        port1 = PortPrototype("Port1", PortType.PROVIDER)
        port2 = PortPrototype("Port2", PortType.REQUIRER)
        
        assert port1.can_connect_to(port2)
        assert port1.connect_to(port2)
        assert port1.is_connected()
        assert port1.get_connection_count() == 1
        print("✅ Connection management working")
        
        # Test 4: Interface compatibility
        print("✓ Testing interface compatibility...")
        
        interface1 = PortInterface("Interface1", False)
        interface2 = PortInterface("Interface2", False)
        
        data1 = DataElement("Data1", DataType.INTEGER)
        data2 = DataElement("Data1", DataType.INTEGER)  # Same name and type
        
        interface1.add_data_element(data1)
        interface2.add_data_element(data2)
        
        assert interface1.is_compatible_with(interface2)
        print("✅ Interface compatibility working")
        
        # Test 5: Composition integrity
        print("✓ Testing composition integrity...")
        
        composition = Composition("TestComposition")
        comp1 = SwComponentType("Comp1", SwComponentTypeCategory.APPLICATION)
        comp2 = SwComponentType("Comp2", SwComponentTypeCategory.APPLICATION)
        
        composition.add_component_type(comp1)
        composition.add_component_type(comp2)
        
        assert composition.get_component_count() == 2
        assert composition.get_connection_count() == 0
        print("✅ Composition integrity working")
        
        return True
        
    except Exception as e:
        print(f"❌ Business operations test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_domain_events():
    """Test domain events integration"""
    print("\n" + "=" * 60)
    print("TESTING DOMAIN EVENTS")
    print("=" * 60)
    
    try:
        from src.core.models.autosar_elements import SwComponentType, SwComponentTypeCategory
        from src.core.domain_events.event_bus import EventBusFactory
        from src.core.domain_events import ElementRenamed, SwComponentTypeUpdated
        
        # Test 1: Event bus setup
        print("✓ Testing event bus setup...")
        
        event_bus = EventBusFactory.create_sync_bus()
        received_events = []
        
        def event_handler(event):
            received_events.append(event)
        
        event_bus.subscribe(ElementRenamed, event_handler)
        event_bus.subscribe(SwComponentTypeUpdated, event_handler)
        print("✅ Event bus setup working")
        
        # Test 2: Element rename events
        print("✓ Testing element rename events...")
        
        comp = SwComponentType("TestComponent", SwComponentTypeCategory.APPLICATION)
        comp.set_event_bus(event_bus)
        
        comp.rename("NewComponentName")
        comp.publish_domain_events()
        
        assert len(received_events) == 1
        assert received_events[0].event_type == "ElementRenamed"
        assert received_events[0].old_name == "TestComponent"
        assert received_events[0].new_name == "NewComponentName"
        print("✅ Element rename events working")
        
        # Test 3: Component change events
        print("✓ Testing component change events...")
        
        comp.change_category(SwComponentTypeCategory.ATOMIC)
        comp.publish_domain_events()
        
        assert len(received_events) == 2
        assert received_events[1].event_type == "SwComponentTypeUpdated"
        print("✅ Component change events working")
        
        return True
        
    except Exception as e:
        print(f"❌ Domain events test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all DDD improvement tests"""
    print("Testing DDD Improvements Implementation")
    print("=" * 60)
    
    tests = [
        ("Aggregate Boundaries", test_aggregate_boundaries),
        ("Enriched Domain Models", test_enriched_domain_models),
        ("Domain Invariants", test_domain_invariants),
        ("Business Operations", test_business_operations),
        ("Domain Events", test_domain_events)
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
    print("DDD IMPROVEMENTS TEST RESULTS")
    print("=" * 60)
    print(f"✅ PASSED: {passed}")
    print(f"❌ FAILED: {failed}")
    print(f"📊 SUCCESS RATE: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL DDD IMPROVEMENTS TESTS PASSED!")
        print("   - Aggregate boundaries strengthened")
        print("   - Domain models enriched with business logic")
        print("   - Domain invariants implemented")
        print("   - Business operations working")
        print("   - Domain events integrated")
        print("\n🚀 DDD Compliance Improvements:")
        print("   - Better encapsulation in aggregates")
        print("   - Rich domain models with behavior")
        print("   - Comprehensive business rule validation")
        print("   - Enhanced domain event system")
        print("   - Improved separation of concerns")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the implementation.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)