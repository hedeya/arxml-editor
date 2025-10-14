"""
ARXML Parser Service
Handles parsing and serialization of ARXML files
"""

import os
from typing import List, Optional, Dict, Any
from lxml import etree
from PyQt6.QtCore import QObject, pyqtSignal
from ..models.autosar_elements import (
    SwComponentType, ApplicationSwComponentType, AtomicSwComponentType, 
    CompositionSwComponentType, Composition, PortInterface, ServiceInterface,
    PortPrototype, DataElement, ServiceElement, ServiceOperation,
    SwComponentTypeCategory, PortType, DataType
)

class ARXMLParser(QObject):
    """ARXML parser service"""
    
    # Signals
    parse_progress = pyqtSignal(int, int)  # current, total
    parse_completed = pyqtSignal(bool, str)  # success, message
    
    def __init__(self, schema_service=None):
        super().__init__()
        self._namespaces = {
            'ar': 'http://autosar.org/schema/r4.0',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }
        self._schema_service = schema_service
    
    def parse_arxml_file(self, file_path: str) -> Optional[etree.Element]:
        """Parse ARXML file and return root element"""
        try:
            # Parse XML file
            tree = etree.parse(file_path)
            root = tree.getroot()
            
            # Auto-detect and set schema version if schema service is available
            if self._schema_service:
                self._schema_service.auto_detect_and_set_version(file_path=file_path)
                # Update namespaces based on detected version
                self._update_namespaces_from_detected_version()
            
            # Validate namespace
            if not self._is_valid_arxml(root):
                raise ValueError("Invalid ARXML namespace or structure")
            
            return root
        
        except Exception as e:
            self.parse_completed.emit(False, f"Parse error: {str(e)}")
            return None
    
    def parse_arxml_content(self, content: str) -> Optional[etree.Element]:
        """Parse ARXML content string and return root element"""
        try:
            # Parse XML content
            root = etree.fromstring(content.encode('utf-8'))
            
            # Auto-detect and set schema version if schema service is available
            if self._schema_service:
                self._schema_service.auto_detect_and_set_version(arxml_content=content)
                # Update namespaces based on detected version
                self._update_namespaces_from_detected_version()
            
            # Validate namespace
            if not self._is_valid_arxml(root):
                raise ValueError("Invalid ARXML namespace or structure")
            
            return root
        
        except Exception as e:
            self.parse_completed.emit(False, f"Parse error: {str(e)}")
            return None
    
    def _update_namespaces_from_detected_version(self):
        """Update namespaces based on detected schema version"""
        if not self._schema_service or not self._schema_service.detected_version:
            return
        
        # Get the namespace for the detected version
        version_info = self._schema_service.get_version_info(self._schema_service.detected_version)
        if version_info:
            self._namespaces['ar'] = version_info.namespace
    
    def _is_valid_arxml(self, root: etree.Element) -> bool:
        """Check if root element is valid ARXML"""
        # Check namespace - be more flexible with namespace validation
        namespace_uri = root.nsmap.get(None)
        if not namespace_uri or not namespace_uri.startswith('http://autosar.org/schema/'):
            return False
        
        # Check root element name
        if root.tag != f"{{{namespace_uri}}}AUTOSAR":
            return False
        
        return True
    
    def extract_sw_component_types(self, root: etree.Element) -> List[SwComponentType]:
        """Extract software component types from ARXML"""
        component_types = []
        
        # Find all AR-PACKAGE elements
        packages = root.xpath('.//ar:AR-PACKAGE', namespaces=self._namespaces)
        
        for package in packages:
            # Find APPLICATION-SW-COMPONENT-TYPE elements
            app_components = package.xpath('.//ar:APPLICATION-SW-COMPONENT-TYPE', namespaces=self._namespaces)
            for comp_elem in app_components:
                component = self._parse_application_component(comp_elem)
                if component:
                    component_types.append(component)
            
            # Find ATOMIC-SW-COMPONENT-TYPE elements
            atomic_components = package.xpath('.//ar:ATOMIC-SW-COMPONENT-TYPE', namespaces=self._namespaces)
            for comp_elem in atomic_components:
                component = self._parse_atomic_component(comp_elem)
                if component:
                    component_types.append(component)
            
            # Find COMPOSITION-SW-COMPONENT-TYPE elements
            composition_components = package.xpath('.//ar:COMPOSITION-SW-COMPONENT-TYPE', namespaces=self._namespaces)
            for comp_elem in composition_components:
                component = self._parse_composition_component(comp_elem)
                if component:
                    component_types.append(component)
        
        return component_types
    
    def extract_compositions(self, root: etree.Element) -> List[Composition]:
        """Extract compositions from ARXML"""
        compositions = []
        
        # Find all COMPOSITION elements
        comp_elements = root.xpath('.//ar:COMPOSITION', namespaces=self._namespaces)
        
        for comp_elem in comp_elements:
            composition = self._parse_composition(comp_elem)
            if composition:
                compositions.append(composition)
        
        return compositions
    
    def extract_port_interfaces(self, root: etree.Element) -> List[PortInterface]:
        """Extract port interfaces from ARXML"""
        port_interfaces = []
        
        # Find all SENDER-RECEIVER-INTERFACE elements
        sri_elements = root.xpath('.//ar:SENDER-RECEIVER-INTERFACE', namespaces=self._namespaces)
        for sri_elem in sri_elements:
            port_interface = self._parse_sender_receiver_interface(sri_elem)
            if port_interface:
                port_interfaces.append(port_interface)
        
        return port_interfaces
    
    def extract_service_interfaces(self, root: etree.Element) -> List[ServiceInterface]:
        """Extract service interfaces from ARXML"""
        service_interfaces = []
        
        # Find all CLIENT-SERVER-INTERFACE elements
        csi_elements = root.xpath('.//ar:CLIENT-SERVER-INTERFACE', namespaces=self._namespaces)
        for csi_elem in csi_elements:
            service_interface = self._parse_client_server_interface(csi_elem)
            if service_interface:
                service_interfaces.append(service_interface)
        
        return service_interfaces
    
    def extract_ecuc_elements(self, root: etree.Element) -> List[dict]:
        """Extract ECUC elements from ARXML"""
        ecuc_elements = []
        
        # Find all ECUC-MODULE-CONFIGURATION-VALUES elements
        ecuc_elements_xml = root.xpath('.//ar:ECUC-MODULE-CONFIGURATION-VALUES', namespaces=self._namespaces)
        for ecuc_elem in ecuc_elements_xml:
            ecuc_data = self._parse_ecuc_module_configuration(ecuc_elem)
            if ecuc_data:
                ecuc_elements.append(ecuc_data)
        
        return ecuc_elements
    
    def _parse_ecuc_module_configuration(self, elem: etree.Element) -> Optional[dict]:
        """Parse ECUC-MODULE-CONFIGURATION-VALUES element"""
        try:
            short_name = self._get_text_content(elem, './/ar:SHORT-NAME')
            uuid = elem.get('UUID', '')
            
            if not short_name:
                return None
            
            ecuc_data = {
                'type': 'ECUC-MODULE-CONFIGURATION-VALUES',
                'short_name': short_name,
                'uuid': uuid,
                'containers': []
            }
            
            # Extract ECUC-CONTAINER-VALUE elements
            containers = elem.xpath('.//ar:ECUC-CONTAINER-VALUE', namespaces=self._namespaces)
            for container in containers:
                container_data = self._parse_ecuc_container_value(container)
                if container_data:
                    ecuc_data['containers'].append(container_data)
            
            return ecuc_data
        
        except Exception as e:
            print(f"Error parsing ECUC module configuration: {e}")
            return None
    
    def _parse_ecuc_container_value(self, elem: etree.Element) -> Optional[dict]:
        """Parse ECUC-CONTAINER-VALUE element"""
        try:
            short_name = self._get_text_content(elem, './/ar:SHORT-NAME')
            definition_ref = self._get_text_content(elem, './/ar:DEFINITION-REF')
            
            if not short_name:
                return None
            
            container_data = {
                'type': 'ECUC-CONTAINER-VALUE',
                'short_name': short_name,
                'definition_ref': definition_ref,
                'parameters': []
            }
            
            # Extract ECUC-PARAMETER-VALUE elements
            parameters = elem.xpath('.//ar:ECUC-PARAMETER-VALUE', namespaces=self._namespaces)
            for param in parameters:
                param_data = self._parse_ecuc_parameter_value(param)
                if param_data:
                    container_data['parameters'].append(param_data)
            
            return container_data
        
        except Exception as e:
            print(f"Error parsing ECUC container value: {e}")
            return None
    
    def _parse_ecuc_parameter_value(self, elem: etree.Element) -> Optional[dict]:
        """Parse ECUC-PARAMETER-VALUE element"""
        try:
            short_name = self._get_text_content(elem, './/ar:SHORT-NAME')
            definition_ref = self._get_text_content(elem, './/ar:DEFINITION-REF')
            value = self._get_text_content(elem, './/ar:VALUE')
            
            if not short_name:
                return None
            
            return {
                'type': 'ECUC-PARAMETER-VALUE',
                'short_name': short_name,
                'definition_ref': definition_ref,
                'value': value
            }
        
        except Exception as e:
            print(f"Error parsing ECUC parameter value: {e}")
            return None
    
    def _parse_application_component(self, elem: etree.Element) -> Optional[ApplicationSwComponentType]:
        """Parse APPLICATION-SW-COMPONENT-TYPE element"""
        try:
            # Extract basic properties
            short_name = self._get_text_content(elem, './/ar:SHORT-NAME')
            desc = self._get_text_content(elem, './/ar:DESC')
            
            if not short_name:
                return None
            
            # Create component
            component = ApplicationSwComponentType(
                short_name=short_name,
                desc=desc
            )
            
            # Extract ports
            ports = self._extract_ports(elem)
            component.ports = ports
            
            return component
        
        except Exception as e:
            print(f"Error parsing application component: {e}")
            return None
    
    def _parse_atomic_component(self, elem: etree.Element) -> Optional[AtomicSwComponentType]:
        """Parse ATOMIC-SW-COMPONENT-TYPE element"""
        try:
            # Extract basic properties
            short_name = self._get_text_content(elem, './/ar:SHORT-NAME')
            desc = self._get_text_content(elem, './/ar:DESC')
            implementation_ref = self._get_text_content(elem, './/ar:IMPLEMENTATION-REF')
            
            if not short_name:
                return None
            
            # Create component
            component = AtomicSwComponentType(
                short_name=short_name,
                desc=desc,
                implementation_ref=implementation_ref
            )
            
            # Extract ports
            ports = self._extract_ports(elem)
            component.ports = ports
            
            return component
        
        except Exception as e:
            print(f"Error parsing atomic component: {e}")
            return None
    
    def _parse_composition_component(self, elem: etree.Element) -> Optional[CompositionSwComponentType]:
        """Parse COMPOSITION-SW-COMPONENT-TYPE element"""
        try:
            # Extract basic properties
            short_name = self._get_text_content(elem, './/ar:SHORT-NAME')
            desc = self._get_text_content(elem, './/ar:DESC')
            
            if not short_name:
                return None
            
            # Create component
            component = CompositionSwComponentType(
                short_name=short_name,
                desc=desc
            )
            
            # Extract ports
            ports = self._extract_ports(elem)
            component.ports = ports
            
            return component
        
        except Exception as e:
            print(f"Error parsing composition component: {e}")
            return None
    
    def _parse_composition(self, elem: etree.Element) -> Optional[Composition]:
        """Parse COMPOSITION element"""
        try:
            # Extract basic properties
            short_name = self._get_text_content(elem, './/ar:SHORT-NAME')
            desc = self._get_text_content(elem, './/ar:DESC')
            
            if not short_name:
                return None
            
            # Create composition
            composition = Composition(
                short_name=short_name,
                desc=desc
            )
            
            # Extract component types and connections
            # This would be implemented based on the specific ARXML structure
            
            return composition
        
        except Exception as e:
            print(f"Error parsing composition: {e}")
            return None
    
    def _parse_sender_receiver_interface(self, elem: etree.Element) -> Optional[PortInterface]:
        """Parse SENDER-RECEIVER-INTERFACE element"""
        try:
            # Extract basic properties
            short_name = self._get_text_content(elem, './/ar:SHORT-NAME')
            desc = self._get_text_content(elem, './/ar:DESC')
            
            if not short_name:
                return None
            
            # Create port interface
            port_interface = PortInterface(
                short_name=short_name,
                desc=desc,
                is_service=False
            )
            
            # Extract data elements
            data_elements = self._extract_data_elements(elem)
            port_interface.data_elements = data_elements
            
            return port_interface
        
        except Exception as e:
            print(f"Error parsing sender-receiver interface: {e}")
            return None
    
    def _parse_client_server_interface(self, elem: etree.Element) -> Optional[ServiceInterface]:
        """Parse CLIENT-SERVER-INTERFACE element"""
        try:
            # Extract basic properties
            short_name = self._get_text_content(elem, './/ar:SHORT-NAME')
            desc = self._get_text_content(elem, './/ar:DESC')
            
            if not short_name:
                return None
            
            # Create service interface
            service_interface = ServiceInterface(
                short_name=short_name,
                desc=desc
            )
            
            # Extract service elements
            service_elements = self._extract_service_elements(elem)
            service_interface.service_elements = service_elements
            
            return service_interface
        
        except Exception as e:
            print(f"Error parsing client-server interface: {e}")
            return None
    
    def _extract_ports(self, elem: etree.Element) -> List[PortPrototype]:
        """Extract port prototypes from component element"""
        ports = []
        
        # Find P-PORT-PROTOTYPE elements
        p_ports = elem.xpath('.//ar:P-PORT-PROTOTYPE', namespaces=self._namespaces)
        for port_elem in p_ports:
            port = self._parse_port_prototype(port_elem, PortType.PROVIDER)
            if port:
                ports.append(port)
        
        # Find R-PORT-PROTOTYPE elements
        r_ports = elem.xpath('.//ar:R-PORT-PROTOTYPE', namespaces=self._namespaces)
        for port_elem in r_ports:
            port = self._parse_port_prototype(port_elem, PortType.REQUIRER)
            if port:
                ports.append(port)
        
        # Find PR-PORT-PROTOTYPE elements
        pr_ports = elem.xpath('.//ar:PR-PORT-PROTOTYPE', namespaces=self._namespaces)
        for port_elem in pr_ports:
            port = self._parse_port_prototype(port_elem, PortType.PROVIDER_REQUIRER)
            if port:
                ports.append(port)
        
        return ports
    
    def _parse_port_prototype(self, elem: etree.Element, port_type: PortType) -> Optional[PortPrototype]:
        """Parse port prototype element"""
        try:
            short_name = self._get_text_content(elem, './/ar:SHORT-NAME')
            desc = self._get_text_content(elem, './/ar:DESC')
            interface_ref = self._get_text_content(elem, './/ar:REQUIRED-INTERFACE-TREF | .//ar:PROVIDED-INTERFACE-TREF')
            
            if not short_name:
                return None
            
            return PortPrototype(
                short_name=short_name,
                desc=desc,
                port_type=port_type,
                interface_ref=interface_ref
            )
        
        except Exception as e:
            print(f"Error parsing port prototype: {e}")
            return None
    
    def _extract_data_elements(self, elem: etree.Element) -> List[DataElement]:
        """Extract data elements from interface element"""
        data_elements = []
        
        # Find DATA-ELEMENT-PROTOTYPE elements
        data_elem_elements = elem.xpath('.//ar:DATA-ELEMENT-PROTOTYPE', namespaces=self._namespaces)
        
        for data_elem in data_elem_elements:
            data_element = self._parse_data_element(data_elem)
            if data_element:
                data_elements.append(data_element)
        
        return data_elements
    
    def _parse_data_element(self, elem: etree.Element) -> Optional[DataElement]:
        """Parse data element prototype"""
        try:
            short_name = self._get_text_content(elem, './/ar:SHORT-NAME')
            desc = self._get_text_content(elem, './/ar:DESC')
            
            if not short_name:
                return None
            
            # Determine data type (simplified)
            data_type = DataType.STRING  # Default
            type_ref = self._get_text_content(elem, './/ar:TYPE-TREF')
            if type_ref:
                if 'boolean' in type_ref.lower():
                    data_type = DataType.BOOLEAN
                elif 'integer' in type_ref.lower():
                    data_type = DataType.INTEGER
                elif 'float' in type_ref.lower():
                    data_type = DataType.FLOAT
            
            return DataElement(
                short_name=short_name,
                desc=desc,
                data_type=data_type
            )
        
        except Exception as e:
            print(f"Error parsing data element: {e}")
            return None
    
    def _extract_service_elements(self, elem: etree.Element) -> List[ServiceElement]:
        """Extract service elements from service interface"""
        service_elements = []
        
        # Find OPERATION elements
        operation_elements = elem.xpath('.//ar:OPERATION', namespaces=self._namespaces)
        
        for op_elem in operation_elements:
            service_element = self._parse_service_element(op_elem)
            if service_element:
                service_elements.append(service_element)
        
        return service_elements
    
    def _parse_service_element(self, elem: etree.Element) -> Optional[ServiceElement]:
        """Parse service element (operation)"""
        try:
            short_name = self._get_text_content(elem, './/ar:SHORT-NAME')
            desc = self._get_text_content(elem, './/ar:DESC')
            
            if not short_name:
                return None
            
            return ServiceElement(
                short_name=short_name,
                desc=desc,
                service_kind="operation"
            )
        
        except Exception as e:
            print(f"Error parsing service element: {e}")
            return None
    
    def _get_text_content(self, elem: etree.Element, xpath: str) -> Optional[str]:
        """Get text content from element using XPath"""
        try:
            result = elem.xpath(xpath, namespaces=self._namespaces)
            if result and len(result) > 0:
                return result[0].text
            return None
        except Exception:
            return None
    
    def serialize_to_arxml(self, document) -> str:
        """Serialize document to ARXML string"""
        try:
            # Create root element with proper namespace handling
            root = etree.Element("AUTOSAR", 
                xmlns=self._namespaces['ar'])
            
            # Add schema location
            root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", 
                    "http://autosar.org/schema/r4.0 AUTOSAR_4-7-0.xsd")
            
            # Add AR-PACKAGES
            ar_packages = etree.SubElement(root, "AR-PACKAGES")
            ar_package = etree.SubElement(ar_packages, "AR-PACKAGE")
            etree.SubElement(ar_package, "SHORT-NAME").text = "RootPackage"
            elements = etree.SubElement(ar_package, "ELEMENTS")
            
            # Add software component types
            for component_type in document.sw_component_types:
                comp_elem = self._serialize_sw_component_type(component_type)
                if comp_elem:
                    elements.append(comp_elem)
            
            # Add compositions
            for composition in document.compositions:
                comp_elem = self._serialize_composition(composition)
                if comp_elem:
                    elements.append(comp_elem)
            
            # Add port interfaces
            for port_interface in document.port_interfaces:
                interface_elem = self._serialize_port_interface(port_interface)
                if interface_elem:
                    elements.append(interface_elem)
            
            # Add service interfaces
            for service_interface in document.service_interfaces:
                interface_elem = self._serialize_service_interface(service_interface)
                if interface_elem:
                    elements.append(interface_elem)
            
            # Convert to string
            return etree.tostring(root, 
                                pretty_print=True, 
                                xml_declaration=True, 
                                encoding='UTF-8').decode('utf-8')
        
        except Exception as e:
            print(f"Error serializing to ARXML: {e}")
            return ""
    
    def _serialize_sw_component_type(self, component_type: SwComponentType) -> Optional[etree.Element]:
        """Serialize software component type to XML element"""
        try:
            if component_type.category == SwComponentTypeCategory.APPLICATION:
                elem = etree.Element("APPLICATION-SW-COMPONENT-TYPE")
            elif component_type.category == SwComponentTypeCategory.ATOMIC:
                elem = etree.Element("ATOMIC-SW-COMPONENT-TYPE")
            elif component_type.category == SwComponentTypeCategory.COMPOSITION:
                elem = etree.Element("COMPOSITION-SW-COMPONENT-TYPE")
            else:
                return None
            
            # Add basic properties
            etree.SubElement(elem, "SHORT-NAME").text = component_type.short_name
            if component_type.desc:
                desc_elem = etree.SubElement(elem, "DESC")
                etree.SubElement(desc_elem, "L-2").text = component_type.desc
            
            # Add ports
            for port in component_type.ports:
                port_elem = self._serialize_port_prototype(port)
                if port_elem:
                    elem.append(port_elem)
            
            return elem
        
        except Exception as e:
            print(f"Error serializing component type: {e}")
            return None
    
    def _serialize_composition(self, composition: Composition) -> Optional[etree.Element]:
        """Serialize composition to XML element"""
        try:
            elem = etree.Element("COMPOSITION")
            
            # Add basic properties
            etree.SubElement(elem, "SHORT-NAME").text = composition.short_name
            if composition.desc:
                desc_elem = etree.SubElement(elem, "DESC")
                etree.SubElement(desc_elem, "L-2").text = composition.desc
            
            return elem
        
        except Exception as e:
            print(f"Error serializing composition: {e}")
            return None
    
    def _serialize_port_interface(self, port_interface: PortInterface) -> Optional[etree.Element]:
        """Serialize port interface to XML element"""
        try:
            elem = etree.Element("SENDER-RECEIVER-INTERFACE")
            
            # Add basic properties
            etree.SubElement(elem, "SHORT-NAME").text = port_interface.short_name
            if port_interface.desc:
                desc_elem = etree.SubElement(elem, "DESC")
                etree.SubElement(desc_elem, "L-2").text = port_interface.desc
            
            # Add data elements
            for data_element in port_interface.data_elements:
                data_elem = self._serialize_data_element(data_element)
                if data_elem:
                    elem.append(data_elem)
            
            return elem
        
        except Exception as e:
            print(f"Error serializing port interface: {e}")
            return None
    
    def _serialize_service_interface(self, service_interface) -> Optional[etree.Element]:
        """Serialize service interface to XML element"""
        try:
            elem = etree.Element("CLIENT-SERVER-INTERFACE")
            
            # Add basic properties
            etree.SubElement(elem, "SHORT-NAME").text = service_interface.short_name
            if service_interface.desc:
                desc_elem = etree.SubElement(elem, "DESC")
                etree.SubElement(desc_elem, "L-2").text = service_interface.desc
            
            return elem
        
        except Exception as e:
            print(f"Error serializing service interface: {e}")
            return None
    
    def _serialize_port_prototype(self, port: PortPrototype) -> Optional[etree.Element]:
        """Serialize port prototype to XML element"""
        try:
            if port.port_type == PortType.PROVIDER:
                elem = etree.Element("P-PORT-PROTOTYPE")
            elif port.port_type == PortType.REQUIRER:
                elem = etree.Element("R-PORT-PROTOTYPE")
            elif port.port_type == PortType.PROVIDER_REQUIRER:
                elem = etree.Element("PR-PORT-PROTOTYPE")
            else:
                return None
            
            # Add basic properties
            etree.SubElement(elem, "SHORT-NAME").text = port.short_name
            if port.desc:
                desc_elem = etree.SubElement(elem, "DESC")
                etree.SubElement(desc_elem, "L-2").text = port.desc
            
            # Add interface reference
            if port.interface_ref:
                if port.port_type == PortType.PROVIDER:
                    etree.SubElement(elem, "PROVIDED-INTERFACE-TREF").text = port.interface_ref
                else:
                    etree.SubElement(elem, "REQUIRED-INTERFACE-TREF").text = port.interface_ref
            
            return elem
        
        except Exception as e:
            print(f"Error serializing port prototype: {e}")
            return None
    
    def _serialize_data_element(self, data_element: DataElement) -> Optional[etree.Element]:
        """Serialize data element to XML element"""
        try:
            elem = etree.Element("DATA-ELEMENT-PROTOTYPE")
            
            # Add basic properties
            etree.SubElement(elem, "SHORT-NAME").text = data_element.short_name
            if data_element.desc:
                desc_elem = etree.SubElement(elem, "DESC")
                etree.SubElement(desc_elem, "L-2").text = data_element.desc
            
            return elem
        
        except Exception as e:
            print(f"Error serializing data element: {e}")
            return None