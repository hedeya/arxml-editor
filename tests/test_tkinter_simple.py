#!/usr/bin/env python3
"""
Simple Tkinter test to verify basic functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

def test_tkinter():
    """Test basic Tkinter functionality"""
    try:
        print("Testing Tkinter import...")
        import tkinter
        print("✓ Tkinter import successful")
        
        print("Creating test window...")
        root = tk.Tk()
        root.title("Tkinter Test")
        root.geometry("400x300")
        
        # Add a simple label
        label = ttk.Label(root, text="Tkinter is working!", font=("Arial", 16))
        label.pack(pady=50)
        
        # Add a button
        def on_button_click():
            messagebox.showinfo("Success", "Tkinter is working correctly!")
            
        button = ttk.Button(root, text="Click Me", command=on_button_click)
        button.pack(pady=20)
        
        # Add a quit button
        quit_button = ttk.Button(root, text="Quit", command=root.quit)
        quit_button.pack(pady=10)
        
        print("✓ Test window created successfully")
        print("✓ Starting main loop...")
        
        # Start the main loop
        root.mainloop()
        
        print("✓ Test completed successfully")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("Tkinter Simple Test")
    print("=" * 50)
    
    success = test_tkinter()
    
    if success:
        print("\n✓ Tkinter test PASSED")
    else:
        print("\n✗ Tkinter test FAILED")
        
    input("\nPress Enter to exit...")