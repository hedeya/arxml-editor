#!/usr/bin/env python3
"""
Script to patch the source code to use standard library XML parser instead of lxml
This avoids compilation issues on Windows.
"""

import os
import re

def patch_file(file_path):
    """Patch a single file to use xml_compat instead of lxml"""
    if not os.path.exists(file_path):
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace lxml imports with our compatibility layer
    original_content = content
    
    # Replace from lxml import etree
    content = re.sub(
        r'from lxml import etree',
        'from src.core.services.xml_compat import etree',
        content
    )
    
    # Replace import lxml.etree as etree
    content = re.sub(
        r'import lxml\.etree as etree',
        'from src.core.services.xml_compat import etree',
        content
    )
    
    # If content changed, write it back
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Patched: {file_path}")
    else:
        print(f"No changes needed: {file_path}")

def main():
    """Patch all source files"""
    files_to_patch = [
        'src/core/models/arxml_document.py',
        'src/core/services/arxml_parser.py',
        'src/core/services/schema_service.py'
    ]
    
    for file_path in files_to_patch:
        patch_file(file_path)
    
    print("Patching complete!")

if __name__ == '__main__':
    main()