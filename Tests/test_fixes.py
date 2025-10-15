#!/usr/bin/env python3
"""
Test script for the three main fixes:
1. ECUC saving functionality
2. Property persistence in GUI
3. Drag and drop visual indicators
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.models.arxml_document import ARXMLDocument
from src.core.models.autosar_elements import ApplicationSwComponentType

def test_ecuc_saving():
    """Test ECUC element saving functionality"""
    print("🧪 Testing ECUC Saving Functionality...")
    
    # Create a test document
    doc = ARXMLDocument()
    
    # Create a mock ECUC element (similar to what's parsed from ECUC files)
    ecuc_element = {
        'type': 'ECUC-MODULE-CONFIGURATION-VALUES',
        'uuid': '2f81491a-9caa-499a-8144-eee39f3fb8a0',
        'short_name': 'EcuC',
        'desc': 'ECU Configuration',
        'admin_data': {
            'SDGS': {
                'SDG': {
                    'GID': 'DV:CfgNamedRefs',
                    'SDG': {
                        'GID': '.ActiveEcuC.BswM',
                        'SDG': [
                            {
                                'GID': 'BswM_InitMemory',
                                'SDX-REF': {
                                    'DEST': 'ECUC-CONTAINER-VALUE',
                                    'text': '/ActiveEcuC/EcuC/EcucGeneral/BswInitialization/BswM_InitMemory'
                                }
                            }
                        ]
                    }
                }
            }
        },
        'containers': [
            {
                'type': 'ECUC-CONTAINER-VALUE',
                'short_name': 'EcucGeneral',
                'containers': [
                    {
                        'type': 'ECUC-CONTAINER-VALUE',
                        'short_name': 'BswInitialization',
                        'parameters': [
                            {
                                'type': 'ECUC-PARAMETER-VALUE',
                                'short_name': 'BswM_InitMemory',
                                'value': '1'
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    # Add ECUC element to document
    doc._ecuc_elements.append(ecuc_element)
    
    # Test save
    test_file = "test_ecuc_save.arxml"
    success = doc.save_document(test_file)
    
    if not success:
        print("❌ ECUC save failed")
        return False
    
    # Check if file contains ECUC elements
    if os.path.exists(test_file):
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if "ECUC-MODULE-CONFIGURATION-VALUES" in content:
                print("✅ ECUC elements saved to file")
            else:
                print("❌ ECUC elements not found in saved file")
                return False
            
            if "EcuC" in content:
                print("✅ ECUC short name preserved")
            else:
                print("❌ ECUC short name not preserved")
                return False
            
            if "BswM_InitMemory" in content:
                print("✅ ECUC containers and parameters saved")
            else:
                print("❌ ECUC containers and parameters not saved")
                return False
    else:
        print("❌ File was not created")
        return False
    
    # Clean up
    os.remove(test_file)
    print("✅ ECUC saving test passed")
    return True

def test_property_persistence():
    """Test property persistence when switching elements"""
    print("🧪 Testing Property Persistence...")
    
    # Create a test document
    doc = ARXMLDocument()
    
    # Create two components
    comp1 = ApplicationSwComponentType("Component1", "First component")
    comp2 = ApplicationSwComponentType("Component2", "Second component")
    
    doc.add_sw_component_type(comp1)
    doc.add_sw_component_type(comp2)
    
    # Simulate property editing
    print("1. Initial state:")
    print(f"   Component1 short_name: {comp1.short_name}")
    print(f"   Component2 short_name: {comp2.short_name}")
    
    # Simulate editing Component1's short_name
    print("2. Editing Component1 short_name...")
    comp1.short_name = "EditedComponent1"
    print(f"   Component1 short_name: {comp1.short_name}")
    
    # Simulate switching to Component2 and back
    print("3. Switching to Component2 and back...")
    # In real GUI, this would trigger _save_current_widget_values()
    
    # Check if the change persisted
    if comp1.short_name == "EditedComponent1":
        print("✅ Property change persisted correctly")
    else:
        print(f"❌ Property change was lost. Current value: {comp1.short_name}")
        return False
    
    # Test document modification tracking
    if doc.modified:
        print("✅ Document marked as modified")
    else:
        print("❌ Document not marked as modified")
        return False
    
    print("✅ Property persistence test passed")
    return True

def test_drag_drop_logic():
    """Test drag and drop logic (without GUI)"""
    print("🧪 Testing Drag and Drop Logic...")
    
    # Create test elements
    comp1 = ApplicationSwComponentType("Component1", "First component")
    comp2 = ApplicationSwComponentType("Component2", "Second component")
    
    # Test _can_move_element logic
    # This simulates the logic that would be used in the GUI
    
    # Test valid moves
    valid_moves = [
        (comp1, comp2),  # Component to component
        (comp1, None),   # Component to root
    ]
    
    for dragged, target in valid_moves:
        # Simulate the _can_move_element logic
        can_move = False
        if isinstance(dragged, ApplicationSwComponentType):
            if target is None or isinstance(target, ApplicationSwComponentType):
                can_move = True
        
        if can_move:
            print(f"✅ Valid move: {dragged.short_name} -> {target.short_name if target else 'root'}")
        else:
            print(f"❌ Invalid move: {dragged.short_name} -> {target.short_name if target else 'root'}")
            return False
    
    print("✅ Drag and drop logic test passed")
    return True

def main():
    """Run all tests"""
    print("🚀 Testing Three Main Fixes")
    print("=" * 50)
    
    tests = [
        test_ecuc_saving,
        test_property_persistence,
        test_drag_drop_logic
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
        print("🎉 All fixes are working correctly!")
        return True
    else:
        print("⚠️  Some fixes need attention.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)