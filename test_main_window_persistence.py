#!/usr/bin/env python3
"""
Test property persistence using the exact MainWindow setup
This mimics how the real application connects signals
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from src.ui.views.tree_navigator import TreeNavigator
from src.ui.views.property_editor import PropertyEditor
from src.core.application import ARXMLEditorApp

def test_main_window_persistence():
    """Test property persistence with MainWindow-style signal connections"""
    print("=" * 60)
    print("TESTING MAIN WINDOW PERSISTENCE")
    print("=" * 60)
    
    # Create Qt application
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Create ARXMLEditorApp (same as MainWindow)
    arxml_app = ARXMLEditorApp()
    
    # Create components (same as MainWindow)
    tree_navigator = TreeNavigator(arxml_app)
    property_editor = PropertyEditor(arxml_app)
    
    # Connect signals EXACTLY like MainWindow does
    tree_navigator.element_selected.connect(property_editor.set_element)
    
    # Load the ECUC file
    try:
        ecuc_file = "Backup/ECUC/FCA_mPAD_Safety_Can_Can_ecuc.arxml"
        print(f"Loading: {ecuc_file}")
        arxml_app.load_document(ecuc_file)
        print("✓ Document loaded successfully")
        
        # Refresh tree navigator to populate it
        tree_navigator.refresh()
        print("✓ Tree navigator refreshed")
        
        if not arxml_app.current_document or not arxml_app.current_document.ecuc_elements:
            print("❌ No ECUC elements found")
            return
            
        # Get the first ECUC element
        element1 = arxml_app.current_document.ecuc_elements[0]
        print(f"Using element: id={id(element1)} short_name='{element1.get('short_name')}'")
        
        # Create a second test element for switching
        element2 = {
            'short_name': 'TestElement',
            'type': 'ECUC-MODULE-CONFIGURATION-VALUES',
            'containers': []
        }
        arxml_app.current_document.ecuc_elements.append(element2)
        print(f"Created second element: id={id(element2)} short_name='{element2.get('short_name')}'")
        
        print("\n--- TEST 1: Simulate tree selection (like real application) ---")
        
        # Step 1: Simulate tree navigator selection (this is what happens in real app)
        print("Simulating tree selection of element1...")
        tree_navigator.element_selected.emit(element1)
        
        # Verify the property editor received the element
        if property_editor._current_element is not None:
            print(f"✓ Property editor set element: id={id(property_editor._current_element)} short_name='{property_editor._current_element.get('short_name')}'")
        else:
            print("❌ Property editor did not receive element")
            return
        
        # Step 2: Simulate editing a property
        print("Simulating property edit...")
        if 'short_name' in property_editor._property_widgets:
            widget = property_editor._property_widgets['short_name']
            original_value = widget.text()
            new_value = original_value + "_EDITED_VIA_SIGNAL"
            widget.setText(new_value)
            print(f"Changed widget from '{original_value}' to '{new_value}'")
            
            # Verify the change was applied to the element
            current_element_value = property_editor._current_element.get('short_name')
            print(f"Element value after edit: '{current_element_value}'")
        else:
            print("❌ No short_name widget found")
            return
        
        # Step 3: Simulate switching to another element (like clicking another node)
        print("\nSimulating tree selection of element2...")
        tree_navigator.element_selected.emit(element2)
        
        if property_editor._current_element is not None:
            print(f"✓ Switched to element2: id={id(property_editor._current_element)} short_name='{property_editor._current_element.get('short_name')}'")
        else:
            print("❌ Failed to switch to element2")
            return
        
        # Step 4: Switch back to element1 to test persistence
        print("\nSimulating return to element1...")
        tree_navigator.element_selected.emit(element1)
        
        if property_editor._current_element is not None:
            print(f"✓ Returned to element1: id={id(property_editor._current_element)} short_name='{property_editor._current_element.get('short_name')}'")
            
            # Check if the widget shows the edited value
            if 'short_name' in property_editor._property_widgets:
                widget = property_editor._property_widgets['short_name']
                widget_value = widget.text()
                element_value = property_editor._current_element.get('short_name')
                
                print(f"Widget value after return: '{widget_value}'")
                print(f"Element value after return: '{element_value}'")
                
                if "_EDITED_VIA_SIGNAL" in widget_value and "_EDITED_VIA_SIGNAL" in element_value:
                    print("✅ SUCCESS: Property persistence worked via signal connections!")
                else:
                    print("❌ FAILURE: Property edit was lost!")
                    print(f"Expected to contain '_EDITED_VIA_SIGNAL'")
                    print(f"Widget: '{widget_value}'")
                    print(f"Element: '{element_value}'")
            else:
                print("❌ No short_name widget found after return")
        else:
            print("❌ Failed to return to element1")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_main_window_persistence()