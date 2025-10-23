#!/usr/bin/env python3
"""
Simple test for exit confirmation functionality
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox
from PyQt6.QtCore import QTimer
from src.ui.main_window import MainWindow

class SimpleTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_window = MainWindow()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup simple test UI"""
        self.setWindowTitle("Simple Exit Test")
        self.setGeometry(100, 100, 500, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add the main window as a widget
        layout.addWidget(self.main_window)
        
        # Add test buttons
        test_layout = QVBoxLayout()
        
        # Load document button
        load_btn = QPushButton("1. Load Test Document")
        load_btn.clicked.connect(self.load_test_document)
        test_layout.addWidget(load_btn)
        
        # Modify document button
        modify_btn = QPushButton("2. Modify Document (Mark as Dirty)")
        modify_btn.clicked.connect(self.modify_document)
        test_layout.addWidget(modify_btn)
        
        # Test exit button
        exit_btn = QPushButton("3. Test Exit Confirmation")
        exit_btn.clicked.connect(self.test_exit)
        test_layout.addWidget(exit_btn)
        
        # Status label
        self.status_label = QLabel("Ready - Click buttons in order to test")
        test_layout.addWidget(self.status_label)
        
        layout.addLayout(test_layout)
    
    def load_test_document(self):
        """Load a test document"""
        try:
            ecuc_file = 'Backup/ECUC/FCA_mPAD_Safety_Can_Can_ecuc.arxml'
            if self.main_window.app.load_document(ecuc_file):
                self.status_label.setText(f"✅ Document loaded: {ecuc_file}")
                self.status_label.setStyleSheet("color: green;")
            else:
                self.status_label.setText("❌ Failed to load document")
                self.status_label.setStyleSheet("color: red;")
        except Exception as e:
            self.status_label.setText(f"❌ Error loading document: {e}")
            self.status_label.setStyleSheet("color: red;")
    
    def modify_document(self):
        """Modify the document to trigger dirty state"""
        try:
            if self.main_window.app.current_document:
                # Mark as modified
                self.main_window.app.current_document.set_modified(True)
                
                # Update window title to show dirty state
                self.main_window._update_title()
                
                self.status_label.setText("✅ Document marked as modified (dirty state)")
                self.status_label.setStyleSheet("color: orange;")
            else:
                self.status_label.setText("❌ No document loaded")
                self.status_label.setStyleSheet("color: red;")
        except Exception as e:
            self.status_label.setText(f"❌ Error modifying document: {e}")
            self.status_label.setStyleSheet("color: red;")
    
    def test_exit(self):
        """Test the exit confirmation"""
        self.status_label.setText("🔄 Testing exit confirmation...")
        self.status_label.setStyleSheet("color: blue;")
        
        # Simulate close event
        from PyQt6.QtGui import QCloseEvent
        event = QCloseEvent()
        self.main_window.closeEvent(event)
        
        if event.isAccepted():
            self.status_label.setText("✅ Exit was accepted (no confirmation shown or user chose to close)")
            self.status_label.setStyleSheet("color: green;")
        else:
            self.status_label.setText("✅ Exit was ignored (confirmation shown and user chose to cancel)")
            self.status_label.setStyleSheet("color: orange;")

def main():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    window = SimpleTestWindow()
    window.show()
    
    return app.exec()

if __name__ == "__main__":
    main()