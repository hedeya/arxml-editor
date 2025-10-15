#!/usr/bin/env python3
"""
Test script to verify lambda behavior

This test simulates the lambda function behavior to ensure
it's updating the correct element.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_lambda_behavior():
    """Test the lambda behavior directly"""
    print("🧪 Testing Lambda Behavior...")
    
    # Create test data
    container1 = {'short_name': 'Container1', 'type': 'ECUC-CONTAINER'}
    container2 = {'short_name': 'Container2', 'type': 'ECUC-CONTAINER'}
    
    print(f"📝 Container 1: {container1}")
    print(f"📝 Container 2: {container2}")
    
    # Simulate the lambda function behavior
    def simulate_lambda(ecuc_element, property_name, new_value):
        """Simulate what the lambda function does"""
        print(f"Lambda called with:")
        print(f"  - ecuc_element: {ecuc_element}")
        print(f"  - property_name: {property_name}")
        print(f"  - new_value: '{new_value}'")
        
        # Update the element
        old_value = ecuc_element.get(property_name, '')
        ecuc_element[property_name] = new_value
        
        print(f"  - Updated {property_name}: '{old_value}' -> '{new_value}'")
        print(f"  - Element after update: {ecuc_element}")
        
        return ecuc_element
    
    # Test 1: Edit container1
    print("\n🔄 Test 1: Edit Container 1")
    result1 = simulate_lambda(container1, "short_name", "Container1-Edited")
    print(f"Container 1 after edit: {container1}")
    
    # Test 2: Edit container2
    print("\n🔄 Test 2: Edit Container 2")
    result2 = simulate_lambda(container2, "short_name", "Container2-Edited")
    print(f"Container 2 after edit: {container2}")
    
    # Test 3: Edit container1 again
    print("\n🔄 Test 3: Edit Container 1 again")
    result3 = simulate_lambda(container1, "short_name", "Container1-Edited-Again")
    print(f"Container 1 after second edit: {container1}")
    
    # Verify results
    if (container1['short_name'] == "Container1-Edited-Again" and 
        container2['short_name'] == "Container2-Edited"):
        print("✅ Lambda behavior is correct - each element is updated independently")
        return True
    else:
        print("❌ Lambda behavior is incorrect")
        print(f"  Container 1: {container1}")
        print(f"  Container 2: {container2}")
        return False

def test_widget_lifecycle():
    """Test the widget lifecycle simulation"""
    print("\n🧪 Testing Widget Lifecycle...")
    
    # Simulate the widget lifecycle
    class MockWidget:
        def __init__(self, initial_text):
            self.text_value = initial_text
        
        def text(self):
            return self.text_value
        
        def setText(self, text):
            self.text_value = text
    
    class MockPropertyEditor:
        def __init__(self):
            self._current_element = None
            self._property_widgets = {}
        
        def create_widget_for_element(self, element):
            """Simulate creating a widget for an element"""
            print(f"Creating widget for element: {element}")
            
            # Create widget
            widget = MockWidget(element.get('short_name', ''))
            
            # Create lambda that captures the element reference
            def lambda_func(text):
                print(f"Lambda called with text: '{text}'")
                print(f"  - Captured element: {element}")
                print(f"  - Current element: {self._current_element}")
                print(f"  - Are they the same? {element is self._current_element}")
                
                # Update the captured element
                element['short_name'] = text
                print(f"  - Updated element: {element}")
            
            # Store the widget
            self._property_widgets['short_name'] = widget
            
            return widget, lambda_func
        
        def set_element(self, element):
            """Simulate set_element"""
            print(f"\nset_element called with: {element}")
            print(f"Current element: {self._current_element}")
            
            # Save current widget values
            self._save_current_widget_values()
            
            # Clear widgets
            self._property_widgets.clear()
            
            # Set new element
            self._current_element = element
            
            # Create new widgets
            if element:
                widget, lambda_func = self.create_widget_for_element(element)
                self._widget_lambda = lambda_func
        
        def _save_current_widget_values(self):
            """Simulate saving widget values"""
            print("_save_current_widget_values called")
            if self._current_element and 'short_name' in self._property_widgets:
                widget = self._property_widgets['short_name']
                value = widget.text()
                print(f"  - Saving widget value: '{value}'")
                self._current_element['short_name'] = value
                print(f"  - Updated current element: {self._current_element}")
        
        def simulate_typing(self, text):
            """Simulate typing in the widget"""
            if 'short_name' in self._property_widgets:
                widget = self._property_widgets['short_name']
                widget.setText(text)
                print(f"Widget text set to: '{text}'")
                
                # Simulate the lambda being called
                if hasattr(self, '_widget_lambda'):
                    self._widget_lambda(text)
    
    # Test the lifecycle
    editor = MockPropertyEditor()
    
    # Create test elements
    container1 = {'short_name': 'Container1', 'type': 'ECUC-CONTAINER'}
    container2 = {'short_name': 'Container2', 'type': 'ECUC-CONTAINER'}
    
    print(f"📝 Container 1: {container1}")
    print(f"📝 Container 2: {container2}")
    
    # Set container1
    print("\n🔄 Setting Container 1")
    editor.set_element(container1)
    
    # Type in the widget
    print("\n🔄 Typing in Container 1 widget")
    editor.simulate_typing("Container1-Edited")
    print(f"Container 1 after typing: {container1}")
    
    # Switch to container2
    print("\n🔄 Switching to Container 2")
    editor.set_element(container2)
    
    # Type in the widget
    print("\n🔄 Typing in Container 2 widget")
    editor.simulate_typing("Container2-Edited")
    print(f"Container 2 after typing: {container2}")
    
    # Switch back to container1
    print("\n🔄 Switching back to Container 1")
    editor.set_element(container1)
    print(f"Container 1 after switch back: {container1}")
    
    # Verify results
    if (container1['short_name'] == "Container1-Edited" and 
        container2['short_name'] == "Container2-Edited"):
        print("✅ Widget lifecycle works correctly")
        return True
    else:
        print("❌ Widget lifecycle has issues")
        print(f"  Container 1: {container1}")
        print(f"  Container 2: {container2}")
        return False

def main():
    """Run all lambda behavior tests"""
    print("🚀 Testing Lambda Behavior")
    print("=" * 50)
    
    tests = [
        ("Lambda Behavior", test_lambda_behavior),
        ("Widget Lifecycle", test_widget_lifecycle)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All lambda behavior tests passed!")
        return True
    else:
        print("⚠️  Some lambda behavior tests failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)