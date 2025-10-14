#!/usr/bin/env python3
"""
Create distribution package for ARXML Editor
This script creates a ready-to-distribute package
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_distribution():
    """Create distribution package"""
    print("Creating ARXML Editor Distribution Package")
    print("=" * 45)
    
    # Create distribution directory
    dist_dir = Path("ARXML_Editor_Windows")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    # Copy executable if it exists
    exe_path = Path("dist/ARXML_Editor.exe")
    if exe_path.exists():
        shutil.copy2(exe_path, dist_dir / "ARXML_Editor.exe")
        print(f"✓ Copied executable: {exe_path}")
    else:
        print("⚠ Executable not found. Please build first using build_windows.bat")
        # Create a placeholder
        (dist_dir / "ARXML_Editor.exe").touch()
    
    # Copy sample files
    sample_files = [
        "sample.arxml",
        "README_Windows.md",
        "BUILD_INSTRUCTIONS.md"
    ]
    
    for file in sample_files:
        if os.path.exists(file):
            shutil.copy2(file, dist_dir / file)
            print(f"✓ Copied: {file}")
        else:
            print(f"⚠ Missing: {file}")
    
    # Copy Backup directory if it exists
    if os.path.exists("Backup"):
        shutil.copytree("Backup", dist_dir / "Backup")
        print("✓ Copied: Backup/ directory")
    
    # Copy schemas directory if it exists
    if os.path.exists("schemas"):
        shutil.copytree("schemas", dist_dir / "schemas")
        print("✓ Copied: schemas/ directory")
    
    # Create a simple launcher script for testing
    launcher_content = """@echo off
echo Starting ARXML Editor...
echo.
if exist "ARXML_Editor.exe" (
    ARXML_Editor.exe
) else (
    echo ERROR: ARXML_Editor.exe not found!
    echo Please ensure the executable is in the same directory.
    pause
)
"""
    
    with open(dist_dir / "run_editor.bat", "w") as f:
        f.write(launcher_content)
    print("✓ Created: run_editor.bat")
    
    # Create zip file
    zip_path = "ARXML_Editor_Windows.zip"
    if os.path.exists(zip_path):
        os.remove(zip_path)
    
    print(f"\nCreating zip file: {zip_path}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, dist_dir.parent)
                zipf.write(file_path, arc_path)
    
    print(f"✓ Created: {zip_path}")
    
    # Show distribution contents
    print(f"\nDistribution Package Contents:")
    print(f"Directory: {dist_dir}")
    print(f"Zip file: {zip_path}")
    print("\nFiles included:")
    for root, dirs, files in os.walk(dist_dir):
        level = root.replace(str(dist_dir), '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")
    
    print(f"\n🎉 Distribution package created successfully!")
    print(f"📦 Send '{zip_path}' to your friend")
    print(f"📁 Or send the entire '{dist_dir}' folder")
    
    return zip_path, dist_dir

if __name__ == "__main__":
    create_distribution()