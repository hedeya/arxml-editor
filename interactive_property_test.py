#!/usr/bin/env python3
"""
Interactive Property Persistence Test
This test will help you identify exactly when and how the property persistence fails
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QTextEdit
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
import subprocess
import os

class PropertyTestUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ARXML Property Persistence Test")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        
        # Left side - Controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setMaximumWidth(300)
        
        # Title
        title_label = QLabel("Property Persistence Test")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        left_layout.addWidget(title_label)
        
        # Instructions
        instructions = QLabel("""
Instructions:
1. Click 'Start Monitor' 
2. Click 'Launch ARXML Editor'
3. In the editor:
   - Load an ARXML file
   - Select an element
   - Edit a property
   - Switch to another element
   - Switch back
4. Check the log for details
        """)
        instructions.setWordWrap(True)
        left_layout.addWidget(instructions)
        
        # Buttons
        self.start_monitor_btn = QPushButton("Start Monitor")
        self.start_monitor_btn.clicked.connect(self.start_monitor)
        left_layout.addWidget(self.start_monitor_btn)
        
        self.launch_editor_btn = QPushButton("Launch ARXML Editor")
        self.launch_editor_btn.clicked.connect(self.launch_editor)
        left_layout.addWidget(self.launch_editor_btn)
        
        self.clear_log_btn = QPushButton("Clear Log")
        self.clear_log_btn.clicked.connect(self.clear_log)
        left_layout.addWidget(self.clear_log_btn)
        
        left_layout.addStretch()
        
        # Right side - Log display
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        log_label = QLabel("Property Change Log:")
        log_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        right_layout.addWidget(log_label)
        
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFont(QFont("monospace", 9))
        right_layout.addWidget(self.log_display)
        
        # Add panels to main layout
        layout.addWidget(left_panel)
        layout.addWidget(right_panel)
        
        # Monitor timer
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_log)
        
        # Log file tracking
        self.log_file = "/tmp/arxml_property_monitor.log"
        self.last_log_size = 0
        
        # Monitor process
        self.monitor_process = None
        
        self.log("Property Test UI Ready")
        self.log("Click 'Start Monitor' then 'Launch ARXML Editor'")
        self.log("=" * 50)
    
    def log(self, message):
        """Add message to log display"""
        self.log_display.append(f"[TEST] {message}")
    
    def start_monitor(self):
        """Start the property monitor"""
        try:
            # Clear previous log
            with open(self.log_file, "w") as f:
                f.write("")
            self.last_log_size = 0
            
            # Start monitor process
            monitor_script = os.path.join(os.getcwd(), "live_property_monitor.py")
            self.monitor_process = subprocess.Popen([sys.executable, monitor_script])
            
            # Start timer to check log updates
            self.monitor_timer.start(500)
            
            self.log("Property monitor started")
            self.start_monitor_btn.setText("Monitor Running")
            self.start_monitor_btn.setEnabled(False)
            
        except Exception as e:
            self.log(f"Failed to start monitor: {e}")
    
    def launch_editor(self):
        """Launch the ARXML editor"""
        try:
            main_script = os.path.join(os.getcwd(), "main.py")
            subprocess.Popen([sys.executable, main_script])
            self.log("ARXML Editor launched")
            self.log("Now perform your property editing test in the editor")
        except Exception as e:
            self.log(f"Failed to launch editor: {e}")
    
    def update_log(self):
        """Check for new log entries"""
        try:
            if os.path.exists(self.log_file):
                current_size = os.path.getsize(self.log_file)
                if current_size > self.last_log_size:
                    with open(self.log_file, "r") as f:
                        f.seek(self.last_log_size)
                        new_content = f.read()
                        if new_content.strip():
                            for line in new_content.strip().split('\n'):
                                if line.strip():
                                    self.log_display.append(line)
                        self.last_log_size = current_size
        except Exception as e:
            pass
    
    def clear_log(self):
        """Clear the log display"""
        self.log_display.clear()
        try:
            with open(self.log_file, "w") as f:
                f.write("")
            self.last_log_size = 0
        except:
            pass
        self.log("Log cleared")
    
    def closeEvent(self, event):
        """Clean up when closing"""
        if self.monitor_process:
            self.monitor_process.terminate()
        event.accept()

if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    test_ui = PropertyTestUI()
    test_ui.show()
    
    sys.exit(app.exec())