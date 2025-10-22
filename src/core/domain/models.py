"""
Pure domain models (dataclasses) — a Qt-free representation of core domain objects.
These are used as a migration target; adapters can convert between QObject-based models
and these dataclasses.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class PortType(Enum):
    PROVIDER = "P-PORT"
    REQUIRER = "R-PORT"
    PROVIDER_REQUIRER = "PR-PORT"


@dataclass
class DataElement:
    short_name: str
    data_type: Optional[str] = None
    desc: Optional[str] = None


@dataclass
class PortInterface:
    short_name: str
    is_service: bool = False
    data_elements: List[DataElement] = field(default_factory=list)


@dataclass
class SwComponentType:
    short_name: str
    category: str
    desc: Optional[str] = None
    ports: List[str] = field(default_factory=list)  # list of port names
    compositions: List[str] = field(default_factory=list)  # list of composition ids/names


@dataclass
class Composition:
    short_name: str
    desc: Optional[str] = None
    component_type_names: List[str] = field(default_factory=list)


def from_qobject_data_element(qobj) -> DataElement:
    return DataElement(short_name=getattr(qobj, 'short_name', ''), data_type=getattr(qobj, 'data_type', None), desc=getattr(qobj, 'desc', None))


def from_qobject_port_interface(qobj) -> PortInterface:
    data_elems = []
    for de in getattr(qobj, 'data_elements', []) or []:
        data_elems.append(from_qobject_data_element(de))
    return PortInterface(short_name=getattr(qobj, 'short_name', ''), is_service=getattr(qobj, 'is_service', False), data_elements=data_elems)


def to_qobject_port_interface(domain_obj, qobj_factory):
    # qobj_factory creates a PortInterface QObject with signature (short_name, desc, is_service)
    try:
        q = qobj_factory(domain_obj.short_name, getattr(domain_obj, 'desc', ''), domain_obj.is_service)
    except Exception:
        # fallback minimal creation
        from ..models.autosar_elements import PortInterface as QPortInterface
        q = QPortInterface(domain_obj.short_name, getattr(domain_obj, 'desc', None), domain_obj.is_service)

    # add data elements if possible
    for de in getattr(domain_obj, 'data_elements', []) or []:
        try:
            from ..models.autosar_elements import DataElement as QDataElement
            q.add_data_element(QDataElement(de.short_name, None))
        except Exception:
            pass

    return q


def from_qobject_sw_component_type(qobj) -> SwComponentType:
    ports = [getattr(p, 'short_name', '') for p in getattr(qobj, 'ports', []) or []]
    comps = [getattr(c, 'short_name', '') for c in getattr(qobj, 'compositions', []) or []]
    category = getattr(qobj, 'category', None)
    if hasattr(category, 'value'):
        category = category.value
    return SwComponentType(short_name=getattr(qobj, 'short_name', ''), category=category or 'Unknown', desc=getattr(qobj, 'desc', None), ports=ports, compositions=comps)


def to_qobject_sw_component_type(domain_obj, qobj_factory):
    # qobj_factory is a callable to produce a SwComponentType QObject instance
    q = qobj_factory(domain_obj.short_name, domain_obj.desc)
    # set category if possible
    try:
        from ..models.autosar_elements import SwComponentTypeCategory
        for c in SwComponentTypeCategory:
            if c.value == domain_obj.category or c.name == domain_obj.category:
                q.category = c
                break
    except Exception:
        pass
    # ports and compositions are left to repository or later wiring
    return q
