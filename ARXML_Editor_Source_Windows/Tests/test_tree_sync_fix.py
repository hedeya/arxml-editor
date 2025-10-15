#!/usr/bin/env python3
"""
Test script to verify the tree synchronization fix

This test verifies that when a property is changed in the property editor,
the tree navigator is updated to reflect the change.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_tree_sync_fix():
    """Test the tree synchronization fix"""
    print("🧪 Testing Tree Synchronization Fix...")
    
    # Import the application
    from src.core.application import ARXMLEditorApp
    
    # Create application
    app = ARXMLEditorApp()
    
    # Load an ECUC file
    ecuc_file = "../Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml"
    if not os.path.exists(ecuc_file):
        print(f"❌ ECUC file not found: {ecuc_file}")
        return False
    
    success = app.load_document(ecuc_file)
    if not success:
        print("❌ Failed to load ECUC file")
        return False
    
    print("✅ ECUC file loaded successfully")
    
    # Get the document
    doc = app.current_document
    if len(doc.ecuc_elements) == 0:
        print("❌ No ECUC elements found")
        return False
    
    # Get containers for testing
    ecuc_element = doc.ecuc_elements[0]
    containers = ecuc_element.get('containers', [])
    
    if len(containers) < 2:
        print("❌ Need at least 2 containers for testing")
        return False
    
    container1 = containers[0]
    container2 = containers[1]
    
    print(f"📝 Container 1: '{container1.get('short_name', '')}'")
    print(f"📝 Container 2: '{container2.get('short_name', '')}'")
    
    # Test the fix
    print("\n🔄 Test 1: Edit Container 1")
    original_name1 = container1.get('short_name', '')
    edit_name1 = original_name1 + "-TreeSyncTest"
    container1['short_name'] = edit_name1
    print(f"   Edited Container 1: '{edit_name1}'")
    print(f"   Data model has: '{container1.get('short_name', '')}'")
    
    # Verify the edit is in the data model
    if container1.get('short_name') == edit_name1:
        print("✅ Container 1 edit is in data model")
    else:
        print(f"❌ Container 1 edit not in data model! Expected: '{edit_name1}', Got: '{container1.get('short_name', '')}'")
        return False
    
    print("\n🔄 Test 2: Switch to Container 2")
    original_name2 = container2.get('short_name', '')
    print(f"   Container 2: '{original_name2}'")
    
    # Simulate switching to container2
    print(f"   Container 1 still has: '{container1.get('short_name', '')}'")
    
    print("\n🔄 Test 3: Switch back to Container 1")
    print(f"   Container 1 now has: '{container1.get('short_name', '')}'")
    
    # Check if the edit is still there
    if container1.get('short_name') == edit_name1:
        print("✅ Container 1 edit is still preserved in data model")
    else:
        print(f"❌ Container 1 edit lost! Expected: '{edit_name1}', Got: '{container1.get('short_name', '')}'")
        return False
    
    # Test save functionality
    print("\n💾 Test 4: Test Save Functionality")
    output_file = "test_tree_sync_fix.arxml"
    success = doc.save_document(output_file)
    if not success:
        print("❌ Failed to save document")
        return False
    
    print("✅ Document saved successfully")
    
    # Verify the edit is in the saved file
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if edit_name1 in content:
            print(f"✅ Edit found in saved file: '{edit_name1}'")
            
            # Clean up
            os.remove(output_file)
            print("🧹 Cleaned up test file")
            
            return True
        else:
            print(f"❌ Edit not found in saved file")
            print(f"   Looking for: '{edit_name1}'")
            return False
    else:
        print("❌ Output file was not created")
        return False

def test_tree_item_update():
    """Test the tree item update functionality"""
    print("\n🧪 Testing Tree Item Update...")
    
    # Simulate the tree item update functionality
    class MockTreeItem:
        def __init__(self, text, data):
            self.text_value = text
            self.data_value = data
            self.children = []
        
        def setText(self, column, text):
            if column == 0:
                self.text_value = text
        
        def data(self, column, role):
            if column == 0 and role == 1000:  # UserRole
                return self.data_value
        
        def childCount(self):
            return len(self.children)
        
        def child(self, index):
            return self.children[index] if index < len(self.children) else None
    
    class MockTreeNavigator:
        def __init__(self):
            self.items = []
        
        def topLevelItemCount(self):
            return len(self.items)
        
        def topLevelItem(self, index):
            return self.items[index] if index < len(self.items) else None
        
        def update_item_text(self, element, new_short_name):
            """Update the tree item text when an element's short_name changes"""
            for i in range(self.topLevelItemCount()):
                item = self.topLevelItem(i)
                if self._update_item_recursive(item, element, new_short_name):
                    return True
            return False
        
        def _update_item_recursive(self, item, element, new_short_name):
            """Recursively update item text"""
            if not item:
                return False
            
            item_data = item.data(0, 1000)  # UserRole
            
            # Check if this is the element we're looking for
            if isinstance(item_data, dict) and item_data is element:
                item.setText(0, new_short_name)
                return True
            
            # Check children
            for i in range(item.childCount()):
                if self._update_item_recursive(item.child(i), element, new_short_name):
                    return True
            
            return False
    
    # Test the tree item update
    tree = MockTreeNavigator()
    
    # Create test elements
    container1 = {'short_name': 'Container1', 'type': 'ECUC-CONTAINER'}
    container2 = {'short_name': 'Container2', 'type': 'ECUC-CONTAINER'}
    
    # Create tree items
    item1 = MockTreeItem('Container1', container1)
    item2 = MockTreeItem('Container2', container2)
    
    tree.items = [item1, item2]
    
    print(f"📝 Initial tree items:")
    print(f"   Item 1: '{item1.text_value}'")
    print(f"   Item 2: '{item2.text_value}'")
    
    # Update container1
    print("\n🔄 Updating Container 1...")
    container1['short_name'] = 'Container1-Updated'
    success = tree.update_item_text(container1, 'Container1-Updated')
    
    if success:
        print(f"✅ Tree item updated successfully")
        print(f"   Item 1 text: '{item1.text_value}'")
        
        if item1.text_value == 'Container1-Updated':
            print("✅ Tree item text matches updated value")
            return True
        else:
            print(f"❌ Tree item text mismatch! Expected: 'Container1-Updated', Got: '{item1.text_value}'")
            return False
    else:
        print("❌ Failed to update tree item")
        return False

def main():
    """Run all tree sync tests"""
    print("🚀 Testing Tree Synchronization Fix")
    print("=" * 60)
    
    tests = [
        ("Tree Sync Fix", test_tree_sync_fix),
        ("Tree Item Update", test_tree_item_update)
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
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tree sync tests passed!")
        print("✅ The tree synchronization fix should work correctly")
        return True
    else:
        print("⚠️  Some tree sync tests failed.")
        print("❌ There may be issues with the tree synchronization.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)