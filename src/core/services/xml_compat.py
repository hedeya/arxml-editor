"""
XML compatibility layer to replace lxml with standard library xml.etree.ElementTree
This avoids compilation issues on Windows by using only built-in libraries.
"""

import xml.etree.ElementTree as ET
from typing import Optional, List, Any
import io

class ElementTree:
    """Compatibility class to mimic lxml.etree interface using standard library"""
    
    @staticmethod
    def Element(tag: str, attrib: dict = None, **extra) -> ET.Element:
        """Create an element, compatible with lxml.etree.Element"""
        if attrib is None:
            attrib = {}
        elif isinstance(attrib, str):
            # Handle case where attrib is passed as a string (namespace)
            attrib = {}
        
        # Merge extra keyword arguments into attrib
        attrib.update(extra)
        
        # Handle namespace prefix in tag if needed
        if 'xmlns' in attrib:
            # For standard library, we need to handle namespaces differently
            # Create element with namespace prefix
            namespace = attrib.pop('xmlns')
            if namespace:
                # Create a qualified name with namespace
                qname = f"{{{namespace}}}{tag}"
                return ET.Element(qname, attrib)
        
        # Call ET.Element with attrib as keyword argument
        return ET.Element(tag, attrib=attrib)
    
    @staticmethod
    def SubElement(parent: ET.Element, tag: str, attrib: dict = None, **extra) -> ET.Element:
        """Create a subelement, compatible with lxml.etree.SubElement"""
        if attrib is None:
            attrib = {}
        elif isinstance(attrib, str):
            # Handle case where attrib is passed as a string (namespace)
            attrib = {}
        
        # Merge extra keyword arguments into attrib
        attrib.update(extra)
        
        # Handle namespace prefix in tag if needed
        if 'xmlns' in attrib:
            # For standard library, we need to handle namespaces differently
            # Create element with namespace prefix
            namespace = attrib.pop('xmlns')
            if namespace:
                # Create a qualified name with namespace
                qname = f"{{{namespace}}}{tag}"
                return ET.SubElement(parent, qname, attrib)
        
        # Call ET.SubElement with attrib as keyword argument
        return ET.SubElement(parent, tag, attrib=attrib)
    
    @staticmethod
    def parse(file_path: str) -> ET.ElementTree:
        """Parse XML file, compatible with lxml.etree.parse"""
        return ET.parse(file_path)
    
    @staticmethod
    def fromstring(content: bytes) -> ET.Element:
        """Parse XML from string, compatible with lxml.etree.fromstring"""
        return ET.fromstring(content)
    
    @staticmethod
    def tostring(element: ET.Element, pretty_print: bool = False, encoding: str = 'utf-8', xml_declaration: bool = False) -> bytes:
        """Convert element to string, compatible with lxml.etree.tostring"""
        # Basic implementation - doesn't support pretty_print or xml_declaration
        # but should work for basic XML generation
        xml_str = ET.tostring(element, encoding=encoding)
        if xml_declaration:
            xml_str = f'<?xml version="1.0" encoding="{encoding}"?>\n'.encode(encoding) + xml_str
        return xml_str
    
    class XMLSyntaxError(Exception):
        """Compatibility exception for XML syntax errors"""
        pass

# Create a mock etree module that mimics lxml.etree
class MockETree:
    """Mock etree module that provides lxml.etree compatibility"""
    
    @staticmethod
    def Element(tag: str, attrib: dict = None, **extra) -> ET.Element:
        """Create an element, compatible with lxml.etree.Element"""
        return ElementTree.Element(tag, attrib, **extra)
    
    @staticmethod
    def SubElement(parent: ET.Element, tag: str, attrib: dict = None, **extra) -> ET.Element:
        """Create a subelement, compatible with lxml.etree.SubElement"""
        return ElementTree.SubElement(parent, tag, attrib, **extra)
    
    @staticmethod
    def parse(file_path: str) -> ET.ElementTree:
        """Parse XML file, compatible with lxml.etree.parse"""
        return ElementTree.parse(file_path)
    
    @staticmethod
    def fromstring(content: bytes) -> ET.Element:
        """Parse XML from string, compatible with lxml.etree.fromstring"""
        return ElementTree.fromstring(content)
    
    @staticmethod
    def tostring(element: ET.Element, pretty_print: bool = False, encoding: str = 'utf-8', xml_declaration: bool = False) -> bytes:
        """Convert element to string, compatible with lxml.etree.tostring"""
        return ElementTree.tostring(element, pretty_print, encoding, xml_declaration)
    
    XMLSyntaxError = ElementTree.XMLSyntaxError

# Create the etree object that can be imported
etree = MockETree()