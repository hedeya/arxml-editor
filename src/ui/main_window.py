"""
Main Window
Main application window with menu, toolbar, and view management
"""

from PyQt6.QtWidgets import (
    QMainWindow, QMenuBar, QToolBar, QStatusBar, QSplitter,
    QVBoxLayout, QHBoxLayout, QWidget, QMessageBox,
    QFileDialog, QApplication, QTabWidget, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QSettings
from PyQt6.QtGui import QKeySequence, QIcon, QAction
from .views.tree_navigator import TreeNavigator
from .views.property_editor import PropertyEditor
from .views.validation_list import ValidationList
from .views.diagram_view import DiagramView
from ..core.application import ARXMLEditorApp
from ..core.container import setup_container

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        # Setup dependency injection container
        self._container = setup_container()
        self.app = ARXMLEditorApp(self._container)
        
        # Settings for saving/restoring UI state
        self.settings = QSettings('ARXMLEditor', 'MainWindow')
        
        self._setup_ui()
        self._connect_signals()
        self._setup_shortcuts()
        self._restore_ui_state()
    
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
        
        # Create main horizontal splitter with enhanced configuration
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.setChildrenCollapsible(False)  # Prevent panels from collapsing
        self.main_splitter.setHandleWidth(4)  # Make splitter handle more visible
        main_layout.addWidget(self.main_splitter)
        
        # Left panel (Tree Navigator)
        left_panel = QWidget()
        left_panel.setMinimumWidth(250)  # Reduced minimum, more flexible
        left_panel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(5, 5, 5, 5)
        
        self.tree_navigator = TreeNavigator(self.app)
        left_layout.addWidget(self.tree_navigator)
        
        # Right panel with vertical splitter for tabs
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(5, 5, 5, 5)
        
        # Create vertical splitter for right panel tabs
        self.right_splitter = QSplitter(Qt.Orientation.Vertical)
        self.right_splitter.setChildrenCollapsible(False)
        self.right_splitter.setHandleWidth(4)
        
        # Create tab widget for upper right area
        self.tab_widget = QTabWidget()
        
        # Property Editor tab
        self.property_editor = PropertyEditor(self.app)
        self.tab_widget.addTab(self.property_editor, "Properties")
        
        # Diagram View tab
        self.diagram_view = DiagramView(self.app)
        self.tab_widget.addTab(self.diagram_view, "Diagram")
        
        # Validation List as separate panel in vertical splitter
        self.validation_list = ValidationList(self.app)
        
        # Add widgets to vertical splitter
        self.right_splitter.addWidget(self.tab_widget)
        self.right_splitter.addWidget(self.validation_list)
        
        # Set initial proportions for vertical splitter (properties larger than validation)
        self.right_splitter.setSizes([600, 200])
        
        right_layout.addWidget(self.right_splitter)
        
        # Add panels to main horizontal splitter
        self.main_splitter.addWidget(left_panel)
        self.main_splitter.addWidget(right_panel)
        
        # Set initial main splitter proportions (will be overridden by saved settings)
        self.main_splitter.setSizes([350, 1050])
        
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
        
        # Connect tree navigator to property editor with improved sync
        self.tree_navigator.element_selected.connect(self._on_element_selected)
        self.tree_navigator.element_double_clicked.connect(self._on_element_double_clicked)
        
        # Connect property editor to tree navigator for updates
        self.property_editor.property_changed.connect(self._on_property_changed)
        
        # Track splitter state changes for auto-save
        self.main_splitter.splitterMoved.connect(self._save_splitter_state)
        self.right_splitter.splitterMoved.connect(self._save_splitter_state)
    
    def _setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Additional shortcuts can be added here
        pass
    
    def _save_splitter_state(self):
        """Save splitter positions to settings"""
        self.settings.setValue('main_splitter_state', self.main_splitter.saveState())
        self.settings.setValue('right_splitter_state', self.right_splitter.saveState())
        self.settings.setValue('main_splitter_sizes', self.main_splitter.sizes())
        self.settings.setValue('right_splitter_sizes', self.right_splitter.sizes())
    
    def _restore_ui_state(self):
        """Restore UI state from settings"""
        # Restore window geometry
        geometry = self.settings.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
        
        # Restore splitter states
        main_state = self.settings.value('main_splitter_state')
        if main_state:
            self.main_splitter.restoreState(main_state)
        
        right_state = self.settings.value('right_splitter_state')
        if right_state:
            self.right_splitter.restoreState(right_state)
        
        # Restore splitter sizes as fallback
        main_sizes = self.settings.value('main_splitter_sizes')
        if main_sizes:
            try:
                sizes = [int(size) for size in main_sizes]
                self.main_splitter.setSizes(sizes)
            except (ValueError, TypeError):
                pass  # Use default sizes
        
        right_sizes = self.settings.value('right_splitter_sizes')
        if right_sizes:
            try:
                sizes = [int(size) for size in right_sizes]
                self.right_splitter.setSizes(sizes)
            except (ValueError, TypeError):
                pass  # Use default sizes
    
    def closeEvent(self, event):
        """Handle window close event to save state"""
        # Save window geometry and splitter states
        self.settings.setValue('geometry', self.saveGeometry())
        self._save_splitter_state()
        
        # Call parent close event
        super().closeEvent(event)
    
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
            print(f"Attempting to open: {file_path}")
            if self.app.load_document(file_path):
                self.status_bar.showMessage(f"Opened: {file_path}")
                print(f"Successfully opened: {file_path}")
            else:
                print(f"Failed to open: {file_path}")
                QMessageBox.critical(self, "Error", f"Failed to open document:\n{file_path}\n\nCheck the console for detailed error messages.")
    
    def _save_document(self):
        """Save document"""
        if self.app.current_document:
            if self.app.current_document.file_path:
                print(f"Attempting to save document to: {self.app.current_document.file_path}")
                if self.app.save_document():
                    self.status_bar.showMessage("Document saved")
                    print("Document saved successfully")
                    # Update window title to remove modified indicator
                    self._update_title()
                else:
                    print("Save failed")
                    QMessageBox.critical(self, "Error", "Failed to save document")
            else:
                print("No file path, using save as")
                self._save_as_document()
        else:
            print("No current document")
            QMessageBox.information(self, "Info", "No document to save")
    
    def _save_as_document(self):
        """Save document as"""
        if self.app.current_document:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save ARXML Document", "", "ARXML Files (*.arxml);;All Files (*)"
            )
            if file_path:
                print(f"Attempting to save document as: {file_path}")
                if self.app.save_document(file_path):
                    self.status_bar.showMessage(f"Saved as: {file_path}")
                    print("Document saved as successfully")
                    # Update window title to remove modified indicator
                    self._update_title()
                else:
                    print("Save as failed")
                    QMessageBox.critical(self, "Error", "Failed to save document")
        else:
            print("No current document for save as")
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
        # Remember current selection before refresh
        current_element = self.property_editor._current_element if hasattr(self.property_editor, '_current_element') else None
        
        # Update UI components
        self.tree_navigator.refresh()
        self.property_editor.clear()
        
        # Trigger validation for the new document
        if self.app.current_document:
            self.app.validation_service.validate_document(self.app.current_document)
        
        self.validation_list.refresh()
        
        # Update window title and status
        self._update_title()
        
        # Update status bar
        if self.app.current_document:
            filename = self.app.current_document.file_path.split('/')[-1] if self.app.current_document.file_path else "Untitled"
            self.status_bar.showMessage(f"Document loaded: {filename}")
        else:
            self.status_bar.showMessage("No document loaded")
    
    def _on_validation_changed(self):
        """Handle validation changed signal with enhanced feedback"""
        self.validation_list.refresh()
        error_count = self.app.validation_service.error_count
        warning_count = self.app.validation_service.warning_count
        info_count = getattr(self.app.validation_service, 'info_count', 0)
        
        # Update status bar with detailed counts
        if error_count > 0 or warning_count > 0:
            self.status_bar.showMessage(f"Validation: {error_count} errors, {warning_count} warnings, {info_count} info")
            
            # Auto-show validation panel if there are errors
            if error_count > 0:
                current_sizes = self.right_splitter.sizes()
                if len(current_sizes) == 2 and current_sizes[1] < 100:  # If validation panel is too small
                    total_height = sum(current_sizes)
                    self.right_splitter.setSizes([int(total_height * 0.7), int(total_height * 0.3)])
        else:
            self.status_bar.showMessage("Validation: No issues")
    
    def _on_command_stack_changed(self):
        """Handle command stack changed signal"""
        # Update undo/redo button states
        pass
    
    def _on_element_selected(self, element):
        """Handle element selection from tree navigator"""
        # Set element in property editor and switch to Properties tab
        self.property_editor.set_element(element)
        self.tab_widget.setCurrentWidget(self.property_editor)
        
        # Update status bar with element info
        if element:
            element_type = type(element).__name__
            element_name = getattr(element, 'short_name', 'Unnamed')
            self.status_bar.showMessage(f"Selected: {element_type} - {element_name}")
        else:
            self.status_bar.showMessage("No element selected")
    
    def _on_element_double_clicked(self, element):
        """Handle element double-click from tree navigator"""
        # Double-click behavior: focus on property editor and expand element details
        self._on_element_selected(element)
        # You could add additional behavior here like opening in a new tab or dialog
    
    def _on_property_changed(self, element, property_name, new_value):
        """Handle property changes with enhanced synchronization"""
        # Refresh tree to show updated names/properties
        self.tree_navigator.refresh()
        
        # Mark document as modified
        self.app.mark_document_modified()
        
        # Update status bar
        element_type = type(element).__name__
        element_name = getattr(element, 'short_name', 'Unnamed')
        self.status_bar.showMessage(f"Modified: {element_type}.{property_name} = {new_value}")
    
    def _update_title(self):
        """Update window title based on document state"""
        title = "ARXML Editor"
        
        if hasattr(self.app, 'current_document') and self.app.current_document:
            if self.app.current_document.file_path:
                filename = self.app.current_document.file_path.split('/')[-1]
                title = f"{filename} - ARXML Editor"
                
                # Add modified indicator
                if self.app.current_document.modified:
                    title = f"*{title}"
            else:
                title = "Untitled - ARXML Editor"
        
        self.setWindowTitle(title)
    
    def closeEvent(self, event):
        """Handle close event with save confirmation"""
        if self.app.current_document and self.app.current_document.modified:
            # Document has unsaved changes, ask user what to do
            reply = QMessageBox.question(
                self,
                "Save Changes?",
                "The document has been modified. Do you want to save your changes before closing?",
                QMessageBox.StandardButton.Save | 
                QMessageBox.StandardButton.Discard | 
                QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Save
            )
            
            if reply == QMessageBox.StandardButton.Save:
                # Try to save the document
                if self._save_document():
                    event.accept()
                else:
                    # Save failed, ask if user wants to close anyway
                    reply2 = QMessageBox.question(
                        self,
                        "Save Failed",
                        "Failed to save the document. Do you want to close without saving?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                        QMessageBox.StandardButton.No
                    )
                    if reply2 == QMessageBox.StandardButton.Yes:
                        event.accept()
                    else:
                        event.ignore()
            elif reply == QMessageBox.StandardButton.Discard:
                # User chose to discard changes
                event.accept()
            else:
                # User chose to cancel
                event.ignore()
        else:
            # No unsaved changes, close normally
            event.accept()