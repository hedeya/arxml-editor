"""
Validation List View
Shows validation errors, warnings, and info messages
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, 
    QListWidgetItem, QPushButton, QGroupBox, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QColor
from ...core.services.validation_service import ValidationSeverity

class ValidationList(QWidget):
    """Validation list widget"""
    
    # Signals
    issue_selected = pyqtSignal(object)
    
    def __init__(self, app):
        super().__init__()
        self.app = app
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Setup the validation list UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Title and controls
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("Validation")
        self.title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh)
        header_layout.addWidget(self.refresh_button)
        
        # Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_issues)
        header_layout.addWidget(self.clear_button)
        
        layout.addLayout(header_layout)
        
        # Summary
        self.summary_label = QLabel("No validation issues")
        self.summary_label.setStyleSheet("color: green; font-weight: bold;")
        layout.addWidget(self.summary_label)
        
        # Issues list
        self.issues_list = QListWidget()
        self.issues_list.setAlternatingRowColors(True)
        self.issues_list.itemClicked.connect(self._on_issue_clicked)
        layout.addWidget(self.issues_list)
    
    def _connect_signals(self):
        """Connect signals"""
        self.app.validation_changed.connect(self.refresh)
        self.app.document_changed.connect(self.refresh)
    
    def refresh(self):
        """Refresh the validation list"""
        self.issues_list.clear()
        
        if not self.app.current_document:
            self.summary_label.setText("No document loaded")
            self.summary_label.setStyleSheet("color: gray; font-weight: bold;")
            return
        
        # Get existing validation issues without running validation again
        issues = self.app.validation_service.issues
        
        # Update summary
        error_count = self.app.validation_service.error_count
        warning_count = self.app.validation_service.warning_count
        info_count = len([issue for issue in issues if issue.severity == ValidationSeverity.INFO])
        
        if error_count > 0:
            self.summary_label.setText(f"Validation: {error_count} errors, {warning_count} warnings, {info_count} info")
            self.summary_label.setStyleSheet("color: red; font-weight: bold;")
        elif warning_count > 0:
            self.summary_label.setText(f"Validation: {warning_count} warnings, {info_count} info")
            self.summary_label.setStyleSheet("color: orange; font-weight: bold;")
        elif info_count > 0:
            self.summary_label.setText(f"Validation: {info_count} info messages")
            self.summary_label.setStyleSheet("color: blue; font-weight: bold;")
        else:
            self.summary_label.setText("Validation: No issues")
            self.summary_label.setStyleSheet("color: green; font-weight: bold;")
        
        # Add issues to list
        for issue in issues:
            self._add_issue_item(issue)
    
    def _add_issue_item(self, issue):
        """Add issue item to list"""
        item = QListWidgetItem()
        
        # Set text
        issue_text = f"[{issue.severity.value.upper()}] {issue.message}"
        if issue.property_name:
            issue_text += f" (Property: {issue.property_name})"
        if issue.line_number:
            issue_text += f" (Line: {issue.line_number})"
        
        item.setText(issue_text)
        
        # Set color based on severity
        if issue.severity == ValidationSeverity.ERROR:
            item.setForeground(QColor(200, 0, 0))  # Red
        elif issue.severity == ValidationSeverity.WARNING:
            item.setForeground(QColor(200, 100, 0))  # Orange
        else:  # INFO
            item.setForeground(QColor(0, 0, 200))  # Blue
        
        # Store issue data
        item.setData(Qt.ItemDataRole.UserRole, issue)
        
        self.issues_list.addItem(item)
    
    def _get_severity_icon(self, severity: str):
        """Get icon for severity level"""
        # In a real implementation, you would load actual icons
        # For now, return None to use text-based indicators
        return None
    
    def _on_issue_clicked(self, item):
        """Handle issue item clicked"""
        issue = item.data(Qt.ItemDataRole.UserRole)
        if issue:
            self.issue_selected.emit(issue)
    
    def clear_issues(self):
        """Clear all validation issues"""
        self.app.validation_service.clear_issues()
        self.refresh()
    
    def get_issues_by_severity(self, severity: ValidationSeverity):
        """Get issues by severity level"""
        return [item.data(Qt.ItemDataRole.UserRole) for item in 
                [self.issues_list.item(i) for i in range(self.issues_list.count())]
                if item.data(Qt.ItemDataRole.UserRole).severity == severity]
    
    def get_error_count(self) -> int:
        """Get number of errors"""
        return len(self.get_issues_by_severity(ValidationSeverity.ERROR))
    
    def get_warning_count(self) -> int:
        """Get number of warnings"""
        return len(self.get_issues_by_severity(ValidationSeverity.WARNING))
    
    def get_info_count(self) -> int:
        """Get number of info messages"""
        return len(self.get_issues_by_severity(ValidationSeverity.INFO))