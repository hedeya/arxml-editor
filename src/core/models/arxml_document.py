"""
ARXML Document Model
Represents the complete ARXML document with all AUTOSAR elements
"""

import os
from typing import List, Optional, Dict, Any
import xml.etree.ElementTree as std_etree
from src.core.services.xml_compat import etree
from PyQt6.QtCore import QObject, pyqtSignal
from .autosar_elements import (
    SwComponentType, PortPrototype, Composition, 
    ApplicationSwComponentType, AtomicSwComponentType,
    PortInterface, DataElement, ServiceInterface
)
from ..services.arxml_parser import ARXMLParser
from ..repositories import IRepositoryFactory

class ARXMLDocument(QObject):
    """Main ARXML document model with repository support"""
    
    # Signals
    element_added = pyqtSignal(object)
    element_removed = pyqtSignal(object)
    element_modified = pyqtSignal(object)
    
    def __init__(self, repository_factory: Optional[IRepositoryFactory] = None):
        super().__init__()
        self._file_path: Optional[str] = None
        self._schema_version: str = "4.7.0"
        self._root_element: Optional[etree.Element] = None
        self._parser = ARXMLParser()
        self._modified: bool = False
        
        # Repository factory for data access
        self._repository_factory = repository_factory
        self._repositories: Optional[Dict[str, Any]] = None
        
        # AUTOSAR elements (legacy collections for backward compatibility)
        self._sw_component_types: List[SwComponentType] = []
        self._compositions: List[Composition] = []
        self._port_interfaces: List[PortInterface] = []
        self._service_interfaces: List[ServiceInterface] = []
        self._ecuc_elements: List[dict] = []
        self._original_xml_elements: List[etree.Element] = []
        
        # Initialize repositories if factory provided
        if self._repository_factory:
            self._initialize_repositories()
        
        # Initialize with empty ARXML structure
        self._initialize_empty_document()
    
    @property
    def file_path(self) -> Optional[str]:
        """Get current file path"""
        return self._file_path
    
    @property
    def schema_version(self) -> str:
        """Get AUTOSAR schema version"""
        return self._schema_version
    
    @property
    def modified(self) -> bool:
        """Get modified status"""
        return self._modified
    
    def set_modified(self, modified: bool):
        """Set modified status"""
        self._modified = modified
    
    @property
    def sw_component_types(self) -> List[SwComponentType]:
        """Get all software component types"""
        return self._sw_component_types
    
    @property
    def compositions(self) -> List[Composition]:
        """Get all compositions"""
        return self._compositions
    
    @property
    def port_interfaces(self) -> List[PortInterface]:
        """Get all port interfaces"""
        return self._port_interfaces
    
    @property
    def service_interfaces(self) -> List[ServiceInterface]:
        """Get all service interfaces"""
        return self._service_interfaces
    
    # Repository-based query methods
    def get_sw_component_type_by_name(self, name: str) -> Optional[SwComponentType]:
        """Get software component type by name using repository"""
        if self._repositories and 'sw_component_types' in self._repositories:
            return self._repositories['sw_component_types'].find_by_name(name)
        # Fallback to legacy collection
        return next((comp for comp in self._sw_component_types if comp.short_name == name), None)
    
    def get_port_interface_by_name(self, name: str) -> Optional[PortInterface]:
        """Get port interface by name using repository"""
        if self._repositories and 'port_interfaces' in self._repositories:
            return self._repositories['port_interfaces'].find_by_name(name)
        # Fallback to legacy collection
        return next((iface for iface in self._port_interfaces if iface.short_name == name), None)
    
    def get_composition_by_name(self, name: str) -> Optional[Composition]:
        """Get composition by name using repository"""
        if self._repositories and 'compositions' in self._repositories:
            return self._repositories['compositions'].find_by_name(name)
        # Fallback to legacy collection
        return next((comp for comp in self._compositions if comp.short_name == name), None)
    
    def search_sw_component_types(self, pattern: str) -> List[SwComponentType]:
        """Search software component types by pattern using repository"""
        if self._repositories and 'sw_component_types' in self._repositories:
            return self._repositories['sw_component_types'].find_by_name_pattern(pattern)
        # Fallback to legacy collection
        import re
        try:
            regex = re.compile(pattern, re.IGNORECASE)
            return [comp for comp in self._sw_component_types if regex.search(comp.short_name)]
        except:
            return []
    
    def search_port_interfaces(self, pattern: str) -> List[PortInterface]:
        """Search port interfaces by pattern using repository"""
        if self._repositories and 'port_interfaces' in self._repositories:
            return self._repositories['port_interfaces'].find_by_name_pattern(pattern)
        # Fallback to legacy collection
        import re
        try:
            regex = re.compile(pattern, re.IGNORECASE)
            return [iface for iface in self._port_interfaces if regex.search(iface.short_name)]
        except:
            return []
    
    def get_repository(self, entity_type: str):
        """Get repository for specific entity type"""
        if self._repositories and entity_type in self._repositories:
            return self._repositories[entity_type]
        return None
    
    @property
    def ecuc_elements(self) -> List[dict]:
        """Get all ECUC elements"""
        return self._ecuc_elements
    
    def _initialize_repositories(self):
        """Initialize repositories for data access"""
        if not self._repository_factory:
            return
        
        self._repositories = {
            'sw_component_types': self._repository_factory.create_sw_component_type_repository(),
            'port_interfaces': self._repository_factory.create_port_interface_repository(),
            'service_interfaces': self._repository_factory.create_service_interface_repository(),
            'compositions': self._repository_factory.create_composition_repository()
        }
    
    def _initialize_empty_document(self):
        """Initialize with empty ARXML structure"""
        # Create root element with proper namespace handling
        self._root_element = etree.Element("AUTOSAR", 
            attrib={"xmlns": "http://autosar.org/schema/r4.0"})
        
        # Add schema location as attribute
        self._root_element.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", 
                              "http://autosar.org/schema/r4.0 AUTOSAR_4-7-0.xsd")
        
        # Create AR-PACKAGES element
        ar_packages = etree.SubElement(self._root_element, "AR-PACKAGES")
        ar_package = etree.SubElement(ar_packages, "AR-PACKAGE")
        etree.SubElement(ar_package, "SHORT-NAME").text = "RootPackage"
        etree.SubElement(ar_package, "ELEMENTS")
    
    @classmethod
    def load_from_file(cls, file_path: str) -> 'ARXMLDocument':
        """Load ARXML document from file"""
        doc = cls()
        doc._file_path = file_path
        
        try:
            # Parse XML file using parser
            doc._root_element = doc._parser.parse_arxml_file(file_path)
            if not doc._root_element:
                raise Exception("Failed to parse ARXML file")
            
            # Extract schema version from namespace
            namespace = doc._root_element.nsmap.get(None, "")
            if "r4.0" in namespace:
                doc._schema_version = "4.7.0"
            
            # Parse AUTOSAR elements using parser
            doc._sw_component_types = doc._parser.extract_sw_component_types(doc._root_element)
            doc._compositions = doc._parser.extract_compositions(doc._root_element)
            doc._port_interfaces = doc._parser.extract_port_interfaces(doc._root_element)
            doc._service_interfaces = doc._parser.extract_service_interfaces(doc._root_element)
            
        except Exception as e:
            raise Exception(f"Failed to load ARXML file: {e}")
        
        return doc
    
    def load_from_element(self, root_element: etree.Element, parser: ARXMLParser):
        """Load ARXML document from parsed XML element"""
        self._root_element = root_element
        
        # Some callers may pass a stdlib xml.etree.ElementTree.Element which
        # doesn't implement lxml's xpath() API. Try to convert it to a
        # real lxml.etree.Element (if lxml is available) so our parser (which
        # relies on xpath) works. If lxml isn't available, fall back to the
        # project's xml_compat etree behavior.
        if not hasattr(root_element, 'xpath'):
            try:
                # Prefer using real lxml if present
                import importlib
                lxml_etree = importlib.import_module('lxml.etree')
                xml_bytes = std_etree.tostring(root_element, encoding='utf-8')
                root_element = lxml_etree.fromstring(xml_bytes)
            except Exception:
                try:
                    # Fall back to the compatibility etree (may be stdlib-backed)
                    xml_bytes = std_etree.tostring(root_element, encoding='utf-8')
                    root_element = etree.fromstring(xml_bytes)
                except Exception:
                    # Give up conversion and continue with the original element
                    pass

        # Extract schema version from namespace
        if hasattr(root_element, 'nsmap'):
            namespace = root_element.nsmap.get(None, "")
        else:
            # For standard library, extract namespace from tag
            if '}' in root_element.tag:
                namespace = root_element.tag.split('}')[0][1:]
            else:
                namespace = ""
        if "r4.0" in namespace:
            self._schema_version = "4.7.0"
        elif "r4.1" in namespace:
            self._schema_version = "4.6.0"
        elif "r4.2" in namespace:
            self._schema_version = "4.5.0"
        elif "r4.3" in namespace:
            self._schema_version = "4.4.0"
        elif "r4.4" in namespace:
            self._schema_version = "4.3.0"
        else:
            self._schema_version = "4.7.0"  # Default fallback
        
        # Parse AUTOSAR elements using parser
        self._sw_component_types = parser.extract_sw_component_types(root_element)
        self._compositions = parser.extract_compositions(root_element)
        self._port_interfaces = parser.extract_port_interfaces(root_element)
        self._service_interfaces = parser.extract_service_interfaces(root_element)
        self._ecuc_elements = parser.extract_ecuc_elements(root_element)
        
        # Store original XML elements for better preservation
        self._original_xml_elements = []
        elements_container = root_element.find('.//{http://autosar.org/schema/r4.0}ELEMENTS')
        if elements_container is not None:
            for child in elements_container:
                # Store all elements that are not basic AUTOSAR elements
                if not child.tag.endswith(('APPLICATION-SW-COMPONENT-TYPE', 'ATOMIC-SW-COMPONENT-TYPE', 
                                         'COMPOSITION-SW-COMPONENT-TYPE', 'PORT-INTERFACE', 'SERVICE-INTERFACE')):
                    self._original_xml_elements.append(child)

        # Debug: print parsed ECUC elements identities after loading
        try:
            print("Loaded ECUC elements:")
            for e in self._ecuc_elements:
                try:
                    print(f"  id={id(e)} short_name='{e.get('short_name')}' type='{e.get('type')}' containers={len(e.get('containers', []))}")
                except Exception:
                    print(f"  id={id(e)} (unreadable content)")
        except Exception:
            pass
    
    def save_to_file(self, file_path: str):
        """Save document to file"""
        self._file_path = file_path
        
        try:
            # Serialize to ARXML using parser
            arxml_content = self._parser.serialize_to_arxml(self)
            if not arxml_content:
                raise Exception("Failed to serialize document")
            
            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(arxml_content)
        
        except Exception as e:
            raise Exception(f"Failed to save ARXML file: {e}")
    
    
    def add_sw_component_type(self, component_type: SwComponentType):
        """Add a software component type"""
        # Add to repository if available
        if self._repositories and 'sw_component_types' in self._repositories:
            self._repositories['sw_component_types'].save(component_type)
        
        # Add to legacy collection for backward compatibility
        self._sw_component_types.append(component_type)
        self._modified = True
        self.element_added.emit(component_type)
    
    def remove_sw_component_type(self, component_type: SwComponentType):
        """Remove a software component type"""
        # Remove from repository if available
        if self._repositories and 'sw_component_types' in self._repositories:
            self._repositories['sw_component_types'].delete(component_type)
        
        # Remove from legacy collection
        if component_type in self._sw_component_types:
            self._sw_component_types.remove(component_type)
            self._modified = True
            self.element_removed.emit(component_type)
    
    def add_composition(self, composition: Composition):
        """Add a composition"""
        # Add to repository if available
        if self._repositories and 'compositions' in self._repositories:
            self._repositories['compositions'].save(composition)
        
        # Add to legacy collection
        self._compositions.append(composition)
        self._modified = True
        self.element_added.emit(composition)
    
    def remove_composition(self, composition: Composition):
        """Remove a composition"""
        # Remove from repository if available
        if self._repositories and 'compositions' in self._repositories:
            self._repositories['compositions'].delete(composition)
        
        # Remove from legacy collection
        if composition in self._compositions:
            self._compositions.remove(composition)
            self._modified = True
            self.element_removed.emit(composition)
    
    def add_port_interface(self, port_interface: PortInterface):
        """Add a port interface"""
        # Add to repository if available
        if self._repositories and 'port_interfaces' in self._repositories:
            self._repositories['port_interfaces'].save(port_interface)
        
        # Add to legacy collection
        self._port_interfaces.append(port_interface)
        self._modified = True
        self.element_added.emit(port_interface)
    
    def remove_port_interface(self, port_interface: PortInterface):
        """Remove a port interface"""
        # Remove from repository if available
        if self._repositories and 'port_interfaces' in self._repositories:
            self._repositories['port_interfaces'].delete(port_interface)
        
        # Remove from legacy collection
        if port_interface in self._port_interfaces:
            self._port_interfaces.remove(port_interface)
            self._modified = True
            self.element_removed.emit(port_interface)
    
    def add_service_interface(self, service_interface: ServiceInterface):
        """Add a service interface"""
        # Add to repository if available
        if self._repositories and 'service_interfaces' in self._repositories:
            self._repositories['service_interfaces'].save(service_interface)
        
        # Add to legacy collection
        self._service_interfaces.append(service_interface)
        self._modified = True
        self.element_added.emit(service_interface)
    
    def remove_service_interface(self, service_interface: ServiceInterface):
        """Remove a service interface"""
        # Remove from repository if available
        if self._repositories and 'service_interfaces' in self._repositories:
            self._repositories['service_interfaces'].delete(service_interface)
        
        # Remove from legacy collection
        if service_interface in self._service_interfaces:
            self._service_interfaces.remove(service_interface)
            self._modified = True
            self.element_removed.emit(service_interface)
    
    def add_sw_component_type(self, component_type: SwComponentType):
        """Add a software component type"""
        self._sw_component_types.append(component_type)
        self._modified = True
        self.element_added.emit(component_type)
    
    def remove_sw_component_type(self, component_type: SwComponentType):
        """Remove a software component type"""
        if component_type in self._sw_component_types:
            self._sw_component_types.remove(component_type)
            self._modified = True
            self.element_removed.emit(component_type)
    
    def add_composition(self, composition: Composition):
        """Add a composition"""
        self._compositions.append(composition)
        self._modified = True
        self.element_added.emit(composition)
    
    def remove_composition(self, composition: Composition):
        """Remove a composition"""
        if composition in self._compositions:
            self._compositions.remove(composition)
            self._modified = True
            self.element_removed.emit(composition)
    
    def save_document(self, file_path: Optional[str] = None) -> bool:
        """Save the document to file"""
        try:
            if file_path:
                self._file_path = file_path
            
            if not self._file_path:
                print("No file path specified for saving")
                return False
            
            print(f"Saving document to: {self._file_path}")
            print(f"Document has {len(self._sw_component_types)} component types")
            print(f"Document has {len(self._port_interfaces)} port interfaces")
            print(f"Document has {len(self._compositions)} compositions")

            # Debug: print ECUC elements identities and short names to verify model state
            try:
                print("ECUC elements in model:")
                for e in self._ecuc_elements:
                    try:
                        print(f"  id={id(e)} short_name='{e.get('short_name')}' type='{e.get('type')}' containers={len(e.get('containers', []))}")
                    except Exception:
                        print(f"  id={id(e)} (unreadable content)")
            except Exception:
                pass
            
            # Generate XML from current elements
            root = self._generate_xml()
            print(f"Generated XML root: {root.tag}")
            
            # Write to file
            with open(self._file_path, 'wb') as f:
                xml_content = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True)
                f.write(xml_content)
                print(f"Wrote {len(xml_content)} bytes to file")
            
            self._modified = False
            print("Document saved successfully")
            return True
            
        except Exception as e:
            print(f"Error saving document: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _generate_xml(self) -> etree.Element:
        """Generate XML from current elements"""
        # Create root element
        root = etree.Element("AUTOSAR", 
                           attrib={"xmlns": "http://autosar.org/schema/r4.0"})
        root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", 
                "http://autosar.org/schema/r4.0 AUTOSAR_4-7-0.xsd")
        
        # Add AR-PACKAGE
        ar_package = etree.SubElement(root, "AR-PACKAGES")
        ar_package_item = etree.SubElement(ar_package, "AR-PACKAGE")
        
        # Add short name
        short_name = etree.SubElement(ar_package_item, "SHORT-NAME")
        short_name.text = "AUTOSAR_Package"
        
        # Add elements
        elements = etree.SubElement(ar_package_item, "ELEMENTS")
        
        # Add software component types
        for component_type in self._sw_component_types:
            comp_elem = self._component_type_to_xml(component_type)
            elements.append(comp_elem)
        
        # Add port interfaces
        for port_interface in self._port_interfaces:
            port_elem = self._port_interface_to_xml(port_interface)
            elements.append(port_elem)
        
        # Add compositions
        for composition in self._compositions:
            comp_elem = self._composition_to_xml(composition)
            elements.append(comp_elem)
        
        # Add ECUC elements (these are the editable ones)
        for ecuc_element in self._ecuc_elements:
            ecuc_elem = self._ecuc_element_to_xml(ecuc_element)
            elements.append(ecuc_elem)
        
        # Add original XML elements only for elements that are NOT already parsed
        # This ensures we don't duplicate content and preserve unparsed elements
        for xml_elem in self._original_xml_elements:
            # Check if this element is already represented in our parsed data
            # by checking if it's an ECUC element that we've already processed
            if xml_elem.tag.endswith('ECUC-MODULE-CONFIGURATION-VALUES'):
                # Skip this element as it's already been processed as a parsed ECUC element
                continue
            
            # Create a copy of the element to avoid modifying the original
            import copy
            elem_copy = copy.deepcopy(xml_elem)
            elements.append(elem_copy)
        
        return root
    
    def _component_type_to_xml(self, component_type: SwComponentType) -> etree.Element:
        """Convert component type to XML element"""
        if component_type.category.value == "APPLICATION":
            elem = etree.Element("APPLICATION-SW-COMPONENT-TYPE")
        else:
            elem = etree.Element("ATOMIC-SW-COMPONENT-TYPE")
        
        # Add short name
        short_name = etree.SubElement(elem, "SHORT-NAME")
        short_name.text = component_type.short_name
        
        # Add description if available
        if component_type.desc:
            desc = etree.SubElement(elem, "DESC")
            desc_l2 = etree.SubElement(desc, "L-2")
            desc_l2.text = component_type.desc
        
        # Add ports
        if component_type.ports:
            ports = etree.SubElement(elem, "PORTS")
            for port in component_type.ports:
                port_elem = self._port_prototype_to_xml(port)
                ports.append(port_elem)
        
        return elem
    
    def _port_prototype_to_xml(self, port: PortPrototype) -> etree.Element:
        """Convert port prototype to XML element"""
        if port.port_type.value == "PROVIDER":
            elem = etree.Element("P-PORT-PROTOTYPE")
        elif port.port_type.value == "REQUIRER":
            elem = etree.Element("R-PORT-PROTOTYPE")
        else:
            elem = etree.Element("PR-PORT-PROTOTYPE")
        
        # Add short name
        short_name = etree.SubElement(elem, "SHORT-NAME")
        short_name.text = port.short_name
        
        # Add description if available
        if port.desc:
            desc = etree.SubElement(elem, "DESC")
            desc_l2 = etree.SubElement(desc, "L-2")
            desc_l2.text = port.desc
        
        # Add interface reference
        if port.interface_ref:
            interface_ref = etree.SubElement(elem, "REQUIRED-INTERFACE-TREF")
            interface_ref.text = port.interface_ref
        
        return elem
    
    def _port_interface_to_xml(self, port_interface: PortInterface) -> etree.Element:
        """Convert port interface to XML element"""
        if port_interface.is_service:
            elem = etree.Element("SERVICE-INTERFACE")
        else:
            elem = etree.Element("SENDER-RECEIVER-INTERFACE")
        
        # Add short name
        short_name = etree.SubElement(elem, "SHORT-NAME")
        short_name.text = port_interface.short_name
        
        # Add description if available
        if port_interface.desc:
            desc = etree.SubElement(elem, "DESC")
            desc_l2 = etree.SubElement(desc, "L-2")
            desc_l2.text = port_interface.desc
        
        # Add data elements
        if port_interface.data_elements:
            data_elements = etree.SubElement(elem, "DATA-ELEMENTS")
            for data_elem in port_interface.data_elements:
                data_elem_xml = self._data_element_to_xml(data_elem)
                data_elements.append(data_elem_xml)
        
        return elem
    
    def _data_element_to_xml(self, data_element: DataElement) -> etree.Element:
        """Convert data element to XML element"""
        elem = etree.Element("DATA-ELEMENT-PROTOTYPE")
        
        # Add short name
        short_name = etree.SubElement(elem, "SHORT-NAME")
        short_name.text = data_element.short_name
        
        # Add description if available
        if data_element.desc:
            desc = etree.SubElement(elem, "DESC")
            desc_l2 = etree.SubElement(desc, "L-2")
            desc_l2.text = data_element.desc
        
        # Add type reference
        type_ref = etree.SubElement(elem, "TYPE-TREF")
        type_ref.text = data_element.data_type.value
        
        return elem
    
    def _composition_to_xml(self, composition: Composition) -> etree.Element:
        """Convert composition to XML element"""
        elem = etree.Element("COMPOSITION-SW-COMPONENT-TYPE")
        
        # Add short name
        short_name = etree.SubElement(elem, "SHORT-NAME")
        short_name.text = composition.short_name
        
        # Add description if available
        if composition.desc:
            desc = etree.SubElement(elem, "DESC")
            desc_l2 = etree.SubElement(desc, "L-2")
            desc_l2.text = composition.desc
        
        return elem
    
    def _ecuc_element_to_xml(self, ecuc_element: dict) -> etree.Element:
        """Convert ECUC element to XML element"""
        # Create the appropriate ECUC element type
        element_type = ecuc_element.get('type', 'ECUC-MODULE-CONFIGURATION-VALUES')
        elem = etree.Element(element_type)
        
        # Add UUID if present
        if 'uuid' in ecuc_element:
            elem.set('UUID', ecuc_element['uuid'])
        
        # Add short name
        if 'short_name' in ecuc_element:
            short_name = etree.SubElement(elem, "SHORT-NAME")
            short_name.text = ecuc_element['short_name']
        
        # Add description if available
        if 'desc' in ecuc_element and ecuc_element['desc']:
            desc = etree.SubElement(elem, "DESC")
            desc_l2 = etree.SubElement(desc, "L-2")
            desc_l2.text = ecuc_element['desc']
        
        # Add admin data if present
        if 'admin_data' in ecuc_element and ecuc_element['admin_data']:
            admin_data = etree.SubElement(elem, "ADMIN-DATA")
            # Convert admin data from dict to XML structure
            self._dict_to_xml(admin_data, ecuc_element['admin_data'])
        
        # Add containers if present
        if 'containers' in ecuc_element and ecuc_element['containers']:
            for container in ecuc_element['containers']:
                container_elem = self._ecuc_element_to_xml(container)
                elem.append(container_elem)
        
        # Add parameters if present
        if 'parameters' in ecuc_element and ecuc_element['parameters']:
            for parameter in ecuc_element['parameters']:
                param_elem = self._ecuc_element_to_xml(parameter)
                elem.append(param_elem)
        
        return elem
    
    def _dict_to_xml(self, parent_elem, data_dict):
        """Convert dictionary to XML structure recursively"""
        for key, value in data_dict.items():
            if isinstance(value, dict):
                # Create sub-element for nested dict
                sub_elem = etree.SubElement(parent_elem, key)
                self._dict_to_xml(sub_elem, value)
            elif isinstance(value, list):
                # Handle lists
                for item in value:
                    if isinstance(item, dict):
                        sub_elem = etree.SubElement(parent_elem, key)
                        self._dict_to_xml(sub_elem, item)
                    else:
                        sub_elem = etree.SubElement(parent_elem, key)
                        sub_elem.text = str(item)
            else:
                # Simple key-value pair
                sub_elem = etree.SubElement(parent_elem, key)
                if value is not None:
                    sub_elem.text = str(value)