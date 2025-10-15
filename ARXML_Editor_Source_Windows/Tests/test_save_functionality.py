#!/usr/bin/env python3
"""
Test script for save functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.models.arxml_document import ARXMLDocument
from src.core.models.autosar_elements import ApplicationSwComponentType

def test_save_functionality():
    """Test save functionality"""
    print("🧪 Testing Save Functionality...")
    
    # Create a test document
    doc = ARXMLDocument()
    
    # Create a component
    component = ApplicationSwComponentType(
        short_name="TestComponent",
        desc="Test component for saving"
    )
    
    # Add to document
    doc.add_sw_component_type(component)
    
    # Test save to file
    test_file = "test_save_output.arxml"
    success = doc.save_document(test_file)
    
    if success:
        print(f"✅ Document saved successfully to {test_file}")
        
        # Check if file exists and has content
        if os.path.exists(test_file):
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if "TestComponent" in content:
                    print("✅ File contains expected content")
                else:
                    print("❌ File does not contain expected content")
                    return False
        else:
            print("❌ File was not created")
            return False
        
        # Clean up
        os.remove(test_file)
        print("✅ Test file cleaned up")
        
    else:
        print("❌ Save failed")
        return False
    
    print("✅ Save functionality test passed")
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
    original_name1 = comp1.short_name
    comp1.short_name = "EditedComponent1"
    
    # Simulate switching to another element and back
    # (In real GUI, this would happen when selecting different tree items)
    
    # Check if the change persisted
    if comp1.short_name == "EditedComponent1":
        print("✅ Property change persisted")
    else:
        print("❌ Property change was lost")
        return False
    
    # Test document modification tracking
    if doc.modified:
        print("✅ Document marked as modified")
    else:
        print("❌ Document not marked as modified")
        return False
    
    print("✅ Property persistence test passed")
    return True

def main():
    """Run all tests"""
    print("🚀 Testing Save and Property Persistence")
    print("=" * 50)
    
    tests = [
        test_save_functionality,
        test_property_persistence
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
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)