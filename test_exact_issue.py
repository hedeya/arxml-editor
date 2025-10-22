#!/usr/bin/env python3
"""
Simple test to reproduce the exact issue reported by the user
This test will help identify the exact failure mode
"""

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer
from src.ui.views.tree_navigator import TreeNavigator
from src.ui.views.property_editor import PropertyEditor
from src.core.application import ARXMLEditorApp

def test_exact_user_issue():
    """Test the exact issue the user reported"""
    print("=" * 60)
    print("TESTING EXACT USER ISSUE")
    print("=" * 60)
    
    # Create Qt application
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Create the components exactly like main.py would
    arxml_app = ARXMLEditorApp()
    
    # Load a document first (this is critical)
    try:
        # Load using the same path format as user would
        ecuc_file = "Backup/ECUC/FCA_mPAD_Safety_Can_Can_ecuc.arxml"
        print(f"Loading document: {ecuc_file}")
        arxml_app.load_document(ecuc_file)
        
        if not arxml_app.current_document or not arxml_app.current_document.ecuc_elements:
            print("❌ Failed to load document properly")
            return
            
        print("✓ Document loaded successfully")
        
        # Create the UI components
        tree_navigator = TreeNavigator(arxml_app)
        property_editor = PropertyEditor(arxml_app)
        
        # Connect the signal EXACTLY like MainWindow does
        tree_navigator.element_selected.connect(property_editor.set_element)
        print("✓ Signal connection established")
        
        # Populate the tree (this would happen when UI is shown)
        tree_navigator.refresh()
        print("✓ Tree populated")
        
        # Get the first element
        element = arxml_app.current_document.ecuc_elements[0]
        print(f"Working with element: id={id(element)} short_name='{element.get('short_name')}'")
        
        print("\n--- STEP 1: Simulate clicking on first tree node ---")
        # This simulates what happens when user clicks a tree node
        tree_navigator.element_selected.emit(element)
        
        # Check that property editor received it
        if property_editor._current_element is None:
            print("❌ Property editor didn't receive element")
            return
        print(f"✓ Property editor has element: id={id(property_editor._current_element)}")
        
        print("\n--- STEP 2: Simulate editing property ---")
        # Find the short_name widget and edit it
        if 'short_name' not in property_editor._property_widgets:
            print("❌ No short_name widget found")
            return
            
        widget = property_editor._property_widgets['short_name']
        original_value = widget.text()
        new_value = original_value + "_EDITED"
        
        print(f"Changing '{original_value}' to '{new_value}'")
        widget.setText(new_value)
        
        # Verify the change took effect
        current_value = property_editor._current_element.get('short_name')
        print(f"Element now has short_name: '{current_value}'")
        
        if new_value not in current_value:
            print("❌ Edit didn't take effect properly")
            return
        print("✓ Edit applied successfully")
        
        print("\n--- STEP 3: Simulate clicking another tree node ---")
        # Create a second element for testing (this simulates having multiple nodes)
        second_element = {
            'short_name': 'SecondElement',
            'type': 'ECUC-MODULE-CONFIGURATION-VALUES',
            'containers': []
        }
        arxml_app.current_document.ecuc_elements.append(second_element)
        
        # Simulate clicking the second node
        tree_navigator.element_selected.emit(second_element)
        
        # Check that we switched
        if property_editor._current_element is not second_element:
            print("❌ Didn't switch to second element")
            return
        print(f"✓ Switched to second element: id={id(property_editor._current_element)}")
        
        print("\n--- STEP 4: Simulate clicking back to first node ---")
        # This is where the issue would manifest - when returning to the first element
        tree_navigator.element_selected.emit(element)
        
        # Check that we're back to the first element
        if property_editor._current_element is not element:
            print("❌ Didn't switch back to first element")
            return
        print(f"✓ Back to first element: id={id(property_editor._current_element)}")
        
        print("\n--- STEP 5: Check if edit persisted ---")
        # Check both the widget and the element
        if 'short_name' not in property_editor._property_widgets:
            print("❌ No short_name widget found after return")
            return
            
        widget = property_editor._property_widgets['short_name']
        widget_value = widget.text()
        element_value = property_editor._current_element.get('short_name')
        
        print(f"Widget shows: '{widget_value}'")
        print(f"Element has: '{element_value}'")
        
        # The test: does the widget still show the edited value?
        if "_EDITED" in widget_value and "_EDITED" in element_value:
            print("✅ SUCCESS: Edit persisted correctly!")
            return True
        else:
            print("❌ FAILURE: Edit was lost!")
            print(f"Expected both to contain '_EDITED'")
            print(f"Widget: '{widget_value}' (contains _EDITED: {'_EDITED' in widget_value})")
            print(f"Element: '{element_value}' (contains _EDITED: {'_EDITED' in element_value})")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_exact_user_issue()
    if success:
        print("\n🎉 The issue seems to be resolved!")
        print("If you're still seeing the problem, please:")
        print("1. Make sure you're running the latest version of the code")
        print("2. Try restarting the application completely")
        print("3. Check if there are any error messages in the console")
    else:
        print("\n🔍 Issue reproduced! Let's investigate further...")