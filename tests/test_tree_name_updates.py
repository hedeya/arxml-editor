#!/usr/bin/env python3
"""
Test real-time tree name updates when editing properties
"""

import sys
from PyQt6.QtWidgets import QApplication
from src.ui.views.tree_navigator import TreeNavigator
from src.ui.views.property_editor import PropertyEditor
from src.core.application import ARXMLEditorApp

def test_tree_name_updates():
    """Test that tree names update when properties change"""
    print("=" * 80)
    print("TREE NAME UPDATE TEST")
    print("=" * 80)
    
    # Create Qt application
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Create ARXML app and components
    arxml_app = ARXMLEditorApp()
    tree_navigator = TreeNavigator(arxml_app)
    property_editor = PropertyEditor(arxml_app)
    
    # Connect signals like MainWindow does
    tree_navigator.element_selected.connect(property_editor.set_element)
    
    # Connect property changes to tree updates (like main window)
    def on_property_changed(element, property_name, new_value):
        print(f"✓ Property changed: {property_name}='{new_value}' on element id={id(element)}")
        if property_name == 'short_name':
            result = tree_navigator.update_element_name_in_tree(element, new_value)
            if result:
                print(f"✅ Tree updated successfully with new name: '{new_value}'")
            else:
                print(f"❌ Failed to update tree with new name: '{new_value}'")
    
    property_editor.property_changed.connect(on_property_changed)
    
    # Load document
    try:
        ecuc_file = "Backup/ECUC/FCA_mPAD_Safety_Can_Can_ecuc.arxml"
        print(f"Loading: {ecuc_file}")
        arxml_app.load_document(ecuc_file)
        tree_navigator.refresh()
        
        if not arxml_app.current_document or not arxml_app.current_document.ecuc_elements:
            print("❌ No ECUC elements found")
            return False
            
        # Get first element for testing
        element = arxml_app.current_document.ecuc_elements[0]
        original_name = element.get('short_name')
        print(f"Original element name: '{original_name}'")
        
        # Select the element (like clicking in tree)
        tree_navigator.element_selected.emit(element)
        
        # Find the tree item
        tree_item = tree_navigator.find_tree_item_by_element(element)
        if tree_item:
            print(f"✓ Found tree item for element: '{tree_item.text(0)}'")
        else:
            print("❌ Could not find tree item for element")
            return False
        
        print(f"\n" + "="*50)
        print("TESTING REAL-TIME NAME UPDATE")
        print("="*50)
        
        # Test 1: Update name through property editor
        if 'short_name' in property_editor._property_widgets:
            widget = property_editor._property_widgets['short_name']
            new_name = original_name + "_UPDATED"
            
            print(f"Changing name from '{original_name}' to '{new_name}'")
            widget.setText(new_name)
            
            # Check if tree item was updated
            tree_text = tree_item.text(0)
            if tree_text == new_name:
                print(f"✅ SUCCESS: Tree shows updated name '{tree_text}'")
                return True
            else:
                print(f"❌ FAILURE: Tree still shows '{tree_text}', expected '{new_name}'")
                return False
        else:
            print("❌ No short_name widget found in property editor")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = test_tree_name_updates()
    if result:
        print("\n🎉 Tree name update functionality works correctly!")
    else:
        print("\n💡 Tree name update needs debugging.")
        print("Check that:")
        print("- Property editor emits property_changed signal")
        print("- Main window connects this signal to tree updates")
        print("- Tree navigator can find items by element identity")