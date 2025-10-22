"""
Tkinter-based main window for ARXML Editor - Fixed Version
This version includes better error handling and debugging
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
from typing import Optional, List, Dict, Any

# Add the src directory to the path so we can import our modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..', '..')
sys.path.insert(0, project_root)

print(f"Project root: {project_root}")
print(f"Current working directory: {os.getcwd()}")

try:
    from src.core.services.arxml_parser import ARXMLParser
    from src.core.services.schema_service import SchemaService
    from src.core.services.validation_service import ValidationService
    from src.core.models.arxml_document import ARXMLDocument
    print("✓ Core modules imported successfully")
except ImportError as e:
    print(f"ERROR importing core modules: {e}")
    # Create dummy classes for testing
    class ARXMLParser:
        def parse_arxml_file(self, file_path): return None
        def extract_sw_component_types(self, root): return []
        def extract_compositions(self, root): return []
        def extract_port_interfaces(self, root): return []
    
    class SchemaService:
        def detect_schema_version(self, file_path): return None
        def validate_arxml_file(self, file_path): return True, []
        def get_schema_file(self, version): return ""
    
    class ValidationService:
        pass
    
    class ARXMLDocument:
        def __init__(self, file_path, root):
            self.file_path = file_path
            self.root = root


class TkinterMainWindow:
    """Main window class using Tkinter instead of PyQt6"""
    
    def __init__(self):
        try:
            print("Initializing Tkinter main window...")
            self.root = tk.Tk()
            self.root.title("ARXML Editor - Tkinter Version")
            self.root.geometry("1200x800")
            
            # Initialize services
            print("Initializing services...")
            self.parser = ARXMLParser()
            self.schema_service = SchemaService()
            self.validation_service = ValidationService()
            self.current_document: Optional[ARXMLDocument] = None
            
            # Create the UI
            print("Creating UI widgets...")
            self.create_widgets()
            print("✓ Tkinter main window initialized successfully")
            
        except Exception as e:
            print(f"ERROR initializing main window: {e}")
            import traceback
            traceback.print_exc()
            raise
        
    def create_widgets(self):
        """Create all UI widgets"""
        try:
            # Create main menu
            self.create_menu()
            
            # Create main frame with paned window
            main_frame = ttk.Frame(self.root)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Create paned window for resizable panels
            paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
            paned_window.pack(fill=tk.BOTH, expand=True)
            
            # Left panel - Tree navigator
            self.create_tree_panel(paned_window)
            
            # Right panel - Property editor and validation
            self.create_property_panel(paned_window)
            
            # Status bar
            self.create_status_bar()
            
            print("✓ UI widgets created successfully")
            
        except Exception as e:
            print(f"ERROR creating widgets: {e}")
            import traceback
            traceback.print_exc()
            raise
        
    def create_menu(self):
        """Create the main menu bar"""
        try:
            menubar = tk.Menu(self.root)
            self.root.config(menu=menubar)
            
            # File menu
            file_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="File", menu=file_menu)
            file_menu.add_command(label="Open ARXML...", command=self.open_file)
            file_menu.add_command(label="Save", command=self.save_file)
            file_menu.add_command(label="Save As...", command=self.save_as_file)
            file_menu.add_separator()
            file_menu.add_command(label="Exit", command=self.root.quit)
            
            # Tools menu
            tools_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Tools", menu=tools_menu)
            tools_menu.add_command(label="Validate ARXML", command=self.validate_current_file)
            tools_menu.add_command(label="Schema Information", command=self.show_schema_info)
            
            # Help menu
            help_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Help", menu=help_menu)
            help_menu.add_command(label="About", command=self.show_about)
            
        except Exception as e:
            print(f"ERROR creating menu: {e}")
            import traceback
            traceback.print_exc()
            
    def create_tree_panel(self, parent):
        """Create the tree navigation panel"""
        try:
            tree_frame = ttk.Frame(parent)
            parent.add(tree_frame, weight=1)
            
            # Tree label
            ttk.Label(tree_frame, text="ARXML Structure", font=("Arial", 12, "bold")).pack(pady=(0, 5))
            
            # Tree view
            tree_frame_inner = ttk.Frame(tree_frame)
            tree_frame_inner.pack(fill=tk.BOTH, expand=True)
            
            # Create tree with scrollbars
            self.tree = ttk.Treeview(tree_frame_inner)
            tree_scrollbar_y = ttk.Scrollbar(tree_frame_inner, orient=tk.VERTICAL, command=self.tree.yview)
            tree_scrollbar_x = ttk.Scrollbar(tree_frame_inner, orient=tk.HORIZONTAL, command=self.tree.xview)
            self.tree.configure(yscrollcommand=tree_scrollbar_y.set, xscrollcommand=tree_scrollbar_x.set)
            
            # Pack tree and scrollbars
            self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            tree_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
            tree_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
            
            # Bind tree selection
            self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
            
        except Exception as e:
            print(f"ERROR creating tree panel: {e}")
            import traceback
            traceback.print_exc()
            
    def create_property_panel(self, parent):
        """Create the property editor and validation panel"""
        try:
            prop_frame = ttk.Frame(parent)
            parent.add(prop_frame, weight=2)
            
            # Create notebook for tabs
            notebook = ttk.Notebook(prop_frame)
            notebook.pack(fill=tk.BOTH, expand=True)
            
            # Properties tab
            self.create_properties_tab(notebook)
            
            # Validation tab
            self.create_validation_tab(notebook)
            
            # Schema tab
            self.create_schema_tab(notebook)
            
        except Exception as e:
            print(f"ERROR creating property panel: {e}")
            import traceback
            traceback.print_exc()
            
    def create_properties_tab(self, notebook):
        """Create the properties tab"""
        try:
            prop_tab = ttk.Frame(notebook)
            notebook.add(prop_tab, text="Properties")
            
            # Properties label
            ttk.Label(prop_tab, text="Element Properties", font=("Arial", 12, "bold")).pack(pady=(0, 5))
            
            # Properties text area
            self.properties_text = scrolledtext.ScrolledText(prop_tab, wrap=tk.WORD, height=15)
            self.properties_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
        except Exception as e:
            print(f"ERROR creating properties tab: {e}")
            import traceback
            traceback.print_exc()
            
    def create_validation_tab(self, notebook):
        """Create the validation tab"""
        try:
            val_tab = ttk.Frame(notebook)
            notebook.add(val_tab, text="Validation")
            
            # Validation label
            ttk.Label(val_tab, text="Validation Results", font=("Arial", 12, "bold")).pack(pady=(0, 5))
            
            # Validation text area
            self.validation_text = scrolledtext.ScrolledText(val_tab, wrap=tk.WORD, height=15)
            self.validation_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Validation buttons
            val_button_frame = ttk.Frame(val_tab)
            val_button_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Button(val_button_frame, text="Validate Current File", command=self.validate_current_file).pack(side=tk.LEFT, padx=(0, 5))
            ttk.Button(val_button_frame, text="Clear Results", command=self.clear_validation).pack(side=tk.LEFT)
            
        except Exception as e:
            print(f"ERROR creating validation tab: {e}")
            import traceback
            traceback.print_exc()
            
    def create_schema_tab(self, notebook):
        """Create the schema information tab"""
        try:
            schema_tab = ttk.Frame(notebook)
            notebook.add(schema_tab, text="Schema")
            
            # Schema label
            ttk.Label(schema_tab, text="Schema Information", font=("Arial", 12, "bold")).pack(pady=(0, 5))
            
            # Schema text area
            self.schema_text = scrolledtext.ScrolledText(schema_tab, wrap=tk.WORD, height=15)
            self.schema_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Schema buttons
            schema_button_frame = ttk.Frame(schema_tab)
            schema_button_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Button(schema_button_frame, text="Detect Schema", command=self.detect_schema).pack(side=tk.LEFT, padx=(0, 5))
            ttk.Button(schema_button_frame, text="Clear Info", command=self.clear_schema).pack(side=tk.LEFT)
            
        except Exception as e:
            print(f"ERROR creating schema tab: {e}")
            import traceback
            traceback.print_exc()
            
    def create_status_bar(self):
        """Create the status bar"""
        try:
            self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
            self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
            
        except Exception as e:
            print(f"ERROR creating status bar: {e}")
            import traceback
            traceback.print_exc()
            
    def open_file(self):
        """Open an ARXML file"""
        try:
            file_path = filedialog.askopenfilename(
                title="Open ARXML File",
                filetypes=[("ARXML files", "*.arxml"), ("XML files", "*.xml"), ("All files", "*.*")]
            )
            
            if file_path:
                self.load_arxml_file(file_path)
                
        except Exception as e:
            print(f"ERROR opening file: {e}")
            messagebox.showerror("Error", f"Failed to open file: {str(e)}")
            
    def load_arxml_file(self, file_path: str):
        """Load and parse an ARXML file"""
        try:
            self.status_bar.config(text=f"Loading {os.path.basename(file_path)}...")
            self.root.update()
            
            # Parse the ARXML file
            root = self.parser.parse_arxml_file(file_path)
            if root is None:
                messagebox.showerror("Error", "Failed to parse ARXML file")
                return
                
            # Create document model
            self.current_document = ARXMLDocument(file_path, root)
            
            # Populate tree
            self.populate_tree(root)
            
            # Detect schema
            schema_version = self.schema_service.detect_schema_version(file_path)
            if schema_version:
                self.schema_text.insert(tk.END, f"Detected schema version: {schema_version}\n")
            
            self.status_bar.config(text=f"Loaded: {os.path.basename(file_path)}")
            
        except Exception as e:
            print(f"ERROR loading file: {e}")
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
            self.status_bar.config(text="Error loading file")
            
    def populate_tree(self, root):
        """Populate the tree view with ARXML structure"""
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # Add root element
            root_item = self.tree.insert("", "end", text=f"{root.tag} (root)", values=("root",))
            
            # Add children recursively
            self.add_tree_children(root_item, root)
            
            # Expand root
            self.tree.item(root_item, open=True)
            
        except Exception as e:
            print(f"ERROR populating tree: {e}")
            import traceback
            traceback.print_exc()
            
    def add_tree_children(self, parent_item, element):
        """Recursively add children to tree"""
        try:
            for child in element:
                if hasattr(child, 'tag'):  # Check if it's an Element
                    child_item = self.tree.insert(
                        parent_item, "end", 
                        text=child.tag, 
                        values=(child.tag,)
                    )
                    # Add attributes as children
                    for attr_name, attr_value in child.attrib.items():
                        self.tree.insert(
                            child_item, "end",
                            text=f"@{attr_name} = {attr_value}",
                            values=(f"@{attr_name}", attr_value)
                        )
                    # Add text content if present
                    if child.text and child.text.strip():
                        self.tree.insert(
                            child_item, "end",
                            text=f"text = {child.text.strip()}",
                            values=("text", child.text.strip())
                        )
                    # Recursively add children
                    self.add_tree_children(child_item, child)
                    
        except Exception as e:
            print(f"ERROR adding tree children: {e}")
            import traceback
            traceback.print_exc()
            
    def on_tree_select(self, event):
        """Handle tree selection"""
        try:
            selection = self.tree.selection()
            if not selection:
                return
                
            item = selection[0]
            values = self.tree.item(item, "values")
            
            if values:
                element_type = values[0]
                element_value = values[1] if len(values) > 1 else ""
                
                # Update properties
                self.properties_text.delete(1.0, tk.END)
                self.properties_text.insert(tk.END, f"Element Type: {element_type}\n")
                if element_value:
                    self.properties_text.insert(tk.END, f"Value: {element_value}\n")
                
                # Add more detailed information
                self.properties_text.insert(tk.END, f"\nFull Path: {self.get_item_path(item)}\n")
                
        except Exception as e:
            print(f"ERROR handling tree selection: {e}")
            import traceback
            traceback.print_exc()
            
    def get_item_path(self, item):
        """Get the full path of an item in the tree"""
        try:
            path_parts = []
            current = item
            
            while current:
                text = self.tree.item(current, "text")
                path_parts.insert(0, text)
                current = self.tree.parent(current)
                
            return " > ".join(path_parts)
            
        except Exception as e:
            print(f"ERROR getting item path: {e}")
            return "Unknown path"
            
    def validate_current_file(self):
        """Validate the current ARXML file"""
        try:
            if not self.current_document:
                messagebox.showwarning("Warning", "No file loaded")
                return
                
            self.status_bar.config(text="Validating...")
            self.root.update()
            
            # Validate against schema
            is_valid, errors = self.schema_service.validate_arxml_file(self.current_document.file_path)
            
            # Clear previous results
            self.validation_text.delete(1.0, tk.END)
            
            if is_valid:
                self.validation_text.insert(tk.END, "✓ ARXML file is valid\n")
                self.validation_text.insert(tk.END, "No validation errors found.\n")
            else:
                self.validation_text.insert(tk.END, "✗ ARXML file has validation errors:\n\n")
                for error in errors:
                    self.validation_text.insert(tk.END, f"• {error}\n")
                    
            self.status_bar.config(text="Validation complete")
            
        except Exception as e:
            print(f"ERROR validating file: {e}")
            messagebox.showerror("Error", f"Validation failed: {str(e)}")
            self.status_bar.config(text="Validation failed")
            
    def detect_schema(self):
        """Detect schema version of current file"""
        try:
            if not self.current_document:
                messagebox.showwarning("Warning", "No file loaded")
                return
                
            schema_version = self.schema_service.detect_schema_version(self.current_document.file_path)
            
            self.schema_text.delete(1.0, tk.END)
            if schema_version:
                self.schema_text.insert(tk.END, f"Detected schema version: {schema_version}\n")
                self.schema_text.insert(tk.END, f"Schema file: {self.schema_service.get_schema_file(schema_version)}\n")
            else:
                self.schema_text.insert(tk.END, "Could not detect schema version\n")
                
        except Exception as e:
            print(f"ERROR detecting schema: {e}")
            messagebox.showerror("Error", f"Schema detection failed: {str(e)}")
            
    def clear_validation(self):
        """Clear validation results"""
        try:
            self.validation_text.delete(1.0, tk.END)
        except Exception as e:
            print(f"ERROR clearing validation: {e}")
            
    def clear_schema(self):
        """Clear schema information"""
        try:
            self.schema_text.delete(1.0, tk.END)
        except Exception as e:
            print(f"ERROR clearing schema: {e}")
            
    def save_file(self):
        """Save current file"""
        try:
            if not self.current_document:
                messagebox.showwarning("Warning", "No file loaded")
                return
            # TODO: Implement save functionality
            messagebox.showinfo("Info", "Save functionality not yet implemented")
        except Exception as e:
            print(f"ERROR saving file: {e}")
            messagebox.showerror("Error", f"Save failed: {str(e)}")
            
    def save_as_file(self):
        """Save current file as new file"""
        try:
            if not self.current_document:
                messagebox.showwarning("Warning", "No file loaded")
                return
            # TODO: Implement save as functionality
            messagebox.showinfo("Info", "Save As functionality not yet implemented")
        except Exception as e:
            print(f"ERROR saving as file: {e}")
            messagebox.showerror("Error", f"Save As failed: {str(e)}")
            
    def show_schema_info(self):
        """Show schema information dialog"""
        try:
            if not self.current_document:
                messagebox.showwarning("Warning", "No file loaded")
                return
            self.detect_schema()
        except Exception as e:
            print(f"ERROR showing schema info: {e}")
            messagebox.showerror("Error", f"Schema info failed: {str(e)}")
            
    def show_about(self):
        """Show about dialog"""
        try:
            about_text = """ARXML Editor - Tkinter Version
            
A standalone ARXML editor built with Python and Tkinter.

Features:
• ARXML file parsing and viewing
• Schema validation
• Tree-based navigation
• Property inspection

This version uses Tkinter instead of PyQt6 for better compatibility.
            """
            messagebox.showinfo("About ARXML Editor", about_text)
        except Exception as e:
            print(f"ERROR showing about: {e}")
            messagebox.showerror("Error", f"About dialog failed: {str(e)}")
            
    def run(self):
        """Start the application"""
        try:
            print("Starting Tkinter main loop...")
            self.root.mainloop()
            print("Tkinter main loop ended")
        except Exception as e:
            print(f"ERROR in main loop: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Main entry point for Tkinter version"""
    try:
        print("=" * 50)
        print("ARXML Editor - Tkinter Version")
        print("=" * 50)
        
        app = TkinterMainWindow()
        app.run()
        
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        
        # Try to show error in a message box if possible
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showerror("Fatal Error", f"Application failed to start:\n\n{str(e)}")
        except:
            pass


if __name__ == "__main__":
    main()