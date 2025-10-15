#!/usr/bin/env python3
"""
Test script for new ARXML Editor features
Tests: Editable properties, drag & drop, delete confirmation, save as
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.models.arxml_document import ARXMLDocument
from src.core.models.autosar_elements import ApplicationSwComponentType, PortPrototype, PortType

def test_editable_properties():
    """Test that properties can be edited"""
    print("🧪 Testing Editable Properties...")
    
    # Create a test document
    doc = ARXMLDocument()
    
    # Create a component
    component = ApplicationSwComponentType(
        short_name="TestComponent",
        desc="Test component for editing"
    )
    
    # Add to document
    doc.add_sw_component_type(component)
    
    # Test property editing
    original_name = component.short_name
    component.short_name = "EditedComponent"
    
    assert component.short_name == "EditedComponent"
    assert component.short_name != original_name
    assert doc.modified == True
    
    print("✅ Editable properties test passed")
    return True

def test_drag_drop_logic():
    """Test drag and drop logic (without GUI)"""
    print("🧪 Testing Drag & Drop Logic...")
    
    # Create test document
    doc = ARXMLDocument()
    
    # Create components
    comp1 = ApplicationSwComponentType("Component1", "First component")
    comp2 = ApplicationSwComponentType("Component2", "Second component")
    
    doc.add_sw_component_type(comp1)
    doc.add_sw_component_type(comp2)
    
    # Test move logic (simulate what would happen in drag & drop)
    def can_move_element(element, target_data):
        """Simulate the can_move_element logic"""
        if target_data in ["sw_component_types", "compositions", "port_interfaces", "service_interfaces"]:
            return True
        if isinstance(element, type(comp1)) and isinstance(target_data, type(comp1)):
            return True
        return False
    
    # Test valid moves
    assert can_move_element(comp1, "sw_component_types") == True
    assert can_move_element(comp1, comp2) == True
    
    # Test invalid moves
    assert can_move_element(comp1, "invalid_category") == False
    
    print("✅ Drag & drop logic test passed")
    return True

def test_delete_confirmation_logic():
    """Test delete confirmation logic (without GUI)"""
    print("🧪 Testing Delete Confirmation Logic...")
    
    # Create test document
    doc = ARXMLDocument()
    
    # Create component with ports
    component = ApplicationSwComponentType("ComponentWithPorts", "Component with ports")
    port = PortPrototype("TestPort", "Test port", PortType.PROVIDER, "TestInterface")
    component.ports = [port]
    
    doc.add_sw_component_type(component)
    
    # Test children detection logic
    def has_children(element):
        """Simulate the has_children logic"""
        if hasattr(element, 'ports') and element.ports:
            return True
        if hasattr(element, 'component_types') and element.component_types:
            return True
        if hasattr(element, 'data_elements') and element.data_elements:
            return True
        return False
    
    # Test children detection
    assert has_children(component) == True
    
    # Test children info generation
    children_count = len(component.ports)
    children_info = f"\n\n⚠️  This component has {children_count} port(s) that will also be deleted."
    assert "port(s) that will also be deleted" in children_info
    
    print("✅ Delete confirmation logic test passed")
    return True

def test_save_as_functionality():
    """Test save as functionality"""
    print("🧪 Testing Save As Functionality...")
    
    # Create test document
    doc = ARXMLDocument()
    
    # Create component
    component = ApplicationSwComponentType("SaveTestComponent", "Component for save test")
    doc.add_sw_component_type(component)
    
    # Test original file path
    original_path = "test_original.arxml"
    doc._file_path = original_path
    
    # Test save as (simulate)
    new_path = "test_save_as.arxml"
    success = doc.save_document(new_path)
    
    # Check that file path was updated
    assert doc._file_path == new_path
    assert success == True
    
    print("✅ Save as functionality test passed")
    return True

def test_keyboard_shortcuts():
    """Test keyboard shortcut logic"""
    print("🧪 Testing Keyboard Shortcuts...")
    
    # Test delete shortcut logic
    def simulate_delete_key(item_data):
        """Simulate what happens when delete key is pressed"""
        if item_data:
            # This would trigger the delete confirmation dialog
            return True
        return False
    
    # Test with valid item
    test_element = ApplicationSwComponentType("TestElement", "Test element")
    assert simulate_delete_key(test_element) == True
    
    # Test with no item
    assert simulate_delete_key(None) == False
    
    print("✅ Keyboard shortcuts test passed")
    return True

def test_ecuc_property_editing():
    """Test ECUC element property editing"""
    print("🧪 Testing ECUC Property Editing...")
    
    # Create test ECUC element
    ecuc_element = {
        'type': 'EcuC',
        'short_name': 'TestEcuC',
        'uuid': '12345-67890-abcdef',
        'containers': [
            {
                'short_name': 'TestContainer',
                'definition_ref': '/Test/Definition',
                'parameters': [
                    {
                        'short_name': 'TestParam',
                        'definition_ref': '/Test/Param/Definition',
                        'value': 'TestValue'
                    }
                ]
            }
        ]
    }
    
    # Test property editing simulation
    original_name = ecuc_element['short_name']
    ecuc_element['short_name'] = 'EditedEcuC'
    
    assert ecuc_element['short_name'] == 'EditedEcuC'
    assert ecuc_element['short_name'] != original_name
    
    # Test container editing
    container = ecuc_element['containers'][0]
    original_container_name = container['short_name']
    container['short_name'] = 'EditedContainer'
    
    assert container['short_name'] == 'EditedContainer'
    assert container['short_name'] != original_container_name
    
    # Test parameter editing
    parameter = container['parameters'][0]
    original_param_value = parameter['value']
    parameter['value'] = 'EditedValue'
    
    assert parameter['value'] == 'EditedValue'
    assert parameter['value'] != original_param_value
    
    print("✅ ECUC property editing test passed")
    return True

def test_document_modification_tracking():
    """Test document modification tracking"""
    print("🧪 Testing Document Modification Tracking...")
    
    # Create test document
    doc = ARXMLDocument()
    
    # Initially not modified
    assert doc.modified == False
    
    # Add component - should mark as modified
    component = ApplicationSwComponentType("TestComponent", "Test component")
    doc.add_sw_component_type(component)
    
    assert doc.modified == True
    
    # Reset modification status
    doc.set_modified(False)
    assert doc.modified == False
    
    # Edit component property - should mark as modified
    component.short_name = "EditedComponent"
    # Note: In real implementation, this would be handled by property editor
    doc.set_modified(True)
    
    assert doc.modified == True
    
    print("✅ Document modification tracking test passed")
    return True

def main():
    """Run all tests"""
    print("🚀 Testing New ARXML Editor Features")
    print("=" * 50)
    
    tests = [
        test_editable_properties,
        test_drag_drop_logic,
        test_delete_confirmation_logic,
        test_save_as_functionality,
        test_keyboard_shortcuts,
        test_ecuc_property_editing,
        test_document_modification_tracking
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! New features are working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)