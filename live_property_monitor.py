#!/usr/bin/env python3
"""
Live Property Persistence Monitor
Run this alongside your main ARXML editor to track property changes in real-time
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
import json
from datetime import datetime

class PropertyMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ARXML Property Persistence Monitor")
        self.setGeometry(100, 100, 800, 600)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Status label
        self.status_label = QLabel("Monitoring property changes...")
        self.status_label.setStyleSheet("color: blue; font-weight: bold;")
        layout.addWidget(self.status_label)
        
        # Clear button
        self.clear_btn = QPushButton("Clear Log")
        self.clear_btn.clicked.connect(self.clear_log)
        layout.addWidget(self.clear_btn)
        
        # Log display
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        font = QFont("monospace", 9)
        self.log_display.setFont(font)
        layout.addWidget(self.log_display)
        
        self.setLayout(layout)
        
        # Timer to check for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_for_updates)
        self.timer.start(500)  # Check every 500ms
        
        # Track last modification time
        self.log_file = "/tmp/arxml_property_monitor.log"
        self.last_size = 0
        
        self.log("Property Monitor Started")
        self.log("Watching for property changes in ARXML Editor...")
        self.log("=" * 60)
    
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        formatted_message = f"[{timestamp}] {message}"
        self.log_display.append(formatted_message)
        
        # Also write to file for persistence
        try:
            with open(self.log_file, "a") as f:
                f.write(formatted_message + "\n")
        except:
            pass
    
    def check_for_updates(self):
        # This would be called by the main application
        # For now, just check if log file has new content
        try:
            if os.path.exists(self.log_file):
                current_size = os.path.getsize(self.log_file)
                if current_size > self.last_size:
                    # Read new content
                    with open(self.log_file, "r") as f:
                        f.seek(self.last_size)
                        new_content = f.read()
                        if new_content.strip():
                            lines = new_content.strip().split('\n')
                            for line in lines:
                                if line and not line.startswith('['):  # Avoid duplicating our own logs
                                    self.log_display.append(line)
                    self.last_size = current_size
        except:
            pass
    
    def clear_log(self):
        self.log_display.clear()
        self.log("Log cleared")
        self.log("=" * 60)
        
        # Clear the log file too
        try:
            with open(self.log_file, "w") as f:
                f.write("")
            self.last_size = 0
        except:
            pass

def create_monitor_hooks():
    """
    Create monitoring hooks that can be injected into property_editor.py
    """
    monitor_code = '''
# Property Monitor Injection - Add this to property_editor.py for live monitoring
import os
from datetime import datetime

def _monitor_log(message):
    """Log property changes for debugging"""
    try:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_file = "/tmp/arxml_property_monitor.log"
        with open(log_file, "a") as f:
            f.write(f"PROPERTY_MONITOR [{timestamp}] {message}\\n")
    except:
        pass

# Add these lines to key methods in PropertyEditor:

# In set_element() method, after element resolution:
_monitor_log(f"SET_ELEMENT: id={id(element)} short_name='{element.get('short_name')}' type='{element.get('type')}'")

# In _save_current_widget_values() method:
_monitor_log(f"SAVE_START: element id={id(self._current_element)} short_name='{self._current_element.get('short_name')}'")

# In _on_ecuc_property_changed():
_monitor_log(f"PROPERTY_CHANGED: '{old_value}' -> '{new_value}' on element id={id(element)} short_name='{element.get('short_name')}'")

# After saving each property:
_monitor_log(f"SAVED_PROPERTY: {property_name}='{new_value}' on element id={id(element)}")

# When recreating widgets, log the source value:
_monitor_log(f"RECREATE_WIDGET: {property_name}='{value}' from element id={id(element)}")
'''
    
    return monitor_code

if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    monitor = PropertyMonitor()
    monitor.show()
    
    print("Property Monitor launched!")
    print("To enable live monitoring, add the following hooks to property_editor.py:")
    print("=" * 70)
    print(create_monitor_hooks())
    print("=" * 70)
    
    sys.exit(app.exec())