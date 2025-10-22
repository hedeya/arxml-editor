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
        attrib.update(extra)
        return ET.Element(tag, attrib)
    
    @staticmethod
    def SubElement(parent: ET.Element, tag: str, attrib: dict = None, **extra) -> ET.Element:
        """Create a subelement, compatible with lxml.etree.SubElement"""
        if attrib is None:
            attrib = {}
        attrib.update(extra)
        return ET.SubElement(parent, tag, attrib)
    
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
    
    Element = ElementTree.Element
    SubElement = ElementTree.SubElement
    parse = ElementTree.parse
    fromstring = ElementTree.fromstring
    tostring = ElementTree.tostring
    XMLSyntaxError = ElementTree.XMLSyntaxError

# Create the etree object that can be imported
etree = MockETree()