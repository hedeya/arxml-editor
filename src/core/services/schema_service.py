"""
Schema Service
Manages AUTOSAR schema versions and validation
"""

import os
import re
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass
from PyQt6.QtCore import QObject, pyqtSignal
import xmlschema
from src.core.services.xml_compat import etree
try:
    from ..interfaces import ISchemaService
except ImportError:
    # Fallback for cases where interfaces are not available
    class ISchemaService:
        pass

@dataclass
class SchemaVersion:
    """AUTOSAR schema version information"""
    version: str
    display_name: str
    xsd_file: str
    namespace: str
    description: str

class SchemaService(QObject):
    """Service for AUTOSAR schema management"""
    
    # Signals
    schema_version_changed = pyqtSignal(str)
    validation_schema_loaded = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        self._current_version: Optional[str] = None
        self._current_schema: Optional[xmlschema.XMLSchema] = None
        self._available_versions: List[SchemaVersion] = []
        self._detected_version: Optional[str] = None
        
        # Initialize available schema versions
        self._initialize_schema_versions()
        
        # Initialize namespace to version mapping
        self._namespace_version_map = self._initialize_namespace_mapping()
    
    def _initialize_schema_versions(self):
        """Initialize available AUTOSAR schema versions"""
        self._available_versions = [
            SchemaVersion(
                version="4.7.0",
                display_name="AUTOSAR 4.7.0",
                xsd_file="schemas/autosar_4-7-0.xsd",
                namespace="http://autosar.org/schema/r4.0",
                description="AUTOSAR Classic Platform 4.7.0"
            ),
            SchemaVersion(
                version="4.6.0",
                display_name="AUTOSAR 4.6.0",
                xsd_file="schemas/autosar_4-6-0.xsd",
                namespace="http://autosar.org/schema/r4.0",
                description="AUTOSAR Classic Platform 4.6.0"
            ),
            SchemaVersion(
                version="4.5.0",
                display_name="AUTOSAR 4.5.0",
                xsd_file="schemas/autosar_4-5-0.xsd",
                namespace="http://autosar.org/schema/r4.0",
                description="AUTOSAR Classic Platform 4.5.0"
            ),
            SchemaVersion(
                version="4.4.0",
                display_name="AUTOSAR 4.4.0",
                xsd_file="schemas/autosar_4-4-0.xsd",
                namespace="http://autosar.org/schema/r4.0",
                description="AUTOSAR Classic Platform 4.4.0"
            ),
            SchemaVersion(
                version="4.3.0",
                display_name="AUTOSAR 4.3.0",
                xsd_file="schemas/autosar_4-3-0.xsd",
                namespace="http://autosar.org/schema/r4.0",
                description="AUTOSAR Classic Platform 4.3.0"
            )
        ]
        
        # Set default version
        self._current_version = "4.7.0"
    
    def _initialize_namespace_mapping(self) -> Dict[str, str]:
        """Initialize namespace to version mapping"""
        return {
            "http://autosar.org/schema/r4.0": "4.7.0",  # Default for R4.0
            "http://autosar.org/schema/r4.1": "4.6.0",
            "http://autosar.org/schema/r4.2": "4.5.0",
            "http://autosar.org/schema/r4.3": "4.4.0",
            "http://autosar.org/schema/r4.4": "4.3.0",
        }
    
    @property
    def current_version(self) -> Optional[str]:
        """Get current schema version"""
        return self._current_version
    
    @property
    def current_schema(self) -> Optional[xmlschema.XMLSchema]:
        """Get current schema object"""
        return self._current_schema
    
    @property
    def available_versions(self) -> List[SchemaVersion]:
        """Get available schema versions"""
        return self._available_versions.copy()
    
    @property
    def detected_version(self) -> Optional[str]:
        """Get detected schema version from ARXML file"""
        return self._detected_version
    
    def get_available_versions(self) -> List[str]:
        """Get list of available version strings"""
        return [version.version for version in self._available_versions]
    
    def get_version_info(self, version: str) -> Optional[SchemaVersion]:
        """Get schema version information"""
        for schema_version in self._available_versions:
            if schema_version.version == version:
                return schema_version
        return None
    
    def set_version(self, version: str) -> bool:
        """Set the AUTOSAR schema version"""
        if version == self._current_version and self._current_schema is not None:
            return True
        
        version_info = self.get_version_info(version)
        if not version_info:
            return False
        
        try:
            # Load schema if XSD file exists
            xsd_path = os.path.abspath(version_info.xsd_file)
            if os.path.exists(xsd_path):
                self._current_schema = xmlschema.XMLSchema(xsd_path)
                self.validation_schema_loaded.emit(True)
            else:
                # Create a basic schema for validation
                self._current_schema = self._create_basic_schema(version_info)
                self.validation_schema_loaded.emit(True)
            
            self._current_version = version
            self.schema_version_changed.emit(version)
            return True
        
        except Exception as e:
            print(f"Error loading schema version {version}: {e}")
            self.validation_schema_loaded.emit(False)
            return False
    
    def _create_basic_schema(self, version_info: SchemaVersion) -> xmlschema.XMLSchema:
        """Create a basic schema for validation when XSD file is not available"""
        # This is a simplified schema for basic validation
        # In a real implementation, you would load the actual XSD files
        schema_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           targetNamespace="{version_info.namespace}"
           xmlns:ar="{version_info.namespace}"
           elementFormDefault="qualified">
  
  <xs:element name="AUTOSAR">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="AR-PACKAGES" minOccurs="0">
          <xs:complexType>
            <xs:sequence>
              <xs:element name="AR-PACKAGE" maxOccurs="unbounded">
                <xs:complexType>
                  <xs:sequence>
                    <xs:element name="SHORT-NAME" type="xs:string"/>
                    <xs:element name="ELEMENTS" minOccurs="0"/>
                  </xs:sequence>
                </xs:complexType>
              </xs:element>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
  
</xs:schema>'''
        
        return xmlschema.XMLSchema(schema_content)
    
    def validate_arxml(self, arxml_content: str) -> List[str]:
        """Validate ARXML content against current schema"""
        if not self._current_schema:
            return ["No schema loaded for validation"]
        
        try:
            # Parse ARXML content
            from src.core.services.xml_compat import etree
            root = etree.fromstring(arxml_content.encode('utf-8'))
            
            # Validate against schema
            self._current_schema.validate(root)
            return []
        
        except Exception as e:
            return [f"Validation error: {str(e)}"]
    
    def validate_arxml_file(self, file_path: str) -> List[str]:
        """Validate ARXML file against current schema"""
        if not self._current_schema:
            return ["No schema loaded for validation"]
        
        try:
            # Validate file against schema
            self._current_schema.validate(file_path)
            return []
        
        except Exception as e:
            return [f"Validation error: {str(e)}"]
    
    def get_schema_element_info(self, element_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a schema element"""
        if not self._current_schema:
            return None
        
        try:
            # Get element definition from schema
            element = self._current_schema.elements.get(element_name)
            if element:
                return {
                    'name': element_name,
                    'type': str(element.type) if hasattr(element, 'type') else 'unknown',
                    'min_occurs': getattr(element, 'min_occurs', 0),
                    'max_occurs': getattr(element, 'max_occurs', 1),
                    'description': getattr(element, 'annotation', {}).get('documentation', '')
                }
        except Exception as e:
            print(f"Error getting schema element info: {e}")
        
        return None
    
    def get_required_attributes(self, element_name: str) -> List[str]:
        """Get required attributes for an element"""
        if not self._current_schema:
            return []
        
        try:
            element = self._current_schema.elements.get(element_name)
            if element and hasattr(element, 'attributes'):
                required_attrs = []
                for attr_name, attr_def in element.attributes.items():
                    if getattr(attr_def, 'use', 'optional') == 'required':
                        required_attrs.append(attr_name)
                return required_attrs
        except Exception as e:
            print(f"Error getting required attributes: {e}")
        
        return []
    
    def get_element_children(self, element_name: str) -> List[str]:
        """Get child elements for an element"""
        if not self._current_schema:
            return []
        
        try:
            element = self._current_schema.elements.get(element_name)
            if element and hasattr(element, 'content'):
                children = []
                for child_name in element.content:
                    children.append(child_name)
                return children
        except Exception as e:
            print(f"Error getting element children: {e}")
        
        return []
    
    def detect_schema_version_from_file(self, file_path: str) -> Optional[str]:
        """Detect AUTOSAR schema version from ARXML file"""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"Error: File not found: {file_path}")
                return None
            
            # Parse the XML file
            tree = etree.parse(file_path)
            root = tree.getroot()
            
            return self._detect_schema_version_from_element(root)
        
        except etree.XMLSyntaxError as e:
            print(f"Error: Invalid XML syntax in file {file_path}: {e}")
            return None
        except PermissionError as e:
            print(f"Error: Permission denied accessing file {file_path}: {e}")
            return None
        except Exception as e:
            print(f"Error detecting schema version from file {file_path}: {e}")
            return None
    
    def detect_schema_version_from_content(self, arxml_content: str) -> Optional[str]:
        """Detect AUTOSAR schema version from ARXML content string"""
        try:
            # Check if content is empty
            if not arxml_content or not arxml_content.strip():
                print("Error: Empty ARXML content provided")
                return None
            
            # Parse the XML content
            root = etree.fromstring(arxml_content.encode('utf-8'))
            
            return self._detect_schema_version_from_element(root)
        
        except etree.XMLSyntaxError as e:
            print(f"Error: Invalid XML syntax in content: {e}")
            return None
        except UnicodeDecodeError as e:
            print(f"Error: Unable to decode content as UTF-8: {e}")
            return None
        except Exception as e:
            print(f"Error detecting schema version from content: {e}")
            return None
    
    def _detect_schema_version_from_element(self, root: etree.Element) -> Optional[str]:
        """Detect schema version from XML root element"""
        try:
            # Method 1: Check namespace URI
            namespace_uri = root.nsmap.get(None)
            if namespace_uri in self._namespace_version_map:
                detected_version = self._namespace_version_map[namespace_uri]
                self._detected_version = detected_version
                return detected_version
            
            # Method 2: Check xsi:schemaLocation attribute
            schema_location = root.get("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation")
            if schema_location:
                version = self._extract_version_from_schema_location(schema_location)
                if version:
                    self._detected_version = version
                    return version
            
            # Method 3: Check for version-specific elements or attributes
            version = self._detect_version_from_elements(root)
            if version:
                self._detected_version = version
                return version
            
            # Method 4: Check for AUTOSAR version attribute
            autosar_version = root.get("AUTOSAR-VERSION")
            if autosar_version:
                # Map AUTOSAR version to schema version
                mapped_version = self._map_autosar_version_to_schema(autosar_version)
                if mapped_version:
                    self._detected_version = mapped_version
                    return mapped_version
            
            # Default fallback
            self._detected_version = "4.7.0"
            return "4.7.0"
        
        except Exception as e:
            print(f"Error detecting schema version from element: {e}")
            return None
    
    def _extract_version_from_schema_location(self, schema_location: str) -> Optional[str]:
        """Extract version from xsi:schemaLocation attribute"""
        try:
            # Look for patterns like "AUTOSAR_4-7-0.xsd" or "AUTOSAR_4.7.0.xsd"
            patterns = [
                r'AUTOSAR_(\d+)-(\d+)-(\d+)\.xsd',
                r'AUTOSAR_(\d+)\.(\d+)\.(\d+)\.xsd',
                r'AUTOSAR_(\d+)_(\d+)_(\d+)\.xsd'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, schema_location)
                if match:
                    major, minor, patch = match.groups()
                    version = f"{major}.{minor}.{patch}"
                    return version
            
            return None
        
        except Exception as e:
            print(f"Error extracting version from schema location: {e}")
            return None
    
    def _detect_version_from_elements(self, root: etree.Element) -> Optional[str]:
        """Detect version from specific elements or attributes in the XML"""
        try:
            # Check for version-specific elements that might indicate AUTOSAR version
            # This is a heuristic approach based on known differences between versions
            
            # Check for elements that were introduced in specific versions
            if root.xpath('.//*[local-name()="SOME-V4.7-SPECIFIC-ELEMENT"]'):
                return "4.7.0"
            elif root.xpath('.//*[local-name()="SOME-V4.6-SPECIFIC-ELEMENT"]'):
                return "4.6.0"
            # Add more version-specific checks as needed
            
            return None
        
        except Exception as e:
            print(f"Error detecting version from elements: {e}")
            return None
    
    def _map_autosar_version_to_schema(self, autosar_version: str) -> Optional[str]:
        """Map AUTOSAR version string to schema version"""
        try:
            # Clean up the version string
            version = autosar_version.strip()
            
            # Direct mapping for common version formats
            version_mapping = {
                "4.7.0": "4.7.0",
                "4.6.0": "4.6.0",
                "4.5.0": "4.5.0",
                "4.4.0": "4.4.0",
                "4.3.0": "4.3.0",
            }
            
            if version in version_mapping:
                return version_mapping[version]
            
            # Try to extract version from string
            version_match = re.search(r'(\d+)\.(\d+)\.(\d+)', version)
            if version_match:
                major, minor, patch = version_match.groups()
                version_str = f"{major}.{minor}.{patch}"
                if version_str in version_mapping:
                    return version_mapping[version_str]
            
            return None
        
        except Exception as e:
            print(f"Error mapping AUTOSAR version: {e}")
            return None
    
    def auto_detect_and_set_version(self, file_path: Optional[str] = None, arxml_content: Optional[str] = None) -> bool:
        """Automatically detect and set schema version from ARXML file or content"""
        try:
            detected_version = None
            
            if file_path:
                detected_version = self.detect_schema_version_from_file(file_path)
            elif arxml_content:
                detected_version = self.detect_schema_version_from_content(arxml_content)
            
            if detected_version:
                # Set the detected version
                success = self.set_version(detected_version)
                if success:
                    print(f"Auto-detected and set schema version: {detected_version}")
                    return True
                else:
                    print(f"Failed to set detected schema version: {detected_version}")
                    return False
            else:
                print("Could not detect schema version, using default")
                return self.set_version("4.7.0")
        
        except Exception as e:
            print(f"Error in auto-detect and set version: {e}")
            return False