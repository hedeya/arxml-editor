#!/usr/bin/env python3
"""
Test the crash fixes for nested container elements
"""

import sys
from PyQt6.QtWidgets import QApplication
from src.ui.views.tree_navigator import TreeNavigator
from src.ui.views.property_editor import PropertyEditor
from src.ui.main_window import MainWindow
from src.core.application import ARXMLEditorApp

def test_nested_container_crash_fix():
    """Test that nested container editing doesn't crash"""
    print("=" * 80)
    print("NESTED CONTAINER CRASH FIX TEST")
    print("=" * 80)
    
    # Create Qt application
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        # Create main window (which creates its own ARXMLEditorApp)
        main_window = MainWindow()
        
        # Test that _update_title method exists and works
        print("✓ Testing _update_title method...")
        main_window._update_title()  # Should not crash
        print("✓ _update_title method works")
        
        # Load document to test tree functionality
        ecuc_file = "Backup/ECUC/FCA_mPAD_Safety_Can_Can_ecuc.arxml"
        print(f"Loading: {ecuc_file}")
        main_window.app.load_document(ecuc_file)
        main_window.tree_navigator.refresh()
        
        if not main_window.app.current_document or not main_window.app.current_document.ecuc_elements:
            print("❌ No ECUC elements found")
            return False
        
        # Get first element and find a nested container
        element = main_window.app.current_document.ecuc_elements[0]
        containers = element.get('containers', [])
        if not containers:
            print("❌ No containers found")
            return False
            
        nested_container = containers[0]  # Get first container (like CanGeneral)
        print(f"Testing with nested container: '{nested_container.get('short_name')}'")
        
        # Test tree item finding for nested container
        tree_item = main_window.tree_navigator.find_tree_item_by_element(nested_container)
        if tree_item:
            print(f"✅ Found tree item for nested container: '{tree_item.text(0)}'")
        else:
            print(f"⚠️  Could not find tree item for nested container (this might be expected)")
            
        # Test property change without crashing
        print("✓ Testing property change for nested container...")
        main_window._on_property_changed(nested_container, 'short_name', 'TestName')
        print("✅ Property change completed without crash")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = test_nested_container_crash_fix()
    if result:
        print("\n🎉 Crash fixes are working correctly!")
    else:
        print("\n💡 There may still be issues to address.")