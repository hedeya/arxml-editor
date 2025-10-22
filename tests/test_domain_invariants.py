from src.core.models.autosar_elements import SwComponentType, PortInterface, DataElement, SwComponentTypeCategory


def run_tests():
    # Test 1: SwComponentType with empty name
    comp = SwComponentType('', SwComponentTypeCategory.APPLICATION)
    violations = comp.validate_invariants()
    if not any('empty' in v.lower() or 'name cannot' in v.lower() for v in violations):
        raise AssertionError('SwComponentType invariants did not detect empty name')

    # Test 2: PortInterface duplicate data element names
    pi = PortInterface('IF')
    de1 = DataElement('elem')
    de2 = DataElement('elem')
    pi.add_data_element(de1)
    # add second with same name
    pi.add_data_element(de2)
    violations = pi.validate_invariants()
    if not any('unique' in v.lower() for v in violations):
        raise AssertionError('PortInterface invariants did not detect duplicate data element names')


if __name__ == '__main__':
    run_tests()
    print('test_domain_invariants: OK')
