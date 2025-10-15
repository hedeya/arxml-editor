#!/usr/bin/env python3
"""
Debug test to reproduce the exact GUI issue

This test will help us understand why property changes
are not persisting when switching between nodes.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_debug_gui_issue():
    """Test to debug the GUI issue"""
    print("🧪 Debugging GUI Issue...")
    
    # Import the application
    from src.core.application import ARXMLEditorApp
    from src.ui.main_window import MainWindow
    from PyQt6.QtWidgets import QApplication
    
    # Create application
    app = QApplication([])
    main_window = MainWindow()
    
    # Load an ECUC file
    ecuc_file = "../Backup/ECUC/FCA_mPAD_Safety_EcuC_EcuC_ecuc.arxml"
    if not os.path.exists(ecuc_file):
        print(f"❌ ECUC file not found: {ecuc_file}")
        return False
    
    success = main_window.app.load_document(ecuc_file)
    if not success:
        print("❌ Failed to load ECUC file")
        return False
    
    print("✅ ECUC file loaded successfully")
    
    # Get the document
    doc = main_window.app.current_document
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
    
    # Test the property editor directly
    property_editor = main_window.property_editor
    
    print("\n🔄 Test 1: Set Container 1")
    property_editor.set_element(container1)
    print(f"Current element after set: {property_editor._current_element}")
    print(f"Property widgets: {list(property_editor._property_widgets.keys())}")
    
    if "short_name" in property_editor._property_widgets:
        short_name_widget = property_editor._property_widgets["short_name"]
        print(f"Short name widget text: '{short_name_widget.text()}'")
        
        # Simulate typing
        print("\n🔄 Test 2: Simulate typing in widget")
        new_text = short_name_widget.text() + "-DebugTest"
        short_name_widget.setText(new_text)
        print(f"Widget text after setText: '{short_name_widget.text()}'")
        print(f"Data model short_name: '{property_editor._current_element.get('short_name', '')}'")
        
        # Check if the data model was updated
        if property_editor._current_element.get('short_name') == new_text:
            print("✅ Data model updated correctly")
        else:
            print(f"❌ Data model not updated! Expected: '{new_text}', Got: '{property_editor._current_element.get('short_name', '')}'")
    
    print("\n🔄 Test 3: Switch to Container 2")
    property_editor.set_element(container2)
    print(f"Current element after switch: {property_editor._current_element}")
    
    print("\n🔄 Test 4: Switch back to Container 1")
    property_editor.set_element(container1)
    print(f"Current element after switch back: {property_editor._current_element}")
    print(f"Data model short_name: '{property_editor._current_element.get('short_name', '')}'")
    
    if "short_name" in property_editor._property_widgets:
        widget_text = property_editor._property_widgets["short_name"].text()
        print(f"Widget text: '{widget_text}'")
        
        if widget_text == property_editor._current_element.get('short_name', ''):
            print("✅ Widget and data model are in sync")
        else:
            print(f"❌ Widget and data model are out of sync!")
            print(f"  Widget: '{widget_text}'")
            print(f"  Data model: '{property_editor._current_element.get('short_name', '')}'")
    
    return True

def main():
    """Run the debug test"""
    print("🚀 Debugging GUI Issue")
    print("=" * 50)
    
    try:
        if test_debug_gui_issue():
            print("✅ Debug test completed")
        else:
            print("❌ Debug test failed")
    except Exception as e:
        print(f"❌ Debug test failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()