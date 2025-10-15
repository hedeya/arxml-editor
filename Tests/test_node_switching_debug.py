#!/usr/bin/env python3
"""
Debug test for node switching issue

This test simulates the exact scenario where edits are lost when switching between nodes.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.application import ARXMLEditorApp

def test_node_switching_debug():
    """Debug the node switching issue"""
    print("🧪 Debugging Node Switching Issue...")
    
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
    if len(doc.ecuc_elements) < 2:
        print("❌ Need at least 2 ECUC elements for testing")
        return False
    
    # Get two ECUC elements
    element1 = doc.ecuc_elements[0]
    element2 = doc.ecuc_elements[1] if len(doc.ecuc_elements) > 1 else doc.ecuc_elements[0]
    
    print(f"📝 Element 1 SHORT-NAME: '{element1.get('short_name', '')}'")
    print(f"📝 Element 2 SHORT-NAME: '{element2.get('short_name', '')}'")
    
    # Simulate editing element 1
    original_name1 = element1.get('short_name', '')
    new_name1 = original_name1 + "-NodeSwitchTest"
    element1['short_name'] = new_name1
    print(f"✏️  Edited Element 1: '{original_name1}' -> '{new_name1}'")
    
    # Simulate switching to element 2 (this should trigger _save_current_widget_values)
    print("🔄 Switching to Element 2...")
    
    # Simulate what happens in the GUI when switching nodes
    # The property editor's set_element method should be called
    from src.ui.views.property_editor import PropertyEditor
    from PyQt6.QtWidgets import QApplication
    
    # Create QApplication if it doesn't exist
    qt_app = QApplication.instance()
    if qt_app is None:
        qt_app = QApplication(sys.argv)
    
    property_editor = PropertyEditor(app)
    
    # Set element 1 first
    property_editor.set_element(element1)
    print(f"📝 Property editor set to Element 1: '{element1.get('short_name', '')}'")
    
    # Simulate editing in the GUI (modify the widget directly)
    if 'short_name' in property_editor._property_widgets:
        widget = property_editor._property_widgets['short_name']
        gui_edit_name = original_name1 + "-GUIEdit"
        widget.setText(gui_edit_name)
        print(f"✏️  GUI edit: '{gui_edit_name}'")
        
        # Now switch to element 2 (this should save the GUI edit)
        print("🔄 Switching to Element 2 (should save GUI edit)...")
        property_editor.set_element(element2)
        
        # Check if the GUI edit was saved to element 1
        if element1['short_name'] == gui_edit_name:
            print(f"✅ GUI edit was saved: '{element1['short_name']}'")
        else:
            print(f"❌ GUI edit was NOT saved. Element 1 still has: '{element1['short_name']}'")
            return False
        
        # Switch back to element 1
        print("🔄 Switching back to Element 1...")
        property_editor.set_element(element1)
        
        # Check if the widget shows the saved value
        if 'short_name' in property_editor._property_widgets:
            widget = property_editor._property_widgets['short_name']
            widget_value = widget.text()
            if widget_value == gui_edit_name:
                print(f"✅ Widget shows saved value: '{widget_value}'")
                return True
            else:
                print(f"❌ Widget shows wrong value: '{widget_value}' (expected: '{gui_edit_name}')")
                return False
        else:
            print("❌ Short name widget not found after switching back")
            return False
    else:
        print("❌ Short name widget not found")
        return False

def main():
    """Run the debug test"""
    print("🚀 Debugging Node Switching Issue")
    print("=" * 50)
    
    try:
        if test_node_switching_debug():
            print("\n🎉 Node switching debug completed successfully!")
            print("✅ The issue might be elsewhere in the GUI flow")
        else:
            print("\n❌ Node switching debug found the issue!")
            print("⚠️  The property editor is not saving widget values correctly")
    except Exception as e:
        print(f"\n❌ Debug test failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()