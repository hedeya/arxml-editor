#!/usr/bin/env python3
"""
Test script for the enhanced ARXML Editor UI features:
- Adjustable splitters with persistence
- Automatic synchronization between tree and properties panels
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from factory import ARXMLEditorFactory

def test_enhanced_ui():
    """Test the enhanced UI features"""
    
    # Create application
    app_qt = QApplication(sys.argv)
    app_qt.setApplicationName("ARXML Editor Enhanced UI Test")
    
    # Create main window using factory
    main_window = ARXMLEditorFactory.create_main_window()
    app = main_window.app
    
    main_window.show()
    
    # Test auto-loading a sample ARXML file after a short delay
    def auto_load_sample():
        sample_files = ['sample.arxml', 'haytham.arxml', 'master.arxml']
        for sample_file in sample_files:
            if os.path.exists(sample_file):
                print(f"Auto-loading sample file: {sample_file}")
                if app.load_document(sample_file):
                    main_window.status_bar.showMessage(f"Auto-loaded: {sample_file}")
                    break
    
    # Schedule auto-load after 2 seconds
    QTimer.singleShot(2000, auto_load_sample)
    
    # Show information about enhanced features
    def show_features_info():
        info_text = """
Enhanced ARXML Editor UI Features:

✓ Adjustable Splitters:
  - Horizontal splitter between Tree Navigator and Properties/Diagram panels
  - Vertical splitter in right panel between tabs and validation list
  - Splitter positions automatically saved and restored between sessions
  - Minimum panel sizes prevent UI collapse

✓ Automatic Synchronization:
  - Tree selection automatically updates Properties panel
  - Properties tab automatically activated when element selected
  - Property changes automatically refresh tree display
  - Status bar shows current selection and modifications

✓ Enhanced Layout:
  - Professional splitter handles with proper width
  - Flexible panel sizing with size policies
  - Collapsible panels disabled to maintain UI stability
  - Settings persistence for window geometry and splitter states

To test these features:
1. Resize panels by dragging splitter handles
2. Select different elements in the tree navigator
3. Modify properties and observe tree updates
4. Restart application to see saved layout restored
        """
        
        QMessageBox.information(main_window, "Enhanced UI Features", info_text)
    
    # Show features info after 3 seconds
    QTimer.singleShot(3000, show_features_info)
    
    # Run the application
    return app_qt.exec()

if __name__ == "__main__":
    try:
        sys.exit(test_enhanced_ui())
    except Exception as e:
        print(f"Error running enhanced UI test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)