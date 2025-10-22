#!/usr/bin/env python3
"""
Deep debugging test to verify if element values are actually being saved and restored correctly
"""

import sys
from PyQt6.QtWidgets import QApplication
from src.ui.views.tree_navigator import TreeNavigator
from src.ui.views.property_editor import PropertyEditor
from src.core.application import ARXMLEditorApp

def test_save_restore_cycle():
    """Test the complete save and restore cycle in detail"""
    print("=" * 80)
    print("DETAILED SAVE/RESTORE CYCLE TEST")
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
    
    # Load document
    try:
        ecuc_file = "Backup/ECUC/FCA_mPAD_Safety_Can_Can_ecuc.arxml"
        print(f"Loading: {ecuc_file}")
        arxml_app.load_document(ecuc_file)
        tree_navigator.refresh()
        
        if not arxml_app.current_document or not arxml_app.current_document.ecuc_elements:
            print("❌ No ECUC elements found")
            return
            
        # Get elements for testing
        element1 = arxml_app.current_document.ecuc_elements[0]
        element2 = {
            'short_name': 'TestElement',
            'type': 'ECUC-MODULE-CONFIGURATION-VALUES',
            'containers': []
        }
        arxml_app.current_document.ecuc_elements.append(element2)
        
        print(f"Element1: id={id(element1)} short_name='{element1.get('short_name')}'")
        print(f"Element2: id={id(element2)} short_name='{element2.get('short_name')}'")
        
        print("\n" + "="*60)
        print("STEP 1: Load element1")
        print("="*60)
        
        # Step 1: Load element1
        tree_navigator.element_selected.emit(element1)
        
        # Verify initial state
        if property_editor._current_element is None:
            print("❌ Property editor didn't receive element1")
            return
            
        initial_value = element1.get('short_name')
        print(f"✓ Element1 loaded: short_name='{initial_value}'")
        
        # Check widget value
        if 'short_name' in property_editor._property_widgets:
            widget = property_editor._property_widgets['short_name']
            widget_value = widget.text()
            print(f"✓ Widget shows: '{widget_value}'")
            
            if widget_value != initial_value:
                print(f"⚠️  Widget value mismatch! Widget: '{widget_value}' vs Element: '{initial_value}'")
        else:
            print("❌ No short_name widget found")
            return
        
        print("\n" + "="*60)
        print("STEP 2: Edit element1")
        print("="*60)
        
        # Step 2: Edit the property
        new_value = initial_value + "_EDITED_DEEP_TEST"
        widget.setText(new_value)
        print(f"✓ Widget changed to: '{new_value}'")
        
        # Verify immediate change took effect
        current_element_value = property_editor._current_element.get('short_name')
        print(f"✓ Current element shows: '{current_element_value}'")
        
        # Also check the original document element
        doc_element_value = element1.get('short_name')
        print(f"✓ Document element shows: '{doc_element_value}'")
        
        print("\n" + "="*60)
        print("STEP 3: Save element1 and switch to element2")
        print("="*60)
        
        # Step 3: Switch to element2 (this should trigger save)
        print("Before switch - Element1 state:")
        print(f"  Current element: id={id(property_editor._current_element)} short_name='{property_editor._current_element.get('short_name')}'")
        print(f"  Document element1: id={id(element1)} short_name='{element1.get('short_name')}'")
        print(f"  Widget value: '{widget.text()}'")
        
        tree_navigator.element_selected.emit(element2)
        
        print("After switch - Element1 state:")
        print(f"  Document element1: id={id(element1)} short_name='{element1.get('short_name')}'")
        
        # Verify element2 is loaded
        if property_editor._current_element is not element2:
            print(f"❌ Failed to switch to element2")
            print(f"   Expected: id={id(element2)}")
            print(f"   Actual: id={id(property_editor._current_element) if property_editor._current_element else None}")
            return
        print(f"✓ Switched to element2: short_name='{property_editor._current_element.get('short_name')}'")
        
        print("\n" + "="*60)
        print("STEP 4: Switch back to element1 (restore test)")
        print("="*60)
        
        # Step 4: Switch back to element1 (this should restore the edited value)
        print("Before restore - Element1 state:")
        print(f"  Document element1: id={id(element1)} short_name='{element1.get('short_name')}'")
        
        tree_navigator.element_selected.emit(element1)
        
        print("After restore - Element1 state:")
        print(f"  Current element: id={id(property_editor._current_element)} short_name='{property_editor._current_element.get('short_name')}'")
        print(f"  Document element1: id={id(element1)} short_name='{element1.get('short_name')}'")
        
        # Check if widget shows the edited value
        if 'short_name' in property_editor._property_widgets:
            restored_widget = property_editor._property_widgets['short_name']
            restored_widget_value = restored_widget.text()
            print(f"  Restored widget value: '{restored_widget_value}'")
            
            # The critical test: does the widget show the edited value?
            if new_value in restored_widget_value:
                print("✅ SUCCESS: Edit was preserved!")
                return True
            else:
                print("❌ FAILURE: Edit was lost!")
                print(f"   Expected: '{new_value}'")
                print(f"   Actual: '{restored_widget_value}'")
                
                # Debug: Check all possible places where the value might be
                print("\n🔍 DEBUGGING: Where did the value go?")
                print(f"   Original element1 dict: {element1}")
                print(f"   Current _current_element: {property_editor._current_element}")
                print(f"   Are they the same object? {element1 is property_editor._current_element}")
                
                # Check document state
                for i, doc_elem in enumerate(arxml_app.current_document.ecuc_elements):
                    if doc_elem is element1:
                        print(f"   Document element {i}: id={id(doc_elem)} short_name='{doc_elem.get('short_name')}'")
                
                return False
        else:
            print("❌ No short_name widget found after restore")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = test_save_restore_cycle()
    if not result:
        print("\n💡 The issue is confirmed - values are not being properly saved/restored!")
        print("This suggests there's a problem in the save or restore logic.")
    else:
        print("\n🎉 Values are being saved and restored correctly!")