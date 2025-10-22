#!/usr/bin/env python3
"""
Comprehensive diagnostic script to debug the actual property persistence issue
This script will patch the running application to add extensive logging
"""

import sys
import time
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer
from src.ui.main_window import MainWindow
from src.ui.views.property_editor import PropertyEditor
from src.ui.views.tree_navigator import TreeNavigator

# Global diagnostic state
diagnostics = {
    'property_editor': None,
    'tree_navigator': None,
    'last_element': None,
    'last_widget_value': None,
    'edit_history': [],
    'selection_history': []
}

def patch_property_editor(property_editor):
    """Add comprehensive logging to property editor"""
    diagnostics['property_editor'] = property_editor
    
    # Store original methods
    original_set_element = property_editor.set_element
    original_save_values = property_editor._save_current_widget_values
    original_on_change = property_editor._on_ecuc_property_changed
    
    def logged_set_element(element):
        """Logged version of set_element"""
        print(f"\n🔍 [DIAGNOSTIC] PropertyEditor.set_element called")
        print(f"   Incoming element: id={id(element)} short_name='{element.get('short_name') if isinstance(element, dict) else 'N/A'}'")
        print(f"   Current element: id={id(property_editor._current_element) if property_editor._current_element else None}")
        
        # Check if we have unsaved changes
        if hasattr(property_editor, '_property_widgets') and 'short_name' in property_editor._property_widgets:
            widget = property_editor._property_widgets['short_name']
            widget_value = widget.text()
            element_value = property_editor._current_element.get('short_name') if property_editor._current_element else 'None'
            print(f"   Current widget value: '{widget_value}'")
            print(f"   Current element value: '{element_value}'")
            if widget_value != element_value:
                print(f"   ⚠️  UNSAVED CHANGES DETECTED!")
                diagnostics['edit_history'].append({
                    'time': time.time(),
                    'action': 'unsaved_changes_detected',
                    'widget_value': widget_value,
                    'element_value': element_value,
                    'element_id': id(property_editor._current_element) if property_editor._current_element else None
                })
        
        # Record selection
        diagnostics['selection_history'].append({
            'time': time.time(),
            'element_id': id(element),
            'short_name': element.get('short_name') if isinstance(element, dict) else 'N/A'
        })
        
        # Call original method
        result = original_set_element(element)
        
        print(f"   After set_element: new current element id={id(property_editor._current_element)}")
        return result
    
    def logged_save_values():
        """Logged version of _save_current_widget_values"""
        print(f"\n💾 [DIAGNOSTIC] _save_current_widget_values called")
        if property_editor._current_element:
            print(f"   Saving for element: id={id(property_editor._current_element)} short_name='{property_editor._current_element.get('short_name')}'")
        
        if hasattr(property_editor, '_property_widgets') and 'short_name' in property_editor._property_widgets:
            widget = property_editor._property_widgets['short_name']
            widget_value = widget.text()
            print(f"   Widget value being saved: '{widget_value}'")
            diagnostics['edit_history'].append({
                'time': time.time(),
                'action': 'save_values',
                'widget_value': widget_value,
                'element_id': id(property_editor._current_element) if property_editor._current_element else None
            })
        
        return original_save_values()
    
    def logged_on_change(old_value, new_value):
        """Logged version of _on_ecuc_property_changed"""
        print(f"\n📝 [DIAGNOSTIC] _on_ecuc_property_changed called")
        print(f"   Change: '{old_value}' -> '{new_value}'")
        print(f"   Current element: id={id(property_editor._current_element)} short_name='{property_editor._current_element.get('short_name') if property_editor._current_element else 'None'}'")
        
        diagnostics['edit_history'].append({
            'time': time.time(),
            'action': 'property_changed',
            'old_value': old_value,
            'new_value': new_value,
            'element_id': id(property_editor._current_element) if property_editor._current_element else None
        })
        
        return original_on_change(old_value, new_value)
    
    # Apply patches
    property_editor.set_element = logged_set_element
    property_editor._save_current_widget_values = logged_save_values
    property_editor._on_ecuc_property_changed = logged_on_change
    
    print("✅ Property editor patched with diagnostic logging")

def patch_tree_navigator(tree_navigator):
    """Add logging to tree navigator"""
    diagnostics['tree_navigator'] = tree_navigator
    
    # Store original method
    original_on_selection = tree_navigator._on_selection_changed
    
    def logged_on_selection():
        """Logged version of _on_selection_changed"""
        print(f"\n🎯 [DIAGNOSTIC] TreeNavigator._on_selection_changed called")
        current_item = tree_navigator.currentItem()
        if current_item:
            item_data = current_item.data(0, 0x0100)  # UserRole
            item_data_alt = current_item.data(0, 0x0101)  # UserRole+1
            print(f"   Item data (UserRole): id={id(item_data) if item_data else None}")
            print(f"   Item data (UserRole+1): id={id(item_data_alt) if item_data_alt else None}")
        else:
            print("   No current item")
        
        return original_on_selection()
    
    # Apply patch
    tree_navigator._on_selection_changed = logged_on_selection
    
    print("✅ Tree navigator patched with diagnostic logging")

def show_diagnostic_report():
    """Show a comprehensive diagnostic report"""
    print("\n" + "="*80)
    print("COMPREHENSIVE DIAGNOSTIC REPORT")
    print("="*80)
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total selections: {len(diagnostics['selection_history'])}")
    print(f"   Total edit events: {len(diagnostics['edit_history'])}")
    
    print(f"\n📝 EDIT HISTORY:")
    for i, event in enumerate(diagnostics['edit_history']):
        print(f"   {i+1}. {event['action'].upper()}")
        print(f"      Time: {event['time']:.2f}")
        if 'widget_value' in event:
            print(f"      Widget value: '{event['widget_value']}'")
        if 'element_value' in event:
            print(f"      Element value: '{event['element_value']}'")
        if 'old_value' in event:
            print(f"      Change: '{event['old_value']}' -> '{event['new_value']}'")
        print(f"      Element ID: {event['element_id']}")
        print()
    
    print(f"\n🎯 SELECTION HISTORY:")
    for i, event in enumerate(diagnostics['selection_history']):
        print(f"   {i+1}. Selected: id={event['element_id']} short_name='{event['short_name']}'")
        print(f"      Time: {event['time']:.2f}")
        print()
    
    # Check for potential issues
    print(f"\n🔍 ISSUE DETECTION:")
    
    # Look for unsaved changes
    unsaved_changes = [e for e in diagnostics['edit_history'] if e['action'] == 'unsaved_changes_detected']
    if unsaved_changes:
        print(f"   ⚠️  Found {len(unsaved_changes)} instances of unsaved changes!")
        for event in unsaved_changes:
            print(f"      - Widget: '{event['widget_value']}' vs Element: '{event['element_value']}'")
    else:
        print("   ✅ No unsaved changes detected")
    
    # Look for edit/save mismatches
    changes = [e for e in diagnostics['edit_history'] if e['action'] == 'property_changed']
    saves = [e for e in diagnostics['edit_history'] if e['action'] == 'save_values']
    print(f"   📊 Property changes: {len(changes)}, Save operations: {len(saves)}")
    
    if changes and not saves:
        print("   ⚠️  Changes made but no saves detected!")
    elif len(changes) > len(saves):
        print("   ⚠️  More changes than saves - potential data loss!")
    else:
        print("   ✅ Change/save ratio looks good")

def main():
    """Main diagnostic application"""
    print("🚀 Starting ARXML Editor with comprehensive diagnostics")
    print("This will help identify the exact cause of property persistence issues")
    
    app = QApplication(sys.argv)
    
    # Create main window
    main_window = MainWindow()
    
    # Find the property editor and tree navigator
    property_editor = None
    tree_navigator = None
    
    def find_components(widget):
        nonlocal property_editor, tree_navigator
        if isinstance(widget, PropertyEditor):
            property_editor = widget
        elif isinstance(widget, TreeNavigator):
            tree_navigator = widget
        for child in widget.findChildren(object):
            find_components(child)
    
    find_components(main_window)
    
    if property_editor and tree_navigator:
        print("✅ Found PropertyEditor and TreeNavigator components")
        patch_property_editor(property_editor)
        patch_tree_navigator(tree_navigator)
    else:
        print("❌ Could not find PropertyEditor or TreeNavigator components")
        return
    
    # Set up periodic diagnostic reporting
    def periodic_report():
        if diagnostics['edit_history'] or diagnostics['selection_history']:
            show_diagnostic_report()
            # Clear history to avoid spam
            diagnostics['edit_history'].clear()
            diagnostics['selection_history'].clear()
    
    timer = QTimer()
    timer.timeout.connect(periodic_report)
    timer.start(30000)  # Report every 30 seconds
    
    # Show the window
    main_window.show()
    
    print("\n🎯 INSTRUCTIONS FOR TESTING:")
    print("1. Load an ARXML file using File -> Open")
    print("2. Click on an element in the tree to select it")
    print("3. Edit the 'short_name' property in the Properties panel")
    print("4. Click on another element in the tree")
    print("5. Click back on the original element")
    print("6. Check if your edit persisted")
    print("7. Watch the terminal output for diagnostic information!")
    
    # Run the application
    try:
        sys.exit(app.exec())
    finally:
        print("\n📋 FINAL DIAGNOSTIC REPORT:")
        show_diagnostic_report()

if __name__ == "__main__":
    main()