#!/usr/bin/env python3
"""
Test exit confirmation functionality
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import QTimer
from src.ui.main_window import MainWindow

class TestMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_window = MainWindow()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup test UI"""
        self.setWindowTitle("Exit Confirmation Test")
        self.setGeometry(100, 100, 600, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add the main window as a widget
        layout.addWidget(self.main_window)
        
        # Add test buttons
        test_layout = QVBoxLayout()
        
        # Load document button
        load_btn = QPushButton("Load Test Document")
        load_btn.clicked.connect(self.load_test_document)
        test_layout.addWidget(load_btn)
        
        # Modify document button
        modify_btn = QPushButton("Modify Document (Change Short Name)")
        modify_btn.clicked.connect(self.modify_document)
        test_layout.addWidget(modify_btn)
        
        # Save document button
        save_btn = QPushButton("Save Document")
        save_btn.clicked.connect(self.save_document)
        test_layout.addWidget(save_btn)
        
        # Test exit button
        exit_btn = QPushButton("Test Exit (Should Show Confirmation)")
        exit_btn.clicked.connect(self.test_exit)
        test_layout.addWidget(exit_btn)
        
        # Status label
        self.status_label = QLabel("Ready - Load a document to test")
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
                # Find the first ECUC element and modify its short name
                if self.main_window.app.current_document.ecuc_elements:
                    element = self.main_window.app.current_document.ecuc_elements[0]
                    original_name = element.get('short_name', 'Unknown')
                    new_name = f"{original_name}_Modified"
                    element['short_name'] = new_name
                    
                    # Mark as modified
                    self.main_window.app.current_document.set_modified(True)
                    
                    self.status_label.setText(f"✅ Document modified: '{original_name}' -> '{new_name}'")
                    self.status_label.setStyleSheet("color: orange;")
                else:
                    self.status_label.setText("❌ No ECUC elements to modify")
                    self.status_label.setStyleSheet("color: red;")
            else:
                self.status_label.setText("❌ No document loaded")
                self.status_label.setStyleSheet("color: red;")
        except Exception as e:
            self.status_label.setText(f"❌ Error modifying document: {e}")
            self.status_label.setStyleSheet("color: red;")
    
    def save_document(self):
        """Save the document"""
        try:
            if self.main_window.app.current_document:
                if self.main_window._save_document():
                    self.status_label.setText("✅ Document saved successfully")
                    self.status_label.setStyleSheet("color: green;")
                else:
                    self.status_label.setText("❌ Failed to save document")
                    self.status_label.setStyleSheet("color: red;")
            else:
                self.status_label.setText("❌ No document to save")
                self.status_label.setStyleSheet("color: red;")
        except Exception as e:
            self.status_label.setText(f"❌ Error saving document: {e}")
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
    
    window = TestMainWindow()
    window.show()
    
    return app.exec()

if __name__ == "__main__":
    main()