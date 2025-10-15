"""
Main Window
Main application window with menu, toolbar, and view management
"""

from PyQt6.QtWidgets import (
    QMainWindow, QMenuBar, QToolBar, QStatusBar, QSplitter,
    QVBoxLayout, QHBoxLayout, QWidget, QMessageBox,
    QFileDialog, QApplication, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeySequence, QIcon, QAction
from .views.tree_navigator import TreeNavigator
from .views.property_editor import PropertyEditor
from .views.validation_list import ValidationList
from .views.diagram_view import DiagramView
from ..core.application import ARXMLEditorApp

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.app = ARXMLEditorApp()
        self._setup_ui()
        self._connect_signals()
        self._setup_shortcuts()
    
    def _setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("ARXML Editor - Professional AUTOSAR XML Editor")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create central widget and splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create main splitter
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # Left panel (Tree Navigator)
        left_panel = QWidget()
        left_panel.setMinimumWidth(300)
        left_panel.setMaximumWidth(400)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        self.tree_navigator = TreeNavigator(self.app)
        left_layout.addWidget(self.tree_navigator)
        
        # Right panel with tabs
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Property Editor tab
        self.property_editor = PropertyEditor(self.app)
        self.tab_widget.addTab(self.property_editor, "Properties")
        
        # Validation List tab
        self.validation_list = ValidationList(self.app)
        self.tab_widget.addTab(self.validation_list, "Validation")
        
        # Diagram View tab
        self.diagram_view = DiagramView(self.app)
        self.tab_widget.addTab(self.diagram_view, "Diagram")
        
        right_layout.addWidget(self.tab_widget)
        
        # Add panels to main splitter
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(right_panel)
        
        # Set main splitter proportions
        main_splitter.setSizes([300, 1100])
        
        # Create menu bar
        self._create_menu_bar()
        
        # Create toolbar
        self._create_toolbar()
        
        # Create status bar
        self._create_status_bar()
    
    def _create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        # New
        new_action = QAction("&New", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.setStatusTip("Create a new ARXML document")
        new_action.triggered.connect(self._new_document)
        file_menu.addAction(new_action)
        
        # Open
        open_action = QAction("&Open...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.setStatusTip("Open an ARXML document")
        open_action.triggered.connect(self._open_document)
        file_menu.addAction(open_action)
        
        # Save
        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.setStatusTip("Save the current document")
        save_action.triggered.connect(self._save_document)
        file_menu.addAction(save_action)
        
        # Save As
        save_as_action = QAction("Save &As...", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.setStatusTip("Save the current document with a new name")
        save_as_action.triggered.connect(self._save_as_document)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Exit
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        # Undo
        undo_action = QAction("&Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.setStatusTip("Undo the last action")
        undo_action.triggered.connect(self._undo)
        edit_menu.addAction(undo_action)
        
        # Redo
        redo_action = QAction("&Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.setStatusTip("Redo the last undone action")
        redo_action.triggered.connect(self._redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        # Delete
        delete_action = QAction("&Delete", self)
        delete_action.setShortcut(QKeySequence.StandardKey.Delete)
        delete_action.setStatusTip("Delete selected element")
        delete_action.triggered.connect(self._delete_selected)
        edit_menu.addAction(delete_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        # Schema Version
        schema_menu = view_menu.addMenu("&Schema Version")
        for version in self.app.get_available_schema_versions():
            action = QAction(f"AUTOSAR {version}", self)
            action.setCheckable(True)
            action.setChecked(version == "4.7.0")  # Default version
            action.triggered.connect(lambda checked, v=version: self._set_schema_version(v))
            schema_menu.addAction(action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        # About
        about_action = QAction("&About", self)
        about_action.setStatusTip("About ARXML Editor")
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _create_toolbar(self):
        """Create toolbar"""
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        
        # New
        new_action = QAction("New", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self._new_document)
        toolbar.addAction(new_action)
        
        # Open
        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self._open_document)
        toolbar.addAction(open_action)
        
        # Save
        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self._save_document)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # Undo
        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self._undo)
        toolbar.addAction(undo_action)
        
        # Redo
        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self._redo)
        toolbar.addAction(redo_action)
    
    def _create_status_bar(self):
        """Create status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def _connect_signals(self):
        """Connect signals"""
        self.app.document_changed.connect(self._on_document_changed)
        self.app.validation_changed.connect(self._on_validation_changed)
        self.app.command_stack_changed.connect(self._on_command_stack_changed)
        
        # Connect tree navigator to property editor
        self.tree_navigator.element_selected.connect(self.property_editor.set_element)
    
    def _setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Additional shortcuts can be added here
        pass
    
    def _new_document(self):
        """Create new document"""
        self.app.new_document()
        self.status_bar.showMessage("New document created")
    
    def _open_document(self):
        """Open document"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open ARXML Document", "", "ARXML Files (*.arxml);;All Files (*)"
        )
        if file_path:
            if self.app.load_document(file_path):
                self.status_bar.showMessage(f"Opened: {file_path}")
            else:
                QMessageBox.critical(self, "Error", "Failed to open document")
    
    def _save_document(self):
        """Save document"""
        if self.app.current_document:
            if self.app.current_document.file_path:
                if self.app.save_document():
                    self.status_bar.showMessage("Document saved")
                else:
                    QMessageBox.critical(self, "Error", "Failed to save document")
            else:
                self._save_as_document()
        else:
            QMessageBox.information(self, "Info", "No document to save")
    
    def _save_as_document(self):
        """Save document as"""
        if self.app.current_document:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save ARXML Document", "", "ARXML Files (*.arxml);;All Files (*)"
            )
            if file_path:
                if self.app.save_document(file_path):
                    self.status_bar.showMessage(f"Saved as: {file_path}")
                else:
                    QMessageBox.critical(self, "Error", "Failed to save document")
        else:
            QMessageBox.information(self, "Info", "No document to save")
    
    def _undo(self):
        """Undo last action"""
        result = self.app.command_service.undo()
        if result.success:
            self.status_bar.showMessage("Action undone")
        else:
            self.status_bar.showMessage("Nothing to undo")
    
    def _redo(self):
        """Redo last undone action"""
        result = self.app.command_service.redo()
        if result.success:
            self.status_bar.showMessage("Action redone")
        else:
            self.status_bar.showMessage("Nothing to redo")
    
    def _delete_selected(self):
        """Delete selected element"""
        current_item = self.tree_navigator.currentItem()
        if current_item:
            element = current_item.data(0, Qt.ItemDataRole.UserRole + 1)
            if element:
                self.tree_navigator._delete_element(element)
    
    def _set_schema_version(self, version: str):
        """Set AUTOSAR schema version"""
        if self.app.set_schema_version(version):
            self.status_bar.showMessage(f"Schema version set to: {version}")
        else:
            QMessageBox.critical(self, "Error", f"Failed to set schema version: {version}")
    
    def _show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About ARXML Editor",
                         "ARXML Editor v1.0.0\n\n"
                         "Professional Desktop AUTOSAR XML Editor\n\n"
                         "Features:\n"
                         "• MVVM Architecture\n"
                         "• ARXML Parser & Serializer\n"
                         "• Real-time Validation\n"
                         "• Undo/Redo Support\n"
                         "• Multiple AUTOSAR Versions")
    
    def _on_document_changed(self):
        """Handle document changed signal"""
        # Update UI components
        self.tree_navigator.refresh()
        self.property_editor.clear()
        
        # Trigger validation for the new document
        if self.app.current_document:
            self.app.validation_service.validate_document(self.app.current_document)
        
        self.validation_list.refresh()
    
    def _on_validation_changed(self):
        """Handle validation changed signal"""
        self.validation_list.refresh()
        error_count = self.app.validation_service.error_count
        warning_count = self.app.validation_service.warning_count
        
        if error_count > 0 or warning_count > 0:
            self.status_bar.showMessage(f"Validation: {error_count} errors, {warning_count} warnings")
        else:
            self.status_bar.showMessage("Validation: No issues")
    
    def _on_command_stack_changed(self):
        """Handle command stack changed signal"""
        # Update undo/redo button states
        pass
    
    def closeEvent(self, event):
        """Handle close event"""
        # Add save confirmation if needed
        event.accept()